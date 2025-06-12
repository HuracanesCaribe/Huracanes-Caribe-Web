#!/usr/bin/env python
# draw_two_only.py – 2- & 7-day Tropical Weather Outlook + invest “X”

import os, pathlib, time, datetime, zipfile, requests
import geopandas as gpd
from shapely.ops import linemerge
from matplotlib.patches import FancyArrowPatch
import shapely.geometry as shgeom
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import matplotlib.ticker as mticker
import matplotlib.patheffects as pe
import matplotlib.font_manager as font_manager
import re
from zoneinfo import ZoneInfo          # Python 3.9+
import cairocffi as cairo
import numpy as np
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox



# ———  CONFIG  ——————————————————————————————————————————————
os.environ["PROJ_LIB"] = "/Users/tejedawx/miniconda3/envs/huracanes/share/proj"

COL = dict(
    ocean    = "#004066",
    land     = "#e9e9e6",
    coast    = "#000000",
    border   = "#444444",
    state    = "#666666",
    lake     = "#004066",
    two2_low = "#fff66d",
    two2_med = "#ffa200",
    two2_high= "#ff0000",
    two7_low = "#fff66d",
    two7_med = "#ffa200",
    two7_high= "#ff0000",

    # Disturbance “X” colors (low/med/high)
    X_low      = "#fff66d",   # example: green
    X_med      = "#ffa200",   # example: yellow
    X_high     = "#ff0000",   # example: red

    # Arrow colors (matching the X’s), if you separate them
    arrow_low  = "#fff66d",
    arrow_med  = "#ffa200",
    arrow_high = "#ff0000",
)
DEFAULT_EXTENT = {"AL": [-100, -8, 4, 46],
                  "EP": [-130, -78, 4, 30]}

FIGSIZE, DPI = (14, 11), 300

BASE = pathlib.Path(__file__).resolve().parent
OUTDIR, DATADIR = BASE/"output", BASE/"data"
OUTDIR.mkdir(exist_ok=True); DATADIR.mkdir(exist_ok=True)
UTC_NOW = datetime.datetime.now(datetime.timezone.utc)
# ———  DATA GRABBERS  —————————————————————————————————————————
import re
def cairo_arrow_surface(length_px=140, shaft_px=20,
                        head_len_px=50, head_width_px=60,
                        rgb=(1, 1, 0)):
    """Return a cairo ImageSurface with a flat-tail, sharp-head arrow."""
    w = length_px + head_len_px
    h = max(head_width_px, shaft_px) + 4   # 4-px pad
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx  = cairo.Context(surf)

    ctx.set_source_rgba(0, 0, 0, 0)  # transparent background
    ctx.paint()

    # Draw shaft
    ctx.set_source_rgb(*rgb)
    ctx.rectangle(0, (h-shaft_px)/2, length_px, shaft_px)
    ctx.fill()

    # Draw head (triangle)
    ctx.move_to(length_px, (h-head_width_px)/2)
    ctx.line_to(w, h/2)
    ctx.line_to(length_px, (h+head_width_px)/2)
    ctx.close_path()
    ctx.fill()

    # 1-px black outline
    ctx.set_line_width(3)
    ctx.set_source_rgb(0, 0, 0)
    ctx.stroke()

    return surf

def draw_cairo_arrow(ax, x0, y0, x1, y1, rgb, zoom=0.28):
    """Paint a sharp-headed arrow from (x0,y0) → (x1,y1) on *ax*."""
    # Mid-point and bearing
    mid_lon, mid_lat = (x0 + x1) / 2, (y0 + y1) / 2
    bearing = -np.degrees(np.arctan2(y1 - y0, x1 - x0))  # minus = matplotlib rot

    # Build PNG surface → NumPy
    surf = cairo_arrow_surface(rgb=rgb)
    im   = Image.frombuffer(
        "RGBA", (surf.get_width(), surf.get_height()),
        surf.get_data(), "raw", "BGRA", 0, 1)
    arr  = np.array(im)
    arr  = np.array(Image.fromarray(arr).rotate(bearing, expand=True))

    imagebox = OffsetImage(arr, zoom=zoom)
    ab = AnnotationBbox(
        imagebox, (mid_lon, mid_lat),
        frameon=False,
        xycoords=ccrs.PlateCarree()._as_mpl_transform(ax),
        boxcoords="offset points",
        zorder=8
    )
    ax.add_artist(ab)

