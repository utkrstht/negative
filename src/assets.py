from versions import MC_DIR
from utils import check_sha1_hashf, download_file
from pathlib import Path
import requests
import json

def download_asset_index(response: requests.Response) -> None:
    data = json.loads(response.text)

    asset_index_id = data["assetIndex"]["id"]
    asset_index_dir = MC_DIR / "assets" / "indexes" / f"{asset_index_id}.json"
    asset_index_url = data["assetIndex"]["url"]
    asset_index_hash = data["assetIndex"]["sha1"]

    # C:\Users\User\AppData\Roaming\.minecraft\assets\indexes
    asset_index_dir.parent.mkdir(parents=True, exist_ok=True)

    if asset_index_dir.is_file() and check_sha1_hashf(asset_index_dir, asset_index_hash):
        # Asset index is already downloaded
        return None
    
    try:
        download_file(asset_index_url, asset_index_dir, asset_index_hash)
    except requests.RequestException as e:
        print(f"Something happened while downloading asset index: {e}")
        return None

def resolve_asset(asset_hash: str) -> dict:
    # First two letters of asset hash is the asset directory
    asset_folder = asset_hash[:2]

    asset_url = f"https://resources.download.minecraft.net/{asset_folder}/{asset_hash}"
    asset_dir = MC_DIR / "assets" / "objects" / asset_folder / f"{asset_hash}"

    asset_dict = {"url": asset_url, "local": asset_dir, "hash": asset_hash}

    return asset_dict