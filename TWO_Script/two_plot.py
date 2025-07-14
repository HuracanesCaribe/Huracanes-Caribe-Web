# two_plot.py – Core logic to generate GTWO plots per basin

import pathlib
import datetime
from zoneinfo import ZoneInfo
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from two_data import get_two_gdfs, get_points, get_lines
from config import COL, DEFAULT_EXTENT, FIGSIZE, DPI
from two_map import (
    setup_basemap,
    draw_two_polygons,
    draw_points,
    load_points_from_zip,
    draw_arrows,
    draw_legend,
    draw_timestamp,
    label_two_combined
)



def build_outlook(basin, label, prefix, outdir, timestamp, zip_path):
    """Main function to build and save the tropical weather outlook map for one basin."""
    tag = "Atlantic" if basin == "AL" else "Pacific"

    # Load shapefiles
    two = get_two_gdfs(tag, zip_path)
    lines = get_lines(tag, zip_path)
    points = load_points_from_zip(basin, zip_path)

    print(f"DEBUG: type(two) = {type(two)}")
    print(f"DEBUG: type(zip_path) = {type(zip_path)}")
    print(f"DEBUG: Loaded {len(points)} points")

    issue_dt = timestamp

    # Create figure
    fig = plt.figure(figsize=FIGSIZE)
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent(DEFAULT_EXTENT[basin])
    ax.set_facecolor(COL["ocean"])

    # Draw map base
    setup_basemap(ax, basin)

    if two.empty:
        ax.text(
            0.5, 0.5,
            f"Tropical cyclone formation is not expected during the next 7 days.",
            transform=ax.transAxes,
            ha="center", va="center",
            fontsize=16, weight="bold", color="black",
            bbox=dict(boxstyle="round", facecolor="white", edgecolor="black", alpha=0.8),
            zorder=100
        )
    else:
        draw_two_polygons(ax, two)
        draw_points(ax, points)
        label_two_combined(ax, two, points, basin)
        draw_arrows(ax, points, lines, two)
        draw_legend(ax, basin, issue_dt)

    draw_timestamp(ax, basin, issue_dt)

    fig.subplots_adjust(left=0.005, right=0.995, bottom=0.02, top=0.91)

    fig.suptitle(
        f"Combined Graphical Tropical Weather Outlook for {label}",
        fontsize=20,
        weight="bold",
        y=0.99,
    )

    fig.text(
        0.5,
        0.950,
        "Created by Huracanes Caribe – www.huracanescaribe.com –",
        ha="center",
        va="top",
        fontsize=14,
    )

    # Footer UTC and local time
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    stamp_utc = now_utc.strftime("%d %b %Y %H:%M UTC")
    local_tz = ZoneInfo("America/New_York" if basin == "AL" else "America/Los_Angeles")
    stamp_local = now_utc.astimezone(local_tz).strftime("%I:%M %p %Z").lstrip("0")

    ax.text(0, -0.01,
            f"Generated {stamp_utc} / {stamp_local}",
            transform=ax.transAxes,
            ha="left", va="top",
            fontsize=8, style="italic", weight="bold")

    issue_str = issue_dt.strftime("%d %b %Y %H:%M UTC")
    ax.text(1, -0.01,
            f"Data: NHC ({issue_str}) • Map: Huracanes Caribe",
            transform=ax.transAxes,
            ha="right", va="top",
            fontsize=8, style="italic", weight="bold")

    ax.set_autoscale_on(False)
    ax.set_extent(DEFAULT_EXTENT[basin], crs=ccrs.PlateCarree())
    ax.set_xlim(DEFAULT_EXTENT[basin][0], DEFAULT_EXTENT[basin][1])
    ax.set_ylim(DEFAULT_EXTENT[basin][2], DEFAULT_EXTENT[basin][3])
    ax.apply_aspect()

    out_path = outdir / f"{prefix}_{timestamp:%Y%m%dT%H%MZ}.png"
    fig.savefig(out_path, dpi=DPI, transparent=False)
    plt.close(fig)

    return out_path

