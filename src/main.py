# type: ignore
from versions import fetch_versions, download_version_jar, download_version_manifest
from assets import download_asset_index, download_assets
from libraries import download_libraries
from java import download_java, get_java_exe, launch_minecraft
from arguments import parse_game_arguments, parse_jvm_arguments
from requests.exceptions import HTTPError
import json
import requests

latest = "1.19"

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

        data = json.loads(response.text)
        java_version = str(data['javaVersion']['majorVersion'])
        
        print("Downloading client JAR")
        jar_path = download_version_jar(version["id"], data)
        print("Downloaded client JAR")

        print("Downloading version manifest")
        download_version_manifest(version["id"], response)
        print("Downloaded version manifest")

        print("Downloading asset index")
        asset_index_id, asset_index_dir = download_asset_index(data)
        print("Downloaded asset index")

        print("Downloading libraries")
        classpath = download_libraries(data)
        classpath.append(str(jar_path))
        print("Downloaded libraries")

        print("Downloading assets")
        with open(asset_index_dir, "r") as f:
            download_assets(f.read())
        print("Downloaded assets")

        print("Downloading Java")
        download_java(java_version)
        print("Downloaded Java")

        java_path = get_java_exe(version=str(data['javaVersion']['majorVersion']), javaw=False)
        main_class = data['mainClass']

        game_arguments = parse_game_arguments(username="krstht", game_version=latest, asset_index=asset_index_id)
        jvm_arguments = parse_jvm_arguments(data=data, classpath=classpath)

        command = [
            str(java_path),
            *jvm_arguments,
            main_class,
            *game_arguments
        ]

        exit_code = launch_minecraft(command=command)

        print("Minecraft exited with ", exit_code)
        break