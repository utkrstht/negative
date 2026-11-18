# type: ignore
from pathlib import Path
from hashlib import file_digest
from io import BufferedIOBase
from requests import get
from shutil import copyfileobj
from tempfile import TemporaryFile
import sys

# This function follows the naming conventions that the manifest uses for operating systems
def get_operating_system() -> str | None:
    if sys.platform == "win32":
        return "windows"
    elif sys.platform == "darwin":
        return "osx"
    elif sys.platform == "linux":
        return "linux"
    else:
        return None

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

def download_file(file_url: str, file_dir: str | Path, file_hash: str = "") -> None:
    with get(file_url, stream=True, timeout=120) as response:
                response.raise_for_status()

                with TemporaryFile() as t:
                    # Streaming download
                    copyfileobj(response.raw, t)

                    if file_hash:
                        if not check_sha1_hashs(t, file_hash):
                            raise ValueError(f"SHA1 mismatch for file {file_dir}, the downloaded file is corrupted.")
    
                    with open(file_dir, "wb") as f:
                        copyfileobj(t, f)
