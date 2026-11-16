# type: ignore
from urllib.request import urlopen
from pathlib import Path
from requests.exceptions import HTTPError
from os import path
import requests
import json

# TODO: make this cross-platform
MC_DIR = path.expandvars("%APPDATA%\\.minecraft")
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

def download_version_jar(version: str, response: requests.Response):
    # TODO: pass the manifest directly to this function instead of fetching it 
    data = json.loads(response.text)

    jar_url = data["downloads"]["client"]["url"]

    try:
        jar_file = urlopen(jar_url)
    # This can and should probably be more specific
    except Exception as e:
        print(f"Something happened while downloading client jar: {e}")

    # C:\Users\User\AppData\Roaming\.minecraft\version\version.jar
    jar_dir = Path(MC_DIR) / "versions" / version
    jar_dir.mkdir(parents=True, exist_ok=True)

    with open(jar_dir / f"{version}.jar", "wb") as f:
        f.write(jar_file.read())

