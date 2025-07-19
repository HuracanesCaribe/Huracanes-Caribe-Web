# two_map.py — arrow logic cleaned, consistent with draw_two_only.py

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
            continue  # ❌ Skip last longitude label to avoid overlap
        hemi = "W" if lon < 0 else ("E" if lon > 0 else "")
        pos_x = (lon - xmin) / x_range
        halo(pos_x, 0.995, f"{abs(lon):.0f}°{hemi}", ha="center", va="top")


    for lat in yticks:
        hemi = "S" if lat < 0 else ("N" if lat > 0 else "")
        pos_y = (lat - ymin) / y_range
        halo(0.995, pos_y, f"{abs(lat):.0f}°{hemi}", ha="right", va="center")


def draw_two_polygons(ax, two):
    cmap2 = {"Low": COL["two2_low"], "Medium": COL["two2_med"], "High": COL["two2_high"]}
    cmap7 = {"Low": COL["two7_low"], "Medium": COL["two7_med"], "High": COL["two7_high"]}
    mapped_colors = two["PROB2TEXT"].map(cmap2).fillna("white")


    if not two.empty:
        # 7-day outline first
        two.plot(ax=ax, facecolor="none", edgecolor="black", linewidth=5, zorder=5)

        # 2-day color fill
        two.plot(
            ax=ax,
            facecolor=mapped_colors,
            edgecolor="black",
            linewidth=0.5,
            alpha=0.85,
            zorder=6,
            transform=ccrs.PlateCarree()
        )

        # 7-day hatch
        for level in ["Low", "Medium", "High"]:
            subset = two[two["PROB7TEXT"] == level]
            if not subset.empty:
                # Use the same color as the label for the edgecolor
                subset.plot(
                    ax=ax,
                    facecolor="none",
                    edgecolor=cmap7[level],  # Use 2-day color for label/hatch
                    hatch="////",
                    linewidth=3,
                    zorder=7
                )

# def label_two_areas(ax, two, pts):
#     from shapely.geometry import Point

#     offset_directions = [(0, 4), (0, -4), (4, 0), (-4, 0)]  # N, S, E, W
#     used_positions = []
#     direction_idx = 0

#     xmin, xmax, ymin, ymax = ax.get_extent(crs=ccrs.PlateCarree())

#     for i, (_, row) in enumerate(two.iterrows(), start=1):
#         geom = row.geometry
#         cx, cy = geom.centroid.x, geom.centroid.y

#         # Skip labeling if there's a disturbance already inside
#         if any(geom.contains(pt.geometry) for _, pt in pts.iterrows()):
#             continue

#         area_num = row.get("AREA", "?")
#         risk2 = row.get("PROB2TEXT", "Unknown").title()
#         pct2 = row.get("PROB2DAY", "?")
#         risk7 = row.get("PROB7TEXT", "Unknown").title()
#         pct7 = row.get("PROB7DAY", "?")

#         color = {
#             "Low": COL["two2_low"],
#             "Medium": COL["two2_med"],
#             "High": COL["two2_high"]
#         }.get(risk2, "white")

#         label = f"AREA {area_num}\n{risk2}: {pct2} in 2 days\n{risk7}: {pct7} in 7 days"

#         # Try different offsets and avoid collisions with other labels
#         for attempt in range(len(offset_directions)):
#             dx, dy = offset_directions[(direction_idx + attempt) % len(offset_directions)]
#             tx, ty = cx + dx, cy + dy

#             # check bounds
#             if not (xmin + 1 < tx < xmax - 1 and ymin + 1 < ty < ymax - 1):
#                 continue

#             # check overlap with previously used positions (Euclidean distance)
#             too_close = any((abs(tx - x) < 1.5 and abs(ty - y) < 1.5) for (x, y) in used_positions)
#             if not too_close:
#                 break

#         used_positions.append((tx, ty))
#         direction_idx += 1

#         ax.text(
#             tx, ty, label,
#             transform=ccrs.PlateCarree(),
#             color=color, weight="bold", fontsize=14,
#             path_effects=[pe.Stroke(linewidth=4, foreground="black", alpha=0.9), pe.Normal()],
#             zorder=10
#         )



   
# def draw_points_and_arrows(ax, pts, lines, two):
#     import shapely.geometry as sgeom

#     # Store used label positions to avoid overlap
#     used_positions = []
#     def is_far_enough(x, y, min_dist=2.0):
#         return all(np.hypot(x - px, y - py) > min_dist for px, py in used_positions)

