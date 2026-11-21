# type: ignore
from versions import fetch_versions, download_version_jar, download_version_manifest
from assets import download_asset_index, download_assets
from libraries import download_libraries
from requests.exceptions import HTTPError
import requests

latest = fetch_versions(options="latest_release")

all_versions = fetch_versions(options="all")

# TODO: this logic should be in fetch_versions i think
for version in all_versions:
    if version["id"] == latest:
        try:
            # Open version manifest
            response = requests.get(version["url"])
            response.raise_for_status()
        except HTTPError as e:
            print(f"Something happened when fetching version-specific manifest: {e}")
        
        print("Downloading client JAR")
        download_version_jar(version["id"], response)
        print("Downloaded client JAR")

        print("Downloading version manifest")
        download_version_manifest(version["id"], response)
        print("Downloaded version manifest")

        print("Downloading asset index")
        asset_index = download_asset_index(response)
        print("Downloaded asset index")

        print("Downloading libraries")
        download_version_libraries(response)
        print("Downloaded libraries")

        print("Downloading assets")
        with open(asset_index, "r") as f:
            download_assets(f.read())
        print("Downloaded assets")
        break