# models/ecmwf_processor.py
import xarray as xr

def process_precip_data(nc_path: str):
    """
    Processes ECMWF NetCDF precipitation data and returns the first time slice in mm.
    """
    ds = xr.open_dataset(nc_path)
    ds['tp'] = ds['tp'] * 1000  # Convert from meters to mm
    return ds['tp'].isel(time=0)
