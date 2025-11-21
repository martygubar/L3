import requests

# Your eBird API key
API_KEY = "dluifppbf37a"

# Species code to look up
species_code = "dowwoo"

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
        print(taxon_info)
        #print("Scientific Name:", taxon_info.get("sciName"))
        #print("Common Name:", taxon_info.get("comName"))
        #print("Order:", taxon_info.get("order"))
        #print("Family:", taxon_info.get("family"))
        #print("Genus:", taxon_info.get("genus"))
        #print("Species Code:", taxon_info.get("speciesCode"))
    else:
        print(f"No results found for species code {species_code}")
else:
    print(f"Error {response.status_code}: {response.text}")
