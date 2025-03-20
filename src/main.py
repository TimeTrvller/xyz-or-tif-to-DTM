import numpy as np
from PIL import Image
import os
import math

from numpy.ma.extras import median

from src.readTIF import tif2dtm
from src.readXYZ import xyz2list

# import paths
datapath = '../data/BilsterBerg/'
fileExtention = '.tif'

filepaths = [f for f in os.listdir(datapath) if f.endswith(fileExtention)]
filecount = len(np.unique(filepaths))
# Files are usually ordered from southwest going north, then eastwards. Example with 9 files
# 3 6 9
# 2 5 8
# 1 4 7
# the list will be filled from first to last as an "array" contain the matrices, then sorted by the above logic

if fileExtention == '.xyz':
    dtm = xyz2list(datapath,filepaths)
elif fileExtention == '.tif':
    dtm = tif2dtm(datapath,filepaths)
else:
    print('invalid file type')
    exit()

# Normalization
minh = np.min(dtm)
maxh = np.max(dtm)
range = np.round(maxh-minh,2)
dtm_norm_temp = 255 * (dtm-minh)/range
dtm_norm = dtm_norm_temp.astype(np.uint8)

# Export as .tiff to avoid compression
dtm_export = Image.fromarray(dtm_norm)
dtm_export.save('../output/dtm_'+str(datapath[8:-1])+'_dh'+ str(range) +'m.tiff')