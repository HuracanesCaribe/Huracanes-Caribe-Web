# models/ecmwf_downloader.py
import cdsapi

def download_ecmwf_rainfall(date_str: str, output_path: str):
    """
    Downloads ECMWF ERA5 total precipitation data for a given UTC date.
    """
    year, month, day = date_str[:4], date_str[4:6], date_str[6:8]

    c = cdsapi.Client()

    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': 'reanalysis',
            'variable': 'total_precipitation',
            'year': year,
            'month': month,
            'day': day,
            'time': '00:00',
            'format': 'netcdf',
            'area': [35, -100, 5, -50],  # [N, W, S, E]
        },
        output_path
    )

