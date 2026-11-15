import requests
import json

MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

# TODO: cache the manifest
def fetch_versions():
    # Currently fetches all versions (the entire manifest)
    # I should add some options to get specific attributes
    response = requests.get(MANIFEST_URL)
    data = json.loads(response.text)

    return data