def read_caldate_from_zip(zip_path: pathlib.Path, tag="areas"):
    """
    Return a timezone-aware UTC datetime extracted from the <caldate>
    element of the *tag*_*.xml metadata file inside the GTWO zip.
    """
    with zipfile.ZipFile(zip_path) as zf:
        meta_xml = next(
            n for n in zf.namelist()
            if n.lower().endswith(".xml") and tag in n.lower()
        )
        xml_text = zf.read(meta_xml).decode("utf-8", errors="ignore")
    m = re.search(r"<caldate>(.*?)</caldate>", xml_text, re.IGNORECASE)
    if not m:
        return None
    # example: "Sun Jun 01 12:06:50 2025"
    dt = datetime.datetime.strptime(m.group(1), "%a %b %d %H:%M:%S %Y")
    return dt.replace(tzinfo=datetime.timezone.utc)

def get_two_gdfs(basin_tag: str, cache=DATADIR/"two_latest.zip"):
    url = "https://www.nhc.noaa.gov/xgtwo/gtwo_shapefiles.zip"
    if (not cache.exists()) or cache.stat().st_mtime < time.time() - 3*3600:
        cache.write_bytes(requests.get(url, timeout=30).content)
        issue_dt = read_caldate_from_zip(cache, tag="areas")


    with zipfile.ZipFile(cache) as zf:
        areas = [n for n in zf.namelist()
                 if n.lower().endswith(".shp") and "areas" in n.lower()]
        if not areas:
            raise RuntimeError(
                f"❌ No *areas*.shp found in TWO ZIP.  Contents: {zf.namelist()}"
            )
        shp = areas[0]
        gdf = gpd.read_file(f"zip://{cache}!{shp}")

    # ── figure out the official issue time ────────────────────────────
    raw_time = None
    for cand in ["ISSUETIME", "ISSUEDATE", "ISSUETIM", "ISSUEDT"]:
        if cand in gdf.columns and gdf.iloc[0][cand]:
            raw_time = str(gdf.iloc[0][cand])
            break

    # Fallback: pull 12 digits from the filename "..._areas_YYYYMMDDHHMM.shp"
    if raw_time is None:
        m = re.search(r"(\d{12})", shp)
        if m:
            raw_time = m.group(1)

    # If we found something, parse it; else use current UTC as last resort
    if raw_time and len(raw_time) == 12:
        issue_dt = datetime.datetime.strptime(raw_time, "%Y%m%d%H%M"
                     ).replace(tzinfo=datetime.timezone.utc)
    else:
        issue_dt = datetime.datetime.now(datetime.timezone.utc)

    # --------- everything below MUST be indented inside the function ----
    gdf = gdf[gdf["BASIN"].str.contains(basin_tag, case=False)]

    two2 = gdf.copy()
    two2["PROB"] = two2["RISK2DAY"].str.title()
    two2 = two2[two2["PROB"].isin(["Low", "Medium", "High"])]

    two7 = gdf.copy()
    two7["PROB"] = two7["RISK7DAY"].str.title()
    two7 = two7[two7["PROB"].isin(["Low", "Medium", "High"])]

    two7s = two7.copy()               # duplicate for hatching

    return two2, two7, two7s, issue_dt


def get_points(basin_tag: str, cache=DATADIR/"two_latest.zip"):
    with zipfile.ZipFile(cache) as zf:
        pts_files = [n for n in zf.namelist()
                     if n.lower().endswith(".shp") and "points" in n.lower()]
        if not pts_files:
            # return an *empty* GeoDataFrame instead of None
            return gpd.GeoDataFrame(geometry=[], crs="EPSG:4326")
        shp = pts_files[0]
        pts = gpd.read_file(f"zip://{cache}!{shp}")
    return pts[pts["BASIN"].str.contains(basin_tag, case=False)]

# ─── NEW: GET LINES ─────────────────────────────────────────────────────────
def get_lines(basin_tag: str, cache=DATADIR/"two_latest.zip"):
    """
    Read the GTWO_lines shapefile from the same TWO ZIP. Return a GeoDataFrame
    of line geometries for this basin. Each row has at least:
      - BASIN  (e.g. "Atlantic")
      - NUMBER (the disturbance ID, e.g. "01", "02", etc.)
      - RISK2DAY or RISK7DAY (as text like "Low", "Medium", "High")
      - geometry  (LineString or MultiLineString)
    """
    with zipfile.ZipFile(cache) as zf:
        lines_files = [
            n for n in zf.namelist()
            if n.lower().endswith(".shp") and "lines" in n.lower()
        ]
        if not lines_files:
            return gpd.GeoDataFrame(geometry=[], crs="EPSG:4326")
        shp = lines_files[0]
        lines_gdf = gpd.read_file(f"zip://{cache}!{shp}")
    return lines_gdf[lines_gdf["BASIN"].str.contains(basin_tag, case=False)]

