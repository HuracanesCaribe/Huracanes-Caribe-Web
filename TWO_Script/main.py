# main.py – Entry point with CLI support

import pathlib
import argparse
from two_plot import build_outlook
from datetime import datetime, timezone, timedelta
from facebook_poster import post_to_facebook
from gtwo_fetcher import download_gtwo_shapefile
from two_data import download_gtwo_zip, parse_issue_time_from_xml
import matplotlib.pyplot as plt
import platform
import shutil
import os

with open("cron_test.log", "a") as f:
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
    parser.add_argument("--outdir", type=pathlib.Path, default=pathlib.Path("output"),
                        help="Directory to save output PNGs.")
    parser.add_argument("--timestamp", default=None,
                        help="Override issuance timestamp in ISO format.")
    args = parser.parse_args()

    # Determine which basins to run
    selected = BASINS.items() if not args.basin else [(b, BASINS[b]) for b in args.basin]
    outdir = args.outdir
    outdir.mkdir(exist_ok=True)

    if args.timestamp:
        ts = datetime.fromisoformat(args.timestamp)
    else:
        zip_path = download_gtwo_zip()
        ts = parse_issue_time_from_xml(zip_path)

    for basin_tag, (label, prefix) in selected:
        try:
            #download_gtwo_shapefile(basin_tag)
            out_path = build_outlook(basin_tag, label, prefix, outdir, ts)
            issue_dt = parse_issue_time_from_xml(zip_path)
            print(f"{basin_tag} timestamp from XML: {issue_dt.isoformat()}")
            print(f"✅ Saved: {out_path.relative_to(outdir.parent)}")
            timestamp_str = issue_dt.strftime("%Y%m%dT%H%MZ")
            today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

            # archive the GTWO shapefiles into dated folders           
            if platform.system() == "Linux":
                data_target_dir = f"/var/www/html/data/{today_str}"
            else:
                data_target_dir = f"data_archive/{today_str}"

            os.makedirs(data_target_dir, exist_ok=True)

            # archive the downloaded GTWO zips (not .shp extracted)
            for basin in ["atl", "ep"]:
                zipfile_path = "data/gtwo_shapefiles.zip"
                print(f"CHECKING: {zipfile_path}")
                if os.path.exists(zipfile_path):
                    archive_name = f"gtwo_shapefiles_{timestamp_str}.zip"
                    shutil.copy("data/gtwo_shapefiles.zip", os.path.join(data_target_dir, archive_name))
                    print(f"✅ Copied gtwo_shapefiles.zip to {data_target_dir}/{archive_name}")
                    
                    # ALSO write a .txt file with its contents
                    from zipfile import ZipFile

                    with ZipFile("data/gtwo_shapefiles.zip") as zf:
                        names = zf.namelist()
                        txt_log_path = os.path.join(data_target_dir, f"gtwo_shapefiles_{timestamp_str}.txt")
                        with open(txt_log_path, "w") as logf:
                            logf.write("\n".join(names))
                        print(f"✅ Created list of files: {txt_log_path}")
                else:
                    print(f"❌ Missing {zipfile_path}, could not archive")


            # cleanup data folders older than 5 days
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

            # Platform-independent output folder logic

            if platform.system() == "Linux":
                # server path
                target_dir = f"/var/www/html/output/{today_str}"
            else:
                # local Mac path
                target_dir = f"output/{today_str}"

            os.makedirs(target_dir, exist_ok=True)

            # copy the PNG to that folder
            shutil.copy(str(out_path), target_dir)

            # cleanup folders older than 5 days
            output_base = os.path.dirname(target_dir)
            for folder in os.listdir(output_base):
                folder_path = os.path.join(output_base, folder)
                if os.path.isdir(folder_path):
                    try:
                        folder_date = datetime.strptime(folder, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                        if folder_date < datetime.now(timezone.utc) - timedelta(days=5):
                            shutil.rmtree(folder_path)
                            print(f"Removed old folder: {folder_path}")
                    except ValueError:
                        continue




            # 🔽 NEW: Post to Facebook
            #post_to_facebook(
                #image_path=out_path,
                #caption=f"{label} GTWO update – {ts.strftime('%Y-%m-%d %H:%M UTC')}"
            #)

        except Exception as e:
            print(f"❌ Failed for {basin_tag}: {e}")


if __name__ == "__main__":
    main()
