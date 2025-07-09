# check_gtwo_update.py

import pathlib
import subprocess
import datetime
from two_data import download_gtwo_zip, parse_issue_time_from_xml

LAST_TS_FILE = pathlib.Path("last_gtwo_time.txt")
ZIP_PATH = download_gtwo_zip()

# Get new timestamp from GTWO
new_dt = parse_issue_time_from_xml(ZIP_PATH)
new_ts = new_dt.strftime("%Y%m%dT%H%MZ")

# Compare to last run
if LAST_TS_FILE.exists():
    last_ts = LAST_TS_FILE.read_text().strip()
    if new_ts == last_ts:
        print(f"🔁 GTWO unchanged — no action taken.\n -----------------------------------")
        exit(0)

# Save new timestamp
LAST_TS_FILE.write_text(new_ts)

# Run main.py
print(f"⚡ GTWO updated — running main.py\n -----------------------------------")
subprocess.run(["python3", "TWO_Script/main.py"])
