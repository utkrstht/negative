from utils import download_file, create_requests_session, get_operating_system
from versions import MC_DIR
import json
import requests

def download_libraries(response: requests.Response) -> None:
    data = json.loads(response.text)
    libraries = data["libraries"]

    session = create_requests_session()

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

        try:
           download_file(library_url, library_dir, library_hash, session)
        except requests.RequestException as e:
            print(f"Something happened while downloading library {library['name']}: {e}")