# ———  PLOT LOOP  ————————————————————————————————————————————
UTC_NOW = datetime.datetime.now(datetime.timezone.utc)
for basin, label, prefix in [("AL", "Atlantic Basin", "atlantic"),
                             ("EP", "Eastern Pacific", "eastpac")]:

    two2, two7, two7s, issue_dt = get_two_gdfs(
    "Atlantic" if basin == "AL" else "Pacific"
)

    pts= get_points("Atlantic" if basin=="AL" else "Pacific")
    lines = get_lines("Atlantic" if basin == "AL" else "Pacific")

    # figure & map
    fig = plt.figure(figsize=FIGSIZE)
    ax  = plt.axes(projection=ccrs.PlateCarree())
    ax.set_facecolor(COL["ocean"])
    ax.set_extent(DEFAULT_EXTENT[basin])

    # basemap layers
    ax.add_feature(cfeature.LAND.with_scale("10m"), facecolor=COL["land"])
    ax.add_feature(cfeature.LAKES.with_scale("10m"), facecolor=COL["lake"])
    ax.add_feature(cfeature.COASTLINE.with_scale("10m"), edgecolor=COL["coast"])
    ax.add_feature(cfeature.BORDERS.with_scale("10m"),  edgecolor=COL["border"])
    ax.add_feature(cfeature.STATES.with_scale("50m"),   edgecolor=COL["coast"])

    # ── Grid: dotted 5° lines + one neat row/column of labels ────────
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

    # 1) Draw the dotted 5° grid lines (gridlabels turned OFF here)
    gl = ax.gridlines(
        draw_labels = False,
        linewidth    = 1,
        color        = "#222",
        linestyle    = ":",
        alpha        = 0.7
    )
    gl.xlocator = mticker.MultipleLocator(5)
    gl.ylocator = mticker.MultipleLocator(5)

    # 2) Helper function to halo‐draw text
    def halo(x, y, txt, ha="center", va="center"):
        ax.text(
            x, y, txt,
            transform     = ccrs.PlateCarree(),
            ha            = ha, 
            va            = va,
            fontsize      = 9,
            weight        = "bold",
            color         = "white",
            path_effects  = [ pe.Stroke(linewidth=2, foreground="black", alpha=0.8),
                              pe.Normal() ],
            zorder        = 100
        )

    # 3) Figure out the numerical extents (in PlateCarree)
    xmin, xmax, ymin, ymax = ax.get_extent(crs=ccrs.PlateCarree())

    # 4) A “neat” 5°‐spaced range that covers [lo..hi], then drop endpoints
    def neat(lo, hi, step=5):
        import math
        s = int(math.floor(lo / step) * step)
        e = int(math.ceil (hi / step) * step)
        return range(s, e + step, step)

    # Generate 5° ticks from [xmin..xmax], omit the first & last so we never label exactly on the border.
    xticks = neat(xmin, xmax, 5)[1:-1]   # e.g. for x in [-130..-80], this yields [-125,-120,...,-85]
    yticks = neat(ymin, ymax, 5)[1:-1]   # e.g. for y in [5..30], this yields [10,15,20,25]

    # ─────────────────────────────────────────────────────────────────────
    #   (A) LONGITUDE LABELS : placed just *above* the bottom edge
    # ─────────────────────────────────────────────────────────────────────
    # Instead of placing them near ymax, we put them near ymin + offset.
    y_lon = ymax - 0.60   # 0.6° above the bottom boundary

    for lon in xticks:
        # guard: only label if strictly inside (xmin, xmax)
        if lon <= xmin or lon >= xmax:
            continue
        hemi = "W" if lon < 0 else ("E" if lon > 0 else "")
        lab = f"{abs(lon):.0f}°{hemi}"
        # va="bottom" makes the bottom of the text sit at y_lon, so it hangs upward:
        halo(lon, y_lon, lab, ha="center", va="top")

    # ─────────────────────────────────────────────────────────────────────
    #   (B) LATITUDE LABELS : placed just *left* of the right‐hand edge
    # ─────────────────────────────────────────────────────────────────────
    x_lat = xmax - 0.35   # 0.35° inside from the right border

    for lat in yticks:
        # guard: only label if strictly inside (ymin, ymax)
        if lat <= ymin or lat >= ymax:
            continue
        hemi = "S" if lat < 0 else ("N" if lat > 0 else "")
        lab = f"{abs(lat):.0f}°{hemi}"
        # ha="right" makes the right of the text sit at x_lat, so it hangs to the left:
        halo(x_lat, lat, lab, ha="right", va="center")

    # (Optional) If you want to also format them exactly like Cartopy does, 
    # you can still assign the formatters in case you ever want to switch to draw_labels=True:
    gl.xformatter = LongitudeFormatter()
    gl.yformatter = LatitudeFormatter()


    # ---- TWO polygons --------------------------------------------------
    cmap2 = {"Low": COL["two2_low"], "Medium": COL["two2_med"], "High": COL["two2_high"]}
    if not two2.empty:
        two2.plot(ax=ax, facecolor=two2["PROB"].map(cmap2),
                  edgecolor="black", linewidth=0, alpha=.9, zorder=6)

    if not two7.empty:
        # black halo
        two7.plot(ax=ax, facecolor="none", edgecolor="black",
                  linewidth=5, zorder=4)
        # hatched borders
        if not two7s[two7s["PROB"]=="Low"].empty:
            two7s.query("PROB=='Low'").plot(
                ax=ax, facecolor="none", edgecolor=COL["two7_low"],
                hatch="////", linewidth=1.9, zorder=6.5)
        if not two7s[two7s["PROB"]=="Medium"].empty:
            two7s.query("PROB=='Medium'").plot(
                ax=ax, facecolor="none", edgecolor=COL["two7_med"],
                hatch="////", linewidth=1.9, zorder=6.5)
        if not two7s[two7s["PROB"]=="High"].empty:
            two7s.query("PROB=='High'").plot(
                ax=ax, facecolor="none", edgecolor=COL["two7_high"],
                hatch="////", linewidth=1.9, zorder=6.5)

