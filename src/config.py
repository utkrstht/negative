from utils import get_minecraft_dir, get_negative_dir

MC_DIR = get_minecraft_dir()
NATIVES_DIR = MC_DIR / "natives"
LIBRARY_DIR = MC_DIR / "libraries"
ASSETS_DIR = MC_DIR / "assets"

NEGATIVE_DIR = get_negative_dir()

MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

BMCLAPI_OPTIFINE_VERSION_LIST_URL = "https://bmclapi2.bangbang93.com/optifine/:mcversion"
BMCLAPI_OPTIFINE_VERSION_LIST_DIR = NEGATIVE_DIR / "cache" / "optifine"
BMCLAPI_OPTIFINE_DOWNLOAD_URL = "https://bmclapi2.bangbang93.com/optifine/:mcversion/:type/:patch"
BMCLAPI_OPTIFINE_DOWNLOAD_DIR = NEGATIVE_DIR / "cache" / "optifine" / "jars"

LAUNCHER_NAME = "Negative"
LAUNCHER_VERSION = "v0.2.0"

LOG_DIR = NEGATIVE_DIR / "logs"
LAUNCHER_LOG = LOG_DIR / "launcher.log"
MINECRAFT_LOG = LOG_DIR / "minecraft.log"