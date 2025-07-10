import requests
import os
#PAGE_ACCESS_TOKEN = os.environ["FB_PAGE_TOKEN"]
PAGE_ACCESS_TOKEN = "EAAR78aP6Ln8BOZCBrReILBmjOOxQLIl5qL567bfWltObPOZBUtqrwOEmU8m2dZAK7AjPr0M0seFuoMseQD13fRByZC9iNJ7LIAHsvpDmpeHgWKUWds8mWbtN38N53C6ZB7VeiwRlOeUkfZAbrzzuBewLIKZBCP8oJQ57bEf5T9ZAIGZB0gmuRz91YZAYcX1tnS0bbKvYXnZAgmTY9dhnygZC5wbgtEqM"
PAGE_ID = "393356640516670"  # Huracanes Caribe

GRAPH_API_URL = f"https://graph.facebook.com/v23.0/{PAGE_ID}/photos"

def post_to_facebook(image_path: str, caption: str = "", force: bool = False):
    import hashlib
    import os
    import requests

    def file_hash(path, algo="md5"):
        h = hashlib.new(algo)
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    current_hash = file_hash(image_path)
    hash_record_path = f"{image_path}.hash"

    if not force and os.path.exists(hash_record_path):
        with open(hash_record_path) as f:
            last_hash = f.read().strip()
        if current_hash == last_hash:
            print("⏩ Skipping post: image unchanged.")
            return

    with open(image_path, "rb") as img:
        payload = {
            "access_token": PAGE_ACCESS_TOKEN,
            "caption": caption,
        }
        files = {"source": img}
        response = requests.post(GRAPH_API_URL, data=payload, files=files)

    if response.ok:
        print("✅ Posted to Facebook:", response.json().get("post_id", response.text))
        with open(hash_record_path, "w") as f:
            f.write(current_hash)
    else:
        print("❌ Facebook post failed:", response.status_code)
        print(response.json())
