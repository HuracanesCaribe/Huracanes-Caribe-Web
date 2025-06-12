# inspect_cone.py
import requests, zipfile, io, pathlib, geopandas as gpd, datetime, sys

DATA_DIR = pathlib.Path("data")
DATA_DIR.mkdir(exist_ok=True)

STATUS_URL = "https://www.nhc.noaa.gov/CurrentStorms.json"
print("Fetching storm list …")
data = requests.get(STATUS_URL, timeout=10).json()["activeStorms"]

if not data:
    print("No active storms 🎉  (Try again when hurricane season is underway.)")
    sys.exit(0)

storm = data[0]                                    # just the first storm
cone_zip_url = storm["forecastTrack"]["zipFile"]
adv = storm["forecastTrack"]["advNum"]
sid = storm["id"]

zip_path = DATA_DIR / f"{sid}_{adv}.zip"
if not zip_path.exists():                          # cache so we don't redownload
    print(f"Downloading cone ZIP for {sid} Adv {adv} …")
    zbytes = requests.get(cone_zip_url, timeout=30).content
    zip_path.write_bytes(zbytes)
else:
    print("ZIP already downloaded, reusing.")

# ---- open shapefile directly from the zip without extracting everything ----
with zipfile.ZipFile(zip_path) as zf:
    shp_name = next(n for n in zf.namelist() if n.endswith(".shp"))
    shp_path = f"zip://{zip_path}!{shp_name}"      # GDAL virtual path

print(f"Reading {shp_name} …")
gdf = gpd.read_file(shp_path)

print("\nColumns:", list(gdf.columns))
print("\nFirst 3 rows:")
print(gdf.head(3).to_string())

import geopandas as gpd, zipfile, pathlib

zip_path = pathlib.Path("data/two_latest.zip")
with zipfile.ZipFile(zip_path) as zf:
    shp = next(n for n in zf.namelist() if "gtwo_areas" in n and n.endswith(".shp"))
    gdf = gpd.read_file(f"zip://{zip_path}!{shp}")
print("Columns:", gdf.columns)
print(gdf.head(3)[["BASIN", "PROB", "PERIOD"]])   # or DAYNUM / HOUR, etc.