#     # Label offset directions (dx, dy)
#     offset_directions = [(2, 2), (2, -2), (-2, -2), (-2, 2), (3, 0), (0, 3), (-3, 0), (0, -3)]
#     direction_idx = 0

#     # disturbances
#     for _, row in pts.iterrows():
#         lon, lat = row.geometry.x, row.geometry.y
#         risk2 = (row.get("RISK2DAY") or "").title()
#         color = {"Low": COL["two2_low"], "Medium": COL["two2_med"], "High": COL["two2_high"]}.get(risk2, "white")

#         ax.scatter(lon, lat, marker="x", s=400, linewidths=14, color="black",
#                    transform=ccrs.PlateCarree(), zorder=8)
#         ax.scatter(lon, lat, marker="x", s=300, linewidths=8, color=color,
#                    transform=ccrs.PlateCarree(), zorder=9)

#         num = row.get("AREA", "?")
#         prob2 = row.get("PROB2DAY", "").strip()
#         prob7 = row.get("PROB7DAY", "").strip()

#         label = f"Disturbance {num}\n({row.get('PROB2DAY', '')} in 2 Days \n {row.get('PROB7DAY', '')}) in 7 days"

#         # Try multiple offset directions to find non-overlapping spot
#         for _ in range(len(offset_directions)):
#             dx, dy = offset_directions[direction_idx % len(offset_directions)]
#             direction_idx += 1
#             tx, ty = lon + dx, lat + dy
#             if is_far_enough(tx, ty):
#                 used_positions.append((tx, ty))
#                 ax.text(tx, ty, label, transform=ccrs.PlateCarree(),
#                         color=color, weight="bold", fontsize=16,
#                         path_effects=[pe.Stroke(linewidth=5, foreground="black", alpha=0.9), pe.Normal()],
#                         zorder=10)
#                 break

#     # arrows
#     for _, row in lines.iterrows():
#         geom = row.geometry
#         if geom.geom_type != "LineString" or len(geom.coords) < 2:
#             continue
#         x0, y0 = geom.coords[0]
#         x1, y1 = geom.coords[-1]

#         nearest_disturbance = pts.distance(sgeom.Point(x0, y0)).idxmin()
#         disturbance_pt = pts.loc[nearest_disturbance].geometry

#         if not two.empty and two.contains(disturbance_pt).any():
#             continue

#         risk = (row.get("RISK2DAY") or "").title()
#         arr_col = {
#             "Low": COL.get("arrow_low", "yellow"),
#             "Medium": COL.get("arrow_med", "orange"),
#             "High": COL.get("arrow_high", "red")
#         }.get(risk, "white")

#         arrow = ax.annotate(
#             "",
#             xy=(x1, y1), xytext=(x0, y0),
#             arrowprops=dict(
#                 arrowstyle="simple,head_length=0.25,head_width=0.20,tail_width=0.0125",
#                 color=arr_col,
#                 linewidth=5,
#                 mutation_scale=30,
#                 shrinkA=1,
#                 shrinkB=10,
#                 joinstyle="miter",
#             ),
#             transform=ccrs.PlateCarree(),
#             zorder=8
#         )
#         arrow.arrow_patch.set_path_effects([
#             pe.Stroke(linewidth=7, foreground="black", alpha=0.8),
#             pe.Normal()
#         ])

