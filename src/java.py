from pathlib import Path
import jdk
import sys

def get_java_dir() -> Path:
    if sys.platform == "win32":
        java = Path.home() / "AppData" / "Roaming" / ".negative" / "java"
        
    elif sys.platform == "darwin":
        # No javaw here or down in linux because that's windows only
        java = Path.home() / "Library" / "Application Support" / "negative" / "java"
        
    else:
        java = Path.home() / ".negative" / "java"

    return java

def get_java_exe(version: str, javaw: bool | None = True) -> Path | None:
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