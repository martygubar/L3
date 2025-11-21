# Living, Learning Laboratory

Integrate data sets from a variety of sources. These data sets contain observations made by citizen scientists, Maine naturalists and more.
* iNaturalist
* eBird
* ...

We'll start with observations found on Long Mountain Trail - which is part of the Crooked River Conservation area in the Mahoosuc Land Trust

**Location:**
Trailhead:
1268 Vernon St, Bethel, ME 04217
Lat/long: 44.59063, -70.81687

Region:
swlat = 44.33013341761004
swlng = -70.7627261302915
nelat = 44.3374896802915
nelng = -70.74935297782922


## iNaturalist
API: https://api.inaturalist.org/v1/docs/#/Posts


**Project**
https://api.inaturalist.org/v1/observations?project_id=12935

**Box**
Query: 
 quality_grade=any&identifications=any&swlat=44.33013341761004&swlng=-70.7627261302915&nelat=44.3374896802915&nelng=-70.74935297782922

Columns:
 id, uuid, observed_on_string, observed_on, time_observed_at, time_zone, user_id, user_login, user_name, created_at, updated_at, quality_grade, license, url, image_url, sound_url, tag_list, description, num_identification_agreements, num_identification_disagreements, captive_cultivated, oauth_application_id, place_guess, latitude, longitude, positional_accuracy, private_place_guess, private_latitude, private_longitude, public_positional_accuracy, geoprivacy, taxon_geoprivacy, coordinates_obscured, positioning_method, positioning_device, species_guess, scientific_name, common_name, iconic_taxon_name, taxon_id

**Project**
https://www.inaturalist.org/observations?project_id=12935


## eBird
API key: dluifppbf37a

Ebird lets you look up observations by hotspot. There is a hotspot defined for Long Mountain Trail

**Hotspot:** 
{
    "locId": "L6856791",
    "name": "Long Mountain Trail",
    "latitude": 44.3360354,
    "longitude": -70.7609439,
    "countryCode": "US",
    "countryName": "United States",
    "subnational1Name": "Maine",
    "subnational1Code": "US-ME",
    "subnational2Code": "US-ME-017",
    "subnational2Name": "Oxford",
    "isHotspot": True,
    "locName": "Long Mountain Trail",
    "lat": 44.3360354,
    "lng": -70.7609439,
    "hierarchicalName": "Long Mountain Trail, Oxford, Maine, US",
    "locID": "L6856791"
}

curl --location -g 'https://api.ebird.org/v2/data/obs/L6856791/historic/2025/10/11'

# Data fields

## Table: OBSERVATIONS
| Column           | Data type      |   Description          |
|------------------|--------------- |------------------------|
| app_id           | number         | 1-eBird, 2-iNaturalist |
| loaded_timestamp | timestamp      | when the record was loaded |
| quality_grade    | varchar2(100)  | ebird - obsValid=True/False. iNaturalist - quality_grade |
| source_id        | varchar2(100)  | Unique identifier for that observation (from the app) |
| observed_time    | timestamp.     | When the observation was made |
| scientific_name  | varchar2(200)  | Scientific name for the observation. Could be a species, genum, other |
| common_name      | varchar2(200)  | Common name for the observation |
| quantity         | number         | Number of observations for that species |
| latitude         | number         | Latitude of the observation |
| longitude        | number         | Longitude of the observation |
| location_name    | varchar2(200)  | Name of the location (e.g. Long Mountain Trail) |
| city             | varchar2(200)  | City of the observation |
| state            | varchar2(200)  | State of the observation |


## Table: TAXONOMY -
* inaturalist API to determine rank
* ebird api to determine rank info:
    * Every ebird observation has a speciesCode (which may or may not be a species). Use that code to perform a lookup
    * https://api.ebird.org/v2/ref/taxonomy/ebird?fmt=json&species={species_code}
Domain
  └─ Kingdom
       └─ Phylum (or Division for plants/fungi)
            └─ Class
                 └─ Order
                      └─ Family   ← here
                           └─ Genus
                                └─ Species
                                     └─ Subspecies / Variety / Form

Genus + Species is required to uniquely identify a species.
Example:
* albifrons appears in multiple genera:
    * Anas albifrons → White-fronted Goose
    * Motacilla albifrons → hypothetical wagtail example

| Column           | Data type      |   Description          |
|------------------|--------------- |------------------------|
| taxon_id         | number         | Unique identifier for the observed species |
| scientific_name  | varchar2(200)  | Scientific name for the observed species |
| common_name      | varchar2(200)  | Common name for the observed species |

url
image_url
sound_url
description
location
latitude
longitude
positional_accuracy
species
scientific_name
common_name,
iconic_taxon_name  
taxon_id

