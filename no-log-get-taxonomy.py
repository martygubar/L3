import oci
import io
import csv
import requests
from datetime import datetime


# File properties
bucket = 'gold'
source_prefix = 'observed_species'
target_prefix = 'taxonomy'
API_KEY = "dluifppbf37a"
EBIRD="1"
INATURALIST="2"

# Flatten the taxonomy into a standard record
def flatten_taxonomy(source, taxonomy, loaded_timestamp=None):
    flattened_record = {}
    valid_ancestors = ['species', 'genus', 'family', 'order', 'class']
    
    if source == EBIRD:
        flattened_record = {
            "source": source,
            "taxon_code": taxonomy.get("speciesCode"),
            "scientific_name": taxonomy.get("sciName"),
            "common_name": taxonomy.get("comName"),
            "rank": taxonomy.get("category"),
            "species_code": taxonomy.get("speciesCode"),
            "species_scientific_name": taxonomy.get("speciesSciName"),
            "species_common_name": taxonomy.get("speciesComName"),
            "genus_code": "",
            "genus_scientific_name": "",
            "genus_common_name": "",
            "family_code": taxonomy.get("familyCode"),
            "family_scientific_name": taxonomy.get("familySciName"),
            "family_common_name": taxonomy.get("familyComName"),
            "order_code": "",
            "order_scientific_name": taxonomy.get("order"),
            "order_common_name": "",
            "class_code": "",
            "class_scientific_name": "",
            "class_common_name": "",
            "loaded_timestamp":loaded_timestamp
        }
    elif source == INATURALIST:
        
        flattened_record = {}

        # 1. Handle the main taxon fields (species rank, name, common name)
        # We ensure the rank is lowercase for consistent keys
        flattened_record["source"] = source
        flattened_record["taxon_code"] = taxonomy.get('id')
        flattened_record["scientific_name"] = taxonomy.get('name')
        flattened_record["common_name"] = taxonomy.get('preferred_common_name')
        rank = taxonomy.get('rank', 'unknown_rank').lower()
        flattened_record["rank"] = rank

        if rank == 'species':
            flattened_record[f'{rank}_scientific_name'] = taxonomy.get('name')
            flattened_record[f'{rank}_common_name'] = taxonomy.get('preferred_common_name')
            flattened_record[f'{rank}_code'] = taxonomy.get('id')

        # 2. Handle the ancestors (higher taxonomic ranks)
        for ancestor in taxonomy.get('ancestors', []):
            ancestor_rank = ancestor.get('rank', 'unknown_ancestor_rank').lower()

            if ancestor_rank in valid_ancestors:    
                flattened_record[f'{ancestor_rank}_scientific_name'] = ancestor.get('name')
                flattened_record[f'{ancestor_rank}_common_name'] = ancestor.get('preferred_common_name')
            
        flattened_record["loaded_timestamp"] = loaded_timestamp
    return flattened_record

def get_taxonomy_from_csv_file(csv_dict_reader, current_timestamp=None):
    full_taxonomy = []

    # Loop over records and call the corresponding API for each species code    
    for rec in csv_dict_reader:
        taxon = None

        if rec["SOURCE"] == EBIRD:
            taxon = get_ebird_taxonomy(rec)
        elif rec["SOURCE"] == INATURALIST:
            taxon = get_inaturalist_taxonomy(rec)

        if taxon:
            flat_taxonomy = flatten_taxonomy(source=rec["SOURCE"], taxonomy=taxon, loaded_timestamp=current_timestamp)
            full_taxonomy.append(flat_taxonomy)

    return full_taxonomy

def write_taxonomy_to_oci_obj_storage(sequence, taxonomy, object_storage_client):
    if not taxonomy:
        print("No taxonomy data to write.")
        return

    # Define output file name    
    current_timestamp = datetime.now().strftime("%Y_%m_%d")
    output_file = f"{target_prefix}/{current_timestamp}_{sequence}_taxonomy.csv"    
    
    # Create CSV in-memory
    first_row = taxonomy[0]
    fieldnames = list(first_row.keys())

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(taxonomy)

    csv_bytes = output.getvalue().encode("utf-8")

    # Upload CSV
    response = object_storage_client.put_object(
        namespace_name=object_storage_client.get_namespace().data,
        bucket_name=bucket,
        object_name=output_file,
        put_object_body=csv_bytes,
        content_type="text/csv"
    )

    print("Status:", response.status)
    print("ETag:", response.headers.get("etag"))

def get_ebird_taxonomy(record):
    # species code may or may not be an actual species....
    species_code = record["TAXON_CODE"] 

    # eBird taxonomy API URL
    url = f"https://api.ebird.org/v2/ref/taxonomy/ebird?fmt=json&species={species_code}"

    # Set up headers with your API key
    headers = {
        "X-eBirdApiToken": API_KEY
    }

    # Make the request
    response = requests.get(url, headers=headers)

    # Check for errors
    if response.status_code == 200:
        data = response.json()
        if data:
            # The API returns a list of taxa, even for a single species code
            taxon_info = data[0]
            return taxon_info
        else:
            print(f"No results found for species code {species_code}")
            return None
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
    
def get_inaturalist_taxonomy(record):
    # species code may or may not be an actual species....
    taxon_code = record["TAXON_CODE"] 

    # eBird taxonomy API URL
    url = f"https://api.inaturalist.org/v1/taxa/{taxon_code}"

    # Make the request
    response = requests.get(url)

    # Check for errors
    if response.status_code == 200:
        data = response.json()
        if data:
            # The API returns a list of taxa, even for a single species code
            taxon_info = data.get('results', [])[0]
            return taxon_info
        else:
            print(f"No results found for species code {taxon_code}")
            return None
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None    

def connect_to_oci_object_storage():
    # Load config (~/.oci/config)
    config = oci.config.from_file()
    object_storage_client = oci.object_storage.ObjectStorageClient(config)

    return object_storage_client

def get_oci_object_list(object_storage_client):
    object_list = []
    namespace = object_storage_client.get_namespace().data
    objects = object_storage_client.list_objects(namespace, bucket, prefix=source_prefix)

    for obj in objects.data.objects:
        object_list.append(obj.name)
    
    return object_list

def get_oci_obect_csv_reader(object_name, object_storage_client):

    # Get object
    response = object_storage_client.get_object(
        namespace_name=object_storage_client.get_namespace().data,
        bucket_name=bucket,
        object_name=object_name
    )

    # This consumes the stream fully and closes it right away.
    file_content = response.data.content.decode('utf-8')

    # Now we can safely use io.StringIO to treat the in-memory string as a file
    text_stream = io.StringIO(file_content)
    csv_reader = csv.DictReader(text_stream)

    return csv_reader

if __name__ == "__main__":
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    object_storage_client = connect_to_oci_object_storage()
    object_list = get_oci_object_list(object_storage_client)
    i = 0
    for object_name in object_list:
        i += 1
        print(f"Processing object: {object_name}")
        csv_dict_reader = get_oci_obect_csv_reader(object_name, object_storage_client)

        # Get taxonomies from this csv file
        taxonomy = get_taxonomy_from_csv_file(csv_dict_reader=csv_dict_reader,current_timestamp=current_timestamp)

        # Write taxonomy to OCI Object Storage
        write_taxonomy_to_oci_obj_storage(sequence=i,taxonomy=taxonomy, object_storage_client=object_storage_client)


        