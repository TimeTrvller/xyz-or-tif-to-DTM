import os
import numpy as np
from PIL import Image


def tif2dtm(datapath: str, filepaths: list):
    dtm_list = []
    filecount = len(np.unique(filepaths))
    for file in filepaths:
        filepath = os.path.join(datapath, file)
        z_grid = Image.open(filepath)

        # dimensions
        east_dim, north_dim = z_grid.size

        dtm_list.append(np.array(z_grid))

    ########
    # out of loop
    ########

    # Building the combined dtm rightside up as the internal data structure per file is from southwest going north, then eastwards as well
    match filecount:
        case 4:
            dtm_cluster = np.block([[dtm_list[1], dtm_list[3]],
                                    [dtm_list[0], dtm_list[2]]])
        case 9:
            dtm_cluster = np.block([[dtm_list[2], dtm_list[5], dtm_list[8]],
                                    [dtm_list[1], dtm_list[4], dtm_list[7]],
                                    [dtm_list[0], dtm_list[3], dtm_list[6]]])
        case 16:
            dtm_cluster = np.block([[dtm_list[3], dtm_list[7], dtm_list[11], dtm_list[15]],
                                    [dtm_list[2], dtm_list[6], dtm_list[10], dtm_list[14]],
                                    [dtm_list[1], dtm_list[5], dtm_list[9], dtm_list[13]],
                                    [dtm_list[0], dtm_list[4], dtm_list[8], dtm_list[12]]])
        case 36:
            dtm_cluster = np.block([[dtm_list[5], dtm_list[11], dtm_list[17], dtm_list[23], dtm_list[29], dtm_list[35]],
                                    [dtm_list[4], dtm_list[10], dtm_list[16], dtm_list[22], dtm_list[28], dtm_list[34]],
                                    [dtm_list[3], dtm_list[9], dtm_list[15], dtm_list[21], dtm_list[27], dtm_list[33]],
                                    [dtm_list[2], dtm_list[8], dtm_list[14], dtm_list[20], dtm_list[26], dtm_list[32]],
                                    [dtm_list[1], dtm_list[7], dtm_list[13], dtm_list[19], dtm_list[25], dtm_list[31]],
                                    [dtm_list[0], dtm_list[6], dtm_list[12], dtm_list[18], dtm_list[24], dtm_list[30]]])
        case _:
            dtm_cluster = []
            print('not the correct amount of files [needs to be a quadratic number]')
            exit()

    dtm = dtm_cluster
    return dtm