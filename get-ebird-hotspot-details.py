import os
from ebird.api import get_hotspot

ebird_api_key="dluifppbf37a"

# Specify the hotspot location ID (e.g., "L2313391")
hotspot_id = "L6856791"

# Fetch hotspot details
hotspot_info = get_hotspot(ebird_api_key, hotspot_id)

print(hotspot_info)
