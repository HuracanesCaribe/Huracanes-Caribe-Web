# models/gfs_processor.py
import xarray as xr

def process_precip_data(nc_path: str):
    try:
        ds = xr.open_dataset(nc_path)
        if "tp" in ds:
            return ds["tp"]
        else:
            print("⚠️ 'tp' variable not found in dataset.")
            return None
    except Exception as e:
        print(f"❌ Failed to load NetCDF: {e}")
        return None