# ── 5)  Draw movement arrows from GTWO_lines  ──────────────────────────
for _, row in lines.iterrows():
    geom = row.geometry
    if geom.geom_type != "LineString" or len(geom.coords) < 2:
        continue                       # skip multipart / degenerate cases

    (x0, y0), (x1, y1) = geom.coords[0], geom.coords[-1]

    risk = (row.get("RISK2DAY") or "").title()
    rgb  = {
        "Low":    (1, 1, 0),
        "Medium": (1, 0.64, 0),
        "High":   (1, 0, 0),
    }.get(risk, (1, 1, 1))

    draw_cairo_arrow(ax, x0, y0, x1, y1, rgb)



    # ── 6) Draw each disturbance “X” with dynamic color + label “<NUM>:<PROB>” ─
    for _, row in pts.iterrows():
        pt = row.geometry
        lon, lat = pt.x, pt.y

        # Pick the 2-day risk color
        risk2 = (row.get("RISK2DAY") or "").title()
        if risk2 == "Low":
            xcol = COL["X_low"]
        elif risk2 == "Medium":
            xcol = COL["X_med"]
        elif risk2 == "High":
            xcol = COL["X_high"]
        else:
            xcol = "white"

        # Plot the X marker (with black halo behind it)
        ax.scatter(
            lon, lat,
            marker="x",
            s=400,
            linewidths=14,
            color="black",
            transform=ccrs.PlateCarree(),
            zorder=8
        )
        ax.scatter(
            lon, lat,
            marker="x",
            s=300,
            linewidths=8,
            color=xcol,
            transform=ccrs.PlateCarree(),
            zorder=9
        )

        # Annotate with “<NUMBER>: <PROB2DAY>”
        num = row.get("NUMBER", "")
        pct = row.get("PROB2DAY", "")  # e.g. “05%”
        pct7 = row.get("PROB7DAY", "")  # e.g. “05%”
        label_txt = f"{num} ({pct} / {pct7}) \n  in 2/7 days"
        ax.text(
            lon + 0.5, lat + 0.5,    # slightly offset so it doesn’t sit under the X
            label_txt,
            transform=ccrs.PlateCarree(),
            color=xcol,
            weight="bold",
            fontsize=16,
            path_effects=[pe.Stroke(linewidth=5, foreground="black", alpha=0.9), pe.Normal()],
            zorder=10
        )


    # ---- Legend --------------------------------------------------------
    handles, labels = [], []

    # 2-day boxes (always include)
    handles += [
        Patch(facecolor=COL["two2_low"],  edgecolor="black"),
        Patch(facecolor=COL["two2_med"],  edgecolor="black"),
        Patch(facecolor=COL["two2_high"], edgecolor="black"),
    ]
    labels  += ["2-Day Low", "2-Day Medium", "2-Day High"]

    # 7-day hatches (always include)
    handles += [
        Patch(facecolor="none", edgecolor=COL["two7_low"],
              linestyle="--", hatch="////", linewidth=1.5),
        Patch(facecolor="none", edgecolor=COL["two7_med"],
              linestyle="--", hatch="////", linewidth=1.5),
        Patch(facecolor="none", edgecolor=COL["two7_high"],
    )]
    labels += ["7-Day Low", "7-Day Medium", "7-Day High"]


