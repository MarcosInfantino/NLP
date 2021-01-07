from os import listdir
from config import CONFIG
import PyPDF2
import docx
from pptx import Presentation
import main
import nltk.tag.stanford
import nltk as nl
from spacy.lang.es import Spanish
import spacy

nlpSpanish = spacy.load("es_core_news_md")



def readPdf(filename):
    print(filename)
    archivo = open(filename, "rb")
    reader = PyPDF2.PdfFileReader(archivo)
    cant_pags = reader.getNumPages()
    print(cant_pags)
    string_lectura = ""
    print(string_lectura)
    for i in range(cant_pags):
        string_lectura = string_lectura + reader.getPage(i).extractText()

    return string_lectura


def readDoc(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


def readPpt(archivo):
    prs = Presentation(archivo)
    texto = ""
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                texto = texto + shape.text + "/n"

    return texto


def readFile(path):
    fType = fileType(path)
    if fType == "pdf":
        return readPdf(path)
    elif fType == "doc" or fType == "docx":
        return readDoc(path)
    elif fType == "pptx":
        return readPpt(path)
    else:
        return ""


class Parragraph:
    text = ""
    sentences = []
    metadata = []

    @staticmethod
    def newParagraph(text):
        par = Parragraph()
        par.text = text
        par.sentences = text.split(".")
        return par


class Doc:
    name = ""
    text = ""
    fileType = ""
    author = ""
    paragraphs = []

    @staticmethod
    def newDoc(filePath):
        doc = Doc()
        doc.fileType = fileType(filePath)
        doc.text = readFile(filePath)
        doc.paragraphs = [Parragraph.newParagraph(s) for s in doc.text.split("\n")]
        return doc


def ls(ruta):
    return listdir(ruta)


def fileType(path):
    pathTok = path.split(".")
    return (pathTok[len(pathTok) - 1]).lower()


print([x for x in Doc.newDoc("C:/dataset-nlp-plagio-utn/Marketing - TP 0.docx").paragraphs[14].sentences])

doc = nlpSpanish("Juan estaba sentado en la puerta de su casa, cuando escucho un fuerte llanto.")
for token in doc:
    print(token.text, token.pos_)
