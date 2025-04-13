import numpy as np
from PIL import Image
import os
import rasterio

from src.readTIF import tif2dtm
from src.readXYZ import xyz2list
from src.mergeTiff import mergeTiff

# import paths
datapath = '../data/Redbullring/'
fileExtention = '.tif'

filenames = [f for f in os.listdir(datapath) if f.endswith(fileExtention)]
filepaths = [datapath + filename for filename in filenames]
filecount = len(np.unique(filenames))
# Files are usually ordered from southwest going north, then eastwards. Example with 9 files
# 3 6 9
# 2 5 8
# 1 4 7
# the list will be filled from first to last as an "array" contain the matrices, then sorted by the above logic
if fileExtention == '.xyz':
    dtm = xyz2list(filepaths)

    # Normalization
    minh = np.min(dtm)
    maxh = np.max(dtm)
    range = np.round(maxh-minh,2)
    dtm_norm_temp = 255 * (dtm-minh)/range
    dtm_norm = dtm_norm_temp.astype(np.uint8)

    # Export as .tif to avoid compression
    dtm_export = Image.fromarray(dtm_norm)
    dtm_export.save('../output/dtm_'+str(datapath[8:-1])+'_dh'+ str(range) +'m.tif')
elif fileExtention == '.tif':
    # dtm = tif2dtm(datapath,filenames)
    dtm, out_meta = mergeTiff(filepaths)

    # Export as .tif to avoid compression
    with rasterio.open('../output/dtm_'+str(datapath[8:-1])+'.tif', "w", **out_meta) as dest:
        dest.write(dtm)

else:
    print('invalid file type')
    exit()


