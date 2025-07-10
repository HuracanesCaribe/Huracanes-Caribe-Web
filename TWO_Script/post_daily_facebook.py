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

# --- Load secrets ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Constants ---
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR.parent / "output"
DATA_DIR = BASE_DIR.parent / "data_archive"

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


def generate_facebook_caption_with_gpt(rtf_text: str, basin: str, lang: str = "es") -> str:
    """Generate a Facebook caption in warm, professional Caribbean Spanish using GPT."""
    import re
    rtf_text_cleaned = re.sub(r"{\\.*?}|\\[a-z]+\d*|{|}", "", rtf_text)

    if lang == "es":
        prompt = f"""
Eres un comunicador meteorológico de confianza para redes sociales como Facebook y X. Tu tarea es generar una publicación clara, cálida y profesional en español caribeño, basada en el siguiente resumen oficial del Centro Nacional de Huracanes (NHC) sobre el panorama de ciclones tropicales en el {basin}.

Normas:
- Escribe entre 60 y 100 palabras (preferible 60-70, máximo 150).
- Usa ingles neutro y correcto, con estilo cercano, confiable y sin títulos.
- Resalta si hay sistemas con probabilidad de formación (baja, media, alta).
- Usa emojis apropiados 🌧️🌀⚠️ para visibilidad y conexión emocional.
- Incluye principios sutiles de influencia (urgencia, autoridad, prueba social) sin que se noten.
- Cierra con una frase simple como: “Más información en huracanescaribe.com 🌐”.
- Nunca uses lenguaje técnico ni en mayúsculas.

Resumen GTWO (limpio):
{rtf_text_cleaned}
"""
    else:
        prompt = f"""You are a trusted weather communicator. Write a clear, reassuring public Facebook post in English, summarizing the latest tropical outlook for the {basin} based on the following NHC advisory. Max 150 words. Avoid jargon. End with: 'More at huracanescaribe.com 🌐'. Input: {rtf_text_cleaned}"""

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
            return f"{basin.capitalize()} — información no disponible por el momento."




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

    for basin in ["atlantic", "pacific"]:
        image = find_latest_image(basin)
        if not image:
            print(f"❌ No image found for {basin}.")
            continue

        caption = generate_facebook_caption_with_gpt(rtf_texts.get(basin, ""), basin)
        print(f"📸 Posting {image.name} with caption:")
        print(caption)

        # Post to Facebook
        post_to_facebook(str(image), caption=caption)

if __name__ == "__main__":
    main()
