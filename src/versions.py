import requests
import json

MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

def fetch_versions():
    response = requests.get(MANIFEST_URL)
    return response.text

versions = json.loads(fetch_versions())
