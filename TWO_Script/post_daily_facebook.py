# post_daily_facebook.py – Auto-post GTWO maps with ChatGPT-generated captions

import os
import zipfile
from pathlib import Path
from datetime import datetime
import zoneinfo
import re

from dotenv import load_dotenv
from openai import OpenAI
from facebook_poster import post_to_facebook

PAGE_CONFIG = {
    "393356640516670": "en",  # Hurricanes US
    "571167226380026": "es",  # Huracanes Caribe
}

# --- Constants ---
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR.parent / "output"
DATA_DIR = BASE_DIR.parent / "data_archive"

# --- Load secrets ---
load_dotenv(dotenv_path=BASE_DIR / ".envs" / ".env")
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

from datetime import date

def is_image_from_today(image_path: Path) -> bool:
    """Check if image filename includes today's date."""
    today_str = date.today().strftime("%Y%m%d")
    return today_str in image_path.name

def generate_facebook_caption_with_gpt(rtf_text: str, basin: str, lang: str = "en") -> str:
    """Generate a Facebook caption in warm, professional Caribbean English using GPT."""
    import re
    rtf_text_cleaned = re.sub(r"{\\.*?}|\\[a-z]+\d*|{|}", "", rtf_text)

    if lang == "es":
        prompt = f"""
Eres un comunicador meteorológico de confianza para redes sociales como Facebook y X. Tu tarea es generar una publicación clara, cálida y profesional en español caribeño, basada en el siguiente resumen oficial del Centro Nacional de Huracanes (NHC) sobre el panorama de ciclones tropicales en el {basin}.

Normas:
- Escribe entre 60 y 100 palabras (preferible 60–70, máximo 150).
- Observa el mapa y el texto: si dice “No tropical cyclones expected”, no digas lo contrario.
- Usa entre 1 y 3 párrafos, según la longitud del texto.
- Usa un tono amigable y creíble, que se sienta local y humano.
- No uses saludos ni títulos exagerados, formales o cringy (ej: “¡Hola amigos del Caribe!”).
- Usa español neutro y correcto, sin títulos.
- Resalta si hay sistemas con probabilidad de formación (baja, media, alta).
- Usa emojis apropiados 🌧️🌀⚠️ para visibilidad y conexión emocional.
- Incluye principios sutiles de influencia (urgencia, autoridad, prueba social) sin que se noten.
- Cierra con una frase simple como: “Más información en nuestra página web Huracanes_Caribe 🌐” (sin enlace directo).
- Evita lenguaje técnico o mayúsculas, salvo que sea necesario.

Resumen GTWO (limpio):
{rtf_text_cleaned}
"""
    else:
        prompt = f"""
You are a trusted weather communicator for social media audiences in the Caribbean. Your task is to generate a warm, clear, and professional Facebook post in **English** summarizing the following official tropical weather outlook from the National Hurricane Center (NHC) for the {basin} basin.

Guidelines:
- Write between 60 and 100 words (ideally 60–70, max 150).
- Observe both the map and the text. If it says “No tropical cyclones expected,” do **not** say otherwise.
- Use 1–3 paragraphs depending on the length of the outlook.
- Use a friendly, credible tone that feels local and human.
- Avoid overly formal, exaggerated, or cringy greetings (e.g., “Hello Caribbean friends!”).
- Use neutral, natural English — avoid ALL CAPS or technical language unless necessary.
- Highlight any systems with low, medium, or high formation chances.
- Use appropriate emojis 🌧️🌀⚠️ for visibility and emotional connection.
- Subtly include behavioral influence (urgency, authority, social proof) without making it obvious.
- End with: “More at our website Huracanes_Caribe 🌐” (no clickable link).
- Do not contradict clear NHC statements about no expected cyclone formation.

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


def find_latest_image(basin_keyword: str) -> Path | None:
    """Find the latest image for the given basin."""
    folders = sorted(OUTPUT_DIR.glob("*"), reverse=True)
    for folder in folders:
        if folder.is_dir():
            candidates = sorted(folder.glob(f"*{basin_keyword}*.png"), reverse=True)
            if candidates:
                return candidates[0]
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
        for basin in ["atlantic", "eastpac"]:
            image = find_latest_image(basin)

            if not image:
                print(f"❌ No image for {basin}.")
                continue

            if not is_image_from_today(image):
                print(f"⏭️ Skipping {basin} — image is not from today.")
                continue


            caption = generate_facebook_caption_with_gpt(
                rtf_texts.get(basin, ""), basin, lang=lang
            )
            # Log the caption to file
            log_path = BASE_DIR / "facebook_caption_log.txt"
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