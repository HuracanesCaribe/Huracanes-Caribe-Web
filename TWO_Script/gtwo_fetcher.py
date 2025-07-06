import requests
import zipfile
import shutil
import io
import os

def download_gtwo_shapefile(basin_tag):
    url = "https://www.nhc.noaa.gov/xgtwo/gtwo_shapefiles.zip"
    local_zip = "data/gtwo_shapefiles.zip"

    # download
    with requests.get(url, stream=True) as r:
        with open(local_zip, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    # do not delete it
    with zipfile.ZipFile(local_zip, "r") as zf:
        zf.extractall("data")
    
    print(f"✅ Saved zip to {local_zip} and extracted contents")

