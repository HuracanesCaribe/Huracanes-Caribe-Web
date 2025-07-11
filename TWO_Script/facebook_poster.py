import os
import hashlib
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the .env file (adjust path as needed)
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / "TWO_Script" / ".envs" / ".env")

def post_to_facebook(image_path: str, caption: str, page_id: str, force: bool = False):
    """Posts image and caption to the Facebook page using the page-specific token."""
    
    # Load correct token
    token = os.getenv(f"FB_PAGE_TOKEN_{page_id}")
    if not token:
        raise ValueError(f"⚠️ No token found for page ID: {page_id}")

    graph_url = f"https://graph.facebook.com/v18.0/{page_id}/photos"

    # Compute file hash to skip duplicate posts
    def file_hash(path, algo="md5"):
        h = hashlib.new(algo)
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    current_hash = file_hash(image_path)
    hash_record_path = f"{image_path}.{page_id}.hash"

    if not force and os.path.exists(hash_record_path):
        with open(hash_record_path) as f:
            last_hash = f.read().strip()
        if current_hash == last_hash:
            print("⏩ Skipping post: image unchanged.")
            return

    # Send POST request to Facebook
    with open(image_path, "rb") as img:
        payload = {
            "access_token": token,
            "caption": caption,
        }
        files = {"source": img}
        response = requests.post(graph_url, data=payload, files=files)

    # Handle response
    if response.ok:
        print("✅ Posted to Facebook:", response.json().get("post_id", response.text))
        with open(hash_record_path, "w") as f:
            f.write(current_hash)
    else:
        print("❌ Facebook post failed:", response.status_code)
        print(response.json())
