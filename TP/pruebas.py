import docs
from config import CONFIG
import mainFunctions
import pytest
import mainFunctions
import docs
import copy
'''
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
'''

doc = docs.Doc.newDoc("C:/dataset-nlp-plagio-utn/TP 1 - Larga Cola - Campassi Rodrigo .docx")
docPlagio = docs.Doc.newDoc("C:/dataset-nlp-plagio-utn/TP 1 - Larga Cola - Campassi Rodrigo(plagio) .docx")
print(mainFunctions.compareDocuments(doc, docPlagio))