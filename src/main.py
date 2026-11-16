from versions import fetch_versions, download_version_jar

latest = fetch_versions(options="latest_release")

all_versions = fetch_versions(options="all")

# TODO: this logic should be in fetch_versions i think
for version in all_versions:
    if version["id"] == latest:
        download_version_jar(version)
        break