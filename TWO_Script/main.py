# main.py – Entry point with CLI support

import pathlib
import argparse
from datetime import datetime, timezone
from two_plot import build_outlook
from datetime import datetime, timezone, timedelta
from facebook_poster import post_to_facebook
from gtwo_fetcher import download_gtwo_shapefile
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
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).isoformat(),
                        help="UTC timestamp (ISO format) to use in filenames.")
    args = parser.parse_args()

    # Determine which basins to run
    selected = BASINS.items() if not args.basin else [(b, BASINS[b]) for b in args.basin]
    outdir = args.outdir
    outdir.mkdir(exist_ok=True)

    ts = datetime.fromisoformat(args.timestamp)

    for basin_tag, (label, prefix) in selected:
        try:
            download_gtwo_shapefile(basin_tag)
            out_path = build_outlook(basin_tag, label, prefix, outdir, ts)
            print(f"✅ Saved: {out_path.relative_to(outdir.parent)}")
            
         
            # only copy on Linux
            if platform.system() == "Linux":
                # everything that copies to /var/www/html/output
                today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                target_dir = f"/var/www/html/output/{today_str}"
                os.makedirs(target_dir, exist_ok=True)
                shutil.copy(str(out_path), target_dir)

                # cleanup
                output_base = "/var/www/html/output"
                for folder in os.listdir(output_base):
                    folder_path = os.path.join(output_base, folder)
                    if os.path.isdir(folder_path):
                        try:
                            folder_date = datetime.strptime(folder, "%Y-%m-%d")
                            if folder_date < datetime.now(timezone.utc) - timedelta(days=6):
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
