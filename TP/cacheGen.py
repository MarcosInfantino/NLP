import pickle
import mainFunctions
import docs
from config import CONFIG

def createCacheFromDataset():
    documents = mainFunctions.loadDocsFromDb(CONFIG["CANTIDAD_DOCS_DATASET"])
    for doc in documents:

        ##doc_name = doc.name.split(".")[0]
        doc_name = doc.name
        print("Guardando en caché: " + doc_name)
        doc_file = open("cache_dataset/" + doc_name + ".cache", 'wb')
        pickle.dump(doc, doc_file)


def objectFromFile(path):
    file = open(path, "rb")
    return pickle.load(file)

def readDatasetFromCache():
    files = docs.ls("cache_dataset/")
    docList = []
    for i in range(len(files)):
        if i < CONFIG["CANTIDAD_DOCS_DATASET"]:
            docList.append(objectFromFile("cache_dataset/" + files[i]))
    return docList


