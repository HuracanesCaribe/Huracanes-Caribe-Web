# main.py – Entry point with CLI support

import pathlib
import argparse
from datetime import datetime, timezone
from two_plot import build_outlook
from datetime import datetime, timezone
from facebook_poster import post_to_facebook
from gtwo_fetcher import download_gtwo_shapefile
import matplotlib.pyplot as plt

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

            # 🔽 NEW: Post to Facebook
            #post_to_facebook(
                #image_path=out_path,
                #caption=f"{label} GTWO update – {ts.strftime('%Y-%m-%d %H:%M UTC')}"
            #)

        except Exception as e:
            print(f"❌ Failed for {basin_tag}: {e}")


if __name__ == "__main__":
    main()
