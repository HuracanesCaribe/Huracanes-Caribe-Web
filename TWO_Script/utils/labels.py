"""
Centralised label & colour builder
----------------------------------
Keeps ALL human-readable labels and palette logic in one place.
"""

from __future__ import annotations
from config import COL
from dataclasses import dataclass
from typing import Tuple, List, Dict, Optional


# ----------------------------------------------------------------------
# Colour tables
# ----------------------------------------------------------------------

PROB_COLOUR = {
    "LOW": COL["two2_low"],
    "MEDIUM": COL["two2_med"],
    "HIGH": COL["two2_high"],
}

STATUS_COLOUR = {
    "HU": COL.get("storm_hu", "#bd0026"),
    "TS": COL.get("storm_ts", "#fd8d3c"),
    "TD": COL.get("storm_td", "#feb24c"),
    "DB": COL.get("storm_db", "#ffffb2"),
}


DEFAULT_COLOUR = "#cccccc"

# ----------------------------------------------------------------------
# API
# ----------------------------------------------------------------------

@dataclass
class DisturbanceInfo:
    def __init__(self, area_num, prob2, prob7, invest_id=None, status=None, prob2_pct=None, prob7_pct=None):
        self.area_num = area_num
        self.prob2 = prob2
        self.prob7 = prob7
        self.invest_id = invest_id
        self.status = status 
        self.prob2_pct = prob2_pct 
        self.prob7_pct = prob7_pct # Percentages for display

from config import COL

def build_label(info) -> tuple[str, str]:
    """
    Create a multiline label and associated color based on disturbance info.
    Always returns (label_text, color_hex).
    """
    # Default values
    pct2 = info.prob2_pct.strip() if info.prob2_pct and info.prob2_pct.strip() else "--"
    pct7 = info.prob7_pct.strip() if info.prob7_pct and info.prob7_pct.strip() else "--"

    risk2 = info.prob2.title() if info.prob2 else "Low"
    risk7 = info.prob7.title() if info.prob7 else "Low"

    # Determine color from 2-day risk
    color_key = f"two2_{risk2.lower()}"
    color = COL.get(color_key, COL["two2_low"])

    # Only show INVEST {system_id} for invest labels, no status
    if info.invest_id:
        title = f"{info.invest_id}"  # Do not append status
    else:
        title = "DISTURBANCE"

    label = "\n".join([
        f"{title}",
        f"{pct2} in 2-day: {risk2}",
        f"{pct7} in 7-day: {risk7}"
    ])

    return label, color


class SystemMatch:
    """
    Represents a match between GTWO area and a system.
    Parameters:
        system_id (str): System identifier.
        status (str): INVEST or STORM.
        fix_status (str): Status from last fix.
        last_fix (Fix): Last fix object.
        distance_km (float): Distance to GTWO point.
        use_two (bool): True if using GTWO area.
    """
    def __init__(self, system_id, status, fix_status, last_fix, distance_km, use_two=False):
        self.system_id = system_id
        self.status = status
        self.fix_status = fix_status
        self.last_fix = last_fix
        self.distance_km = distance_km
        self.use_two = use_two


def normalize_risk_key(risk: str) -> str:
    """
    Normalize risk string to match COL keys.
    Accepts 'low', 'medium', 'med', 'high', etc.
    Returns: 'low', 'med', or 'high'
    """
    risk = risk.strip().lower()
    if risk in ("medium", "med"): return "med"
    if risk in ("high", "hi"): return "high"
    return "low"


def get_risk_color(prob2, prob7):
    """
    Returns color and hatch pattern for GTWO polygons based on risk or percentage.
    Parameters:
        prob2 (str): 2-day probability (e.g. '40%') or risk (e.g. 'Medium').
        prob7 (str): 7-day risk level.
    Returns:
        tuple: (color2, hatch)
    """
    # Use percentage logic for color
    color2 = COL["two2_low"]  # default yellow
    pct = None
    if isinstance(prob2, str) and prob2.strip().endswith('%'):
        try:
            pct = int(prob2.strip().replace('%', ''))
        except Exception:
            pct = None
    if pct is not None:
        if pct < 40:
            color2 = COL["two2_low"]  # yellow
        elif 40 <= pct <= 60:
            color2 = COL["two2_med"]  # orange
        elif pct > 60:
            color2 = COL["two2_high"]  # red
    else:
        color2 = COL.get(f"two2_{normalize_risk_key(prob2)}", COL["two2_low"])
    hatch = "////" if normalize_risk_key(prob7) != "low" else None
    # Debug print
    print(f"[DEBUG] get_risk_color: prob2={prob2}, pct={pct}, color2={color2}, prob7={prob7}, hatch={hatch}")
    return color2, hatch


def label_with_invest_status(area_num, match, reporter, prob2="LOW"):
    """
    Returns label and color for GTWO area based on INVEST/STORM status.
    Parameters:
        area_num (int): GTWO area number.
        match: SystemMatch object or None.
        reporter: Reporter object for logging.
        prob2 (str): 2-day probability (e.g. '40%') or risk (e.g. 'Medium').
    Returns:
        tuple: (label_text, color)
    """
    # Use percentage logic for color
    color = COL["two2_low"]  # default yellow
    pct = None
    if isinstance(prob2, str) and prob2.strip().endswith('%'):
        try:
            pct = int(prob2.strip().replace('%', ''))
        except Exception:
            pct = None
    if pct is not None:
        if pct < 40:
            color = COL["two2_low"]  # yellow
        elif 40 <= pct <= 60:
            color = COL["two2_med"]  # orange
        elif pct > 60:
            color = COL["two2_high"]  # red
    # fallback: if not a percent, use risk string
    else:
        color = COL.get(f"two2_{normalize_risk_key(prob2)}", COL["two2_low"])
    print(f"[DEBUG] label_with_invest_status: area_num={area_num}, match={match}, color={color}, prob2={prob2}")
    if match and getattr(match, "system_type", None) == "INVEST":
        label_text = f"INVEST {match.system_id}"
    elif match and getattr(match, "system_type", None) == "STORM":
        label_text = f"STORM {match.system_id}"
    else:
        label_text = f"DISTURBANCE {area_num}"
    reporter.log(area_num, match.system_id if match else None, match.status if match else None, label_text)
    return label_text, color

