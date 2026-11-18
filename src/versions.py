# type: ignore
from urllib.request import urlopen
from requests.exceptions import HTTPError
from utils import get_minecraft_dir, check_sha1_hashs, check_sha1_hashf, get_operating_system
from shutil import copyfileobj
from tempfile import TemporaryFile
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

    jar_dir.parent.mkdir(parents=True, exist_ok=True)

    if jar_dir.is_file() and check_sha1_hashf(jar_dir, jar_hash):
        # Client JAR is already downloaded
        return None

    try:
        with requests.get(jar_url, stream=True, timeout=120) as response:
            response.raise_for_status()

            with TemporaryFile() as t:
                # Streaming download
                copyfileobj(response.raw, t)

                if not check_sha1_hashs(t, jar_hash):
                    raise ValueError("The client jar hash does not match the given hash from manifest, the downloaded jar is corrupted.")

                with open(jar_dir, "wb") as f:
                    copyfileobj(t, f)
    except requests.RequestException as e:
        print(f"Something happened while downloading client jar: {e}")
        return None

def download_version_manifests(version: str, response: requests.Response) -> None:
    data = json.loads(response.text)

    jar_manifest_dir = MC_DIR / "versions" / version / f"{version}.json"

    asset_index_id = data["assetIndex"]["id"]
    asset_index_dir = MC_DIR / "assets" / "indexes" / f"{asset_index_id}.json"
    asset_index_url = data["assetIndex"]["url"]
    asset_index_hash = data["assetIndex"]["sha1"]

    # C:\Users\User\AppData\Roaming\.minecraft\assets\indexes
    asset_index_dir.parent.mkdir(parents=True, exist_ok=True)

    if asset_index_dir.is_file() and check_sha1_hashf(asset_index_dir, asset_index_hash):
        # Asset index is already downloaded
        return None
    
    try:
        with requests.get(asset_index_url, stream=True, timeout=120) as response:
            response.raise_for_status()

            with TemporaryFile() as t:
                # Streaming download
                copyfileobj(response.raw, t)

                if not check_sha1_hashs(t, asset_index_hash):
                    raise ValueError("The asset index hash does not match the given hash from manifest, the asset index is corrupted")

                with open(asset_index_dir, "wb") as f:
                    copyfileobj(t, f)
    except requests.RequestException as e:
        print(f"Something happened while downloading asset index: {e}")
        return None

    # No checks on this one because this IS the source of truth
    with open(jar_manifest_dir, 'w') as f:
        f.write(response.text)

def download_version_libraries(response: requests.Response) -> None:
    data = json.loads(response.text)
    libraries = data["libraries"]

    for library in libraries:
        library_dir = MC_DIR / "libraries" / library["downloads"]["artifact"]["path"]
        library_url = library["downloads"]["artifact"]["url"]
        library_hash = library["downloads"]["artifact"]["sha1"]
        library_rules = library.get("rules")

        if library_rules:
            # Based on my analysis of the manifest, I'm pretty sure the only rules for the libraries are for the operating system
            # Future me: This is mostly true for modern versions, but some versions before 1.19 also include other fields, I will work on this later.
            os = library_rules[0]["os"]["name"]
            # If the library isn't meant for our operating system, skip it
            if not os == get_operating_system():
                continue

        if library_dir.is_file() and check_sha1_hashf(library_dir, library_hash):
            # Library already exists
            return None

        library_dir.parent.mkdir(parents=True, exist_ok=True)

        try:
            with requests.get(library_url, stream=True, timeout=120) as response:
                response.raise_for_status()

                with TemporaryFile() as t:
                    copyfileobj(response.raw, t)

                    if not check_sha1_hashs(t, library_hash):
                        raise ValueError(f"The library {library['name']} hash does not match the given hash from manifest, the library is corrupted.")

                    with open(library_dir, "wb") as f:
                        copyfileobj(t, f)

        except requests.RequestException as e:
            print(f"Something happened while downloading library {library['name']}: {e}")

