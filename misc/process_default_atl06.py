#!/usr/bin/env python3

import geopandas as gpd
import numpy as np
import coincident
from tqdm import tqdm
from scipy import stats

import sys
import os
sys.path.append(os.path.abspath('/home/jehayes/gda_final/ATL06_LaserLottery/misc'))
import sr_wrapper
import stac_helper


def process_default_atl06():
    gf_flights = gpd.read_file("/home/jehayes/gda_final/ATL06_LaserLottery/test_data/wesm_2021_bboxes_30d_esa.geojson")
    bias_threshold = 5

    for i in tqdm(range(len(gf_flights))):
        atl06_items = stac_helper.get_atl06_stac(gf_flights.iloc[i])
        gf_atl06_stac = stac_helper.to_geopandas(atl06_items[0].item_collection())
        gf_atl06_points = sr_wrapper.get_atl06(
            gf_atl06_stac,
            window_start = atl06_items[1],
            window_end = atl06_items[2],
            aoi_geometry= gf_flights.iloc[i].geometry,
            include_3dep=True,
            include_worldcover=True,
        )

        gf_wesm = coincident.search.wesm.load_by_fid(fids=gf_flights.iloc[[i]].fid.values).to_crs(gf_atl06_points.crs)

        # convert any list-like values to floats in '3dep.value'
        try:
            gf_atl06_points['3dep.value'] = gf_atl06_points['3dep.value'].apply(lambda x: x[0] if isinstance(x, (list, np.ndarray)) else x)
        except KeyError:
            print(f"Skipping row {i} due to no 3dep samples")
            continue
        # Create forest GDF with valid 3DEP values and forest landcover
        gf_atl06_forest = gf_atl06_points[
            (gf_atl06_points['3dep.value'].notna()) & 
            (gf_atl06_points['worldcover.value'] == 10.0)
        ]
        gf_atl06_forest = gpd.overlay(gf_atl06_forest, gf_wesm, how='intersection')
        if gf_atl06_forest.empty:
            print(f"Skipping row {i} as no samples after forest filtering")
            continue 
        gf_atl06_forest["elev_diff"] = gf_atl06_forest["h_mean"] - gf_atl06_forest["3dep.value"]

        # remove "bias" cycles
        #median_diff_by_cycle = gf_atl06_forest.groupby("cycle")["elev_diff"].median()
        #biased_cycles = median_diff_by_cycle[median_diff_by_cycle.abs() > bias_threshold].index
        #gf_atl06_forest_unbiased = gf_atl06_forest[~gf_atl06_forest["cycle"].isin(biased_cycles)]
        gf_atl06_forest_unbiased = gf_atl06_forest

        elev_diff = gf_atl06_forest_unbiased['elev_diff']
        gf_wesm.at[0, "mean_diff"] = elev_diff.mean()
        gf_wesm.at[0, "med_diff"] = elev_diff.median()
        gf_wesm.at[0, "std_diff"] = elev_diff.std()
        gf_wesm.at[0, "nmad_diff"] = stats.median_abs_deviation(elev_diff, scale="normal")
        gf_wesm.at[0, "n_points"] = len(gf_atl06_forest_unbiased)

        med_cm = int(round(np.nanmedian(elev_diff) * 100))
        fn_wesm = f"{gf_wesm.iloc[0].workunit}_{len(gf_atl06_forest_unbiased)}_count_{med_cm}_med.parquet"
        fn_atl06 = f"{gf_wesm.iloc[0].workunit}_default_{len(gf_atl06_forest_unbiased)}_count_{med_cm}_med.parquet"
        gf_wesm.to_parquet(f"/home/jehayes/gda_final/ATL06_LaserLottery/data/wesm/{fn_wesm}")

        # drop cols with list dtypes
        cols_to_drop = [col for col in gf_atl06_forest_unbiased.columns
                        if (col.startswith('worldcover') or col.startswith('3dep')) and col != '3dep.value']
        gf_atl06_forest_unbiased.drop(columns=cols_to_drop, inplace=True)
        gf_atl06_forest_unbiased.to_parquet(f"/home/jehayes/gda_final/ATL06_LaserLottery/data/atl06_default/{fn_atl06}")
        print(f"processing complete fpr {gf_wesm.iloc[0].workunit}")

if __name__ == "__main__":
    process_default_atl06()
