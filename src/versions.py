# type: ignore
from urllib.request import urlopen
from requests.exceptions import HTTPError
from utils import get_minecraft_dir
import requests
import json

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

    try:
        # TODO: verify jar with the sha1 hash provided by manifest
        jar_file = urlopen(jar_url)
    # This can and should probably be more specific
    except Exception as e:
        print(f"Something happened while downloading client jar: {e}")
        return None

    # C:\Users\User\AppData\Roaming\.minecraft\version\version.jar
    jar_dir = MC_DIR / "versions" / version
    jar_dir.mkdir(parents=True, exist_ok=True)

    with open(jar_dir / f"{version}.jar", "wb") as f:
        f.write(jar_file.read())

    with open(jar_dir / f"{version}.json", "w") as f:
        f.write(response.text)

def download_version_libraries(response: requests.Response) -> None:
    data = json.loads(response.text)
    libraries = data["libraries"]

    for library in libraries:
        # TODO: check rules for libraries and download depending on that
        # TODO: verify library jars with sha1 hash provided
        library_dir = MC_DIR / "libraries" / library["downloads"]["artifact"]["path"]
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