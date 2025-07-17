"""
Robust ATCF *.dat / *.btk reader
--------------------------------
Parses fixes into a typed list that tolerates malformed lines and
captures SPAWNINVEST / GENESIS tags.

Usage:
    from utils.dat_parser import load_dat
    fixes = load_dat(Path("/path/to/al932025.dat"))
"""

from __future__ import annotations

import datetime as dt
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

# ----------------------------------------------------------------------
# Models
# ----------------------------------------------------------------------

@dataclass
class Fix:
    """One position fix (single line in an ATCF file)."""
    ymdhm: dt.datetime        # always UTC
    status: str               # DB/TD/TS/HU/EX/SI/.. (first 2 chars of col 11)
    lat: float                # +N, −S  (decimal degrees)
    lon: float                # +E, −W  (decimal degrees, 0‒360 handled)
    tag: str = ""             # free-form trailing tag (GENESISxxx, INVEST...)
    spawninvest: bool = False
    system_id: str = ""       # e.g., '93L' for al932025.dat

# ----------------------------------------------------------------------
# Internal helpers
# ----------------------------------------------------------------------

_LOGGER = logging.getLogger(__name__)

_DATE_RE = re.compile(r"^(\d{4})(\d{2})(\d{2})(\d{2})$")
_LAT_RE  = re.compile(r"^(\d{2,3})([NS])$")
_LON_RE  = re.compile(r"^(\d{3,4})([EW])$")

def _parse_latlon(lat_tok: str, lon_tok: str) -> Tuple[float, float] | None:
    """Return (+lat, +lon) decimal degrees or None if malformed."""
    mlat, mlon = _LAT_RE.match(lat_tok), _LON_RE.match(lon_tok)
    if not (mlat and mlon):
        return None
    lat_d, ns = mlat.groups()
    lon_d, ew = mlon.groups()
    lat = int(lat_d) / 10.0 * (-1 if ns == "S" else 1)
    lon = int(lon_d) / 10.0 * (-1 if ew == "W" else 1)
    # normalise west-longitudes to negative range if desired:
    if lon > 180:
        lon -= 360.0
    return lat, lon

# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------

def load_dat(path: Path) -> List[Fix]:
    """
    Parse an ATCF *.dat or *.btk file.

    * Bad lines are skipped with a warning (never raises).
    * Returned list is sorted chronologically.
    """
    fixes: List[Fix] = []
    system_id = ""

    try:
        text = path.read_text()
    except FileNotFoundError:
        _LOGGER.warning("ATCF file missing: %s", path)
        return fixes

    fname = path.name
    # Example: al932025.dat -> system_id = '93L'
    fname_lower = fname.lower()
    if fname_lower.startswith("al") or fname_lower.startswith("ep"):
        num = fname[2:4]
        basin = fname[:2].upper()
        year = fname[4:8]
        system_id = f"{num}{'L' if basin == 'AL' else 'E'}"
    # Ensure system_id is set for every Fix
    for ln_num, line in enumerate(text.splitlines(), 1):
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 11:
            _LOGGER.warning("%s:%d – too few columns", path.name, ln_num)
            continue

        # --- timestamp -------------------------------------------------
        candidate_ts = parts[0] if _DATE_RE.match(parts[0]) else (
            parts[2] if len(parts) > 2 and _DATE_RE.match(parts[2]) else None)

        if candidate_ts:
            dtm = _DATE_RE.match(candidate_ts)
            y, m, d, H = map(int, dtm.groups())
            ymdhm = dt.datetime(y, m, d, H, 0, tzinfo=dt.timezone.utc)
        else:
            _LOGGER.warning("%s:%d – bad timestamp (tried parts[0] and parts[2]): %s", path.name, ln_num, parts)
            continue

        # --- lat / lon --------------------------------------------------
        latlon = _parse_latlon(parts[6], parts[7])
        if not latlon:
            _LOGGER.warning("%s:%d – bad lat/lon: %s, %s", path.name, ln_num, parts[6], parts[7])
            continue
        lat, lon = latlon

        # --- status & tag ----------------------------------------------
        status = parts[10][:2].upper()
        tag = parts[28].strip().upper() if len(parts) > 28 else ""
        spawninvest = "spawninvest" in line.lower()
        fix = Fix(ymdhm, status, lat, lon, tag, spawninvest, system_id)
        print(f"[DEBUG] Parsed Fix: system_id={fix.system_id}, status={fix.status}, tag={fix.tag}, spawninvest={fix.spawninvest}, lat={fix.lat}, lon={fix.lon}, ymdhm={fix.ymdhm}")
        fixes.append(fix)

    fixes.sort(key=lambda f: f.ymdhm)
    return fixes

