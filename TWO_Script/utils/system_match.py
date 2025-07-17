# TWO_Script/utils/system_match.py

from dataclasses import dataclass
import datetime as dt

@dataclass
class Fix:
    ymdhm: dt.datetime
    status: str
    lat: float
    lon: float
    tag: str = ""

@dataclass
class SystemMatch:
    system_id: str       # e.g. AL93, EP01
    system_type: str     # "STORM" or "INVEST"
    status: str          # TD, TS, HU, DB
    fix: Fix             # last available fix at or before GTWO time
    distance_km: float   # distance from GTWO point
    use_two: bool        # True if TWO geometry should be shown
