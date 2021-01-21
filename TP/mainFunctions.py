import copy

import nltk as nl
import logging
from config import CONFIG
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import docs
import web_scrapper
import threading
import urllib
from bs4 import BeautifulSoup as soup
import re
import time
from random import seed
from random import gauss

root_logger= logging.getLogger()
root_logger.setLevel(logging.INFO) # or whatever
handler = logging.FileHandler(CONFIG["LOG_FILE"], 'w', 'utf-8') # or whatever
formatter = logging.Formatter('%(asctime)s %(message)s') # or whatever
handler.setFormatter(formatter) # Pass handler as a parameter, not assign
root_logger.addHandler(handler)




stopwordsSpanish = stopwords.words('spanish')
spanishStemmer = nl.stem.SnowballStemmer("spanish")

class Log:
    def info(self, string):
       print(string)
       logging.info(string)

log = Log()
log.info("--------------------------------------------------------------INICIA LA APLICACION--------------------------------------------------------------")
class Tokenizer:
    def ejecutar(self, string):
        sTok = [PosTaggedWord.newPosTaggedWord(x.pos_, x.text, x.text) for x in docs.nlpSpanish(string)]
        return sTok

class PunctuationRemover:
    def ejecutar(self, string_array):
        return [x for x in string_array if x.text.isalnum()]

class StopWordsRemover:
    def ejecutar(self, string_array):
        return [x for x in string_array if x.text not in stopwordsSpanish]

class LowerCaseConverter:
    def ejecutar(self, stringArray):
        return [PosTaggedWord.newPosTaggedWord(x.pos, x.text.lower(), x.original.lower()) for x in stringArray]

class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: (spanishStemmer.stem(w) for w in analyzer(doc) if w not in stopwordsSpanish)

stemVectorizer = StemmedCountVectorizer(min_df=1)
stemAnalize = stemVectorizer.build_analyzer()

class Stemmer:
    def ejecutar(self, string):
        sTok = tokenizer.ejecutar(string)
        sRet = []
        for x in sTok:
            textStem = [x for x in stemAnalize(x.text)]
            if len(textStem) > 0:
                element = PosTaggedWord.newPosTaggedWord(x.pos, textStem[0], x.text.lower())
                sRet.append(element)

        return sRet


tokenizer = Tokenizer()
punctuationRemover = PunctuationRemover()
stopWordsRemover=StopWordsRemover()
lowerCaseConverter = LowerCaseConverter()
stemmer = Stemmer()


class PreProcessor:
    preTokenizer = ""
    preProcessors = []
    def preProcesar(self, string):
        stringTok = self.preTokenizer.ejecutar(string)

        stringRet = stringTok

        for i in range(len(self.preProcessors)):
                stringRet = self.preProcessors[i].ejecutar(stringRet)

        return stringRet




class PreProcessorBuilder:
    varPreProcessor = PreProcessor()

    def build(self):
        if CONFIG["STEMMING"]:
            ##log.info("STEMMING ACTIVADO")
            self.varPreProcessor.preTokenizer = stemmer
            return self.varPreProcessor
        else:
            log.info("TOKENIZER ACTIVADO")
            self.varPreProcessor.preTokenizer = tokenizer
            if CONFIG["PUNCTUATION_REMOVAL"]:
                ##log.info("PUNCTUATION REMOVAL ACTIVADO")
                self.varPreProcessor.preProcessors.append(punctuationRemover)
            if CONFIG["LOWER_CASE_CONVERTION"]:
                ##log.info("LOWER CASE CONVERTION ACTIVADO")
                self.varPreProcessor.preProcessors.append(lowerCaseConverter)
            if CONFIG["STOPWORD_REMOVAL"]:
                ##log.info("STOPWORD REMOVAL ACTIVADO")
                self.varPreProcessor.preProcessors.append(stopWordsRemover)
            return self.varPreProcessor



def containsPosWord(stringTok, posWord):
    for x in stringTok:
        if x.pos == posWord.pos and x.text == posWord.text:
            return True
        '''if x.pos == posWord.pos :
            if CONFIG["POS"] and x.text == posWord.text:
                return True
            else:
                return True'''
    return False


def repeticionesNGramas(stringTok1, stringTok2): ##cuantos ngramas del string 1 estan en el string 2
    return len( [x for x in filter (lambda x: containsPosWord(stringTok2, x), stringTok1 )])


def containsToken(stringTok, tok):
    for x in stringTok:
        if x.pos == tok.pos and x.text == tok.text:
            return True
    return False

def removeToken(stringTok, tok):
    for x in stringTok:
        if x.pos == tok.pos and x.text == tok.text:
            stringTok.remove(x)


