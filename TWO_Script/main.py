# main.py – Entry point with CLI support

import pathlib
import argparse
from two_plot import build_outlook
from datetime import datetime, timezone, timedelta
from two_data import download_gtwo_zip, parse_issue_time_from_xml
import matplotlib.pyplot as plt
import platform
import shutil
import os
from zipfile import ZipFile

from pathlib import Path
LOG_PATH = Path(__file__).parent / "main_runs.log"
with open(LOG_PATH, "a") as f:
    f.write("Triggered at: " + datetime.now(timezone.utc).isoformat() + "\n")

# Available basins and their config
BASINS = {
    "AL": ("Atlantic Basin", "atlantic"),
    "EP": ("Eastern Pacific", "eastpac"),
}

def main():
    parser = argparse.ArgumentParser(description="Generate 2/7-day GTWO maps.")
    parser.add_argument("--basin", choices=BASINS.keys(), nargs="*",
                        help="Basin code: AL (Atlantic) or EP (Eastern Pacific). If omitted, both run.")
    parser.add_argument("--timestamp", default=None,
                        help="Override issuance timestamp in ISO format.")
    args = parser.parse_args()

    # download GTWO zip and parse timestamp
    if args.timestamp:
        ts = datetime.fromisoformat(args.timestamp)
        zip_path = None  # you cannot archive in that case
    else:
        zip_path = download_gtwo_zip()
        ts = parse_issue_time_from_xml(zip_path)

    today_str = ts.strftime("%Y-%m-%d")
    timestamp_str = ts.strftime("%Y%m%dT%H%MZ")

    # build the target directory for images
    if platform.system() == "Linux":
        target_dir = f"/var/www/html/output/{today_str}"
    else:
        target_dir = f"output/{today_str}"

    os.makedirs(target_dir, exist_ok=True)

    # set outdir to dated folder so maps go there directly
    outdir = pathlib.Path(target_dir)

    # archive .txt manifest if zip was downloaded fresh
    if zip_path:
        if platform.system() == "Linux":
            data_target_dir = f"/var/www/html/data/{today_str}"
        else:
            data_target_dir = f"data_archive/{today_str}"
        os.makedirs(data_target_dir, exist_ok=True)

        with ZipFile(zip_path) as zf:
            names = zf.namelist()
            txt_log_path = os.path.join(data_target_dir, f"gtwo_shapefiles_{timestamp_str}.txt")
            with open(txt_log_path, "w") as logf:
                logf.write("\n".join(names))
            print(f"✅ Created list of files: {txt_log_path}\n")

        # cleanup old data folders
        data_base = os.path.dirname(data_target_dir)
        for folder in os.listdir(data_base):
            folder_path = os.path.join(data_base, folder)
            if os.path.isdir(folder_path):
                try:
                    folder_date = datetime.strptime(folder, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                    if folder_date < datetime.now(timezone.utc) - timedelta(days=5):
                        shutil.rmtree(folder_path)
                        print(f"🗑️ Removed old data folder: {folder_path}")
                except ValueError:
                    continue

    # cleanup old output folders
    output_base = os.path.dirname(target_dir)
    for folder in os.listdir(output_base):
        folder_path = os.path.join(output_base, folder)
        if os.path.isdir(folder_path):
            try:
                folder_date = datetime.strptime(folder, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                if folder_date < datetime.now(timezone.utc) - timedelta(days=5):
                    shutil.rmtree(folder_path)
                    print(f"🗑️ Removed old output folder: {folder_path}")
            except ValueError:
                continue

    # generate maps
    selected = BASINS.items() if not args.basin else [(b, BASINS[b]) for b in args.basin]
    for basin_tag, (label, prefix) in selected:
        try:
            out_path = build_outlook(basin_tag, label, prefix, outdir, ts, zip_path)
            print(f"✅ Saved: {out_path.relative_to(outdir.parent)}")

        except Exception as e:
            print(f"❌ Failed for {basin_tag}: {e}")

if __name__ == "__main__":
    main()
