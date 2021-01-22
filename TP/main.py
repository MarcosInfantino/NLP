import docs
import cacheGen
import mainFunctions
from config import CONFIG
import threading


candidateDocument = docs.Doc.newDoc(CONFIG["CANDIDATE_DOC"])
paragraphMap = candidateDocument.generateParragraphMap()
documents = cacheGen.readDatasetFromCache()
threadInternetSearch = ""
if CONFIG["WEB_SCRAPPING"]:
    threadInternetSearch = threading.Thread(target = mainFunctions.internetPlagiarismSearch, args = (candidateDocument, ))
    threadInternetSearch.start()

mainFunctions.compareCandidateText(documents, candidateDocument, paragraphMap)
mainFunctions.showPlagiarismParameters(candidateDocument, paragraphMap, threadInternetSearch)
'''for doc in documents:
    print("Doc: " + doc.name)
    print( doc.getAuthors())'''