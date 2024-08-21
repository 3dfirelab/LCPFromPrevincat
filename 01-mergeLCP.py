import rasterio
from rasterio.merge import merge
import glob
import os
import sys 
import numpy as np 
import shutil 
import os 

# Directory where the raster files are located
input_folder = "./TIF/"

# Output merged raster
output_file = "merged.tif"

# Search criteria to find the raster files in the directory
search_criteria = "*.tif"
q = os.path.join(input_folder, search_criteria)

# List to store the opened raster datasets
src_files_to_mosaic = []

fileid = [25,26,35,36,37,51]
# Loop through and open each raster file, then add it to the list
file2rm = glob.glob(input_folder+'*_masked.tif')
if len(file2rm)>0:
    for fp in file2rm:
        os.remove(fp)

filenames = glob.glob(q)
for fp in filenames:
    
    if int(fp.split('ZHR_')[1].split('.')[0]) not in fileid: continue
    print(fp) 
    src = rasterio.open(fp)
    profile = src.profile
    
    #set -9999 as no data for all band
    mask= np.where(src.read(1)==-9999,0,1)
    
    mapfuel = np.where(mask==0, -9999, src.read(4))
    mapCanopyCover = np.where(mask==0, -9999, src.read(5))
    mapStandHeight = np.where(mask==0, -9999, src.read(6))
    mapCanopyBaseHeight = np.where(mask==0, -9999, src.read(7))
    mapCanopyBulkDensity = np.where(mask==0, -9999, src.read(8))

    #Write to a  file
    with rasterio.open(fp.replace('.tif','_masked.tif'), 'w', **profile) as dst:
        dst.write(src.read(1), 1)  # Writing modified data to the first band
        dst.set_band_description(1, src.descriptions[0])

        dst.write(src.read(2), 2)  # Writing modified data to the first band
        dst.set_band_description(2, src.descriptions[1])
        
        dst.write(src.read(3), 3)  # Writing modified data to the first band
        dst.set_band_description(3, src.descriptions[2])
        
        dst.write(mapfuel, 4)  # Writing modified data to the first band
        dst.set_band_description(4, src.descriptions[3])
        
        dst.write(mapCanopyCover, 5)  # Writing modified data to the first band
        dst.set_band_description(5, src.descriptions[4])
        
        dst.write(mapStandHeight, 6)  # Writing modified data to the first band
        dst.set_band_description(6, src.descriptions[5])
        
        dst.write(mapCanopyBaseHeight, 7)  # Writing modified data to the first band
        dst.set_band_description(7, src.descriptions[6])
        
        dst.write(mapCanopyBulkDensity, 8)  # Writing modified data to the first band
        dst.set_band_description(8, src.descriptions[7])
   
# Close the original raster datasets
for src in src_files_to_mosaic:
    src.close()

bandnames=[]

for fp in filenames:
    if int(fp.split('ZHR_')[1].split('.')[0]) not in fileid: continue
    src = rasterio.open(fp.replace('.tif','_masked.tif'))
    src_files_to_mosaic.append(src)
    if len(bandnames)==0:
        for name_ in src.descriptions:
            bandnames.append(name_)
    
# Merge the rasters
mosaic, out_trans = merge(src_files_to_mosaic)

# Write the merged raster to a new file
with rasterio.open(output_file.replace('.tif','_masked.tif'), 'w', driver='GTiff',
                   height=mosaic.shape[1],
                   width=mosaic.shape[2],
                   count=mosaic.shape[0],
                   dtype=str(mosaic.dtype),
                   crs=src.crs,
                   transform=out_trans, 
                   nodata=-9999) as dest:
    dest.write(mosaic)
    for ib, name_ in enumerate(bandnames):
        dest.set_band_description(ib+1, name_)

# Close the original raster datasets
for src in src_files_to_mosaic:
    src.close()

with rasterio.open(output_file.replace('.tif','_masked.tif')) as src:

    profile = src.profile
    mapfuel = np.where(src.read(4)==-9999, 0, src.read(4))
    mapCanopyCover = np.where(src.read(5)==-9999, 0, src.read(5))
    mapStandHeight = np.where(src.read(6)==-9999, 0, src.read(6))
    mapCanopyBaseHeight = np.where(src.read(7)==-9999, 0, src.read(7))
    mapCanopyBulkDensity = np.where(src.read(8)==-9999, 0, src.read(8))

    #Write to a  file
    with rasterio.open(output_file, 'w', **profile) as dst:
        dst.write(src.read(1), 1)  # Writing modified data to the first band
        dst.set_band_description(1, src.descriptions[0])
        dst.write(src.read(2), 2)  # Writing modified data to the first band
        dst.set_band_description(2, src.descriptions[1])
        dst.write(src.read(3), 3)  # Writing modified data to the first band
        dst.set_band_description(3, src.descriptions[2])
        dst.write(mapfuel, 4)  # Writing modified data to the first band
        dst.set_band_description(4, src.descriptions[3])
        dst.write(mapCanopyCover, 5)  # Writing modified data to the first band
        dst.set_band_description(5, src.descriptions[4])
        dst.write(mapStandHeight, 6)  # Writing modified data to the first band
        dst.set_band_description(6, src.descriptions[5])
        dst.write(mapCanopyBaseHeight, 7)  # Writing modified data to the first band
        dst.set_band_description(7, src.descriptions[6])
        dst.write(mapCanopyBulkDensity, 8)  # Writing modified data to the first band
        dst.set_band_description(8, src.descriptions[7])




