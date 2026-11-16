# type: ignore
from versions import fetch_versions, download_version_jar, download_version_libraries
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
        
        download_version_jar(version["id"], response)
        download_version_libraries(response)
        break