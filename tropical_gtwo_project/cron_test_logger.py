# cron_test_logger.py – quick UTC test logger for manual runs

from datetime import datetime, timezone
import pathlib

log_path = pathlib.Path("/Users/tejedawx/cron_test.log")

timestamp = datetime.now(timezone.utc).isoformat()

with log_path.open("a") as f:
    f.write(f"[TEST] Triggered manually at UTC: {timestamp}\n")

print(f"Logged UTC time: {timestamp}")
