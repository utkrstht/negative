from versions import MC_DIR
from utils import check_sha1_hashf, download_file
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

