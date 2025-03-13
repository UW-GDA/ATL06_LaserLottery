import geopandas as gpd
import shapely.geometry
from sliderule import icesat2, toregion

def stac_to_sliderule_poly(gdf: gpd.GeoDataFrame, aoi: shapely.Geometry) -> list[dict[str, float]]:
    unified_geom = gdf.geometry.union_all().envelope
    clipped_geom = unified_geom.intersection(aoi).envelope
    
    bbox_gdf = gpd.GeoDataFrame(geometry=[clipped_geom], crs="EPSG:4326")
    
    return toregion(bbox_gdf)["poly"]

# NOTE: The 3DEP sampling in sliderule isn’t designed to sample the DEM 
# over the entire ATL06 footprint, it only samples the point geometry...
# https://github.com/SlideRuleEarth/sliderule/blob/main/datasets/usgs3dep/package/Usgs3dep1meterDemRaster.cpp
def get_atl06_default(
    gf_atl06_stac: gpd.GeoDataFrame,
    window_start: str,
    window_end: str,
    aoi_geometry: shapely.Geometry,
    include_3dep: bool = False,
    include_worldcover: bool = False,
) -> gpd.GeoDataFrame:
    """
    Get ATL06 data using SlideRule with default parameters.
    
    Parameters
    ----------
    gf_atl06_stac : gpd.GeoDataFrame
        GeoDataFrame containing ICESat-2 STAC metadata
    window_start : str
        Start time in ISO format
    window_end : str
        End time in ISO format
    aoi_geometry : shapely.Geometry
        Area of interest geometry to clip data
    include_3dep : bool, default=False
        Whether to include 3DEP elevation data sampling
    include_worldcover : bool, default=False
        Whether to include ESA worldcover data sampling
        
    Returns
    -------
    gpd.GeoDataFrame
        ATL06 elevation data with optional 3DEP samples
    """
    search_poly = stac_to_sliderule_poly(gf_atl06_stac, aoi_geometry)

    sliderule_params = {
        "poly": search_poly,
        "t0": window_start,
        "t1": window_end,
        "srt": icesat2.SRT_LAND,
        "cnf": icesat2.CNF_SURFACE_HIGH,
        "ats": 10.0,
        "cnt": 10,
        "len": 40.0,
        "res": 20.0,
        "geoid": True,
        "vars": ["h_mean", "latitude", "longitude", "h_sigma", "quality_summary"]
    }

    if "samples" not in sliderule_params:
        sliderule_params["samples"] = {}

    if include_3dep:
        sliderule_params["samples"].update({
            "3dep": {"asset": "usgs3dep-1meter-dem"}
        })

    if include_worldcover:
        sliderule_params["samples"].update({
            "worldcover": {"asset": "esa-worldcover-10meter"}
        })

    return icesat2.atl06p(sliderule_params)
