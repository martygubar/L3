import requests
import json

scientific_name = "Setophaga coronata"  # Yellow-rumped Warbler

url = "https://api.inaturalist.org/v1/taxa"
params = {"q": scientific_name, "rank": "species"}
response = requests.get(url, params=params)

taxon = response.json()
print(json.dumps(taxon, indent=2))
#print("Target taxon:", taxon["preferred_common_name"])

# Ancestors array - from kingdom down to parent
#for ancestor in taxon.get("ancestors", []):
#    print(f"Rank: {ancestor['rank']}, Name: {ancestor['name']}")
