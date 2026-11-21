# type: ignore
from requests.exceptions import HTTPError
from utils import get_minecraft_dir, get_operating_system, download_file, create_requests_session
import requests
import json

MC_DIR = get_minecraft_dir()
MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

# TODO: cache the manifest
def fetch_versions(options: str = "latest_release") -> str | dict:
    try:
        # Open version manifests
        response = requests.get(MANIFEST_URL)
        response.raise_for_status() 
    except HTTPError as e:
        print(f"Something happened while fetching version manifest: {e.response.text}") 
        return None

    data = json.loads(response.text)

    # I am very sure that this is not the way to go but I don't know what to do
    if options == "latest_release":
        return data["latest"]["release"]
    elif options == "latest_snapshot":
        return data["latest"]["snapshot"]
    elif options == "all":
        return data["versions"]

def download_version_jar(version: str, response: requests.Response) -> None:
    data = json.loads(response.text)

    jar_url = data["downloads"]["client"]["url"]
    jar_hash = data["downloads"]["client"]["sha1"]
    # C:\Users\User\AppData\Roaming\.minecraft\version\version.jar
    jar_dir = MC_DIR / "versions" / version / f"{version}.jar"

    try:
        download_file(jar_url, jar_dir, jar_hash)
    except requests.RequestException as e:
        print(f"Something happened while downloading client jar: {e}")
        return None

def download_version_manifest(version: str, response: requests.Response) -> None:
    jar_manifest_dir = MC_DIR / "versions" / version / f"{version}.json"

    # No checks on this one because this IS the source of truth
    with open(jar_manifest_dir, 'w') as f:
        f.write(response.text)