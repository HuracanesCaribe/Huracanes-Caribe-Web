import geopandas as gpd
import zipfile

zip_path = "data/two_latest.zip"
with zipfile.ZipFile(zip_path) as zf:
    for name in zf.namelist():
        if "lines" in name and name.endswith(".shp"):
            print("Shapefile found:", name)

# Read from inside the zip
gdf = gpd.read_file(f"zip://{zip_path}!GTWO_lines_YYYYMMDDHHMM.shp")
print(gdf.columns)
print(gdf.head())
