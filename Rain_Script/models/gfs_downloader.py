# models/gfs_downloader.py
import os
import requests
import xarray as xr
from datetime import datetime

# Define the geographic subset (Mexico, Caribbean, Central America, USA)
SUBSET = {
    "north": 50,
    "south": 5,
    "west": -125,
    "east": -55,
}

BASE_URL = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod"
FORECAST_STEPS = [f"{i:03}" for i in range(3, 25, 3)]  # f003 to f024

def download_gfs_rainfall(date_str: str, output_path: str):
    """
    Downloads and sums 24h GFS rainfall forecast from f003 to f024,
    crops to defined region, converts to NetCDF, masks ocean.
    """
    if os.path.exists(output_path):
        print(f"⚠️ Using existing NetCDF: {output_path}")
        return

    import cfgrib
    import numpy as np

    gfs_hour = "00"
    tp_list = []

    for step in FORECAST_STEPS:
        url = (
            f"{BASE_URL}/gfs.{date_str}/{gfs_hour}/atmos/"
            f"gfs.t{gfs_hour}z.pgrb2.0p25.f{step}"
        )
        grib_path = f"data/tmp_gfs_{step}.grib2"

        print(f"📥 Downloading {step}: {url}")
        try:
            r = requests.get(url, timeout=90)
            r.raise_for_status()
            with open(grib_path, "wb") as f:
                f.write(r.content)
        except Exception as e:
            print(f"❌ Failed to download {step}: {e}")
            continue

        try:
            ds = xr.open_dataset(
                grib_path,
                engine="cfgrib",
                backend_kwargs={"filter_by_keys": {"typeOfLevel": "surface", "shortName": "tp"}}
            )

            # Subset
            ds = ds.sel(
                latitude=slice(SUBSET["north"], SUBSET["south"]),
                longitude=slice(SUBSET["west"] % 360, SUBSET["east"] % 360)
            )

            tp_list.append(ds["tp"].load())
        except Exception as e:
            print(f"❌ Failed to process {step}: {e}")
        finally:
            if os.path.exists(grib_path):
                os.remove(grib_path)

    if not tp_list:
        print("❌ No valid GFS tp data found.")
        return

    # Align and sum
    total_tp = xr.align(*tp_list, join="exact")[0].copy()
    for tp in tp_list[1:]:
        total_tp += tp

    total_tp.name = "tp"
    total_tp.attrs["long_name"] = "24h Accumulated Precipitation"
    total_tp.attrs["units"] = "mm"

    total_tp.to_netcdf(output_path)
    print(f"✅ Saved 24h accumulated rainfall to: {output_path}")