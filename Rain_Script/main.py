import os
import argparse
from datetime import datetime
from config import OUTPUT_DIR
from models.registry import MODEL_REGISTRY
from models.plot_rainfall import plot_precip_map, DEFAULT_EXTENT

# Parse CLI argument
parser = argparse.ArgumentParser(description="Generate daily rainfall map")
parser.add_argument("--model", type=str, default="ecmwf", choices=MODEL_REGISTRY.keys(), help="Which model to run")
args = parser.parse_args()
model_name = args.model.lower()

# Resolve functions
download_func = MODEL_REGISTRY[model_name]['download']
process_func = MODEL_REGISTRY[model_name]['process']

# Date setup
today = datetime.utcnow().strftime("%Y%m%d")
nc_file = f"{model_name}_{today}.nc"
output_nc_path = os.path.join("data", nc_file)
os.makedirs("data", exist_ok=True)

# Step 1: Download rainfall data
download_func(today, output_nc_path)

# Step 2: Process the NetCDF/GRIB file
precip = process_func(output_nc_path)

for region_key in ["DOM", "PR", "MEX", "CAM", "TX", "FL"]:
    output_png = os.path.join(OUTPUT_DIR, f"rainfall_{model_name}_{today}_{region_key}.png")
    title = f"{model_name.upper()} 24h Rainfall – {region_key}"
    extent = DEFAULT_EXTENT[region_key]
    plot_precip_map(precip, output_png, title=title, extent=extent)

# Step 3: Generate rainfall map (if precipitation data exists)
if precip is not None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_png = os.path.join(OUTPUT_DIR, f"rainfall_{model_name}_{today}.png")
    plot_precip_map(precip, output_png, title=f"{model_name.upper()} 24h Rainfall - {today}")
else:
    print(f"[{model_name.upper()}] No precipitation data available to plot.")
