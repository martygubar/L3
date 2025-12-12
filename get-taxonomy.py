from time import sleep
import oci
import io
import csv
import requests
import logging
from datetime import datetime

# ---------------- Logging setup ----------------
log_filename = 'fetch-taxonomy.log'
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,  # change to DEBUG for more detail
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)
# ------------------------------------------------

# File properties
bucket = 'gold'
source_prefix = 'observed_species'
target_prefix = 'taxonomy'
API_KEY = "dluifppbf37a"
EBIRD = "1"
INATURALIST = "2"


# Flatten the taxonomy into a standard record
def flatten_taxonomy(source, taxonomy, loaded_timestamp=None):
    logger.debug("Flattening taxonomy for source=%s, loaded_timestamp=%s", source, loaded_timestamp)
    flattened_record = {}
    valid_ancestors = ['species', 'genus', 'family', 'order', 'class']

    if source == EBIRD:
        flattened_record = {
            "source": source,
            "taxon_code": taxonomy.get("speciesCode",""),
            "scientific_name": taxonomy.get("sciName","").lower(),
            "common_name": taxonomy.get("comName","").lower(),
            "rank": taxonomy.get("category","").lower(),
            "species_code": taxonomy.get("speciesCode","").lower(),
            "species_scientific_name": taxonomy.get("speciesSciName","").lower(),
            "species_common_name": taxonomy.get("speciesComName","").lower(),
            "genus_code": "",
            "genus_scientific_name": "",
            "genus_common_name": "",
            "family_code": taxonomy.get("familyCode","").lower(),
            "family_scientific_name": taxonomy.get("familySciName","").lower(),
            "family_common_name": taxonomy.get("familyComName","").lower(),
            "order_code": "",
            "order_scientific_name": taxonomy.get("order","").lower(),
            "order_common_name": "",
            "class_code": "",
            "class_scientific_name": "",
            "class_common_name": "",
            "loaded_timestamp": loaded_timestamp,
        }
    elif source == INATURALIST:
        flattened_record = {}

        # 1. Handle the main taxon fields (species rank, name, common name)
        flattened_record["source"] = source
        flattened_record["taxon_code"] = taxonomy.get('id')
        flattened_record["scientific_name"] = taxonomy.get('name',"").lower()
        flattened_record["common_name"] = taxonomy.get('preferred_common_name',"").lower()
        rank = taxonomy.get('rank', '').lower()
        flattened_record["rank"] = rank

        if rank == 'species':
            flattened_record[f'{rank}_scientific_name'] = taxonomy.get('name',"").lower()
            flattened_record[f'{rank}_common_name'] = taxonomy.get('preferred_common_name',"").lower()
            flattened_record[f'{rank}_code'] = taxonomy.get('id',"")

        # 2. Handle the ancestors (higher taxonomic ranks)
        for ancestor in taxonomy.get('ancestors', []):
            ancestor_rank = ancestor.get('rank', '').lower()

            if ancestor_rank in valid_ancestors:
                flattened_record[f'{ancestor_rank}_scientific_name'] = ancestor.get('name',"").lower()
                flattened_record[f'{ancestor_rank}_common_name'] = ancestor.get('preferred_common_name',"").lower()

        flattened_record["loaded_timestamp"] = loaded_timestamp

    logger.debug("Flattened record keys: %s", list(flattened_record.keys()))
    return flattened_record


def get_taxonomy_from_csv_file(csv_dict_reader, current_timestamp=None):
    logger.info("Starting taxonomy extraction for CSV file at %s", current_timestamp)
    full_taxonomy = []

    # Loop over records and call the corresponding API for each species code
    for rec in csv_dict_reader:
        taxon = None
        source = rec.get("SOURCE")

        if source == EBIRD:
            logger.debug("Fetching eBird taxonomy for record: %s", rec)
            taxon = get_ebird_taxonomy(rec)
        elif source == INATURALIST:
            logger.debug("Fetching iNaturalist taxonomy for record: %s", rec)
            taxon = get_inaturalist_taxonomy(rec)
        else:
            logger.warning("Unknown SOURCE value in record: %s", rec)
            continue

        if taxon:
            flat_taxonomy = flatten_taxonomy(
                source=source,
                taxonomy=taxon,
                loaded_timestamp=current_timestamp,
            )
            full_taxonomy.append(flat_taxonomy)
        else:
            logger.warning("No taxonomy returned for record: %s", rec)

    logger.info("Completed taxonomy extraction. Total records: %d", len(full_taxonomy))
    return full_taxonomy


