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
    for p in docs.find_topic(doc.name + '/n' + doc.text):
        print(p)'''
