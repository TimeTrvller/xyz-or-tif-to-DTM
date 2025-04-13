import rasterio
from rasterio.merge import merge


def mergeTiff(filepaths: list[str]):
    all_dtms = [rasterio.open(file) for file in filepaths] # all files at once as list of open objects

    combined_dtm, out_transform = merge(all_dtms)

    # Metadata from the first file as blueprint for the format
    out_meta = all_dtms[0].meta.copy()
    out_meta.update({
        "height": combined_dtm.shape[1],
        "width": combined_dtm.shape[2],
        "transform": out_transform
    })

    for src in all_dtms:    # Close all opened files
        src.close()

    return combined_dtm, out_meta