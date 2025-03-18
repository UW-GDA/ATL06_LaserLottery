#!/usr/bin/env python3
import geopandas as gpd
import coincident
from shapely.geometry import box
from tqdm import tqdm
import xarray as xr
import rioxarray as rxr
from sliderule import icesat2
import numpy as np
import sys
import os
import itertools

# Add misc directory to path
sys.path.append(os.path.abspath('/home/jehayes/gda_final/ATL06_LaserLottery/misc'))
import sr_wrapper
import stac_helper

# Define a function to create a 40m x 40m square centered on a point (buffer of 20m)
def create_square(pt, half_side=20):
    return box(pt.x - half_side, pt.y - half_side, pt.x + half_side, pt.y + half_side)

def main():
    # Read flight boundaries and select AOI
    gf_flights = gpd.read_file("/home/jehayes/gda_final/ATL06_LaserLottery/test_data/wesm_2021_bboxes_30d_esa.geojson")
    aoi = gf_flights.iloc[[0]]
    gf_wesm = coincident.search.wesm.load_by_fid(fids=aoi.fid.values).to_crs(32610)

    # Get ATL06 STAC items and convert to GeoDataFrame
    atl06_items = stac_helper.get_atl06_stac(aoi.iloc[0], window_days=12)
    gf_atl06_stac = stac_helper.to_geopandas(atl06_items[0].item_collection())

    # Open the DEM dataset once; note that we set the CRS to EPSG:32610
    ds_dem = xr.open_dataset("/mnt/c/Users/JackE/uw/courses/wint25/gda/final_data/dem_10x_itrf.tif", 
                             engine="rasterio").squeeze().rename({'band_data': 'elevation'}).rio.write_crs(32610)

    # Define grid search values for sliderule parameters (feel free to adjust these)
    len_values = [30.0, 40.0]      # 'len': length parameter in meters
    res_values = [10.0, 20.0]      # 'res': resolution parameter in meters
    cnt_values = [5, 10]           # 'cnt': count parameter
    ats_values = [5.0, 10.0]       # 'ats': ats parameter

    # Loop over every combination of sliderule parameters
    for len_val, res_val, cnt_val, ats_val in itertools.product(len_values, res_values, cnt_values, ats_values):

        #print(f"Proocessing with len={len_val}, res={res_val}, cnt={cnt_val}, ats={ats_val}")

        # Build sliderule parameters dictionary for this iteration
        sliderule_params = {
            "srt": icesat2.SRT_LAND,
            "cnf": icesat2.CNF_SURFACE_HIGH,
            "ats": ats_val,
            "cnt": cnt_val,
            "len": len_val,
            "res": res_val,
            "geoid": True,
            "vars": ["h_mean", "latitude", "longitude", "h_sigma", "quality_summary"],
            "samples": {},
        }

        # Process ATL06 data with the current sliderule parameters
        gf_atl06_points = sr_wrapper.get_atl06(
            gf_atl06_stac,
            window_start=atl06_items[1],
            window_end=atl06_items[2],
            aoi_geometry=aoi.iloc[0].geometry,
            sliderule_params=sliderule_params
        )

        # Reproject ATL06 points to match the DEM CRS
        gf_atl06_points_utm = gf_atl06_points.to_crs(ds_dem.rio.crs)
        gf_atl06_points_utm = gf_atl06_points_utm.clip(gf_wesm.iloc[0].geometry)

        # Create a new column 'bbox' with 40m x 40m square geometries centered on each point
        half_side = len_val / 2
        gf_atl06_points_utm['bbox'] = gf_atl06_points_utm.geometry.apply(create_square,
                                                                         half_side=half_side)

        # List to hold average DEM elevation values for each bounding box
        dem_elev_avg = []

        # Loop over each bounding box in the geodataframe and compute the mean DEM elevation
        for geom in tqdm(gf_atl06_points_utm['bbox'], desc=f"Processing len={len_val}, res={res_val}, cnt={cnt_val}, ats={ats_val}"):
            minx, miny, maxx, maxy = geom.bounds

            # Subset the DEM elevation data to the bounds of the square
            da_subset = ds_dem.elevation.where(
                (ds_dem.x >= minx) & (ds_dem.x <= maxx) &
                (ds_dem.y >= miny) & (ds_dem.y <= maxy),
                drop=True
            )

            # Calculate the mean elevation using np.nanmean to ignore NaNs
            avg_elev = np.nanmean(da_subset.values)
            dem_elev_avg.append(avg_elev)

        gf_atl06_points_utm['dem_elev'] = dem_elev_avg
        gf_atl06_points_utm['elev_diff'] = gf_atl06_points_utm['h_mean'] - gf_atl06_points_utm['dem_elev']

        out_filename = f"/home/jehayes/gda_final/ATL06_LaserLottery/data/OR_McKenzieRiver_1_2021_atl06/atl06_{len_val}_{res_val}_{cnt_val}_{ats_val}.parquet"
        gf_atl06_points_utm


if __name__ == '__main__':
    main()
