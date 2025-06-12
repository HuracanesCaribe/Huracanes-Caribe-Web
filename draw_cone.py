# draw_cone.py
import pathlib, sys, io, zipfile, requests, datetime, time
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.patches import Patch

# ----------------------------------------------------------------------
# Helper: download & cache the Tropical Weather Outlook (TWO) shapefile
# ----------------------------------------------------------------------
def get_two_gdf():
    cache  = pathlib.Path("data/two_latest.zip")
    url    = "https://www.nhc.noaa.gov/xgtwo/gtwo_shapefiles.zip"

    # Re-download if file doesn't exist OR it's older than 3 h (NHC updates 4×/day)
    if not cache.exists() or cache.stat().st_mtime < (time.time() - 3 * 3600):
        cache.write_bytes(requests.get(url, timeout=30).content)

    with zipfile.ZipFile(cache) as zf:
        shp = next(n for n in zf.namelist() if n.endswith("_areas.shp"))
        gdf = gpd.read_file(f"zip://{cache}!{shp}")

    return gdf.query("BASIN == 'AL'")      # keep only Atlantic basin


# ----------------------------------------------------------------------
# Main script starts here
# ----------------------------------------------------------------------
OUTDIR  = pathlib.Path("output")
DATADIR = pathlib.Path("data")
OUTDIR.mkdir(exist_ok=True)
DATADIR.mkdir(exist_ok=True)

STATUS_URL = "https://www.nhc.noaa.gov/CurrentStorms.json"
storm_list = requests.get(STATUS_URL, timeout=10).json()["activeStorms"]

### 1) Build the YES/NO switch
has_storm = bool(storm_list)         # True if list not empty
storm     = storm_list[0] if has_storm else None

# ----------------------------------------------------------------------
# Create the figure and basic map
# ----------------------------------------------------------------------
fig = plt.figure(figsize=(10, 8))
ax  = plt.axes(projection=ccrs.PlateCarree())

# Default map extent (whole Atlantic); will tighten later if we have a cone
ax.set_extent([-100, -5, 0, 45])     # [west, east, south, north]
ax.add_feature(cfeature.LAND,  facecolor="#f0f0e6")
ax.add_feature(cfeature.OCEAN, facecolor="#cfe8ff")
ax.add_feature(cfeature.COASTLINE, linewidth=0.6)
ax.gridlines(draw_labels=True, x_inline=False, y_inline=False)

# ----------------------------------------------------------------------
# 2) If a storm exists, download the cone & plot it
# ----------------------------------------------------------------------
if has_storm:
    cone_url    = storm["forecastTrack"]["zipFile"]
    adv, sid    = storm["forecastTrack"]["advNum"], storm["id"]
    issued_time = storm["forecastTrack"]["issuance"]

    zip_path = DATADIR / f"{sid}_{adv}.zip"
    if not zip_path.exists():
        print("Downloading cone ZIP …")
        zip_path.write_bytes(requests.get(cone_url, timeout=30).content)

    with zipfile.ZipFile(zip_path) as zf:
        shp_name = next(n for n in zf.namelist() if n.endswith(".shp"))
        gdf = gpd.read_file(f"zip://{zip_path}!{shp_name}")

    # tighten view around the cone (+5° padding)
    minx, miny, maxx, maxy = gdf.total_bounds
    pad = 5
    ax.set_extent([minx - pad, maxx + pad, miny - pad, maxy + pad])

    # plot the cone polygons
    gdf.plot(ax=ax, facecolor="none", edgecolor="red",
             linewidth=1.2, alpha=0.3, zorder=3)

    # cone-specific title
    issued = datetime.datetime.fromisoformat(
        issued_time.replace("Z", "+00:00"))
    title = f"{storm['name']} • Advisory {adv}\n{issued:%d %b %Y %H%M UTC}"
    png_name = f"{sid}_{adv}.png"

else:
    # quiet basin title + filename that includes the date
    title = "Atlantic Basin – No Active Tropical Cyclones"
    png_name = f"no_storm_{datetime.datetime.utcnow():%Y%m%dT%H%MZ}.png"
    # helpful footer so your followers know it's on purpose
    ax.text(0.5, 0.02,
            "No active tropical cyclones at this time",
            transform=ax.transAxes,
            ha="center", fontsize=9, style="italic")

ax.set_title(title, fontsize=13, weight="bold")

# ----------------------------------------------------------------------
# 3) Overlay the TWO areas (yellow/orange/red blobs)
# ----------------------------------------------------------------------
try:
    two = get_two_gdf()
    if not two.empty:
        colour = {"Low": "#ffff66", "Medium": "#ff9900", "High": "#ff0000"}
        two.plot(ax=ax,
                 facecolor=two["PROB"].map(colour).fillna("#cccccc"),
                 edgecolor="black",
                 alpha=0.4, linewidth=0.8, zorder=4)

        handles = [Patch(facecolor=v, edgecolor="black", label=k)
                   for k, v in colour.items()]
        ax.legend(handles=handles, title="Genesis probability (2-day)",
                  loc="lower left")
    else:
        print("TWO shapefile had no Atlantic areas.")
except Exception as e:
    print("TWO overlay skipped –", e)

# ----------------------------------------------------------------------
# 4) Footer branding & save
# ----------------------------------------------------------------------
ax.text(1, -0.05, "Data: NHC • Quick-look map by Huracanes Caribe",
        transform=ax.transAxes, ha="right", va="top",
        fontsize=8, style="italic")

png_path = OUTDIR / png_name
fig.savefig(png_path, dpi=150, bbox_inches="tight")
plt.close(fig)

print("Saved map →", png_path)