def repeticionesNGramasClip(stringTok1, stringTok2):

    stringTok2Copy = copy.copy(stringTok2)

    count = 0
    for tok in stringTok1:
        if containsToken(stringTok2Copy, tok):
            count = count + 1
            removeToken(stringTok2Copy, tok)

    return count


    ##return min([repeticionesNGramas(stringTok1, stringTok2), repeticionesNGramas(stringTok2, stringTok1)])

class NGramas:
    @staticmethod
    def puntaje(sReferencia, sCandidata):
        R = repeticionesNGramasClip(sReferencia, sCandidata) / len(sReferencia)
        P = repeticionesNGramasClip(sReferencia, sCandidata) / len(sCandidata)
        score = (2* R * P) / (R + P)
        return score



class PosTaggedWord:
    pos = ""
    text = ""
    original = ""

    def equals(self, otherWord):
        return self.pos == otherWord.pos and self.text == otherWord.text

    @staticmethod
    def newPosTaggedWord(pos, text, original):
        obj = PosTaggedWord()
        obj.pos = pos
        obj.text = text
        obj.original = original
        return obj


def unionStringTok(stringTok1, stringTok2):
    list = []
    for x in stringTok1:
        if not containsToken(list, x):
            list.append(x)
    for y in stringTok2:
        if not containsToken(list, y):
            list.append(y)

    return list


def JaccardScorePlainText(referenceText, candidateText):
    return JaccardScore(referenceText, candidateText, preProcessor.preProcesar(referenceText), preProcessor.preProcesar(candidateText))




def JaccardScore(referenceText, candidateText, metaReferenceText, metaCandidateText):

    if docs.hasCitations(candidateText):
        return 0


    intersection = repeticionesNGramasClip(metaCandidateText,metaReferenceText)

    ##print("interseccion " + str(intersection))
    union = unionStringTok(metaReferenceText,metaCandidateText)

    ##dividendo = (len(metaReferenceText) + len(metaCandidateText) - intersection)
    dividendo = len(union)

    ##print("union " + str(dividendo))
    if dividendo == 0:
        return 0
    else:
        return (intersection / dividendo)*100


def loadDocsFromDb(cantidad):
    log.info("COMIENZA LA CARGA DE DOCUMENTOS DESDE LA BASE DE DATOS")
    documentsList = docs.ls(CONFIG["DOCS_DB"])
    cantDocs = len(docs.ls(CONFIG["DOCS_DB"]))
    documents = []

    if cantidad > 0 and cantidad < cantDocs:
        cantDocs = cantidad

    for i in range (cantDocs):

        log.info("PORCENTAJE DE LA CARGA: " + str((i/cantDocs)*100))
        filename = documentsList[i]
        log.info("SE CARGA EL DOCUMENTO: " + filename)
        documents.append(docs.Doc.newDoc(CONFIG["DOCS_DB"] + "/" + filename))
    return documents



class PlagiarismRegister:
    referenceDocument = ""
    plagiarismScore = ""
    parragraphNumber = ""
    parragraphTextReference = ""
    parragraphTextCandidate = ""
    @staticmethod
    def newPlagiarismRegister(referenceDocument, plagiarismScore, parragraphNumber, parragraphTextReference, parragraphTextCandidate):
        o = PlagiarismRegister()
        o.referenceDocument = referenceDocument
        o.plagiarismScore = plagiarismScore
        o.parragraphNumber = parragraphNumber
        o.parragraphTextReference = parragraphTextReference
        o.parragraphTextCandidate = parragraphTextCandidate
        return o



def compareDocuments(referenceDocument, candidateDocument):
    paragraphMap = candidateDocument.generateParragraphMap()

    for i in range(len(referenceDocument.paragraphs)):
        actualReferenceParragraph = referenceDocument.paragraphs[i]
        for j in range(len(candidateDocument.paragraphs)):
            actualCandidateParragraph = candidateDocument.paragraphs[j]

            if not CONFIG["QUESTIONS_PUNCTUATION"]:
                if (not docs.isQuestion(actualReferenceParragraph.text)) and (
                not docs.isQuestion(actualCandidateParragraph.text)):
                    score = JaccardScore(actualReferenceParragraph.text, actualCandidateParragraph.text,
                                         actualReferenceParragraph.metadata, actualCandidateParragraph.metadata)
                    paragraphMap[j].append(score)
                    plagiarismRegisters.append(PlagiarismRegister.newPlagiarismRegister(referenceDocument.name, score, j,
                                                                                        actualReferenceParragraph.text,
                                                                                        actualCandidateParragraph.text))


            else:
                score = JaccardScore(actualReferenceParragraph.text, actualCandidateParragraph.text,
                                     actualReferenceParragraph.metadata, actualCandidateParragraph.metadata)
                paragraphMap[j].append(score)
                plagiarismRegisters.append(
                    PlagiarismRegister.newPlagiarismRegister(referenceDocument.name, score, j, actualReferenceParragraph.text,
                                                             actualCandidateParragraph.text))

    return candidateDocument.generalPlagiarism(paragraphMap)


