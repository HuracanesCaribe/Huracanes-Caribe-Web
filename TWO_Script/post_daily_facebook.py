# post_daily_facebook.py – Auto-post GTWO maps with ChatGPT-generated captions

import os
import zipfile
from pathlib import Path
from datetime import datetime
import zoneinfo
import re
import socket
from dotenv import load_dotenv
from openai import OpenAI
from facebook_poster import post_to_facebook

PAGE_CONFIG = {
    "393356640516670": "en",  # Hurricanes US
    "571167226380026": "es",  # Huracanes Caribe
}
# --- Environment detection ---
HOSTNAME = socket.gethostname()

if "huracanes-caribe-vm" in HOSTNAME:
    # Server setup
    BASE_DIR = Path("/home/ubuntu/Huracanes-Caribe-Web")
    OUTPUT_DIR = Path("/var/www/html/output")
    DATA_DIR = BASE_DIR / "TWO_Script" / "data_archive"  # 👈 Add this too
    ENV_PATH = BASE_DIR / "TWO_Script" / ".envs" / ".env"
else:
    # Local Mac setup
    BASE_DIR = Path("/Users/tejedawx/Projects/HuracanesCaribe")
    OUTPUT_DIR = BASE_DIR /  "TWO_Script" / "output"
    DATA_DIR = BASE_DIR / "TWO_Script" /"data_archive"  # 👈 Add this too
    ENV_PATH = BASE_DIR / "TWO_Script" / ".envs" / ".env"

# --- Load environment variables ---
load_dotenv(dotenv_path=ENV_PATH)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# --- Functions ---
def extract_gtwo_rtf_text(zip_path: Path) -> dict:
    """Return contents of two_atl_text_*.rtf and two_pac_text_*.rtf from ZIP as strings."""
    rtf_texts = {}

    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            if name.lower().endswith(".rtf") and "two_" in name.lower():
                with zf.open(name) as f:
                    content = f.read().decode("utf-8", errors="ignore")
                    if "atl" in name.lower():
                        rtf_texts["atlantic"] = content
                    elif "pac" in name.lower():
                        rtf_texts["pacific"] = content
    return rtf_texts

from datetime import date, timezone
from datetime import datetime, timezone
import re

def is_image_recent(image_path: Path) -> bool:
    """Accepts image if it's from today or yesterday (UTC), based on filename."""
    match = re.search(r"_(\d{8})T", image_path.name)
    if not match:
        return False

    image_date = datetime.strptime(match.group(1), "%Y%m%d").date()
    today_utc = datetime.now(timezone.utc).date()
    yesterday_utc = today_utc - timedelta(days=1)

    return image_date in {today_utc, yesterday_utc}



