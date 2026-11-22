from pathlib import Path
from zipfile import ZipFile
import jdk
import sys
import shutil

def get_java_dir() -> Path:
    if sys.platform == "win32":
        java = Path.home() / "AppData" / "Roaming" / ".negative" / "java"
        
    elif sys.platform == "darwin":
        # No javaw here or down in linux because that's windows only
        java = Path.home() / "Library" / "Application Support" / "negative" / "java"
        
    else:
        java = Path.home() / ".negative" / "java"

    return java

def get_java_exe(version: str, javaw: bool = True) -> Path | None:
    base = get_java_dir()
    
    if sys.platform == "win32":
        executable = "javaw.exe" if javaw else "java.exe"
        java = base / version / "bin" / executable
        
    elif sys.platform == "darwin":
        # No javaw here or down in linux because that's windows only
        java = base / version / "Contents" / "Home" / "bin" / "java"
        
    else:
        java = base / version / "bin" / "java"

    # TODO: verify the java installation
    if java.exists():
        return java

    return None

def download_java(version: str) -> None:
    runtimes = get_java_dir()
    runtimes.mkdir(parents=True, exist_ok=True)

    target_folder = runtimes / version
    if target_folder.exists():
        return

    java_folder = jdk.install(version=version, jre=True, path=str(runtimes))

    # Rename the folder to a known format for easy future access
    shutil.move(java_folder, target_folder)

def extract_jar(jar_path: Path, output_dir: Path, exclude_prefixes: tuple = ("META-INF/",)) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    with ZipFile(jar_path, 'r') as jar:
        for member in jar.namelist():
            # If member is a directory or an excluded directory, skip
            if member.endswith("/") or member.startswith(exclude_prefixes):
                continue

            jar.extract(member, output_dir)