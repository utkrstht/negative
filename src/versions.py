from urllib.request import urlopen
from requests.exceptions import HTTPError
import requests
import json

MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

# TODO: cache the manifest
def fetch_versions(options: str = "latest_release"):
    try:
        # Open version manifest
        response = requests.get(MANIFEST_URL)
        response.raise_for_status() 
    except HTTPError as e:
        print(f"Something happened while fetching version manifest: {e.response.text}")   

    data = json.loads(response.text)

    # I am very sure that this is not the way to go but I don't know what to do
    if options == "latest_release":
        return data["latest"]["release"]
    elif options == "latest_snapshot":
        return data["latest"]["snapshot"]
    elif options == "all":
        return data["versions"]

def download_version_jar(version: dict):
    try:
        # Open version manifest
        response = requests.get(version["url"])
        response.raise_for_status()
    except HTTPError as e:
        print(f"Something happened when fetching version-specific manifest: {e}")
        
    data = json.loads(response.text)

    jar_url = data["downloads"]["client"]["url"]

    try:
        jar_file = urlopen(jar_url)
    # This can and should probably be more specific
    except Exception as e:
        print(f"Something happened while downloading client jar: {e}")

    # TODO: write to .minecraft
    with open(f"{version["id"]}_client.jar", "wb") as f:
        f.write(jar_file.read())