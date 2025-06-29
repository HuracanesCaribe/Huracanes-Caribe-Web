# config.py – Centralized configuration for map styling and paths

import pathlib

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
)

# ——— MAP EXTENTS ————————————————————————————————————————
DEFAULT_EXTENT = {
    "AL": [-100, -8, 4, 46],       # Atlantic
    "EP": [-130, -78, 4, 30]      # East Pacific
}

# ——— FIGURE OUTPUT SETTINGS ——————————————————————————————
FIGSIZE = (14, 11)
DPI     = 300

# ——— FILESYSTEM PATHS ——————————————————————————————————————
BASE    = pathlib.Path(__file__).resolve().parent
OUTDIR  = BASE / "output"
DATADIR = BASE / "data"

OUTDIR.mkdir(exist_ok=True)
DATADIR.mkdir(exist_ok=True)
