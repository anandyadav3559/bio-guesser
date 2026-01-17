import requests
import json
from datetime import datetime
from datetime import UTC
import geohash
def fetch_api_data(scientific_name, country="IN", hasCoordinate=True, mediaType="StillImage", limit=1, offset=0):
    url = f"https://api.gbif.org/v1/occurrence/search?scientificname={scientific_name}&country={country}&hasCoordinate={hasCoordinate}&mediaType={mediaType}&limit={limit}&offset={offset}"
    response = requests.get(url)
    return response.json()["results"]

def extracting_features(data):
    if not data:
        return []
    animals = []
    for item in data:
        try:
            specificEpithet = item.get("specificEpithet")
            genericName = item.get("genericName")
            key = item.get("key")
            species_key = item.get("speciesKey")
            modified = item.get("modified")
            ingested_at = datetime.now(UTC).isoformat()
            decimalLatitude = item.get("decimalLatitude")
            decimalLongitude = item.get("decimalLongitude")
            payload = item
            
            media = item.get("media", [])
            image_url = media[0].get("identifier") if media else None
            
            animal = {
                "scientific_name":specificEpithet+"_"+genericName,
                "occurance_key": key,
                "species_key": species_key,
                "source_modified": modified,
                "source_ingested_at": ingested_at,
                "location":{
                    "latitude": decimalLatitude,
                    "longitude": decimalLongitude,
                    "geo_hash": geohash.encode(decimalLatitude, decimalLongitude, precision=6)
                },
                "image_url": image_url,
                "payload":item,

            }
            animals.append(animal)
        except Exception as e:
            print(f"Skipping item due to error: {e}")
            continue
    return animals


def dump_data(data):
    path = "data/data.json"
    try:
        with open(path, "r") as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.append(data)

    with open(path, "w") as f:
        json.dump(existing_data, f, indent=4)

if __name__=='__main__':

    scientific_name="Ophiophagus hannah"

    limit = 30


    try:
        with open("offset.json", "r") as f:
            offset = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        offset = {}
    data = fetch_api_data(scientific_name,limit=limit,offset=offset.get(scientific_name,0))
    offset[scientific_name] = offset.get(scientific_name,0)+limit
    with open("offset.json","w") as file:
        json.dump(offset,file)
    results = extracting_features(data)
    for item in results:
        dump_data(item)
    
    