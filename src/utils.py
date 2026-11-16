from pathlib import Path
import sys

def get_minecraft_dir() -> Path:
    if sys.platform == "win32":
        return Path.home() / "AppData" / "Roaming" / ".minecrafttest"
    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "minecrafttest"
    else:
        # Linux/Unix
        return Path.home() / ".minecrafttest"

    