def label_two_combined(ax, two, pts):
    from shapely.geometry import Point
    import numpy as np

    offset_directions = [(2, 2), (2, -2), (-2, -2), (-2, 2), (3, 0), (0, 3), (-3, 0), (0, -3)]
    used_positions = []
    direction_idx = 0

    xmin, xmax, ymin, ymax = ax.get_extent(crs=ccrs.PlateCarree())

    def is_far_enough(x, y, min_dist=2.0):
        return all(np.hypot(x - px, y - py) > min_dist for px, py in used_positions)

    for _, row in two.iterrows():
        geom = row.geometry
        cx, cy = geom.centroid.x, geom.centroid.y
        area_num = row.get("AREA", "?")

        # Check for disturbance point inside this polygon
        area_num = int(str(row.get("AREA", "?")).lstrip("0") or -1)
        disturbance_matches = pts[pts["AREA"].astype(str).str.lstrip("0") == str(area_num)]

        disturbance = disturbance_matches.iloc[0] if not disturbance_matches.empty else None
        if disturbance is None:
            print(f"[WARN] AREA {area_num} has no disturbance match.")
        if disturbance is not None:
            print(f"[INFO] Disturbance found for AREA {area_num}")
        else:
            print(f"[INFO] Fallback label used for AREA {area_num}")


        if disturbance is not None:
            # ───── Label: Disturbance ─────
            lon, lat = disturbance.geometry.x, disturbance.geometry.y
            prob2 = (disturbance.get("PROB2DAY") or "").strip()
            prob7 = (disturbance.get("PROB7DAY") or "").strip()
            risk2 = (disturbance.get("RISK2DAY") or "").title()
            risk7 = (disturbance.get("RISK7DAY") or "").title()

            label = f"DISTURBANCE {area_num}\n{risk2}: {prob2} in 2 Days \n{risk7}: {prob7} in 7 days"
            color = {"Low": COL["two2_low"], "Medium": COL["two2_med"], "High": COL["two2_high"]}.get(risk2, "white")
            x0, y0 = lon, lat
            fontsize = 14
            lw = 5

            # 🔴 Draw X marker (outer black, inner colored)
            ax.scatter(lon, lat,
                    s=400, marker="x", linewidths=14, color="black",
                    transform=ccrs.PlateCarree(), zorder=11)

            ax.scatter(lon, lat,
                    s=300, marker="x", linewidths=8, color=color,
                    transform=ccrs.PlateCarree(), zorder=12)
        else:
            # ───── Label: AREA ─────
            risk2 = row.get("PROB2TEXT", "Unknown").title()
            pct2 = row.get("PROB2DAY", "?")
            risk7 = row.get("PROB7TEXT", "Unknown").title()
            pct7 = row.get("PROB7DAY", "?")

            label = f"AREA {area_num}\n{risk2}: {pct2} in 2 days\n{risk7}: {pct7} in 7 days"
            color = {"Low": COL["two2_low"], "Medium": COL["two2_med"], "High": COL["two2_high"]}.get(risk2, "white")
            x0, y0 = cx, cy
            fontsize = 14
            lw = 4

        # Try placing label
        for _ in range(len(offset_directions)):
            dx, dy = offset_directions[direction_idx % len(offset_directions)]
            direction_idx += 1
            tx, ty = x0 + dx, y0 + dy

            if not (xmin + 1 < tx < xmax - 1 and ymin + 1 < ty < ymax - 1):
                continue
            if is_far_enough(tx, ty):
                used_positions.append((tx, ty))
                ax.text(tx, ty, label,
                        transform=ccrs.PlateCarree(),
                        color=color, weight="bold", fontsize=fontsize,
                        path_effects=[pe.Stroke(linewidth=lw, foreground="black", alpha=0.9), pe.Normal()],
                        zorder=10)
                break

# def draw_arrows(ax, pts, lines, two):
#     import shapely.geometry as sgeom
#     from shapely.geometry import Point
#     from matplotlib.patches import FancyArrowPatch

#     for _, row in lines.iterrows():
#         geom = row.geometry

#         if geom.geom_type != "LineString" or len(geom.coords) < 2:
#             continue

#         x0, y0 = geom.coords[0]
#         nearest_disturbance = pts.distance(sgeom.Point(x0, y0)).idxmin()
#         disturbance_pt = pts.loc[nearest_disturbance].geometry

#         if not two.empty and two.contains(disturbance_pt).any():
#             continue

#         risk = (row.get("RISK2DAY") or "").title()
#         arr_col = {
#             "Low": COL.get("arrow_low", "yellow"),
#             "Medium": COL.get("arrow_med", "orange"),
#             "High": COL.get("arrow_high", "red")
#         }.get(risk, "white")

#         # 1️⃣ Draw full trajectory
#         ax.plot(*geom.xy,
#                 color=arr_col, linewidth=3.5,
#                 path_effects=[pe.Stroke(linewidth=5.5, foreground="black", alpha=1), pe.Normal()],
#                 transform=ccrs.PlateCarree(),
#                 zorder=10)

#         # 2️⃣ Overshoot arrow
#         x_last, y_last = geom.coords[-1]
#         x_prev, y_prev = geom.coords[-2]

#         # Direction vector (unit)
#         dx = x_last - x_prev
#         dy = y_last - y_prev
#         length = (dx**2 + dy**2)**0.5
#         if length == 0:
#             continue  # avoid zero division

#         ux, uy = dx / length, dy / length

#         # Extend the arrow 20% beyond the final segment length
#         overshoot_length = 1  # degrees — adjust as needed
#         x_tip = x_last + ux * overshoot_length
#         y_tip = y_last + uy * overshoot_length

