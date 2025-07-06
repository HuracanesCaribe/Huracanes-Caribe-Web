# two_plot.py – Core logic to generate GTWO plots per basin

import pathlib
import datetime
from zoneinfo import ZoneInfo
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from two_data import get_two_gdfs, get_points, get_lines
from two_map import setup_basemap, draw_two_polygons, draw_points_and_arrows, draw_legend, draw_timestamp
from config import COL, DEFAULT_EXTENT, FIGSIZE, DPI



def build_outlook(basin, label, prefix, outdir, timestamp, zip_path):

        """Main function to build and save the tropical weather outlook map for one basin."""
        tag = "Atlantic" if basin == "AL" else "Pacific"
        
        two = get_two_gdfs(tag, zip_path)
        issue_dt = timestamp
        points = get_points(tag, zip_path)
        lines  = get_lines(tag, zip_path)

        fig = plt.figure(figsize=FIGSIZE)
        ax  = plt.axes(projection=ccrs.PlateCarree())
        ax.set_extent(DEFAULT_EXTENT[basin])
        ax.set_facecolor(COL["ocean"])

        # Draw map layers, grid, and labels
        setup_basemap(ax, basin)
        draw_two_polygons(ax, two)
        draw_points_and_arrows(ax, points, lines, two)
        draw_legend(ax, basin, issue_dt)
        draw_timestamp(ax, basin, issue_dt)

        fig.subplots_adjust(left=0.005, right=0.995, bottom=0.02, top=0.995)

        # final lock to avoid resizing
        ax.set_autoscale_on(False)
        ax.set_extent(DEFAULT_EXTENT[basin], crs=ccrs.PlateCarree())
        ax.set_xlim(DEFAULT_EXTENT[basin][0], DEFAULT_EXTENT[basin][1])
        ax.set_ylim(DEFAULT_EXTENT[basin][2], DEFAULT_EXTENT[basin][3])
        ax.apply_aspect()
  
        fig.suptitle(
        f"Combined Graphical Tropical Weather Outlook for {label}",
        fontsize=20,
        weight="bold",
        y=0.90,          # ≈ 3 % below the top of the canvas
        )

        fig.text(
        0.5,
        0.87,            # ≈ 3 % under the title
        "Creado por Huracanes Caribe - www.huracanescaribe.com -",
        ha="center",
        va="top",
        fontsize=18,
        )

        # Footer
        stamp = issue_dt.strftime("%d %b %Y %H:%M UTC")
        ax.text(0, -0.01, f"Updated {stamp}", transform=ax.transAxes,
                ha="left", va="top", fontsize=8, style="italic", weight="bold")
        ax.text(1, -0.01, "Data: NHC • Map: Huracanes Caribe",
                transform=ax.transAxes, ha="right", va="top",
                fontsize=8, style="italic", weight="bold")

        # Save
        out_path = outdir / f"{prefix}_{timestamp:%Y%m%dT%H%MZ}.png"
        fig.savefig(out_path, dpi=DPI, bbox_inches="tight")
        plt.close(fig)

        return out_path
