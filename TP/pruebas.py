import docs
from config import CONFIG
import mainFunctions

candidateDocument = docs.Doc.newDoc(CONFIG["CANDIDATE_DOC"])
print(mainFunctions.obtainTextFragments(candidateDocument.text))
internetPlagiarismResults = mainFunctions.internetPlagiarismSearch(candidateDocument)
print(internetPlagiarismResults.score)
print("----------------------------")
for fragmentAndResults in internetPlagiarismResults.results:
    print("Fragment: " + fragmentAndResults.fragment)
    print("Resultados: ")
    for r in fragmentAndResults.searchResults:
        print(r)
