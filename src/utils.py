from pathlib import Path
from hashlib import file_digest
from io import BufferedIOBase
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

def check_sha1_hash(file: BufferedIOBase, hash: str) -> bool:
    file.seek(0)
    digest = file_digest(file, "sha1").hexdigest()
    file.seek(0)

    return digest == hash
