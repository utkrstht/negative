from utils import download_file, create_requests_session, get_operating_system, get_system_architecture
from pathlib import Path
from java import extract_jar
from concurrent.futures import ThreadPoolExecutor
from versions import MC_DIR
import requests

def parse_library_name(library_name: str) -> dict:
    parts = library_name.split(":")

    group_id = parts[0]
    artifact_id = parts[1]
    version = parts[2]
    # Classifer is optional
    classifer = parts[3] if len(parts) > 3 else None

    maven_coords = {"group_id": group_id, "artifact_id": artifact_id, "version": version, "classifer": classifer}

    return maven_coords

def should_i_download_this_library_on_my_pc(library: dict) -> bool:
    library_rules = library.get("rules")
    library_name = library['name']

    maven_coords = parse_library_name(library_name)
    classifier = maven_coords['classifer']

    if classifier:
        os = get_operating_system()
        arch = get_system_architecture()

        # Normalize classifier to match our naming schemes
        classifier = classifier.lower().replace("macos", "osx").replace("aarch_64", "arm64")
        if os in classifier:
            # If no architecture is listed, assume it's x86_64 
            if arch in classifier or (arch == "x86_64" and "arm64" not in classifier):
                return True
        else:
            return False

    if library_rules:
        # Based on my analysis of the manifest, I'm pretty sure the only rules for the libraries are for the operating system
        # Future me: This is mostly true for modern versions, but some versions before 1.19 also include other fields, I will work on this later.
        action = library_rules[0]["action"]
        os = library_rules[0]["os"]["name"]
        # If the library isn't meant for our operating system, skip it
        if not os == get_operating_system() and action == "allow":
            return False

    return True

def process_native_library(library_dir: Path) -> None:
    natives_dir = MC_DIR / "natives"

    extract_jar(library_dir, natives_dir)

def process_library(session: requests.Session, library: dict) -> None:
    library_dir = MC_DIR / "libraries" / library["downloads"]["artifact"]["path"]
    library_url = library["downloads"]["artifact"]["url"]
    library_hash = library["downloads"]["artifact"]["sha1"]
    library_name = library['name']

    if not should_i_download_this_library_on_my_pc(library):
        # Not for our computer
        return None

    try:
        download_file(library_url, library_dir, library_hash, session)
    except requests.RequestException as e:
        print(f"Something happened while downloading library {library_name}: {e}")
        return None

    if 'native' in library_name:
        process_native_library(library_dir)

def download_libraries(data: dict) -> None:
    libraries = data["libraries"]

    session = create_requests_session()

    with ThreadPoolExecutor(max_workers=16) as executor:
        list(executor.map(lambda library: process_library(session, library), libraries))

