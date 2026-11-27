from config import BMCLAPI_OPTIFINE_VERSION_LIST_URL, BMCLAPI_OPTIFINE_DOWNLOAD_DIR, BMCLAPI_OPTIFINE_DOWNLOAD_URL, NEGATIVE_DIR, LAUNCHER_LOG
from utils import download_file
from pathlib import Path
import requests
import logging
import subprocess
import json

logger = logging.getLogger(__name__)

def which_optifine_version_should_i_download_for_my_minecraft_version(optifine_entries: list) -> dict:
    latest_optifine = {}
    latest_optifine_timestamp = -1

    for optifine_entry in optifine_entries:
        # The optifine entries use a timestamped ID so we will use that to sort
        timestamp = int(optifine_entry['_id'][:8], 16)

        if timestamp > latest_optifine_timestamp:
            latest_optifine_timestamp = timestamp
            latest_optifine = optifine_entry.copy()

    if latest_optifine['patch'].startswith('pre'):
        logger.warning("Latest available Optifine version is a preview, continuing anyways")

    return latest_optifine

def download_optifine(minecraft_version: str) -> Path:
    logger.info(f"Downloading Optifine for Minecraft {minecraft_version}")
    # The URL template is customizable so yeah
    bmclapi_optifine_version_list_url = str(BMCLAPI_OPTIFINE_VERSION_LIST_URL).replace(":mcversion", minecraft_version)

    try:
        bmclapi_optifine_version_list_response = requests.get(bmclapi_optifine_version_list_url)
        bmclapi_optifine_version_list_response.raise_for_status()
    except requests.HTTPError:
        # TODO: Log all exceptions with logger.exception()
        logger.exception("Something happened while trying to get version list")
        # Re-raise the exception after logging it
        raise

    optifine_entries = json.loads(bmclapi_optifine_version_list_response.text)
    optifine_version_that_i_should_download = which_optifine_version_should_i_download_for_my_minecraft_version(optifine_entries)

    optifine_type = optifine_version_that_i_should_download['type']
    optifine_patch = optifine_version_that_i_should_download['patch']
    optifine_filename = optifine_version_that_i_should_download['filename']

    # Populate placeholders
    bmclapi_optifine_download_url = str(BMCLAPI_OPTIFINE_DOWNLOAD_URL).replace(":mcversion", minecraft_version).replace(":type", optifine_type).replace(":patch", optifine_patch)
    bmclapi_optifine_download_path = BMCLAPI_OPTIFINE_DOWNLOAD_DIR / optifine_filename

    try:
        download_file(bmclapi_optifine_download_url, bmclapi_optifine_download_path)
    except requests.RequestException:
        logger.exception("Something happened while trying to download optifine")
        raise

    logger.info("Downloaded Optifine")
    return bmclapi_optifine_download_path

# This only runs the installer
def install_optifine(optifine_jar: Path, java_exe: Path) -> None:
    logger.info("Starting Optifine Installer")

    with open(LAUNCHER_LOG, "w") as f:
        process = subprocess.Popen(
            [java_exe, optifine_jar],
            cwd=NEGATIVE_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1)

        if process.stdout is not None:
            for line in process.stdout:
                logger.info(line)
                f.write(line)
                f.flush()
