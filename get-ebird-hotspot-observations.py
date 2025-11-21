import os
import sys
import requests
import csv
from datetime import datetime, timedelta
import logging
import argparse

# Source: eBird=1
SOURCE_EBIRD = 1

# Configure logging
log_filename = 'ebird_fetch.log'
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def flatten_observation(obs):
    return {
        "id": obs.get("obsId"),
        "checklist_id": obs.get("checklistId"),
        "observed_on": obs.get("obsDt"),
        "species_code": obs.get("speciesCode"),
        "scientific_name": obs.get("sciName"),
        "common_name": obs.get("comName"),
        "how_many": obs.get("howMany"),        
        "location_id": obs.get("locId"),       
        "location_name": obs.get("locName"),
        "state": obs.get("subnational1Name"),
        "country": obs.get("countryCode"),
        "latitude": obs.get("lat"),
        "longitude": obs.get("lng"),
        "obs_valid": obs.get("obsValid")
    }

def fetch_ebird_observations(loaded_timestamp, region_code, year, month, day, detail="full"):
    logging.info(f"Script run for date: {year}-{month:02d}-{day:02d}, region: {region_code}")
    ebird_api_key = "dluifppbf37a"

    url = f"https://api.ebird.org/v2/data/obs/{region_code}/historic/{year}/{str(month).zfill(2)}/{str(day).zfill(2)}?detail={detail}"

    headers = {
        'X-eBirdApiToken': ebird_api_key
    }

    try:
        observations = []
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            results = response.json()
            count = len(results)
            logging.info(f"Number of records found: {count}")

            if count == 0:
                logging.info("No observations found for the specified date and region.")
                return

            observations.extend([flatten_observation(obs) for obs in results])

            # file: YYYYMMDD_ebird_observations_{region_code}.csv
            filename = f"./eBird/{year}{str(month).zfill(2)}{str(day).zfill(2)}_ebird_observations_{region_code}.csv"
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            with open(filename, 'w', newline='') as csvfile:
                fieldnames = observations[0].keys()
                extended_fieldnames = list(observations[0].keys()) + ['loaded_timestamp', 'source']
                writer = csv.DictWriter(csvfile, fieldnames=extended_fieldnames)
                writer.writeheader()
                for obs in observations:
                    obs['loaded_timestamp'] = loaded_timestamp
                    obs['source'] = SOURCE_EBIRD
                    writer.writerow(obs)

            logging.info(f"Data successfully written to {filename}")
        else:
            error_msg = f"Error fetching data: {response.status_code} - {response.text}"
            logging.error(error_msg)
    except Exception as e:
        logging.error(f"Exception occurred: {str(e)}")

def fetch_ebird_every_day(loaded_timestamp,region_code, start_date, end_date, detail="full"):
    current_date = start_date
    while current_date <= end_date:
        fetch_ebird_observations(
            loaded_timestamp=loaded_timestamp,
            region_code=region_code,
            year=current_date.year,
            month=current_date.month,
            day=current_date.day,
            detail=detail
        )
        current_date += timedelta(days=1)

def main():
    long_mountain_trail = 'L6856791'  # Example hotspot region code

    parser = argparse.ArgumentParser(description="Process eBird observations within a date range and region.")
    parser.add_argument('--start_date', default=datetime.strptime("2017-01-01", "%Y-%m-%d"),required=False, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end_date', default=datetime.now(), required=False, help='End date (YYYY-MM-DD)')
    parser.add_argument('--region_code', default=long_mountain_trail, required=False, help='Region code (e.g., US-ME)')
    args = parser.parse_args()

    start_date = args.start_date
    end_date = args.end_date
    region_code = args.region_code
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    fetch_ebird_every_day(loaded_timestamp=current_timestamp, region_code=region_code, start_date=start_date, end_date=end_date, detail="full")

if __name__ == "__main__":
    main()

