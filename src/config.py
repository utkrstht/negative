from utils import get_minecraft_dir, get_negative_dir

MC_DIR = get_minecraft_dir()
NATIVES_DIR = MC_DIR / "natives"
LIBRARY_DIR = MC_DIR / "libraries"
ASSETS_DIR = MC_DIR / "assets"

NEGATIVE_DIR = get_negative_dir()

MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

LAUNCHER_NAME = "Negative"
LAUNCHER_VERSION = "v0.2.0"

SERVER_ADDRESS = "utkrstht.aternos.me"
SERVER_PORT = 39930

LOG_DIR = NEGATIVE_DIR / "logs"
LAUNCHER_LOG = LOG_DIR / "launcher.log"
MINECRAFT_LOG = LOG_DIR / "minecraft.log"