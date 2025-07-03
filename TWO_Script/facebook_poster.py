import requests
import os
#PAGE_ACCESS_TOKEN = os.environ["FB_PAGE_TOKEN"]
PAGE_ACCESS_TOKEN = "EAAR78aP6Ln8BOZCBrReILBmjOOxQLIl5qL567bfWltObPOZBUtqrwOEmU8m2dZAK7AjPr0M0seFuoMseQD13fRByZC9iNJ7LIAHsvpDmpeHgWKUWds8mWbtN38N53C6ZB7VeiwRlOeUkfZAbrzzuBewLIKZBCP8oJQ57bEf5T9ZAIGZB0gmuRz91YZAYcX1tnS0bbKvYXnZAgmTY9dhnygZC5wbgtEqM"
PAGE_ID = "393356640516670"  # Huracanes Caribe

GRAPH_API_URL = f"https://graph.facebook.com/v23.0/{PAGE_ID}/photos"

import hashlib

def file_hash(path, algo="md5"):
    """Return hash digest of a file (md5 or sha256)."""
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def post_to_facebook(image_path: str, caption: str = ""):
    """Upload image to Facebook Page if the image is new (not previously posted)."""
    import os
    import requests

    # 🔢 Step 1: Compute hash of current image
    current_hash = file_hash(image_path)
    hash_record_path = f"{image_path}.hash"

    # 🔍 Step 2: Check if image hash matches last posted
    if os.path.exists(hash_record_path):
        with open(hash_record_path) as f:
            last_hash = f.read().strip()
        if current_hash == last_hash:
            print("⏩ Skipping post: image unchanged.")
            return None  # skip upload

    # 📤 Step 3: Post to Facebook
    url = f"https://graph.facebook.com/v23.0/{PAGE_ID}/photos"
    with open(image_path, "rb") as img:
        payload = {
            "access_token": PAGE_ACCESS_TOKEN,
            "caption": caption,
        }
        files = {"source": img}
        response = requests.post(url, data=payload, files=files)

    if response.ok:
        print("✅ Posted to Facebook:", response.json().get("post_id", response.text))
        # 📝 Step 4: Save current hash
        with open(hash_record_path, "w") as f:
            f.write(current_hash)
    else:
        print("❌ Facebook post failed:", response.status_code)
        print(response.json())
print("Using PAGE_ACCESS_TOKEN:", PAGE_ACCESS_TOKEN[:20])