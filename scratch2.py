import requests
import csv
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import logging
import json
import argparse

SOURCE_INATURALIST = 2
id="131214"
base_url = f"https://api.inaturalist.org/v1/taxa/{id}"
response = requests.get(base_url)
if response.status_code != 200:
    print(f"Error fetching data. Status code: {response.status_code}")

data = response.json()
results = data.get("results", [])

print(results)