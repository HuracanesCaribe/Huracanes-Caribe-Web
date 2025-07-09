# two_data.py – Download and parse GTWO shapefiles (areas, points, lines)

import re
import time
import zipfile
import pathlib
import datetime
import requests
import geopandas as gpd
from config import DATADIR
import shutil


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


def download_gtwo_zip(
    url: str = "https://www.nhc.noaa.gov/xgtwo/gtwo_shapefiles.zip"
) -> pathlib.Path:
    """
    Download GTWO ZIP to data_archive/YYYY-MM-DD/ with timestamp
    based on the <caldate> found in the XML inside the zip.
    """
    # download to a truly temp location, like /tmp
    tmp_path = pathlib.Path("/tmp/two_latest.zip")

    # always download fresh
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    tmp_path.write_bytes(r.content)

    # parse caldate
    with zipfile.ZipFile(tmp_path) as zf:
        xml_name = next(n for n in zf.namelist() if n.lower().endswith(".xml"))
        xml_content = zf.read(xml_name).decode("utf-8", errors="ignore")
        match = re.search(r"<caldate>(.*?)</caldate>", xml_content, re.IGNORECASE)
        if not match:
            raise ValueError("No <caldate> found in XML")
        issue_dt = datetime.datetime.strptime(
            match.group(1), "%a %b %d %H:%M:%S %Y"
        ).replace(tzinfo=datetime.timezone.utc)

    today_str = issue_dt.strftime("%Y-%m-%d")
    timestamp_str = issue_dt.strftime("%Y%m%dT%H%MZ")

    archive_dir = DATADIR.parent / "data_archive" / today_str
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = archive_dir / f"gtwo_shapefiles_{timestamp_str}.zip"

    shutil.move(tmp_path, archive_path)

    print(f"✅ GTWO: {archive_path.name}")

    return archive_path



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

def get_two_gdfs(basin_tag: str, zip_path: pathlib.Path) -> gpd.GeoDataFrame:
    """Load the GTWO areas shapefile for a basin directly from the ZIP archive."""

    basin_tag = basin_tag.upper()
    with zipfile.ZipFile(zip_path) as zf:
        # find the .shp file with "gtwo_areas" in its name (timestamp varies)
        shp_name = next(
            n for n in zf.namelist()
            if n.lower().endswith(".shp") and "gtwo_areas" in n.lower()
        )

    # then geopandas can read:
    gdf = gpd.read_file(f"zip://{zip_path}!{shp_name}")
    gdf = gdf[gdf["BASIN"].str.contains(basin_tag, case=False, na=False)].copy()

    gdf["PROB2DAY"] = gdf["RISK2DAY"].str.title()
    gdf["PROB7DAY"] = gdf["RISK7DAY"].str.title()

    gdf = gdf[
        gdf["PROB2DAY"].isin(["Low", "Medium", "High"]) | 
        gdf["PROB7DAY"].isin(["Low", "Medium", "High"])
    ]

    return gdf




def get_points(basin_tag: str, zip_path: pathlib.Path) -> gpd.GeoDataFrame:
    """Load the GTWO points shapefile for a basin directly from the ZIP archive."""
    with zipfile.ZipFile(zip_path) as zf:
        shp = next((n for n in zf.namelist() if n.endswith(".shp") and "points" in n.lower()), None)
        if not shp:
            return gpd.GeoDataFrame(geometry=[], crs="EPSG:4326")

    gdf = gpd.read_file(f"zip://{zip_path}!{shp}")
   
    return gdf[gdf["BASIN"].str.contains(basin_tag, case=False)]
    


def get_lines(basin_tag: str, zip_path: pathlib.Path) -> gpd.GeoDataFrame:

    with zipfile.ZipFile(zip_path) as zf:
        shp = next((n for n in zf.namelist() if n.endswith(".shp") and "lines" in n.lower()), None)
        if not shp:
            return gpd.GeoDataFrame(geometry=[], crs="EPSG:4326")

    gdf = gpd.read_file(f"zip://{zip_path}!{shp}")
    return gdf[gdf["BASIN"].str.contains(basin_tag, case=False)]