# ⬇️ Add arrow proxy to legend
    arrow_proxy = Line2D(
        [0], [0], linestyle='-', color="white", lw=2,
        marker='>', markersize=8, label="Movement",
        path_effects=[pe.Stroke(linewidth=4, foreground="black"), pe.Normal()]
)
    handles.append(arrow_proxy)
    labels.append("Movement")

    # One “X” proxy for “Current Disturbance” (generic white/black halo)
    x_proxy = Line2D(
        [0], [0],
        marker="x",
        linestyle="None",
        markersize=12,
        markeredgewidth=4,
        color="white",
        path_effects=[pe.Stroke(linewidth=8, foreground="black"), pe.Normal()]
    )
    handles.append(x_proxy)
    labels.append("Current Disturbance")

    leg = ax.legend(
        handles, labels,
        loc="lower left",
        title=r"$\bf{Genesis\ Probabilities}$",
        fontsize=10,
        title_fontsize=16,
        prop=font_manager.FontProperties(weight="bold")
    )
# Now increase only the first three labels to size 14 (for example)
    for text, label in zip(leg.get_texts(), labels):
        text.set_fontsize(12)
# ---- Local issue‐time just above legend -------------------------
    loc_tz = ZoneInfo("US/Eastern") if basin == "AL" else ZoneInfo("US/Pacific")
    local_dt = issue_dt.astimezone(loc_tz)

    stamp_txt = "\n".join([
    "Issuance:",                                         # line 1
    local_dt.strftime("%A %d %b %Y"),                    # line 2
    f"At {local_dt.strftime('%I:%M %p %Z')}"             # line 3
])

    ax.text(
        0.95, 0.02,                 # x,y in Axes fraction – tweak if needed
        stamp_txt,
        transform=ax.transAxes,
        ha="right", va="bottom",
        fontsize=14, weight="bold",
        color="white",
        path_effects=[pe.Stroke(linewidth=3, foreground="black"), pe.Normal()],
        zorder=100                 # keep above polygons
    )

    fig.tight_layout(pad=0, rect=[0.005, 0.02, 0.995, 0.93])
    # ---- Title & footer -----------------------------------------------
# leave space for labels but shrink empty margins
    fig.subplots_adjust(left=0.005,   # 3 % of figure width
                    right=0.995,
                    bottom=0.02, # 8 % → room for longitude labels + footer
                    top=0.99)   # room for title + subtitle


    fig.suptitle(f"Combined Graphical Tropical Weather Outlook for {label}",
             fontsize=20, weight="bold", y=0.94)   # y now matches new top

    subtitle = (f"Creado por Huracanes Caribe -www.HuracanesCaribe.com")
    fig.text(0.5, 0.905, subtitle,
         ha="center", va="top",
         fontsize=18)


    stamp = issue_dt.strftime("%d %b %Y %H:%M UTC")
    ax.text(0, -0.01, f"Updated {stamp}", transform=ax.transAxes,
            ha="left", va="top", fontsize=8, style="italic", weight="bold")
    ax.text(1, -0.01, "Data: NHC • Map: Huracanes Caribe",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=8, style="italic", weight="bold")

   
    # ---- Save ----------------------------------------------------------
    out_png = OUTDIR / f"{prefix}_{UTC_NOW:%Y%m%dT%H%MZ}.png"
    fig.savefig(out_png, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print("Saved", out_png)