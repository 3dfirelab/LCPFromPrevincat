import rasterio
from netCDF4 import Dataset
import numpy as np
from rasterio.mask import mask
from shapely.geometry import box
import geopandas as gpd
from pyproj import CRS
import rasterio
from netCDF4 import Dataset
import numpy as np
from rasterio.mask import mask
from shapely.geometry import box
import geopandas as gpd
from pyproj import CRS

# Load the NetCDF file
nc_file = '/mnt/Clouds/Dropbox/Lecture/UPC_2023/fireBehavior/flamMapData/LCP_cataluna/NC-MNH/PGD_D80mA.nested.nc'
nc_data = Dataset(nc_file, mode='r')

# Assume the extent is defined by the variables 'lon' and 'lat'
lons = nc_data.variables['longitude'][:]
lats = nc_data.variables['latitude'][:]

# Get the extent
marge = 0.5
min_lon, max_lon = np.min(lons)-marge, np.max(lons)+marge
min_lat, max_lat = np.min(lats)-marge, np.max(lats)+marge

# Create a bounding box
bbox = box(min_lon, min_lat, max_lon, max_lat)

# Convert the bbox to a GeoDataFrame
geo_df = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs=CRS.from_epsg(4326))

# Load the TIFF file
tiff_file = 'merged.tif'
with rasterio.open(tiff_file) as src:
    # Reproject the bounding box to the TIFF's CRS
    geo_df = geo_df.to_crs(src.crs)
    
    # Clip the TIFF with the bounding box
    out_image, out_transform = mask(src, [geo_df.geometry.iloc[0]], crop=True)

    # Update metadata
    out_meta = src.meta.copy()
    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})

    # Save the clipped image
    with rasterio.open('lcp_pgd80.tif', 'w', **out_meta) as dest:
        dest.write(out_image)

print("TIFF clipped successfully!")
