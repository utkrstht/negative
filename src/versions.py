from urllib.request import urlopen
import requests
import json

MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

# TODO: cache the manifest
def fetch_versions(options: str = "latest_release"):
    response = requests.get(MANIFEST_URL)
    data = json.loads(response.text)

    # I am very sure that this is not the way to go but I don't know what to do
    if options == "latest_release":
        return data["latest"]["release"]
    elif options == "latest_snapshot":
        return data["latest"]["snapshot"]
    elif options == "all":
        return data["versions"]

def download_version_jar(version: dict):
    response = requests.get(version["url"])
    data = json.loads(response.text)

    jar_url = data["downloads"]["client"]["url"]

    jar_file = urlopen(jar_url)

    # TODO: write to .minecraft
    with open(f"{version["id"]}_client.jar", "wb") as f:
        f.write(jar_file.read())
        


