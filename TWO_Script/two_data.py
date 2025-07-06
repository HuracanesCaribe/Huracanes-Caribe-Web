# two_data.py – Download and parse GTWO shapefiles (areas, points, lines)

import re
import time
import zipfile
import pathlib
import datetime
import requests
import geopandas as gpd
from config import DATADIR


def read_caldate_from_zip(zip_path: pathlib.Path, tag="areas") -> datetime.datetime | None:
    """Extract <caldate> timestamp from XML metadata inside ZIP."""
    with zipfile.ZipFile(zip_path) as zf:
        meta_xml = next((n for n in zf.namelist() if n.lower().endswith(".xml") and tag in n.lower()), None)
        if not meta_xml:
            return None
        xml_text = zf.read(meta_xml).decode("utf-8", errors="ignore")

    m = re.search(r"<caldate>(.*?)</caldate>", xml_text, re.IGNORECASE)
    if not m:
        return None

    dt = datetime.datetime.strptime(m.group(1), "%a %b %d %H:%M:%S %Y")
    return dt.replace(tzinfo=datetime.timezone.utc)


def download_gtwo_zip(url: str = "https://www.nhc.noaa.gov/xgtwo/gtwo_shapefiles.zip",
                      cache: pathlib.Path = DATADIR / "two_latest.zip") -> pathlib.Path:
    """Download GTWO ZIP if older than 3 hours or missing."""
    if cache.exists() and cache.stat().st_mtime > time.time() - 3 * 3600:
        return cache

    r = requests.get(url, timeout=30)
    r.raise_for_status()
    cache.write_bytes(r.content)
    return cache

def parse_issue_time_from_xml(zip_path: pathlib.Path) -> datetime.datetime:
    """Return issuance time from <caldate> inside the GTWO ZIP in UTC."""
    with zipfile.ZipFile(zip_path) as zf:
        xml_files = [n for n in zf.namelist() if n.lower().endswith(".xml")]
        for xml_name in xml_files:
            xml_content = zf.read(xml_name).decode("utf-8", errors="ignore")
            match = re.search(r"<caldate>(.*?)</caldate>", xml_content, re.IGNORECASE)
            if match:
                # parse as UTC
                dt = datetime.datetime.strptime(match.group(1), "%a %b %d %H:%M:%S %Y")
                return dt.replace(tzinfo=datetime.timezone.utc)
    # fallback
    return datetime.datetime.now(datetime.timezone.utc)

# def parse_issue_time_from_gdf(gdf: gpd.GeoDataFrame, fallback_shp: str) -> datetime.datetime:
#     """
#     Try to infer issue datetime from GDF metadata or filename.
#     Priority:
#       1. metadata columns (ISSUETIME etc)
#       2. fallback from filename
#       3. last resort: current UTC
#     """
#     for key in ["ISSUETIME", "ISSUEDATE", "ISSUETIM", "ISSUEDT"]:
#         if key in gdf.columns:
#             raw = str(gdf.iloc[0].get(key, "")).strip()
#             if len(raw) == 12 and raw.isdigit():
#                 return datetime.datetime.strptime(raw, "%Y%m%d%H%M").replace(tzinfo=datetime.timezone.utc)

#     # Fallback from filename
#     m = re.search(r"(\d{12})", fallback_shp)
#     if m:
#         return datetime.datetime.strptime(m.group(1), "%Y%m%d%H%M").replace(tzinfo=datetime.timezone.utc)

#     # truly last resort
#     return datetime.datetime.now(datetime.timezone.utc)



def get_two_gdfs(basin_tag: str, data_dir="data") -> gpd.GeoDataFrame:
    import geopandas as gpd
    import pathlib
    import datetime

    basin_tag = basin_tag.upper()
    data_path = pathlib.Path(data_dir)

    shp_files = sorted(data_path.glob("gtwo_areas_*.shp"), reverse=True)
    if not shp_files:
        raise FileNotFoundError("No gtwo_areas_*.shp found in data directory")

    shp = shp_files[0]
    gdf = gpd.read_file(shp)

    gdf = gdf[gdf["BASIN"].str.contains(basin_tag, case=False, na=False)].copy()

    gdf["PROB2DAY"] = gdf["RISK2DAY"].str.title()
    gdf["PROB7DAY"] = gdf["RISK7DAY"].str.title()

    gdf = gdf[
        gdf["PROB2DAY"].isin(["Low", "Medium", "High"]) | 
        gdf["PROB7DAY"].isin(["Low", "Medium", "High"])
    ]

    return gdf




def get_points(basin_tag: str) -> gpd.GeoDataFrame:
    zip_path = download_gtwo_zip()

    with zipfile.ZipFile(zip_path) as zf:
        shp = next((n for n in zf.namelist() if n.endswith(".shp") and "points" in n.lower()), None)
        if not shp:
            return gpd.GeoDataFrame(geometry=[], crs="EPSG:4326")

    gdf = gpd.read_file(f"zip://{zip_path}!{shp}")
   
    return gdf[gdf["BASIN"].str.contains(basin_tag, case=False)]
    


def get_lines(basin_tag: str) -> gpd.GeoDataFrame:
    zip_path = download_gtwo_zip()

    with zipfile.ZipFile(zip_path) as zf:
        shp = next((n for n in zf.namelist() if n.endswith(".shp") and "lines" in n.lower()), None)
        if not shp:
            return gpd.GeoDataFrame(geometry=[], crs="EPSG:4326")

    gdf = gpd.read_file(f"zip://{zip_path}!{shp}")
    return gdf[gdf["BASIN"].str.contains(basin_tag, case=False)]

