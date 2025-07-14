# config.py

OUTPUT_DIR = "output"

DEFAULT_EXTENT = {
    "AL": [-100, -8, 5.5, 46],
    "DOM": [-72.5, -68, 17, 20],     # Dominican Republic
    "PR": [-68.5, -64.5, 16, 19],    # Puerto Rico
    "MEX": [-118, -86, 14, 33],      # Mexico
    "CAM": [-94, -82, 6, 19],        # Central America
    "TX": [-107, -93, 24, 33],       # Texas
    "FL": [-88.5, -79.5, 24, 31.5],  # Florida
}


# Coordinate Reference System for plotting
CRS = "EPSG:4326"