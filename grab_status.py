#grab_status.py
import json, pathlib, requests, datetime
url = "https://www.nhc.noaa.gov/CurentStorms.json"
out = pathlib.Path("CurrentStorms_"+datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")+".json")
out.write_text(requests.get(url, timeout=10).text)
print(f"Saved: {out}")