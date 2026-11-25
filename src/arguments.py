from typing import List
from rules import evalute_rules
from os import pathsep
from config import MC_DIR, NATIVES_DIR, ASSETS_DIR, LAUNCHER_NAME, LAUNCHER_VERSION, SERVER_ADDRESS, SERVER_PORT
import hashlib
# Because otherwise this would cause naming conflicts
import uuid as uid

def populate_placeholders(arg: str, classpath: str) -> str:
    arg = arg.replace("${natives_directory}", str(NATIVES_DIR))
    arg = arg.replace("${launcher_name}", str(LAUNCHER_NAME))
    arg = arg.replace("${launcher_version}", str(LAUNCHER_VERSION))
    arg = arg.replace("${classpath}", classpath)

    return arg

def parse_jvm_arguments(data: dict, classpath: List) -> List:
    classpath_str = pathsep.join(classpath)

    try:
        args = data['arguments']['jvm']
    except KeyError:
        # Super old versions do not provide JVM argumentss
        print("Manifest does not provide JVM arguments, continuing with defaults")
        default_jvm_args = [
            '-Xmx2G',
            '-Xms512M',
            f'-Djava.library.path={NATIVES_DIR}',
            "-cp",
            classpath_str
        ]
        return default_jvm_args

    parsed_args = []
    classpath_str = pathsep.join(classpath)

    for arg in args:
        if isinstance(arg, str):
            arg = populate_placeholders(arg, classpath_str)
            parsed_args.append(arg)
            continue

        arg_rules = arg.get('rules')
        if arg_rules:
            allow = evalute_rules(arg_rules)

            if not allow:
                continue

            value = arg['value']
            if isinstance(value, list):
                # <1.19 can have values as lists
                parsed_args.extend(populate_placeholders(item, classpath_str) for item in value)
            else:
                parsed_args.append(populate_placeholders(value, classpath_str))
            continue

    return parsed_args

def parse_game_arguments(username: str, game_version: str, asset_index: str) -> List:
    # Currently hardcoded arguments
    raw_uuid = hashlib.md5(f"OfflinePlayer:{username}".encode("utf-8")).digest()
    uuid = uid.UUID(bytes=raw_uuid, version=3).hex

    return [
        "--username", username,
        "--version", game_version,
        "--gameDir", str(MC_DIR),
        "--assetsDir", str(ASSETS_DIR),
        "--assetIndex", asset_index,
        "--uuid", uuid,
        "--accessToken", "0",
        "--clientId", "",
        "--xuid", "",
        "--versionType", "release",
        "--server", SERVER_ADDRESS,
        "--port", str(SERVER_PORT)
    ]
