import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.patches import Polygon
import matplotlib.patheffects as PathEffects

def create_caribbean_forecast_map(title="Pronóstico Caribe", subtitle="",
                                   annotations=None, arrows=None, highlight_polygon=None,
                                   output_file=None):
    """
    Create a reusable Caribbean impact-style forecast map with annotations, arrows, and highlight areas.

    Parameters:
    - title: Main title of the map
    - subtitle: Subtext or date info
    - annotations: List of dicts {text, lon, lat, size, color}
    - arrows: List of dicts {start_lon, start_lat, end_lon, end_lat, color}
    - highlight_polygon: List of (lon, lat) tuples
    - output_file: Path to save the image
    """
    fig = plt.figure(figsize=(12, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([-85, -60, 10, 25], crs=ccrs.PlateCarree())

    # Add geographic features
    ax.add_feature(cfeature.LAND, facecolor='black')
    ax.add_feature(cfeature.OCEAN, facecolor='darkslategray')
    ax.add_feature(cfeature.BORDERS, linestyle=':', edgecolor='gray')
    ax.add_feature(cfeature.COASTLINE, edgecolor='gray')
    ax.add_feature(cfeature.LAKES, facecolor='gray')
    ax.add_feature(cfeature.RIVERS, edgecolor='gray')

    # Add highlight area
    if highlight_polygon:
        poly = Polygon(highlight_polygon, closed=True, color='limegreen', alpha=0.3, zorder=3)
        ax.add_patch(poly)

    # Add arrows
    if arrows:
        for arrow in arrows:
            ax.annotate('', xy=(arrow['end_lon'], arrow['end_lat']),
                        xytext=(arrow['start_lon'], arrow['start_lat']),
                        arrowprops=dict(facecolor=arrow.get('color', 'green'),
                                        arrowstyle='->', linewidth=2),
                        transform=ccrs.PlateCarree())

    # Add annotations
    if annotations:
        for ann in annotations:
            txt = ax.text(ann['lon'], ann['lat'], ann['text'],
                          fontsize=ann.get('size', 12),
                          color=ann.get('color', 'white'),
                          transform=ccrs.PlateCarree(),
                          weight='bold')
            txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='black')])

    # Titles
    plt.title(title, fontsize=16, weight='bold', loc='left')
    if subtitle:
        plt.text(-84, 11, subtitle, fontsize=12, color='white',
                 transform=ccrs.PlateCarree(), weight='bold')

    if output_file:
        plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='black')
    else:
        plt.show()

# Example preview
create_caribbean_forecast_map(
    title="Sábado 27 de Abril – Vaguada en superficie",
    subtitle="@HuracanesCaribe",
    annotations=[
        {"text": "Vientos\nHúmedos", "lon": -73, "lat": 20},
        {"text": "Aguaceros y Tronadas", "lon": -71, "lat": 17}
    ],
    arrows=[
        {"start_lon": -73, "start_lat": 23, "end_lon": -72, "end_lat": 20},
        {"start_lon": -70, "start_lat": 23, "end_lon": -69, "end_lat": 20},
        {"start_lon": -67, "start_lat": 23, "end_lon": -66, "end_lat": 20},
    ],
    highlight_polygon=[(-75, 17), (-65, 17), (-65, 23), (-75, 23)]
)
