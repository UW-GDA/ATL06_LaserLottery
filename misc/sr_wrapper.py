import geopandas as gpd
import shapely.geometry
from sliderule import icesat2, toregion
from typing import Any

def stac_to_sliderule_poly(gdf: gpd.GeoDataFrame, aoi: shapely.Geometry) -> list[dict[str, float]]:
    unified_geom = gdf.geometry.union_all().envelope
    clipped_geom = unified_geom.intersection(aoi).envelope
    
    bbox_gdf = gpd.GeoDataFrame(geometry=[clipped_geom], crs="EPSG:4326")
    
    return toregion(bbox_gdf)["poly"]

# NOTE: The 3DEP sampling in sliderule isn’t designed to sample the DEM 
# over the entire ATL06 footprint, it only samples the point geometry...
# https://github.com/SlideRuleEarth/sliderule/blob/main/datasets/usgs3dep/package/Usgs3dep1meterDemRaster.cpp
# NOTE: Still not sure about 'default' ats and cnt values.
def get_atl06(
    gf_atl06_stac: gpd.GeoDataFrame,
    window_start: str,
    window_end: str,
    aoi_geometry: shapely.Geometry,
    include_3dep: bool = False,
    include_worldcover: bool = False,
    default: bool = True,
    sliderule_params: dict[str, Any] | None = None,
) -> gpd.GeoDataFrame:
    """
    Get ATL06 data using SlideRule.

    Parameters
    ----------
    gf_atl06_stac : gpd.GeoDataFrame
        GeoDataFrame containing ICESat-2 STAC metadata.
    window_start : str
        Start time in ISO format.
    window_end : str
        End time in ISO format.
    aoi_geometry : shapely.Geometry
        Area of interest geometry to clip data.
    include_3dep : bool, default=False
        Whether to include 3DEP elevation data sampling.
    include_worldcover : bool, default=False
        Whether to include ESA WorldCover data sampling.
    default : bool, default=True
        If True, use default ATL06 parameters; if False, allow custom parameters.
        Based on https://icesat-2.gsfc.nasa.gov/sites/default/files/files/ATL06_15June_2018.pdf
    sliderule_params : dict[str, Any] | None, optional
        Custom sliderule parameters dictionary. The keys "poly", "t0", and "t1"
        will always be overwritten with the function values.

    Returns
    -------
    gpd.GeoDataFrame
        ATL06 elevation data with optional additional samples.
    """
    search_poly = stac_to_sliderule_poly(gf_atl06_stac, aoi_geometry)

    if default:
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
            "vars": ["h_mean", "latitude", "longitude", "h_sigma", "quality_summary"],
            "samples": {},
        }
    else:
        # Initialize to empty dict if no custom parameters are provided.
        if sliderule_params is None:
            sliderule_params = {}
        # Always ensure these keys are set.
        sliderule_params["poly"] = search_poly
        sliderule_params["t0"] = window_start
        sliderule_params["t1"] = window_end
        sliderule_params["geoid"] = True
        sliderule_params["vars"] = ["h_mean", "latitude", "longitude", "h_sigma", "quality_summary"]
        # Ensure there's a place to add sample data.
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
    print(sliderule_params)
    return icesat2.atl06p(sliderule_params)
