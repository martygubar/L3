import requests
import csv
from datetime import datetime, timedelta
import logging
import json
import argparse

SOURCE_INATURALIST = 2
base_url = "https://api.inaturalist.org/v1/observations"

# Configure logging
log_filename = 'inaturalist_fetch.log'
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def flatten_observation(obs):
    return {
        "id": obs.get("id"),
        "observed_on": obs.get("time_observed_at"),
        "taxon_id": obs.get("taxon", {}).get("id"),
        "scientific_name": obs.get("taxon", {}).get("name"),
        "common_name": obs.get("taxon", {}).get("preferred_common_name"),
        "rank": obs.get("taxon", {}).get("rank"),
        "native": obs.get("taxon", {}).get("native"),
        "threatened": obs.get("taxon", {}).get("threatened"),         
        "place_guess": obs.get("place_guess"),
        "latitude": obs.get("geojson", {}).get("coordinates", [None, None])[1],
        "longitude": obs.get("geojson", {}).get("coordinates", [None, None])[0],
        "quality_grade": obs.get("quality_grade"),
        "observation_photo": obs.get("observation_photos")[0]["photo"]["url"] if obs.get("observation_photos") else None
    }

# Default observation location to Long Mountain Trail area
def fetch_observations(loaded_timestamp, swlat, swlng, nelat,nelng, year=None, month=None):
    
    # Set date defaults to yesterday if not provided
    if year is None or month is None:
        yesterday = datetime.now() - timedelta(days=1)
        year = yesterday.year
        month = yesterday.month

    params = {
        "swlat": swlat,
        "swlng": swlng,
        "nelat": nelat,
        "nelng": nelng,
        "quality_grade": "any",  # match export tool flexibility,
        "year": year,
        "month":month,
        "verifiable": "true",
        "per_page": 50,
        "page": 1
    }

    observations = []

    while True:
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        data = response.json()
        results = data.get("results", [])

        if not results:
            break

        observations.extend([flatten_observation(obs) for obs in results])

        print(f"Fetched page {params['page']} with {len(results)} observations")

        if params["page"] * params["per_page"] >= data.get("total_results", 0):
            break
        params["page"] += 1

    csv_filename = "inaturalist_export_tool_style.csv"
    if observations:
        with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = observations[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(observations)
        print(f"Export saved to {csv_filename}")
    else:
        print("No observations found.")

def main():
    # Default to Long Mountain Trail area
    region_name= "Long Mountain Trail"

    parser = argparse.ArgumentParser(description="Process eBird observations within a date range and region.")
    parser.add_argument('--start_month', default="2017-01",required=False, help='Start month (YYYY-MM)')
    parser.add_argument('--end_month', default=datetime.now().strftime('%Y-%m'), required=False, help='End month (YYYY-MM)')
    parser.add_argument('--region_name', default=region_name, required=False, help='Name for the region (e.g., Long Mountain Trail)')
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

    fetch_observations(loaded_timestamp=current_timestamp, region_name=region_name,swlat=swlat, swlng=swlng, nelat=nelat,nelng=nelng, start_month=start_month, end_month=end_month)
    
if __name__ == "__main__":
    main()