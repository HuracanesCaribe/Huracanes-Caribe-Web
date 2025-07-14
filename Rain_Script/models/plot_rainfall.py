# plot_rainfall.py – Rainfall map with TWO style
import sys
import os
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import xarray as xr
from datetime import datetime
from scipy.ndimage import gaussian_filter

DEFAULT_EXTENT = {
    "AL": [-100, -8, 5.5, 46],
    "DOM": [-72.5, -68, 17, 20],
    "PR": [-68.5, -64.5, 16, 19],
    "MEX": [-118, -86, 14, 33],
    "CAM": [-94, -82, 6, 19],
    "TX": [-107, -93, 24, 33],
    "FL": [-88.5, -79.5, 24, 31.5],
}

COL = {
    "land": "#f0f0f0",
    "lake": "#aadaff",
    "coast": "#666666",
    "border": "#444444"
}

def setup_basemap(ax, basin):
    ax.add_feature(cfeature.LAND.with_scale("10m"), facecolor=COL["land"])
    ax.add_feature(cfeature.LAKES.with_scale("10m"), facecolor=COL["lake"], zorder=10)
    ax.add_feature(cfeature.COASTLINE.with_scale("10m"), edgecolor=COL["coast"], zorder=10)
    ax.add_feature(cfeature.BORDERS.with_scale("10m"), edgecolor=COL["border"], zorder=10)
    ax.add_feature(cfeature.STATES.with_scale("50m"), edgecolor=COL["coast"], zorder=10)

    gl = ax.gridlines(draw_labels=False, linewidth=1, color="#222", linestyle=":", alpha=0.7)
    gl.xlocator = mticker.MultipleLocator(5)
    gl.ylocator = mticker.MultipleLocator(5)
    gl.xformatter = LongitudeFormatter()
    gl.yformatter = LatitudeFormatter()

    # coordinate labels
    xmin, xmax, ymin, ymax = ax.get_extent(crs=ccrs.PlateCarree())

    def halo(x, y, txt, ha="center", va="center"):
        ax.text(
            x, y, txt,
            transform=ax.transAxes,
            ha=ha, va=va,
            fontsize=9, weight="bold", color="white",
            path_effects=[pe.Stroke(linewidth=2, foreground="black", alpha=0.8), pe.Normal()],
            zorder=100
        )

    def neat(lo, hi, step=5):
        import math
        s = int(math.floor(lo / step) * step)
        e = int(math.ceil(hi / step) * step)
        return range(s, e + step, step)

    xticks = neat(xmin, xmax, 5)[1:-1]
    yticks = neat(ymin, ymax, 5)[1:-1]

    x_range = xmax - xmin if xmax != xmin else 1
    y_range = ymax - ymin if ymax != ymin else 1

    for i, lon in enumerate(xticks):
        if i == len(xticks) - 1:
            continue
        hemi = "W" if lon < 0 else ("E" if lon > 0 else "")
        pos_x = (lon - xmin) / x_range
        halo(pos_x, 0.995, f"{abs(lon):.0f}°{hemi}", ha="center", va="top")

    for lat in yticks:
        hemi = "S" if lat < 0 else ("N" if lat > 0 else "")
        pos_y = (lat - ymin) / y_range
        halo(0.995, pos_y, f"{abs(lat):.0f}°{hemi}", ha="right", va="center")

def plot_precip_map(precip, output_path: str, title: str, extent):
# ⬇️ Dynamically scale canvas for tighter output
    w, e, s, n = extent
    aspect_ratio = (e - w) / (n - s + 0.01)
    width = min(max(5, (e - w) * 0.6), 10)
    height = width / max(aspect_ratio, 0.5)
    fig = plt.figure(figsize=(width, height), dpi=300)
    fig.subplots_adjust(left=0.005, right=0.995, bottom=0.02, top=0.91)  # tighter canvas

    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.set_facecolor("#004066")

    setup_basemap(ax, basin="AL")
    
    # Mask very low values
    precip = precip.where(precip > 0.1)

    # Custom colormap
    colormap = mcolors.ListedColormap([
        '#99FFFF', '#00eded', '#00a1f5', '#0000f5', '#00ff00', '#00c700', '#008f00',
        '#ffff00', '#e8bf00', '#ff8f00', '#ff0000', '#cc3300', '#990000', '#ff00ff', '#9933cc'
    ])
    clev = [2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58, 62]



    cf = ax.contourf(
        precip.longitude,
        precip.latitude,
        precip,
        clev,
        extend='neither',
        cmap=colormap,
        transform=ccrs.PlateCarree()
    )

    cb = plt.colorbar(cf, ax=ax, orientation="horizontal", pad=0.05, extendrect=True, ticks=clev)
    cb.set_label(r"Milimetros", size="large")

    # Annotate max
    if np.nanmax(precip.values) > 0:
        max_val = float(np.nanmax(precip.values))
        lat, lon = np.unravel_index(np.nanargmax(precip.values), precip.shape)
        max_lat = float(precip.latitude[lat])
        max_lon = float(precip.longitude[lon])

        ax.text(
            max_lon,
            max_lat,
            f"Máx: {max_val:.1f} mm",
            transform=ccrs.PlateCarree(),
            fontsize=10,
            weight="bold",
            color="white",
            path_effects=[pe.Stroke(linewidth=2, foreground="black"), pe.Normal()],
            bbox=dict(facecolor="black", alpha=0.4, boxstyle="round,pad=0.2")
        )

    ax.set_title(title, fontsize=14, loc="left", weight="bold")

        # Add timestamp in bottom right
    ax.text(
        0.995,
        0.01,
        datetime.utcnow().strftime("GFS · %Y-%m-%d %H:%M UTC"),
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=9,
        color="white",
        path_effects=[pe.Stroke(linewidth=2, foreground="black", alpha=0.8), pe.Normal()],
        zorder=100
    )

    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"🖼️ Saved: {output_path}")
