#!/bin/bash
# Set target directories
TILE_DIR="/mnt/c/Users/JackE/uw/courses/wint25/gda/final_data/usgs_tiles"
MOSAIC_DIR="/mnt/c/Users/JackE/uw/courses/wint25/gda/final_data"
LINKS_URL="https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/OPR/Projects/OR_McKenzieRiver_2021_B21/OR_McKenzieRiver_1_2021/0_file_download_links.txt"
LIST_FILE="tile_list.txt"
VRT_FILE="mosaic.vrt"
DEM_FILE="$MOSAIC_DIR/dem.tif"
DEM_10X_FILE="$MOSAIC_DIR/dem_10x.tif"

# Download the text file with the download links
wget -O tile_links.txt "$LINKS_URL"

echo "Downloading all tiffs from $LINKS_URL..."
# Loop through each URL in the text file and download the TIFF files
while read -r url; do
    # Skip empty lines
    [ -z "$url" ] && continue
    echo "Downloading: $url"
    wget -P "$TILE_DIR" "$url"
done < tile_links.txt

echo "Creating file list of TIFF files from $TILE_DIR..."
find "$TILE_DIR" -type f -name "*.tif" > "$LIST_FILE"

echo "Building virtual mosaic (VRT) from file list..."
gdalbuildvrt -input_file_list "$LIST_FILE" "$VRT_FILE"

echo "Translating VRT to a single mosaic TIFF..."
gdal_translate "$VRT_FILE" "$DEM_FILE" -co COMPRESS=LZW -co TILED=YES -co BIGTIFF=IF_SAFER

echo "Creating coarser 10x10m product..."
gdal_translate -co COMPRESS=LZW -co TILED=YES -co BIGTIFF=IF_SAFER -outsize 10% 10% "$DEM_FILE" "$DEM_10X_FILE"

echo "Cleaning up temporary files..."
rm "$LIST_FILE" "$VRT_FILE"

echo "Mosaic and coarsening completed."
echo "Mosaic: $DEM_FILE"
echo "Coarser product: $DEM_10X_FILE"