#         arrow = FancyArrowPatch(
#             (x_last, y_last), (x_tip, y_tip),
#             arrowstyle="simple,head_length=10,head_width=8,tail_width=0.5",
#             color=arr_col,
#             transform=ccrs.PlateCarree(),
#             zorder=10,
#             linewidth=0
#         )
#         arrow.set_path_effects([
#             pe.Stroke(linewidth=2, foreground="black"),
#             pe.Normal()
#         ])
#         ax.add_patch(arrow)
from shapely.geometry import Point as ShapelyPoint
from matplotlib.patches import Polygon
import numpy as np
import matplotlib.patheffects as pe
import cartopy.crs as ccrs

def draw_arrows(ax, pts, lines, two, basin):
    for _, row in lines.iterrows():
        geom = row.geometry

        if geom.geom_type != "LineString" or len(geom.coords) < 2:
            continue

        x0, y0 = geom.coords[0]
        nearest_disturbance = pts.distance(ShapelyPoint(x0, y0)).idxmin()
        disturbance_pt = pts.loc[nearest_disturbance].geometry

        if not two.empty and two.contains(disturbance_pt).any():
            continue

        risk = (row.get("RISK2DAY") or "").title()
        arr_col = {
            "Low": COL.get("arrow_low", "yellow"),
            "Medium": COL.get("arrow_med", "orange"),
            "High": COL.get("arrow_high", "red")
        }.get(risk, "white")

        # 1️⃣ Draw full trajectory line
        ax.plot(*geom.xy,
                color=arr_col, linewidth=3.5,
                path_effects=[pe.Stroke(linewidth=5.5, foreground="black"), pe.Normal()],
                transform=ccrs.PlateCarree(), zorder=10)

        # 2️⃣ Construct custom triangle arrowhead
        x_last, y_last = geom.coords[-1]
        x_prev, y_prev = geom.coords[-2]
        dx, dy = x_last - x_prev, y_last - y_prev
        mag = np.hypot(dx, dy)
        if mag == 0:
            continue

        # Unit vector
        ux, uy = dx / mag, dy / mag

        # Scale overshoot by latitude to account for projection distortion
        lat_scale = np.cos(np.radians(y_last))
        arrow_len = 0.6 * lat_scale  # degrees forward
        arrow_width = 0.3 * lat_scale  # degrees wide

        # Tip of arrow
        tip = np.array([x_last + ux * arrow_len, y_last + uy * arrow_len])
        base_center = np.array([x_last, y_last])
        perp = np.array([-uy, ux])

        left = base_center + perp * arrow_width
        right = base_center - perp * arrow_width

        triangle = np.array([tip, left, right])

        # Draw filled arrowhead triangle
        patch = Polygon(triangle, closed=True, color=arr_col, zorder=11,
                        transform=ccrs.PlateCarree())
        patch.set_path_effects([
            pe.Stroke(linewidth=2, foreground="black"),
            pe.Normal()
        ])
        ax.add_patch(patch)


def draw_points(ax, pts):
    for _, row in pts.iterrows():
        lon, lat = row.geometry.x, row.geometry.y
        risk2 = (row.get("RISK2DAY") or "").title()
        color = {"Low": COL["two2_low"], "Medium": COL["two2_med"], "High": COL["two2_high"]}.get(risk2, "white")

        # Outer black X
        ax.scatter(lon, lat, marker="x", s=400, linewidths=14, color="black",
                   transform=ccrs.PlateCarree(), zorder=8)
        # Colored X on top
        ax.scatter(lon, lat, marker="x", s=300, linewidths=8, color=color,
                   transform=ccrs.PlateCarree(), zorder=11)

