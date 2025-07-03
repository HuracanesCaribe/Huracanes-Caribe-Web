# two_map.py – updated with 2-day color + 7-day hatch + 7-day outline

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.ticker as mticker
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from shapely.ops import nearest_points
import shapely

from config import COL


def setup_basemap(ax, basin):
    ax.add_feature(cfeature.LAND.with_scale("10m"), facecolor=COL["land"])
    ax.add_feature(cfeature.LAKES.with_scale("10m"), facecolor=COL["lake"])
    ax.add_feature(cfeature.COASTLINE.with_scale("10m"), edgecolor=COL["coast"])
    ax.add_feature(cfeature.BORDERS.with_scale("10m"),  edgecolor=COL["border"])
    ax.add_feature(cfeature.STATES.with_scale("50m"),   edgecolor=COL["coast"])

    gl = ax.gridlines(draw_labels=False, linewidth=1, color="#222",
                      linestyle=":", alpha=0.7)
    gl.xlocator = mticker.MultipleLocator(5)
    gl.ylocator = mticker.MultipleLocator(5)
    gl.xformatter = LongitudeFormatter()
    gl.yformatter = LatitudeFormatter()

    xmin, xmax, ymin, ymax = ax.get_extent(crs=ccrs.PlateCarree())
        
    def halo(x, y, txt, ha="center", va="center"):
        ax.text(
            x, y, txt,
            transform=ax.transAxes,
            ha=ha, va=va,
            fontsize=9, weight="bold",
            color="white",
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

    # longitude labels positioned at their actual locations
    x_range = xmax - xmin if xmax != xmin else 1
    for lon in xticks:
        hemi = "W" if lon < 0 else ("E" if lon > 0 else "")
        pos_x = (lon - xmin) / x_range
        halo(pos_x, 0.995, f"{abs(lon):.0f}°{hemi}", ha="center", va="top")

    # latitude labels positioned at their actual locations
    y_range = ymax - ymin if ymax != ymin else 1
    for lat in yticks:
        hemi = "S" if lat < 0 else ("N" if lat > 0 else "")
        pos_y = (lat - ymin) / y_range
        halo(0.995, pos_y, f"{abs(lat):.0f}°{hemi}", ha="right", va="center")


def draw_two_polygons(ax, two):
    cmap2 = {"Low": COL["two2_low"], "Medium": COL["two2_med"], "High": COL["two2_high"]}
    cmap7 = {"Low": COL["two7_low"], "Medium": COL["two7_med"], "High": COL["two7_high"]}

    if not two.empty:
        # 7-day strong black outline FIRST
        two.plot(
            ax=ax,
            facecolor="none",
            edgecolor="black",
            linewidth=5,
            zorder=5
        )
        
        # 2-day color fill
        two.plot(
            ax=ax,
            facecolor=two["PROB2DAY"].map(cmap2),
            edgecolor="black",
            linewidth=0.5,
            alpha=0.9,
            zorder=6,
            transform=ccrs.PlateCarree()
        )

        # 7-day hatch
        for level in ["Low", "Medium", "High"]:
            subset = two[two["PROB7DAY"] == level]
            if not subset.empty:
                subset.plot(
                    ax=ax,
                    facecolor="none",
                    edgecolor=cmap7[level],
                    hatch="////",
                    linewidth=3,
                    zorder=7
                )



def draw_cairo_arrow(ax, x0, y0, x1, y1, rgb):
    """Draw a movement arrow from (x0, y0) toward (x1, y1)."""
    arrowprops = dict(
        arrowstyle="-|>",
        color=rgb,
        linewidth=3,
        mutation_scale=15,
        shrinkA=0,
        shrinkB=0,
        path_effects=[
            pe.Stroke(linewidth=5, foreground="black"),
            pe.Normal(),
        ],
    )

    ax.annotate(
        "",
        xy=(x1, y1),
        xytext=(x0, y0),
        xycoords=ccrs.PlateCarree(),
        textcoords=ccrs.PlateCarree(),
        arrowprops=arrowprops,
        zorder=8,
    )


def draw_points_and_arrows(ax, pts, lines, two):
    for _, row in lines.iterrows():
        geom = row.geometry
        if geom.geom_type != "LineString" or len(geom.coords) < 2:
            continue
        x0, y0 = geom.coords[-1]
        if not two.empty:
            # use nearest point on the first 7-day polygon as arrow target
            polygon = two.geometry.iloc[0]
            nearest = nearest_points(polygon.boundary, shapely.Point(x0, y0))[0]
            x1, y1 = nearest.x, nearest.y
        else:
            x1, y1 = x0, y0
        risk = (row.get("RISK2DAY") or "").title()
        rgb = {"Low": (1, 1, 0), "Medium": (1, 0.64, 0), "High": (1, 0, 0)}.get(risk, (1, 1, 1))
        draw_cairo_arrow(ax, x0, y0, x1, y1, rgb)

    for _, row in pts.iterrows():
        lon, lat = row.geometry.x, row.geometry.y
        risk2 = (row.get("RISK2DAY") or "").title()
        color = {"Low": COL["two2_low"], "Medium": COL["two2_med"], "High": COL["two2_high"]}.get(risk2, "white")
        ax.scatter(lon, lat, marker="x", s=400, linewidths=14, color="black",
                   transform=ccrs.PlateCarree(), zorder=8)
        ax.scatter(lon, lat, marker="x", s=300, linewidths=8, color=color,
                   transform=ccrs.PlateCarree(), zorder=9)
        label = f"{row.get('NUMBER', '')} ({row.get('PROB2DAY', '')} / {row.get('PROB7DAY', '')})\n  in 2/7 days"
        ax.text(lon + 0.5, lat + 0.5, label, transform=ccrs.PlateCarree(),
                color=color, weight="bold", fontsize=16,
                path_effects=[pe.Stroke(linewidth=5, foreground="black", alpha=0.9), pe.Normal()],
                zorder=10)


def draw_legend(ax, basin, issue_dt):
    handles = [
        Patch(facecolor=COL["two2_low"], edgecolor="black"),
        Patch(facecolor=COL["two2_med"], edgecolor="black"),
        Patch(facecolor=COL["two2_high"], edgecolor="black"),
        Patch(facecolor="none", edgecolor=COL["two7_low"], hatch="////", linewidth=1.5),
        Patch(facecolor="none", edgecolor=COL["two7_med"], hatch="////", linewidth=1.5),
        Patch(facecolor="none", edgecolor=COL["two7_high"], hatch="////", linewidth=1.5),
        Line2D([0], [0], linestyle='-', color="white", lw=2,
               marker='>', markersize=8,
               path_effects=[pe.Stroke(linewidth=4, foreground="black"), pe.Normal()]),
        Line2D([0], [0], marker="x", linestyle="None", markersize=12,
               markeredgewidth=4, color="white",
               path_effects=[pe.Stroke(linewidth=8, foreground="black"), pe.Normal()])
    ]
    labels = [
        "2-Day Low", "2-Day Medium", "2-Day High",
        "7-Day Low", "7-Day Medium", "7-Day High",
        "Movement", "Current Disturbance"
    ]
    leg = ax.legend(handles, labels, loc="lower left",
                    title=r"$\bf{Genesis\ Probabilities}$",
                    fontsize=10, title_fontsize=16)
    for text in leg.get_texts():
        text.set_fontsize(12)


def draw_timestamp(ax, basin, issue_dt):
    from zoneinfo import ZoneInfo
    tz = ZoneInfo("US/Eastern" if basin == "AL" else "US/Pacific")
    local_dt = issue_dt.astimezone(tz)
    stamp = "\n".join([
        "Issuance:",
        local_dt.strftime("%A %d %b %Y"),
        f"At {local_dt.strftime('%I:%M %p %Z')}"
    ])
    ax.text(0.94, 0.02, stamp, transform=ax.transAxes,
            ha="right", va="bottom", fontsize=14, weight="bold",
            color="white", path_effects=[pe.Stroke(linewidth=3, foreground="black"), pe.Normal()],
            zorder=100)
