# type: ignore
from versions import fetch_versions, download_version_jar, download_version_manifest
from assets import download_asset_index, download_assets
from libraries import download_libraries
from java import download_java, get_java_exe, launch_minecraft
from arguments import parse_game_arguments, parse_jvm_arguments
from config import LAUNCHER_LOG
from requests.exceptions import HTTPError
import json
import requests
import logging

# Setup launcher logger
logging.basicConfig(level=logging.INFO, 
                    format="[%(asctime)s] [%(name)s] %(levelname)s: %(message)s",
                    handlers=[
                        logging.FileHandler(LAUNCHER_LOG),
                        logging.StreamHandler()
                    ])

logger = logging.getLogger(__name__)

# Target version (can be both a release and a snapshot)
target = input("Please select your minecraft version (default: 26.3): ") or "26.3"
username = input("Please enter your username: ") or "TestPlayer"

all_versions = fetch_versions(options="all")

# TODO: this logic should be in fetch_versions i think
for version in all_versions:
    if version["id"] == target:
        try:
            # Open version manifest
            response = requests.get(version["url"])
            response.raise_for_status()
        except HTTPError as e:
            logger.error(f"Something happened when fetching version-specific manifest: {e}")

        data = json.loads(response.text)
        try:
            java_version = str(data['javaVersion']['majorVersion'])
        except KeyError:
            logger.warning("Manifest does not provide javaVersion, defaulting to Java 8")
            java_version = "8"

        jar_path = download_version_jar(version["id"], data)

        download_version_manifest(version["id"], response)

        logger.info("Downloading asset index")
        asset_index_id, asset_index_dir = download_asset_index(data)
        logger.info("Downloaded asset index")

        classpath = download_libraries(data)
        classpath.append(str(jar_path))

        logger.info("Downloading assets")
        with open(asset_index_dir, "r") as f:
            download_assets(f.read())
        logger.info("Downloaded assets")

        download_java(java_version)

        java_path = get_java_exe(version=java_version, javaw=True)
        main_class = data['mainClass']

        game_arguments = parse_game_arguments(username=username, game_version=target, asset_index=asset_index_id)
        jvm_arguments = parse_jvm_arguments(data=data, classpath=classpath)

        command = [
            str(java_path),
            *jvm_arguments,
            main_class,
            *game_arguments
        ]

        exit_code = launch_minecraft(command=command)
        break