def draw_legend(ax, basin, issue_dt, two=None, pts=None, lines=None):
    """
    Draws two horizontal legends side by side below the canvas: genesis probabilities and disturbance types.
    NOTE: You may need to call plt.subplots_adjust(bottom=0.22) or similar in your plotting script to ensure the legends are visible.
    """
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    import matplotlib.patheffects as pe

    # Genesis Probabilities
    prob_handles = [
        Patch(facecolor="none", edgecolor="black", linewidth=1.2, label="2-Day Risk"),
        Patch(facecolor="none", edgecolor="k", hatch="////", linewidth=1.5, label="7-Day Risk"),
        Patch(facecolor=COL["two2_low"], edgecolor="black", linewidth=1.2, label="Low Chance"),
        Patch(facecolor=COL["two2_med"], edgecolor="black", linewidth=1.2, label="Medium Chance"),
        Patch(facecolor=COL["two2_high"], edgecolor="black", linewidth=1.2, label="High Chance"),
        Line2D([0], [0], marker=">", linestyle="-", markersize=12, color="black", label="Movement",
           markerfacecolor="white", markeredgecolor="black", markeredgewidth=2,
           path_effects=[pe.Stroke(linewidth=3, foreground="black"), pe.Normal()]),
    ]
    prob_labels = [h.get_label() for h in prob_handles]

    # Disturbance Types
    dist_handles = [
        Line2D([0], [0], marker="$I$", linestyle="None", markersize=14, color="deepskyblue", label="Invest", markerfacecolor="white", markeredgecolor="deepskyblue", markeredgewidth=2),
        Line2D([0], [0], marker="$P$", linestyle="None", markersize=14, color="purple", label="PTC", markerfacecolor="white", markeredgecolor="purple", markeredgewidth=2),
        Line2D([0], [0], marker="$D$", linestyle="None", markersize=14, color="gray", label="Depression", markerfacecolor="white", markeredgecolor="gray", markeredgewidth=2),
        Line2D([0], [0], marker="$S$", linestyle="None", markersize=14, color="orange", label="Storm", markerfacecolor="white", markeredgecolor="orange", markeredgewidth=2),
        Line2D([0], [0], marker="$H$", linestyle="None", markersize=14, color="red", label="Hurricane", markerfacecolor="white", markeredgecolor="red", markeredgewidth=2),
        Line2D([0], [0], marker="$M$", linestyle="None", markersize=14, color="darkred", label="Major Hurricane", markerfacecolor="white", markeredgecolor="darkred", markeredgewidth=2),
        Line2D([0], [0], marker="$R$", linestyle="None", markersize=14, color="brown", label="Post/Remnant", markerfacecolor="white", markeredgecolor="brown", markeredgewidth=2),
        Line2D([0], [0], marker="X", linestyle="None", markersize=14, color="black", label="Disturbance", markerfacecolor="white", markeredgecolor="black", markeredgewidth=2),
            ]
    dist_labels = [h.get_label() for h in dist_handles]

    # Place the two legends side by side below the axes
    leg1 = ax.legend(
        prob_handles, prob_labels,
        loc='lower left',
        bbox_to_anchor=(0.08, -0.19),  # left legend, shifted right
        ncol=3, columnspacing=1.2,  # 3 on top, 2 on bottom
        title=r"$\bf{Genesis\ Probabilities}$",
        fontsize=12, title_fontsize=14,
        frameon=True, framealpha=0.97, facecolor='white', edgecolor='none',
        borderpad=1.0, labelspacing=0.5, handlelength=1.5, handletextpad=0.7, borderaxespad=0.7
    )
    leg1.set_zorder(1000)
    for text in leg1.get_texts():
        text.set_fontsize(12)
    if leg1.get_title() is not None:
        leg1.get_title().set_fontsize(14)

    leg2 = ax.legend(
        dist_handles, dist_labels,
        loc='lower left',
        bbox_to_anchor=(0.45, -0.19),  # right legend, beside the first
        ncol=4, columnspacing=1.2,  # 5 on top, 4 on bottom
        title=r"$\bf{Disturbance\ Types}$",
        fontsize=12, title_fontsize=13,
        frameon=True, framealpha=0.97, facecolor='white', edgecolor='none',
        borderpad=1.0, labelspacing=0.5, handlelength=1.5, handletextpad=0.7, borderaxespad=0.7
    )
    leg2.set_zorder(1000)
    for text in leg2.get_texts():
        text.set_fontsize(12)
    if leg2.get_title() is not None:
        leg2.get_title().set_fontsize(14)

    # Add both legends to the axes
    ax.add_artist(leg1)
    ax.add_artist(leg2)

def draw_timestamp(ax, basin, issue_dt):
    from zoneinfo import ZoneInfo
    tz = ZoneInfo("US/Eastern" if basin == "AL" else "America/Los_Angeles")
    local_dt = issue_dt.astimezone(tz)
    print(f"DEBUG: {basin} — issue_dt: {issue_dt.isoformat()}, local_dt: {local_dt.isoformat()}")

    stamp = "\n".join([
        "Issuance:",
        local_dt.strftime("%A %d %b %Y"),
        f"At {local_dt.strftime('%I:%M %p %Z')}"
    ])
    ax.text(0.94, 0.02, stamp, transform=ax.transAxes,
            ha="right", va="bottom", fontsize=14, weight="bold",
            color="white", path_effects=[pe.Stroke(linewidth=3, foreground="black"), pe.Normal()],
            zorder=1000)

    # Set the extent and aspect of the map
    min_lon, max_lon = -130, -60  # Adjust these values as needed
    min_lat, max_lat = 20, 50  # Adjust these values as needed
    ax.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())
    ax.set_aspect('auto')  # or 'equal' for a square aspect, but 'auto' is usually best for maps


