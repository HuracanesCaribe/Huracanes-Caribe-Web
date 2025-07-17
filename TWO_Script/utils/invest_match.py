"""
Invest-matching + caching layer
-------------------------------
* Downloads ATCF *.dat on demand (FTP).
* Caches files for up to TTL_HRS to avoid hammering the server.
* Classifies a GTWO disturbance as:
    - Named STORM (AL01–AL89) ➜ suppress TWO, plot storm only
    - INVEST (AL90–AL99)      ➜ plot TWO polygon, use invest label
    - No match                ➜ plot full TWO point + polygon
"""

import datetime as dt
import ftplib
import functools
import logging
import math
import os
from pathlib import Path
from typing import Tuple
from shapely.geometry import Point

from utils.dat_parser import load_dat, Fix
from .system_match import SystemMatch

# ----------------------------------------------------------------------
# Config
# ----------------------------------------------------------------------

ATCF_FTP   = "ftp.nhc.noaa.gov"
FTP_DIR    = "/atcf/btk"
CACHE_DIR  = Path("atcf_dat")
CACHE_DIR.mkdir(exist_ok=True)

BASINS     = ("AL", "EP")
MAX_DEG    = 15.0
TTL_HRS    = 3

_LOGGER = logging.getLogger(__name__)

# ----------------------------------------------------------------------
# Distance
# ----------------------------------------------------------------------

def _haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

# ----------------------------------------------------------------------
# Caching
# ----------------------------------------------------------------------

def _cache_path(basin: str, invest: str) -> Path:
    return CACHE_DIR / f"{basin}{invest}.dat"

def _download_dat(basin: str, invest: str, dst: Path) -> bool:
    fname = f"{basin}{invest}.dat"
    try:
        with ftplib.FTP(ATCF_FTP, timeout=20) as ftp:
            ftp.login()
            ftp.cwd(FTP_DIR)
            with dst.open("wb") as fd:
                ftp.retrbinary(f"RETR {fname}", fd.write)
        _LOGGER.info("Fetched %s", fname)
        return True
    except ftplib.all_errors as exc:
        _LOGGER.warning("No remote file %s (%s)", fname, exc)
        return False

def _get_dat_path(basin: str, invest: str, force_download=False) -> Path | None:
    """
    Returns the path to the ATCF .dat file for the given basin/invest.
    If the file exists locally, always use it (even if older than TTL_HRS).
    If not, or if force_download=True, attempt to fetch from NHC FTP.
    """
    from pathlib import Path

    dat_dir = Path(__file__).resolve().parent.parent / "atcf_dat"
    dat_dir.mkdir(exist_ok=True)
    dat_path = dat_dir / f"{basin}{invest}.dat"

    if dat_path.exists() and not force_download:
        print(f"[DEBUG] Using cached ATCF file: {dat_path}")
        return dat_path

    print(f"[DEBUG] Attempting to download {basin}{invest}.dat from FTP...")

    # Directly call _download_dat (already defined in this file)
    success = _download_dat(basin, invest, dat_path)
    if success:
        print(f"[DEBUG] Downloaded {basin}{invest}.dat and cached at: {dat_path}")
        return dat_path
    else:
        print(f"[WARN] Could not download {basin}{invest}.dat")
        return None


@functools.lru_cache(maxsize=128)
def _get_fixes(basin: str, invest: str) -> list[Fix]:
    path = _get_dat_path(basin, invest)
    return load_dat(path) if path else []

# ----------------------------------------------------------------------
# Genesis splitting
# ----------------------------------------------------------------------

def _split_genesis(fixes: list[Fix]) -> Tuple[list[Fix], list[Fix]]:
    for idx, f in enumerate(fixes):
        if f.status == "SI":
            return fixes[:idx], fixes[idx:]
    return fixes, []

def _latest_status(fixes: list[Fix]) -> str | None:
    for code in ("HU", "TS", "TD", "DB"):
        if any(f.status == code for f in reversed(fixes)):
            return code
    return None

# ----------------------------------------------------------------------
# New match_best_system() — activated
# ----------------------------------------------------------------------