def write_taxonomy_to_oci_obj_storage(sequence, taxonomy, object_storage_client):
    if not taxonomy:
        logger.info("No taxonomy data to write for sequence %s.", sequence)
        return

    current_timestamp = datetime.now().strftime("%Y_%m_%d")
    output_file = f"{target_prefix}/{current_timestamp}_{sequence}_taxonomy.csv"
    logger.info("Preparing to write taxonomy to %s in bucket %s", output_file, bucket)

    # Create CSV in-memory
    first_row = taxonomy[0]
    fieldnames = list(first_row.keys())

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(taxonomy)

    csv_bytes = output.getvalue().encode("utf-8")

    namespace = object_storage_client.get_namespace().data
    logger.debug("Using namespace %s for put_object", namespace)

    response = object_storage_client.put_object(
        namespace_name=namespace,
        bucket_name=bucket,
        object_name=output_file,
        put_object_body=csv_bytes,
        content_type="text/csv",
    )

    logger.info("Uploaded taxonomy file %s (status=%s, etag=%s)",
                output_file, response.status, response.headers.get("etag"))


def get_ebird_taxonomy(record):
    species_code = record["TAXON_CODE"]
    url = f"https://api.ebird.org/v2/ref/taxonomy/ebird?fmt=json&species={species_code}"

    headers = {
        "X-eBirdApiToken": API_KEY
    }

    logger.debug("Requesting eBird taxonomy for species_code=%s", species_code)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data:
            taxon_info = data[0]
            logger.debug("Received eBird taxonomy for species_code=%s", species_code)
            return taxon_info
        else:
            logger.warning("No eBird results found for species code %s", species_code)
            return None
    else:
        logger.error("eBird API error %s for species_code=%s: %s",
                     response.status_code, species_code, response.text)
        return None


def get_inaturalist_taxonomy(record):
    taxon_code = record["TAXON_CODE"]
    url = f"https://api.inaturalist.org/v1/taxa/{taxon_code}"
    sleep(1)  # To avoid hitting rate limits

    logger.debug("Requesting iNaturalist taxonomy for taxon_code=%s", taxon_code)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data:
            results = data.get('results', [])
            if not results:
                logger.warning("No iNaturalist results list for taxon_code=%s", taxon_code)
                return None
            taxon_info = results[0]
            logger.debug("Received iNaturalist taxonomy for taxon_code=%s", taxon_code)
            return taxon_info
        else:
            logger.warning("Empty iNaturalist response body for taxon_code=%s", taxon_code)
            return None
    else:
        logger.error("iNaturalist API error %s for taxon_code=%s: %s",
                     response.status_code, taxon_code, response.text)
        return None


def connect_to_oci_object_storage():
    logger.info("Connecting to OCI Object Storage using default config")
    config = oci.config.from_file()
    object_storage_client = oci.object_storage.ObjectStorageClient(config)
    logger.info("Connected to OCI Object Storage")
    return object_storage_client


def get_oci_object_list(object_storage_client):
    logger.info("Listing objects from bucket=%s with prefix=%s", bucket, source_prefix)
    namespace = object_storage_client.get_namespace().data
    objects = object_storage_client.list_objects(namespace, bucket, prefix=source_prefix)

    object_list = [obj.name for obj in objects.data.objects]
    logger.info("Found %d objects", len(object_list))
    return object_list


def get_oci_obect_csv_reader(object_name, object_storage_client):
    logger.info("Fetching object %s from bucket=%s", object_name, bucket)

    response = object_storage_client.get_object(
        namespace_name=object_storage_client.get_namespace().data,
        bucket_name=bucket,
        object_name=object_name,
    )

    file_content = response.data.content.decode('utf-8')
    text_stream = io.StringIO(file_content)
    csv_reader = csv.DictReader(text_stream)

    logger.debug("Created CSV DictReader for object %s", object_name)
    return csv_reader


if __name__ == "__main__":
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info("Starting taxonomy pipeline at %s", current_timestamp)

    object_storage_client = connect_to_oci_object_storage()
    object_list = get_oci_object_list(object_storage_client)

    for i, object_name in enumerate(object_list, start=1):
        logger.info("Processing object %d/%d: %s", i, len(object_list), object_name)

        csv_dict_reader = get_oci_obect_csv_reader(object_name, object_storage_client)

        taxonomy = get_taxonomy_from_csv_file(
            csv_dict_reader=csv_dict_reader,
            current_timestamp=current_timestamp,
        )

        write_taxonomy_to_oci_obj_storage(
            sequence=i,
            taxonomy=taxonomy,
            object_storage_client=object_storage_client,
        )

    logger.info("Taxonomy pipeline completed")
