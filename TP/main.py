import docs
import cacheGen
import mainFunctions
from config import CONFIG

ejemplo = "La detección de plagios en los trabajos entregados por los alumnos es un problema que ha existido tradicionalmente cuando se entregaban en formato papel pero que en los últimos años se ha incrementado debido a la gran cantidad de información que existe en Internet, a la facilidad para encontrarla usando buscadores y a la entrega electrónica de los trabajos o actividades (ciberplagio). Incluso existen plataformas en Internet que estructuran y ofrecen gratuitamente los trabajos para que se puedan descargar (Qianyi Gu & Sumner, 2006)."

candidateDocument = docs.Doc.newDoc("C:/dataset-nlp-plagio-utn/Trabajo Práctico 1 - Hernan Dalle Nogare.docx")
documents = cacheGen.readDatasetFromCache()
mainFunctions.compareCandidateText(documents, candidateDocument)
mainFunctions.showPlagiarismParameters()
