# From the sexiest, newest python package 'coincident'
# https://coincident.readthedocs.io/en/latest/
import stac_geoparquet
import pystac
import pystac_client
import geopandas as gpd 
from datetime import timedelta

def get_atl06_stac(
    row: gpd.GeoSeries,
    window_days: int = 15
) -> tuple[pystac_client.ItemSearch, str, str]:
    """
    Search for ICESat-2 ATL06 data using STAC API centered around a time window.
    
    Parameters
    ----------
    row : gpd.GeoSeries
        Row containing 'start_datetime', 'end_datetime', and geometry
    window_days : int, default=15
        Number of days before and after the midpoint to search
        
    Returns
    -------
    tuple[pystac_client.ItemSearch, str, str]
        STAC API search results, window start time, window end time
    """
    stc = pystac_client.Client.open("https://cmr.earthdata.nasa.gov/stac/NSIDC_ECS")

    start_date = row['start_datetime']
    end_date = row['end_datetime']
    midpoint = start_date + (end_date - start_date) / 2

    window_start = (midpoint - timedelta(days=window_days)).strftime('%Y-%m-%dT%H:%M:%SZ')
    window_end = (midpoint + timedelta(days=window_days)).strftime('%Y-%m-%dT%H:%M:%SZ')

    items = stc.search(
        collections=["ATL06_006"],
        datetime=f"{window_start}/{window_end}",
        intersects=row.geometry
    )

    return [items, window_start, window_end]

def _filter_assets(assets: gpd.GeoDataFrame) -> dict[str, str]:
    """Remove key:None pairs from assets"""
    keep_keys = []
    for k, v in assets.items():
        if v is not None:
            keep_keys.append(k)

    return {key: assets[key] for key in keep_keys}

def to_geopandas(
    collection: pystac.item_collection.ItemCollection,
) -> gpd.GeoDataFrame:
    """
    Convert a STAC ItemCollection to a GeoDataFrame.
    This function converts a given STAC ItemCollection to a GeoDataFrame using the
    `stac_geoparquet.arrow.parse_stac_items_to_arrow` method. It also adds an additional
    column 'dayofyear' for convenience.

    Parameters
    ----------
    collection : pystac.item_collection.ItemCollection
        The STAC ItemCollection to be converted.

    Returns
    -------
    gpd.GeoDataFrame
        A GeoDataFrame containing the data from the STAC ItemCollection.

    Raises
    ------
    ValueError
        If the provided ItemCollection is empty.
    """
    # Catch if no items are passed
    if len(collection) == 0:
        message = "ItemCollection is empty, cannot convert to GeoDataFrame"
        raise ValueError(message)
    record_batch_reader = stac_geoparquet.arrow.parse_stac_items_to_arrow(collection)
    gf = gpd.GeoDataFrame.from_arrow(record_batch_reader)  # doesn't keep arrow dtypes
    # Workaround stac-geoparquet limitation https://github.com/stac-utils/stac-geoparquet/issues/82
    gf["assets"] = gf["assets"].apply(_filter_assets)
    # Additional columns for convenience
    # NOTE: these become entries under STAC properties
    gf["dayofyear"] = gf["datetime"].dt.dayofyear
    return gf