# config.py – Centralized configuration for map styling and paths

import pathlib
from pathlib import Path

# Resolve BASE_DIR relative to the actual config.py file location
BASE_DIR = Path(__file__).resolve().parent

# ——— COLORS ———————————————————————————————————————————
COL = dict(
    ocean    = "#004066",
    land     = "#e9e9e6",
    coast    = "#000000",
    border   = "#444444",
    state    = "#666666",
    lake     = "#004066",

    two2_low  = "#fff66d",
    two2_med  = "#ffa200",
    two2_high = "#ff0000",

    two7_low  = "#fff66d",
    two7_med  = "#ffa200",
    two7_high = "#ff0000",

    X_low     = "#fff66d",
    X_med     = "#ffa200",
    X_high    = "#ff0000",

    arrow_low  = "#fff66d",
    arrow_med  = "#ffa200",
    arrow_high = "#ff0000",
)


# ——— MAP EXTENTS ————————————————————————————————————————
DEFAULT_EXTENT = {
    "AL": [-100, -8, 5.5, 46],       # Atlantic
    "EP": [-130, -78, 4, 30]      # East Pacific
}

# ——— FIGURE OUTPUT SETTINGS ——————————————————————————————
FIGSIZE = (14, 8)
DPI     = 300

# ——— FILESYSTEM PATHS ——————————————————————————————————————
from pathlib import Path

# Only the folders you actually use
DATADIR = BASE_DIR / "data_archive"
OUTDIR = BASE_DIR / "output"

OUTDIR.mkdir(exist_ok=True)
DATADIR.mkdir(exist_ok=True)