def compareCandidateText(documents, candidateDocument, paragraphMap):
    for i in range(len(documents)):
        actualDoc = documents[i]
        for j in range(len(actualDoc.paragraphs)):
            actualReferenceParragraph = actualDoc.paragraphs[j]
            for k in range(len(candidateDocument.paragraphs)):
                actualCandidateParragraph = candidateDocument.paragraphs[k]

                if not CONFIG["QUESTIONS_PUNCTUATION"]:
                    if (not docs.isQuestion(actualReferenceParragraph.text)) and (not docs.isQuestion(actualCandidateParragraph.text)):
                        score = JaccardScore(actualReferenceParragraph.text, actualCandidateParragraph.text, actualReferenceParragraph.metadata, actualCandidateParragraph.metadata)
                        paragraphMap[k].append(score)
                        plagiarismRegisters.append(PlagiarismRegister.newPlagiarismRegister(actualDoc.name, score, k, actualReferenceParragraph.text, actualCandidateParragraph.text))
                else:
                    score = JaccardScore( actualReferenceParragraph.text, actualCandidateParragraph.text, actualReferenceParragraph.metadata, actualCandidateParragraph.metadata)
                    paragraphMap[k].append(score)
                    plagiarismRegisters.append(PlagiarismRegister.newPlagiarismRegister(actualDoc.name, score, k, actualReferenceParragraph.text, actualCandidateParragraph.text))

def showPlagiarismParameters(doc, paragraphMap):
    log.info("------------------------------------------------------------------------------------------------------------------------------------------------")
    log.info("Archivo procesado: "+ doc.name)
    log.info("Alumno/s: " + doc.getAuthors())
    log.info("Tematica/s: " + doc.getTopics())
    log.info("Porcentaje de plagio general: " + str(doc.generalPlagiarism(paragraphMap)) + "%")
    log.info("------------------------------------------------------------------------------------------------------------------------------------------------")
    for i in range(len(plagiarismRegisters)):
        actual = plagiarismRegisters[i]
        if actual.plagiarismScore > CONFIG["PORCENTAJE_PLAGIO_AVISO"]:
            log.info("------------------------------------------------------------------------------------------------------------------------------------------------")
            log.info("Se ha detectado plagio con el documento " + actual.referenceDocument + ". Parrafo numero: " + str(actual.parragraphNumber) + ". Puntaje del " + str(actual.plagiarismScore) + "%.")
            log.info("Fragmento plagiado")
            log.info("Referencia:")
            log.info(actual.parragraphTextReference)
            log.info("Candidato:")
            log.info(actual.parragraphTextCandidate)

def obtainTextFragments(text):
    fragmentList = []
    count = 0
    actualString = ""
    for i in range(len(text)):
        char = text[i]
        count = count + 1
        actualString = actualString + char
        if count == 140 or i == len(text) - 1 :
            newString = actualString
            fragmentList.append(newString)
            actualString = ""
            count = 0

    return fragmentList

class FragmentAndSearchResults:
    fragment = ""
    searchResults = []

class InternetPlagiarismResult:
    score = 0
    results = []

def randomNumber():
    seed(1)
    return gauss(0, 1.5)

def internetPlagiarismSearch(document):
    internetPlagiarismResult = InternetPlagiarismResult()
    fragments = obtainTextFragments(document.text)
    results = []
    foundFragments = 0
    for f in fragments:
        busqueda = "\"" + f + "\""

        search_results = web_scrapper.scrap(busqueda, 10, "es")
        if len(search_results) > 0:
            foundFragments = foundFragments + 1

        for tuple in search_results:
            results.append(tuple)

        fragmentAndSearchResults = FragmentAndSearchResults()
        fragmentAndSearchResults.fragment = f
        fragmentAndSearchResults.searchResults = search_results
        internetPlagiarismResult.results.append(fragmentAndSearchResults)
        time.sleep(randomNumber())

    score = foundFragments / len(fragments)
    internetPlagiarismResult.score = score

    return internetPlagiarismResult



def synonims(word):
    '''data = str(urllib.request.urlopen('https://educalingo.com/en/dic-es/{}'.format(word)).read())
    final_results = re.findall('\w+', [i.text for i in soup(data, 'lxml').find_all('div', {"class": 'contenido_sinonimos_antonimos'})][0])'''
    return []


plagiarismRegisters = []
preProcessorBuilder = PreProcessorBuilder()
preProcessor = preProcessorBuilder.build()