def match_best_system(point: Point, issue_dt: dt.datetime, atcf_fixes=None, debug=False, radius_deg=10) -> SystemMatch | None:
    """
    Matches a GTWO area (point) to the best INVEST/STORM system within a configurable radius (degrees).
    Args:
        point: Shapely Point (GTWO centroid)
        issue_dt: GTWO issue datetime
        atcf_fixes: Optional list of Fix objects to use for matching
        debug: Print debug info
        radius_deg: Search radius in degrees (default 10)
    Returns:
        SystemMatch or None
    """
    match = None
    min_dist = radius_deg * 111  # radius in km

    if atcf_fixes is not None:
        # Use provided fixes for matching
        systems = {}
        for fix in atcf_fixes:
            if abs((issue_dt - fix.ymdhm).total_seconds()) < 36*3600 and fix.status in ("DB", "TD", "TS", "HU"):
                systems.setdefault(fix.system_id, []).append(fix)
        for system_id, fixes in systems.items():
            # --- ENHANCED INVEST LOGIC ---
            number = int(system_id[:2]) if system_id[:2].isdigit() else 99
            is_invest = any(fix.spawninvest for fix in fixes) or (90 <= number <= 99) or ("INVEST" in system_id)
            if debug:
                print(f"[DEBUG] {system_id}: {len(fixes)} candidate fixes (from provided list)")
                print(f"    INVEST by spawninvest/number: {is_invest}")
                if fixes:
                    last_fix = fixes[-1]
                    dist = _haversine_km(point.y, point.x, last_fix.lat, last_fix.lon)
                    print(f"    Last fix: status={last_fix.status}, system_id={last_fix.system_id}, tag={last_fix.tag}, dist={dist:.2f} km")
            if not fixes:
                continue
            last_fix = fixes[-1]
            dist = _haversine_km(point.y, point.x, last_fix.lat, last_fix.lon)
            if dist > min_dist:
                continue
            status = last_fix.status
            if number < 90:
                return SystemMatch(system_id, "STORM", status, last_fix, dist, use_two=False)
            elif is_invest:
                if match is None or dist < match.distance_km:
                    match = SystemMatch(system_id, "INVEST", status, last_fix, dist, use_two=True)
        return match

    for fname in os.listdir("atcf_dat"):
        if not fname.endswith(".dat"):
            continue
        basin = fname[:2].upper()
        if basin == "CP":
            continue
        try:
            number = int(fname[2:4])
        except ValueError:
            continue
        system_id = basin + f"{number:02d}"
        dat_path = CACHE_DIR / fname
        if not dat_path.exists():
            continue
        # Check if INVEST is mentioned in the .dat file
        with open(dat_path, "r") as f:
            dat_text = f.read().upper()
        fixes = [fix for fix in load_dat(dat_path)
                 if abs((issue_dt - fix.ymdhm).total_seconds()) < 36*3600 and fix.status in ("DB", "TD", "TS", "HU")]
        # Determine INVEST status: either 'INVEST' in .dat or any Fix has spawninvest=True
        is_invest = "INVEST" in dat_text or any(fix.spawninvest for fix in fixes)
        if debug:
            print(f"[DEBUG] {system_id}: {len(fixes)} candidate fixes")
            print(f"    INVEST in .dat: {'INVEST' in dat_text}")
            print(f"    INVEST by spawninvest: {any(fix.spawninvest for fix in fixes)}")
            if fixes:
                last_fix = fixes[-1]
                dist = _haversine_km(point.y, point.x, last_fix.lat, last_fix.lon)
                print(f"    Last fix: status={last_fix.status}, system_id={last_fix.system_id}, tag={last_fix.tag}, dist={dist:.2f} km")
        if not fixes:
            continue
        last_fix = fixes[-1]
        dist = _haversine_km(point.y, point.x, last_fix.lat, last_fix.lon)
        if dist > min_dist:
            continue
        status = last_fix.status
        if number < 90:
            return SystemMatch(system_id, "STORM", status, last_fix, dist, use_two=False)
        elif is_invest:
            if match is None or dist < match.distance_km:
                match = SystemMatch(system_id, "INVEST", status, last_fix, dist, use_two=True)
    return match

def get_atcf_fixes(basin):
    """
    Loads all ATCF fixes for a basin (e.g., 'AL', 'EP').
    Returns: list of Fix objects.
    """
    fixes = []
    for num in range(90, 100):
        fixes.extend(_get_fixes(basin, f"{num:02d}"))
    return fixes
