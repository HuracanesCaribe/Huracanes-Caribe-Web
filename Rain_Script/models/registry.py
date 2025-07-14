# models/registry.py
# from models import ecmwf_downloader, ecmwf_processor
from models import gfs_downloader, gfs_processor
# from models import icon_downloader, icon_processor
# from models import cmc_downloader, cmc_processor

MODEL_REGISTRY = {
    'gfs': {
        'download': gfs_downloader.download_gfs_rainfall,
        'process': gfs_processor.process_precip_data
    },
}

    # 'ecmwf': {
    #     'download': ecmwf_downloader.download_ecmwf_rainfall,
    #     'process': ecmwf_processor.process_precip_data
    # },

    # 'icon': {
    #     'download': icon_downloader.download_icon_rainfall,
    #     'process': icon_processor.process_precip_data
    # },
    # 'cmc': {
    #     'download': cmc_downloader.download_cmc_rainfall,
    #     'process': cmc_processor.process_precip_data
    # },

