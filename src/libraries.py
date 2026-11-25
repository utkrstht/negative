from utils import download_file, create_requests_session, get_operating_system, get_system_architecture
from rules import evalute_rules
from pathlib import Path
from java import extract_jar
from concurrent.futures import ThreadPoolExecutor
from typing import List
from config import MC_DIR, NATIVES_DIR
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
            if arch in classifier or (arch == "x86_64" and "arm64" not in classifier and not classifier.endswith("-x86")):
                return True
            return False
        else:
            return False

    if library_rules:
        return evalute_rules(library_rules)

    return True

def process_native_library(library: dict, session: requests.Session) -> None:
    library_name = library['name']
    library_dir = MC_DIR / "libraries" / library["downloads"]["artifact"]["path"]
    library_natives = library.get('natives')

    extract_rules = library.get('extract') or {}
    exclusions = tuple(extract_rules.get('exclude') or ("META-INF/", ))

    # Modern natives
    if 'native' in library_name:
        extract_jar(library_dir, NATIVES_DIR)   

    # For pre-1.19 manifests
    if library_natives:
        os = get_operating_system()
        classifiers = library['downloads']['classifier']

        # i'm sorry i dont know what to name these i'm sorry i really am 
        native_classifier_name = library_natives.get(os)
        if native_classifier_name:
            native_classifier = classifiers.get(native_classifier_name)

            native_jar_dir = MC_DIR / "libraries" / native_classifier["path"]
            native_jar_url = native_classifier['url']
            native_jar_hash = native_classifier['sha1']

            try:
                download_file(native_jar_url, native_jar_dir, native_jar_hash, session)
            except requests.RequestException as e:
                print(f"Something happened while downloading native library {native_jar_url}: {e}")

            if exclusions:
                extract_jar(native_jar_dir, NATIVES_DIR, exclude_prefixes=exclusions)
            else:
                extract_jar(native_jar_dir, NATIVES_DIR)

def process_library(session: requests.Session, library: dict) -> str | None:
    library_dir = MC_DIR / "libraries" / library["downloads"]["artifact"]["path"]
    library_url = library["downloads"]["artifact"]["url"]
    library_hash = library["downloads"]["artifact"]["sha1"]
    library_name = library['name']

    if not should_i_download_this_library_on_my_pc(library):
        # Not for our computer
        return

    try:
        download_file(library_url, library_dir, library_hash, session)
    except requests.RequestException as e:
        print(f"Something happened while downloading library {library_name}: {e}")
        return None

    process_native_library(library, session)

    # This gets passed to classpath
    return str(library_dir)

def download_libraries(data: dict) -> List:
    libraries = data["libraries"]

    session = create_requests_session()

    with ThreadPoolExecutor(max_workers=16) as executor:
        results = list(executor.map(lambda library: process_library(session, library), libraries))

    # Classpath JARs
    jars = [path for path in results if path is not None]

    return jars