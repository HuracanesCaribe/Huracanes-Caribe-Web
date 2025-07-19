import os
import requests
from dotenv import load_dotenv

# === Load environment variables ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(SCRIPT_DIR, ".envs", ".env")
load_dotenv(dotenv_path)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")       # e.g. @huracanescaribe
TELEGRAM_GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")           # e.g. -1001899699695
TELEGRAM_TOPIC_ID = os.getenv("TELEGRAM_TOPIC_ID")           # e.g. 88

# === Get latest GTWO image ===
def get_latest_image(basin='atlantic'):
    base_dir = os.path.join(SCRIPT_DIR, '..', 'TWO_Script/output')
    if not os.path.exists(base_dir):
        print(f"❌ No se encontró la carpeta {base_dir}")
        return None

    folders = sorted([
        f for f in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, f))
    ], reverse=True)

    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        files = sorted([
            f for f in os.listdir(folder_path)
            if f.startswith(basin) and f.endswith('.png')
        ], reverse=True)

        if files:
            return os.path.join(folder_path, files[0])
    return None

# === Get latest Spanish caption (without metadata header) ===
def get_latest_caption(basin='atlantic', lang='es'):
    path = os.path.join(SCRIPT_DIR, '..', 'TWO_Script/facebook_caption_log.txt')
    if not os.path.exists(path):
        return "🌪️ Huracanes Caribe – No se encontró descripción reciente."
    with open(path, 'r', encoding='utf-8') as f:
        blocks = f.read().split("------------------------------------------------------------")
        for block in reversed(blocks):
            if f"Basin: {basin}" in block and f"Lang: {lang}" in block:
                lines = block.strip().split("\n")
                return "\n".join(lines[1:]).strip()  # Skip header
    return "🌪️ Huracanes Caribe – No se encontró descripción reciente."

# === Step 1: Post to channel and return message_id ===
def post_to_channel_and_get_id(image_path, caption):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    with open(image_path, 'rb') as photo:
        response = requests.post(url, data={
            'chat_id': TELEGRAM_CHANNEL_ID,
            'caption': caption,
            'parse_mode': 'HTML'
        }, files={'photo': photo})
        if response.ok:
            message_id = response.json()['result']['message_id']
            print(f"✅ Publicado en canal (ID: {message_id})")
            return message_id
        else:
            print("❌ Error al publicar en el canal:", response.text)
            return None

# === Step 2: Forward that message to group topic ===
def forward_to_group_topic(message_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/forwardMessage"
    payload = {
        'chat_id': TELEGRAM_GROUP_ID,
        'message_thread_id': TELEGRAM_TOPIC_ID,
        'from_chat_id': TELEGRAM_CHANNEL_ID,
        'message_id': message_id
    }
    response = requests.post(url, data=payload)
    if response.ok:
        print("✅ Mensaje reenviado al grupo (tema)")
    else:
        print("❌ Error al reenviar:", response.text)

# === Main ===
if __name__ == "__main__":
    print("📤 Publicando GTWO en el canal y reenviando al grupo...")

    image_path = get_latest_image('atlantic')
    caption = get_latest_caption('atlantic', 'es')

    if image_path:
        message_id = post_to_channel_and_get_id(image_path, caption)
        if message_id:
            forward_to_group_topic(message_id)
    else:
        print("❌ No se encontró imagen GTWO para el Atlántico.")
