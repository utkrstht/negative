# type: ignore
from urllib.request import urlopen
from requests.exceptions import HTTPError
from utils import get_minecraft_dir, check_sha1_hash, get_operating_system
import tempfile
import requests
import json
import shutil

MC_DIR = get_minecraft_dir()
MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

# TODO: cache the manifest
def fetch_versions(options: str = "latest_release") -> str | dict:
    try:
        # Open version manifest
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

# This function also downloads the JSON manifest for the jar
def download_version_jar(version: str, response: requests.Response) -> None:
    data = json.loads(response.text)

    jar_url = data["downloads"]["client"]["url"]
    jar_hash = data["downloads"]["client"]["sha1"]

    try:
        # TODO: shift this to a utils helper and properly download items
        jar_file = urlopen(jar_url)
    # This can and should probably be more specific
    except Exception as e:
        print(f"Something happened while downloading client jar: {e}")
        return None

    # C:\Users\User\AppData\Roaming\.minecraft\version\version.jar
    jar_dir = MC_DIR / "versions" / version
    jar_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(mode='wb') as t:
        t.write(jar_file.read())

        t.seek(0)

        if not check_sha1_hash(f"{str(jar_dir)}\\{version}.jar", jar_hash):
            raise ValueError("The client jar hash does not match the given hash from manifest, the downloaded jar is corrupted.")
    
        with open(jar_dir / f"{version}.jar", "wb") as f:
            shutil.copyfileobj(f,)


def download_version_manifests(version: str, response: requests.Response) -> None:
    data = json.loads(response.text)

    jar_manifest_dir = MC_DIR / "versions" / version / f"{version}.json"

    asset_index_id = data["assetIndex"]["id"]
    asset_index_dir = MC_DIR / "assets" / "indexes" / f"{asset_index_id}.json"
    asset_index_url = data["assetIndex"]["url"]
    asset_index_hash = data["assetIndex"]["sha1"]

    asset_index_dir.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        asset_index = urlopen(asset_index_url)
    except Exception as e:
        print(f"Something happened while fetching asset index: {e}")
        return None

    with open(jar_manifest_dir, 'w') as f:
        f.write(response.text)

    with open(asset_index_dir, 'wb') as f:
        f.write(asset_index.read())

    if not check_sha1_hash(asset_index_dir, asset_index_hash):
        raise ValueError("The asset index hash does not match the given hash from manifest, the asset index is corrupted.")

def download_version_libraries(response: requests.Response) -> None:
    data = json.loads(response.text)
    libraries = data["libraries"]

    for library in libraries:
        library_dir = MC_DIR / "libraries" / library["downloads"]["artifact"]["path"]
        library_hash = library["downloads"]["artifact"]["sha1"]
        library_rules = library.get("rules")

        if library_rules:
            # Based on my analysis of the manifest, I'm pretty sure the only rules for the libraries are for the operating system
            os = library_rules[0]["os"]["name"]
            # If the library isn't meant for our operating system, skip it
            if not os == get_operating_system():
                continue

        library_saved = library_dir.exists()
        if library_saved:
            continue

        library_dir.parent.mkdir(parents=True, exist_ok=True)

        try:
            # This is inconsistent but I don't like the other methods that use requests instead
            library_jar = urlopen(library["downloads"]["artifact"]["url"])
        except Exception as e:
            print(f"Something happened while downloading library {library["name"]}: {e}")
            return None

        with open(library_dir, "wb") as f:
            f.write(library_jar.read())   

        if not check_sha1_hash(str(library_dir), library_hash):
            raise ValueError(f"The library ({library["name"]}) jar hash does not match the given hash from manifest, the library jar is corrupted.")


