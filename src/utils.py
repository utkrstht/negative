# type: ignore
from pathlib import Path
from hashlib import file_digest
from io import BufferedIOBase
from tempfile import TemporaryFile
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import sys
import platform
import shutil
import requests

# This function follows the naming conventions that the manifest uses for operating systems
def get_operating_system() -> str:
    if sys.platform == "win32":
        return "windows"
    elif sys.platform == "darwin":
        return "osx"
    elif sys.platform == "linux":
        return "linux"

    return sys.platform

def get_system_architecture() -> str:
    if platform.machine() in ["x86_64", "AMD64"]:
        return "x86_64"
    elif platform.machine() in ["ARM64", "aarch64", "arm64"]:
        return "arm64"

    # Meh.
    return platform.machine()

def get_minecraft_dir() -> Path:
    # It should point to .minecraft, but I don't want to corrupt my minecraft installation so it's going to .minecrafttest
    if sys.platform == "win32":
        return Path.home() / "AppData" / "Roaming" / ".minecrafttest"
    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "minecrafttest"
    else:
        # Linux/Unix
        return Path.home() / ".minecrafttest"

# Direct file stream
def check_sha1_hashs(file: BufferedIOBase, hash: str) -> bool:
    file.seek(0)
    digest = file_digest(file, "sha1").hexdigest()
    file.seek(0)

    return digest == hash

# File path
def check_sha1_hashf(file: Path, hash: str) -> bool:
    with open(file, "rb") as f:
        digest = file_digest(f, "sha1").hexdigest()

    return digest == hash

def create_requests_session(max_workers: int = 16) -> requests.Session:
    session = requests.Session()

    status_forcelist = [429, 500, 502, 503, 504]
    retries = Retry(total=3, backoff_factor=0.5, status_forcelist=status_forcelist)

    adapter = HTTPAdapter(pool_connections=max_workers, pool_maxsize=max_workers, max_retries=retries)

    session.mount("https://", adapter)

    return session

def download_file(file_url: str, file_dir: str | Path, file_hash: str = "", session: requests.Session = None) -> None:
    if file_dir.is_file() and check_sha1_hashf(file_dir, file_hash): 
        # File is already downloaded
        return None

    requester = session or requests
    with requester.get(file_url, stream=True, timeout=120) as response:
                response.raise_for_status()
                response.raw.decode_content = True

                with TemporaryFile() as t:
                    # Streaming download
                    shutil.copyfileobj(response.raw, t)

                    if file_hash:
                        if not check_sha1_hashs(t, file_hash):
                            raise ValueError(f"SHA1 mismatch for file {file_dir}, the downloaded file is corrupted.")

                    file_dir.parent.mkdir(parents=True, exist_ok=True)

                    with open(file_dir, "wb") as f:
                        shutil.copyfileobj(t, f)
