import docs
import cacheGen
import mainFunctions
from config import CONFIG


candidateDocument = docs.Doc.newDoc("C:/dataset-nlp-plagio-utn/Trabajo Práctico 1 - Hernan Dalle Nogare.docx")
documents = cacheGen.readDatasetFromCache()
mainFunctions.compareCandidateText(documents, candidateDocument)
mainFunctions.showPlagiarismParameters()
