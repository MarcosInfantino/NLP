import docs
from config import CONFIG
import mainFunctions
import pytest
import mainFunctions
import docs
import copy

candidateDocument = docs.Doc.newDoc(CONFIG["CANDIDATE_DOC"])
print(len("CUESTIONARIO Difusión y adopción TIC TP: PAPER DIFUSION Y ADOPCION PARTE 1  1. Qué se entiende por d"))
for f in mainFunctions.obtainTextFragments(candidateDocument.text):
    print(f)
    print("---------------------------------------")

