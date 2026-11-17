from pathlib import Path
from hashlib import sha1
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
    if sys.platform == "win32":
        return Path.home() / "AppData" / "Roaming" / ".minecrafttest"
    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "minecrafttest"
    else:
        # Linux/Unix
        return Path.home() / ".minecrafttest"

def check_sha1_hash(file_path: str, hash: str) -> bool:
    h = sha1()

    with open(file_path, 'rb') as file:
        while True:
            # Reading is buffered, so we can read smaller chunks
            chunk = file.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)

    file_hash = h.hexdigest()

    return hash == file_hash