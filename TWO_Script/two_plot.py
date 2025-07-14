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
    draw_arrows,
    draw_legend,
    draw_timestamp,
    label_two_combined
)



def build_outlook(basin, label, prefix, outdir, timestamp, zip_path):

        """Main function to build and save the tropical weather outlook map for one basin."""
        tag = "Atlantic" if basin == "AL" else "Pacific"
        
        two = get_two_gdfs(tag, zip_path)
        print(f"DEBUG: type(two) = {type(two)}")
        print(f"DEBUG: type(zip_path) = {type(zip_path)}")
        issue_dt = timestamp
        points = draw_points_data(tag, zip_path)
        plot_points(ax, points)
        lines  = get_lines(tag, zip_path)
        fig = plt.figure(figsize=FIGSIZE)
        ax  = plt.axes(projection=ccrs.PlateCarree())
        ax.set_extent(DEFAULT_EXTENT[basin])
        ax.set_facecolor(COL["ocean"])

        # Draw map layers, grid, and labels
        setup_basemap(ax, basin)

        # ➕ If no TWO areas exist, show fallback message and skip rest of plotting
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
        # Only draw these if TWO areas are present
                draw_two_polygons(ax, two)
                draw_points(ax, points)
                label_two_combined(ax, two, points, basin)

                print("\n🔍 DEBUG: AREA values in `two`:")
                print(sorted(set(two["AREA"].astype(str).str.lstrip("0"))))

                print("\n🔍 DEBUG: AREA values in `pts`:")
                print(sorted(set(points["AREA"].astype(str).str.lstrip("0"))))

                draw_arrows(ax, points, lines, two)
                draw_legend(ax, basin, issue_dt)
                draw_timestamp(ax, basin, issue_dt)

        draw_timestamp(ax, basin, issue_dt)

        fig.subplots_adjust(left=0.005, right=0.995, bottom=0.02, top=0.91)

        # # final lock to avoid resizing
        # ax.set_extent(DEFAULT_EXTENT[basin], crs=ccrs.PlateCarree())
        # ax.set_autoscale_on(False)
        # ax.apply_aspect()
  
        fig.suptitle(
        f"Combined Graphical Tropical Weather Outlook for {label}",
        fontsize=20,
        weight="bold",
        y=0.99,  # top of the figure
        )


        fig.text(
        0.5,
        0.950,  # just under suptitle (adjust if needed)
        "Created by Huracanes Caribe – www.huracanescaribe.com –",
        ha="center",
        va="top",
        fontsize=14,  # slightly smaller for hierarchy
        )



        # Footer
        from datetime import datetime, timezone
        from zoneinfo import ZoneInfo

        # Use current UTC time
        now_utc = datetime.now(timezone.utc)
        stamp_utc = now_utc.strftime("%d %b %Y %H:%M UTC")

        # Determine local time zone by basin
        local_tz = ZoneInfo("America/New_York") if basin == "AL" else ZoneInfo("America/Los_Angeles")
        now_local = now_utc.astimezone(local_tz)

        # Format local time as 12-hour clock with AM/PM, no date
        stamp_local = now_local.strftime("%I:%M %p %Z").lstrip("0")  # e.g., "4:45 PM EDT"

        # Footer left: runtime UTC + local time
        ax.text(0, -0.01,
                f"Generated {stamp_utc} / {stamp_local}",
                transform=ax.transAxes,
                ha="left", va="top",
                fontsize=8, style="italic", weight="bold")

        # Footer right: GTWO issue time (from XML) in UTC
        issue_str = issue_dt.strftime("%d %b %Y %H:%M UTC")
        ax.text(1, -0.01,
                f"Data: NHC ({issue_str}) • Map: Huracanes Caribe",
                transform=ax.transAxes,
                ha="right", va="top",
                fontsize=8, style="italic", weight="bold")

        # 🔒 FINAL LOCK to prevent shrinking after plotting
        ax.set_autoscale_on(False)
        ax.set_extent(DEFAULT_EXTENT[basin], crs=ccrs.PlateCarree())
        ax.set_xlim(DEFAULT_EXTENT[basin][0], DEFAULT_EXTENT[basin][1])
        ax.set_ylim(DEFAULT_EXTENT[basin][2], DEFAULT_EXTENT[basin][3])
        ax.apply_aspect()

        # Save
        out_path = outdir / f"{prefix}_{timestamp:%Y%m%dT%H%MZ}.png"
        fig.savefig(out_path, dpi=DPI, transparent=False)
        plt.close(fig)

        return out_path
