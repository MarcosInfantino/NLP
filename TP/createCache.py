import cacheGen
from config import CONFIG
val_anterior = CONFIG["CANTIDAD_DOCS_DATASET"]
CONFIG["CANTIDAD_DOCS_DATASET"] = 0
cacheGen.createCacheFromDataset()
CONFIG["CANTIDAD_DOCS_DATASET"] = val_anterior