def generate_facebook_caption_with_gpt(rtf_text: str, basin: str, lang: str = "en") -> str:
    """Generate a Facebook caption in warm, professional Caribbean English using GPT."""
    import re
    from datetime import datetime
    # Detect timezone for date formatting
    if "huracanes-caribe-vm" in HOSTNAME:
        LOCAL_TZ = zoneinfo.ZoneInfo("America/New_York")
    else:
        LOCAL_TZ = zoneinfo.ZoneInfo("America/Santo_Domingo")

    local_now = datetime.now(LOCAL_TZ)
    today_str_es = local_now.strftime('%d de %B')
    today_str_en = local_now.strftime('%B %d')

    rtf_text_cleaned = re.sub(r"{\\.*?}|\\[a-z]+\d*|{|}", "", rtf_text)

    if lang == "es":
        prompt = f"""
**SIEMPRE LEA ESTA INSTRUCCIÓN ANTES DE PUBLICAR**
Eres un comunicador meteorológico de confianza para redes sociales como Facebook y X. Tu tarea es generar una publicación clara, cálida y profesional en español, basada en el siguiente resumen oficial del Centro Nacional de Huracanes (NHC) sobre el panorama de ciclones tropicales en el {basin}.
Responde en español neutro, claro y profesional, fácil de entender para el público general, con un tono cálido y tranquilizador, similar al de un comunicador meteorológico de confianza.
Prioriza la claridad y el compromiso comunitario al editar o crear publicaciones para Facebook y otras redes sociales. Mantén los mensajes concisos, idealmente entre 40 y 100 palabras (preferiblemente entre 60-70, máximo 150), y adaptados a las audiencias de habla hispana en el Caribe.
Para Twitter (X), mantén el texto entre 100 y 300 caracteres y no más de 600 caracteres.     
Al reescribir textos, asegúrate de que la gramática y la ortografía sean correctas, y destaca los mensajes críticos de preparación y prevención ante el clima.  
Incorpora sutilmente principios de influencia conductual (como prueba social, urgencia y autoridad confiable) inspirados en el Manual de Operaciones de Comportamiento de Chase Hughes, sin que sean obvios. Siempre incluye suficientes emojis apropiados para mejorar el compromiso emocional y la visibilidad.
No hagas títulos. Haz todo en 1-3 párrafos con un salto de línea entre párrafos. Si necesitas usar un título, mantenlo dentro del texto, no como título.
Si necesitas usar una fecha, usa la fecha actual en la zona horaria local (America/Santo_Domingo) en el formato "dd de MMMM" para español y "MMMM dd" para inglés.
trata de no usar la palabra "comunidad caribeña" o "weather prediction center", usa simplemente la palabra "comunidad" en su lugar.

Resumen GTWO (limpio):
{rtf_text_cleaned}
"""
    else:
        prompt = f"""
**ALWAYS READ THIS PROMPT BEFORE POSTING**
You are a trusted weather communicator for social media audiences in the Caribbean. Your task is to generate a warm, clear, and professional Facebook post in **English** summarizing the following official tropical weather outlook from the National Hurricane Center (NHC) for the {basin} basin.
Respond in neutral, clear, professional English that is easy for a general audience to understand, with a warm and reassuring tone similar to a trusted weather communicator. 
Prioritize clarity and community engagement when editing or creating posts for Facebook and other social networks. Keep messages concise, ideally between 40 and 100 words (preferably between 60-70, max 150), and adapted to english-speaking audiences. 
For twitter (X), keep the text between 100-300 characters and no more than 600 character.
When rewriting texts, ensure correct grammar and orthography, and highlight critical weather preparedness and prevention messages. 
Subtly incorporate behavioral influence principles (such as social proof, urgency, and trusted authority) inspired by the Behavior Ops Manual by Chase Hughes, without making them obvious. Always include enough appropriate emojis to improve emotional engagement and visibility. 
If a question is outside the scope of text editing, community messaging, or hurricane-related public communication, clearly state that this project does not cover that topic.
Don’t make titles at all. Make everything in between 1-3 paragraphs with a line break between paragraphs. if you need to use a title keep it inside the text, not as a title.
if you need to use a date, use the current date in the local timezone (America/Santo_Domingo) in the format "dd de MMMM" for Spanish and "MMMM dd" for English.
try not to use the work caribbean comunity or weather prediction center, use the word "community" instead.

Cleaned NHC outlook:
{rtf_text_cleaned}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ GPT-4o failed, trying GPT-3.5. Reason: {e}")
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e2:
            print(f"❌ OpenAI fallback failed: {e2}")
            return f"{basin.capitalize()} — Info not available for the moment."


from datetime import datetime, timedelta, timezone
from datetime import date, timedelta


def find_latest_image(basin_keyword: str) -> Path | None:
    """Try to find the latest image for today (UTC). If none found, fallback to yesterday."""
    for day_offset in [0, -1]:
        date_folder = (datetime.now(timezone.utc) + timedelta(days=day_offset)).strftime("%Y-%m-%d")
        image_dir = OUTPUT_DIR / date_folder

        if not image_dir.exists():
            if day_offset == 0:
                print(f"⚠️ Folder does not exist: {image_dir}")
            continue

        candidates = sorted(image_dir.glob(f"*{basin_keyword}*.png"), reverse=True)
        if candidates:
            print(f"📁 Using image from {date_folder}: {candidates[0].name}")
            return candidates[0]

    print(f"❌ No image found for basin: {basin_keyword}")
    return None


def find_latest_zip() -> Path | None:
    """Find the latest GTWO zip file in data_archive."""
    folders = sorted(DATA_DIR.glob("*"), reverse=True)
    for folder in folders:
        if folder.is_dir():
            zips = sorted(folder.glob("gtwo_shapefiles_*.zip"), reverse=True)
            if zips:
                return zips[0]
    return None


def main():
    print("📤 Starting Facebook auto-post script...")

    latest_zip = find_latest_zip()
    if not latest_zip:
        print("❌ No GTWO ZIP found.")
        return

    print(f"✅ Using GTWO: {latest_zip.name}")
    rtf_texts = extract_gtwo_rtf_text(latest_zip)

    for page_id, lang in PAGE_CONFIG.items():
        for basin in ["atlantic"]:
            image = find_latest_image(basin)

            if not image:
                print(f"❌ No image for {basin}.")
                continue

            if not is_image_recent(image):
                print(f"⏭️ Skipping {basin} — image is not from today or yesterday.")
                continue


            caption = generate_facebook_caption_with_gpt(
                rtf_texts.get(basin, ""), basin, lang=lang
            )
            # Log the caption to file
            log_path = BASE_DIR / "TWO_Script" / "facebook_caption_log.txt"
            with open(log_path, "a", encoding="utf-8") as log:
                log.write(f"{datetime.now().isoformat()} | Page: {page_id} | Basin: {basin} | Lang: {lang}\n")
                log.write(caption.strip() + "\n" + "-" * 60 + "\n----------------------------------------------------------")


            print(f"📸 Página {page_id} ({lang}) → {image.name}")
            print(caption[:120] + "…")  # preview

            post_to_facebook(
                image_path=str(image),
                caption=caption,
                page_id=page_id,         # pasa el id/token correspondiente
            )


if __name__ == "__main__":
    main()
