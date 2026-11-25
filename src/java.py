from pathlib import Path
from zipfile import ZipFile
from typing import List
from config import MC_DIR, NEGATIVE_DIR, MINECRAFT_LOG
import jdk
import sys
import shutil
import subprocess

def get_java_dir() -> Path:
    return NEGATIVE_DIR / "java"

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

    java_folder = None
    target_folder = runtimes / version
    if target_folder.exists():
        return

    try: 
        java_folder = jdk.install(version=version, jre=True, path=str(runtimes))
    except jdk.JdkError as e:
        print(f"Failed to install Java version {version} as JRE-only. Switching to downloading complete JDK")
        try:
            java_folder = jdk.install(version=version, jre=False, path=str(runtimes))
        except jdk.JdkError as e:
            print(f"Switching to JDK installation did not work: {e}")

    # Rename the folder to a known format for easy future access
    if java_folder:
        shutil.move(java_folder, target_folder)

def extract_jar(jar_path: Path, output_dir: Path, exclude_prefixes: tuple = ("META-INF/",)) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    with ZipFile(jar_path, 'r') as jar:
        for member in jar.namelist():
            # If member is a directory or an excluded directory, skip
            if member.endswith("/") or member.startswith(exclude_prefixes):
                continue

            jar.extract(member, output_dir)

# I'll probably shift this to somewhere else
def launch_minecraft(command: List) -> int:
    print("Starting Minecraft")

    with open(MINECRAFT_LOG, "w", encoding="utf-8") as f:
        process = subprocess.Popen(
            command,
            cwd=MC_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1
        )

        if process.stdout is not None:
            for line in process.stdout:
                print(line, end="")
                f.write(line)
                f.flush()

    return process.wait()