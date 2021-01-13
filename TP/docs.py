from os import listdir
from config import CONFIG
import PyPDF2
import docx
import pdfplumber
from pptx import Presentation
import nltk.tag.stanford
import nltk as nl
from spacy.lang.es import Spanish
import spacy
import re
from tika import parser
import mainFunctions



nlpSpanish = spacy.load("es_core_news_md")


def readPdf(filename):
    pdf = pdfplumber.open(filename)
    cant_pags = len(pdf.pages)
    string_lectura = ""
    for i in range(cant_pags):
        pagActual =  pdf.pages[i].extract_text()
        if pagActual is not None:
            string_lectura = string_lectura + pagActual

    pdf.close()
    return string_lectura

def readPdf2(filename):
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


def readDocX(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def readDoc(filename):
    file = filename
    # Parse data from file
    file_data = parser.from_file(file)
    # Get files text content
    text = file_data['content']

    return text

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

    elif fType == "docx":
        return readDocX(path)

    elif fType == "doc":
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
        par.metadata = mainFunctions.preProcessor.preProcesar(text)
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
        spl = filePath.split("/")
        doc.name = spl[len(spl)-1]
        doc.text = readFile(filePath)
        doc.paragraphs = [Parragraph.newParagraph(s) for s in doc.text.split("\n") if len(s) > 0]
        return doc


def ls(ruta):
    return listdir(ruta)


def fileType(path):
    pathTok = path.split(".")
    return (pathTok[len(pathTok) - 1]).lower()

def citations(string):
    text = string
    num_replaces = 100000000
    text = text.replace('“', '"', num_replaces).replace('”', '"', num_replaces).replace('„', '"', num_replaces).replace('‟', '"', num_replaces)
    pattern = r'\(([^"\)]*|\bAnónimo\b|"[^"\)]*")(, )([\d]+|n\.d\.|[\d]+[\w])\)|\[(1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*\]'
    results = re.finditer(pattern, text)
    citations = [text[match.start(): match.end()] for match in results]
    return citations

def hasCitations(string):
    return len(citations(string)) > 0

def containsQuestionMark(string):
    return ("?" in string) or ("¿" in string)

##print([x for x in Doc.newDoc("C:/dataset-nlp-plagio-utn/Economía de experiencia (1).pdf").paragraphs[14].sentences])

##doc = nlpSpanish("Juan estaba sentado en la puerta de su casa, cuando escucho un fuerte llanto.")
##for token in doc:
  ##  print(token.text, token.pos_)


ejemploCita = "La primer cita es (Anónimo, n.d.), la segunda es (Qianyi Gu & Sumner, 2006). También hay que tener en cuenta a (Sabbagh, 2009) y a (\"Barcelona to Ban Burqa\", 2010). [5] y [500] tambien son muy importantes."

##print([x for x in citations(ejemploCita)])
##print(ls(CONFIG["DOCS_DB"]))
##print(readDoc(CONFIG["DOCS_DB"] + "/" + "TP 1 Wikinomics (1).doc"))
##print(readDoc(CONFIG["DOCS_DB"] + "/" + "TP 0 Gabriela Gonzalez MKTG y NV Economía.doc"))