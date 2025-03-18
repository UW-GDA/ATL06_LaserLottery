from shapely.geometry import mapping
import numpy as np

import os
import sys
sys.path.append(os.path.abspath('/home/jehayes/gda_final/ATL06_LaserLottery/misc'))
from nlcd_plot import nlcd_labels

def sample_nlcd_for_points(gdf, da_nlcd):
    """
    Samples NLCD values at point geometries in the GeoDataFrame using vectorized nearest neighbor interpolation.
    
    Parameters:
        gdf (GeoDataFrame): A GeoDataFrame with a 'geometry' column (point geometries).
        da_nlcd (xarray.DataArray): A DataArray of NLCD values with proper spatial coordinates ('x' and 'y').
    
    Returns:
        GeoDataFrame: The original GeoDataFrame with two new columns:
                      'nlcd_value' (the interpolated integer value) and
                      'nlcd_label' (the human-readable NLCD label).
    """

    da_nlcd = da_nlcd.drop_vars("time", errors="ignore")
    da_nlcd = da_nlcd.drop_vars("spatial_ref", errors="ignore")

    # Get an xarray representation of the point coordinates.
    # This assumes that gdf has a helper method get_coordinates() that returns an xarray object.
    # If not, you can create one using:
    #   coords = xr.Dataset({
    #       "x": ("points", gdf.geometry.x.values),
    #       "y": ("points", gdf.geometry.y.values)
    #   })
    da_points = gdf.get_coordinates().to_xarray()
    
    # Interpolate the da_nlcd at all point coordinates at once using nearest-neighbor.
    samples = (
        da_nlcd
        .interp(da_points, method="nearest")
        .to_dataframe(name="nlcd_value")
        .reset_index()
    )
    
    # Map the NLCD values to their labels.
    samples["nlcd_label"] = samples["nlcd_value"].map(nlcd_labels)
    
    # Since the ordering of samples should match the order of points in gdf, 
    # assign the sampled values back to the GeoDataFrame.
    gdf = gdf.copy()
    gdf["nlcd_value"] = samples["nlcd_value"].values
    gdf["nlcd_label"] = samples["nlcd_label"].values
    
    return gdf

def sample_nlcd_for_bbox(geometry, da_nlcd):
    """
    Clips an NLCD DataArray to polygon geometry and returns
    the dominant (most occuring cell class) NLCD value and its label.
    """
    # Convert geometry to GeoJSON format for clipping
    geom = [mapping(geometry)]
    
    try:
        # Clip da_nlcd to the polygon.
        # Note: This requires da_nlcd to have spatial metadata (e.g., via rioxarray)
        da_clip = da_nlcd.rio.clip(geom, da_nlcd.rio.crs, drop=True)
    except Exception as e:
        # If clipping fails, return NaN/None.
        return np.nan, None

    # Flatten the clipped data and remove NaNs
    values = da_clip.values.flatten()
    values = values[~np.isnan(values)]
    
    if values.size == 0:
        return np.nan, None

    # Convert to integer type since NLCD categories are integers
    values_int = values.astype(int)
    
    # Get the mode (most frequent value) using np.bincount.
    # np.bincount requires non-negative ints.
    counts = np.bincount(values_int)
    dominant_value = np.argmax(counts)
    dominant_label = nlcd_labels.get(dominant_value, "Unknown")
    
    return dominant_value, dominant_label
