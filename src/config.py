from utils import get_minecraft_dir

MC_DIR = get_minecraft_dir()
NATIVES_DIR = MC_DIR / "natives"
LIBRARY_DIR = MC_DIR / "libraries"

MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

LAUNCHER_NAME = "Negative"
LAUNCHER_VERSION = "v0.1.0"