import requests
import zipfile
import io
import os

def download_gtwo_shapefile(basin_code, output_dir="data"):
    basin_map = {
        "AL": "two_atl_7day_shapefiles.zip",
        "EP": "two_epac_7day_shapefiles.zip"
    }
    zip_name = basin_map[basin_code]
    url = f"https://www.nhc.noaa.gov/xgtwo/gtwo_shapefiles.zip"

    print(f"⬇️  Downloading: {url}")
    resp = requests.get(url)
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to fetch shapefile for {basin_code} ({resp.status_code})")

    os.makedirs(output_dir, exist_ok=True)
    z = zipfile.ZipFile(io.BytesIO(resp.content))
    z.extractall(output_dir)
    print(f"✅ Extracted shapefiles to {output_dir}")
