import requests
import zipfile
import shutil
import io
import os

def download_gtwo_shapefile(basin_tag=None):
    """
    Download the GTWO shapefile zip without extraction.
    """
    url = "https://www.nhc.noaa.gov/xgtwo/gtwo_shapefiles.zip"
    local_zip = "data/gtwo_shapefiles.zip"

    with requests.get(url, stream=True, timeout=30) as r:
        with open(local_zip, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    print(f"✅ Downloaded GTWO shapefiles to {local_zip}")


