from config import MC_DIR
from utils import check_sha1_hashf, download_file, create_requests_session
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests
import json

def download_asset_index(data: dict) -> tuple | None:
    asset_index_id = data["assetIndex"]["id"]
    asset_index_dir = MC_DIR / "assets" / "indexes" / f"{asset_index_id}.json"
    asset_index_url = data["assetIndex"]["url"]
    asset_index_hash = data["assetIndex"]["sha1"]

    # C:\Users\User\AppData\Roaming\.minecraft\assets\indexes
    asset_index_dir.parent.mkdir(parents=True, exist_ok=True)

    if asset_index_dir.is_file() and check_sha1_hashf(asset_index_dir, asset_index_hash):
        # Asset index is already downloaded
        return (asset_index_id, asset_index_dir)
    
    try:
        download_file(asset_index_url, asset_index_dir, asset_index_hash)
    except requests.RequestException as e:
        print(f"Something happened while downloading asset index: {e}")
        return None

    return (asset_index_id, asset_index_dir)

def resolve_asset(asset_hash: str) -> dict:
    # First two letters of asset hash is the asset directory
    asset_folder = asset_hash[:2]

    asset_url = f"https://resources.download.minecraft.net/{asset_folder}/{asset_hash}"
    asset_dir = MC_DIR / "assets" / "objects" / asset_folder / f"{asset_hash}"

    asset_dict = {"url": asset_url, "local": asset_dir, "hash": asset_hash}

    return asset_dict

def download_asset(asset_dict: dict, session: requests.Session) -> None:
    try: 
        download_file(asset_dict['url'], asset_dict['local'], asset_dict['hash'], session)
    except requests.RequestException as e:
        print(f"Something happened while downloading asset {asset_dict['url']}: {e}")
        return None

def process_asset(session: requests.Session, asset: dict) -> None:
    asset_hash = asset['hash']
    asset_dict = resolve_asset(asset_hash)

    download_asset(asset_dict, session)

def download_assets(asset_index: str) -> None:
    # TODO: deduplicate hashes before processing
    assets = json.loads(asset_index)['objects']
    session = create_requests_session()

    with ThreadPoolExecutor(max_workers=16) as executor:
        list(executor.map(lambda asset: process_asset(session, asset), assets.values()))
