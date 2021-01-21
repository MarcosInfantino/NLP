import docs
import cacheGen
import mainFunctions
from config import CONFIG


candidateDocument = docs.Doc.newDoc(CONFIG["CANDIDATE_DOC"])
paragraphMap = candidateDocument.generateParragraphMap()
documents = cacheGen.readDatasetFromCache()
mainFunctions.compareCandidateText(documents, candidateDocument, paragraphMap)
mainFunctions.showPlagiarismParameters(candidateDocument, paragraphMap)
'''for doc in documents:
    print("Doc: " + doc.name)
    print( doc.getAuthors())'''