import requests
import csv
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import logging
import json
import argparse

SOURCE_INATURALIST = 2
base_url = "https://api.inaturalist.org/v1/observations"
updated_files = []

# Configure logging
log_filename = 'inaturalist_fetch.log'
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def flatten_observation(obs, loaded_timestamp=None, location_name=None):
    iso_string = obs.get("time_observed_at")
    dt = datetime.fromisoformat(iso_string)
    observed_on = dt.strftime("%Y-%m-%d %H:%M")

    return {
        "id": obs.get("id"),
        "observed_on": observed_on,
        "taxon_id": obs.get("taxon", {}).get("id"),
        "scientific_name": obs.get("taxon", {}).get("name"),
        "common_name": obs.get("taxon", {}).get("preferred_common_name"),
        "rank": obs.get("taxon", {}).get("rank"),
        "native": obs.get("taxon", {}).get("native"),
        "threatened": obs.get("taxon", {}).get("threatened"),         
        "place_guess": obs.get("place_guess"),
        "location_name": location_name,
        "latitude": obs.get("geojson", {}).get("coordinates", [None, None])[1],
        "longitude": obs.get("geojson", {}).get("coordinates", [None, None])[0],
        "obs_validity": obs.get("quality_grade"),
        "observation_photo": obs.get("observation_photos")[0]["photo"]["url"] if obs.get("observation_photos") else None,
        "loaded_timestamp":loaded_timestamp,
        "source": SOURCE_INATURALIST
    }

# Fetch observations for a specific month and bounding box
def fetch_observations(loaded_timestamp, swlat, swlng, nelat,nelng, region_name=None,this_year=None, this_month=None):
    logging.info(f"Script run for date: {this_year}-{this_month:02d}, region: {region_name}")
    
    bad_chars = '\\/:*?"<>|'

    clean_region_name = region_name.lower().replace(" ","_") if region_name else "no_region_name"
    trans = clean_region_name.maketrans({ch: "_" for ch in bad_chars})

    clean_region_name = clean_region_name.translate(trans)

    params = {
        "swlat": swlat,
        "swlng": swlng,
        "nelat": nelat,
        "nelng": nelng,
        "quality_grade": "any",  # match export tool flexibility,
        "year": this_year,
        "month":this_month,
        "verifiable": "true",
        "per_page": 50,
        "page": 1
    }

    observations = []

    while True:
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            logging.info(f"Error fetching data. Status code: {response.status_code}")
            break

        data = response.json()
        logging.info(f"Number of records found: {data.get('total_results', 0)}")
        results = data.get("results", [])

        if not results:
            logging.info("No observations found for the specified date and region.")
            break

        observations.extend([flatten_observation(obs, loaded_timestamp=loaded_timestamp, location_name=region_name) for obs in results])

        logging.info(f"Fetched page {params['page']} with {len(results)} observations")

        if params["page"] * params["per_page"] >= data.get("total_results", 0):
            break
        params["page"] += 1

    csv_filename = f"./iNaturalist/{this_year}{str(this_month).zfill(2)}_inaturalist_observations_{clean_region_name}.csv"
    if observations:
        with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = observations[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(observations)
        logging.info(f"Export saved to {csv_filename}")
        updated_files.append(csv_filename)
    else:
        logging.info("No observations to write to CSV.")


def fetch_every_month(loaded_timestamp, swlat, swlng, nelat, nelng, region_name=None, start_month=None, end_month=None):
    """
    start_month, end_month: 'YYYY-MM' strings, e.g. '2024-01'
    """
    if start_month is None or end_month is None:
        raise ValueError("start_month and end_month must be 'YYYY-MM' strings")

    # Parse YYYY-MM into datetime objects (day fixed as 1)
    current = datetime.strptime(start_month, "%Y-%m")
    end = datetime.strptime(end_month, "%Y-%m")

    while current <= end:
        result = fetch_observations(
            loaded_timestamp=loaded_timestamp,
            swlat=swlat,
            swlng=swlng,
            nelat=nelat,
            nelng=nelng,
            region_name=region_name,
            this_year=current.year,
            this_month=current.month
        )

        # Advance to next month
        current += relativedelta(months=1)

    return 


def main():
    # Default to Long Mountain Trail area
    long_mountain_trail_region_name= "Long Mountain Trail"

    parser = argparse.ArgumentParser(description="Process eBird observations within a date range and region.")
    parser.add_argument('--start_month', default="2017-01",required=False, help='Start month (YYYY-MM)')
    parser.add_argument('--end_month', default=datetime.now().strftime('%Y-%m'), required=False, help='End month (YYYY-MM)')
    parser.add_argument('--region_name', default=long_mountain_trail_region_name, required=False, help='Name for the region (e.g., Long Mountain Trail)')
    parser.add_argument('--swlat', type=float, default=44.33013341761004, required=False, help='Southwest latitude')
    parser.add_argument('--swlng', type=float, default=-70.7627261302915, required=False, help='Southwest longitude')
    parser.add_argument('--nelat', type=float, default=44.3374896802915, required=False, help='Northeast latitude')
    parser.add_argument('--nelng', type=float, default=-70.74935297782922, required=False, help='Northeast longitude')

    args = parser.parse_args()

    start_month = args.start_month
    end_month   = args.end_month
    region_name = args.region_name
    swlat = args.swlat
    swlng = args.swlng
    nelat = args.nelat
    nelng = args.nelng
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    fetch_every_month(loaded_timestamp=current_timestamp, region_name=region_name,swlat=swlat, swlng=swlng, nelat=nelat,nelng=nelng, start_month=start_month, end_month=end_month)

    print("Updated files:") 
    for file in updated_files:
        print(file)

if __name__ == "__main__":
    main()
