import copy

import nltk as nl
import logging
from config import CONFIG
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import docs
import web_scrapper
import time
from random import seed
from random import gauss
import pickle
from datetime import datetime
now = datetime.now()
date_time = now.strftime("%d-%m-%Y, %H_%M_%S")


root_logger= logging.getLogger()
root_logger.setLevel(logging.INFO)
handler = logging.FileHandler(CONFIG["LOG_FILE"] + "log" + "(" + date_time + ")" + ".txt", 'w', 'utf-8')
formatter = logging.Formatter('%(asctime)s %(message)s')
handler.setFormatter(formatter)
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

            self.varPreProcessor.preTokenizer = stemmer
            return self.varPreProcessor
        else:
            log.info("TOKENIZER ACTIVADO")
            self.varPreProcessor.preTokenizer = tokenizer
            if CONFIG["PUNCTUATION_REMOVAL"]:

                self.varPreProcessor.preProcessors.append(punctuationRemover)
            if CONFIG["LOWER_CASE_CONVERTION"]:

                self.varPreProcessor.preProcessors.append(lowerCaseConverter)
            if CONFIG["STOPWORD_REMOVAL"]:

                self.varPreProcessor.preProcessors.append(stopWordsRemover)
            return self.varPreProcessor

def containsToken(stringTok, tok):
    for x in stringTok:
        if x.pos == tok.pos and x.text == tok.text:
            return True
    return False

def removeToken(stringTok, tok):
    for x in stringTok:
        if x.pos == tok.pos and x.text == tok.text:
            stringTok.remove(x)


def intersectionStringTok(stringTok1, stringTok2):

    stringTok2Copy = copy.copy(stringTok2)
    list = []

    for tok in stringTok1:
        if containsToken(stringTok2Copy, tok):
            list.append(tok)
            removeToken(stringTok2Copy, tok)

    return list



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

    intersection = len(intersectionStringTok(metaCandidateText, metaReferenceText))


    union = len(unionStringTok(metaReferenceText, metaCandidateText))

    if union == 0:
        return 0
    else:
        return (intersection / union)*100


def loadDocsFromDb(cantidad):
    log.info("COMIENZA LA CARGA DE DOCUMENTOS DESDE LA BASE DE DATOS")
    documentsList = docs.ls(CONFIG["DOCS_DB"])
    cantDocs = len(docs.ls(CONFIG["DOCS_DB"]))
    documents = []

    if cantidad > 0 and cantidad < cantDocs:
        cantDocs = cantidad

    for i in range (cantDocs):

        log.info("PORCENTAJE DE LA CARGA: " + str(round((i/cantDocs)*100, 2)))
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

            if not CONFIG["QUESTIONS_SCORE"]:
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

                if not CONFIG["QUESTIONS_SCORE"]:
                    if (not docs.isQuestion(actualReferenceParragraph.text)) and (not docs.isQuestion(actualCandidateParragraph.text)):
                        score = JaccardScore(actualReferenceParragraph.text, actualCandidateParragraph.text, actualReferenceParragraph.metadata, actualCandidateParragraph.metadata)
                        paragraphMap[k].append(score)
                        plagiarismRegisters.append(PlagiarismRegister.newPlagiarismRegister(actualDoc.name, score, k, actualReferenceParragraph.text, actualCandidateParragraph.text))
                else:
                    score = JaccardScore( actualReferenceParragraph.text, actualCandidateParragraph.text, actualReferenceParragraph.metadata, actualCandidateParragraph.metadata)
                    paragraphMap[k].append(score)
                    plagiarismRegisters.append(PlagiarismRegister.newPlagiarismRegister(actualDoc.name, score, k, actualReferenceParragraph.text, actualCandidateParragraph.text))
        print("PORCENTAJE DEL ANÁLISIS CON LOS DOCUMENTOS DEL DATASET COMPLETADO: " + str(round((i/len(documents))*100, 2)) + "%")

def showPlagiarismParameters(doc, paragraphMap, threadInternetSearch):
    log.info("------------------------------------------------------------------------------------------------------------------------------------------------")
    log.info("Archivo procesado: "+ doc.name)
    log.info("Alumno/s: " + doc.getAuthors())
    log.info("Tematica/s: " + doc.getTopics())
    log.info("Porcentaje de plagio general: " + str(round(doc.generalPlagiarism(paragraphMap), 2)) + "%")
    log.info("------------------------------------------------------------------------------------------------------------------------------------------------")
    for i in range(len(plagiarismRegisters)):
        actual = plagiarismRegisters[i]
        if actual.plagiarismScore > CONFIG["PORCENTAJE_PLAGIO_AVISO"]:
            log.info("------------------------------------------------------------------------------------------------------------------------------------------------")
            log.info("Se ha detectado plagio con el documento " + actual.referenceDocument + ". Parrafo numero: " + str(actual.parragraphNumber) + ". Puntaje del " + str(round(actual.plagiarismScore,2)) + "%.")
            log.info("Fragmento plagiado")
            log.info("Referencia:")
            log.info(actual.parragraphTextReference)
            log.info("Candidato:")
            log.info(actual.parragraphTextCandidate)

    if CONFIG["WEB_SCRAPPING"]:
        log.info("------------------------------------------------------------------------------------------------------------------------------------------------")
        print("Esperando a que se terminen de recoletar los datos de la web...")
        threadInternetSearch.join()
        log.info("------------------------------------------------------------------------------------------------------------------------------------------------")
        log.info("RESULTADOS DE BÚSQUEDA EN LA WEB")
        log.info("------------------------------------------------------------------------------------------------------------------------------------------------")
        log.info("Puntaje de plagio en la web :" + str(round(internetPlagiarismResult.score,2))+"%")
        log.info("Fragmentos encontrados en la web:")
        for fragmentAndResults in internetPlagiarismResult.results:
            if len(fragmentAndResults.searchResults) > 0:
                log.info("Fragmento: " )
                log.info(fragmentAndResults.fragment)
                log.info("Resultados: ")
                for r in fragmentAndResults.searchResults:
                    log.info(r[1])
        if len(internetPlagiarismResult.results) == 0:
            print("Ninguno")


def obtainTextFragments(text):
    fragmentList = []
    count = 0
    actualString = ""
    for i in range(len(text)):
        char = text[i]
        if char != '\"':
            ##and char != '\n':
            count = count + 1
            actualString = actualString + char

        if count == 100 or i == len(text) - 1 :
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

internetPlagiarismResult = InternetPlagiarismResult()

def internetPlagiarismSearch(document):
    fragments = obtainTextFragments(document.text)
    results = []
    foundFragments = 0
    count = 0
    for f in fragments:
        busqueda = "\"" + f + "\""

        search_results = web_scrapper.scrap(busqueda)
        if len(search_results) > 0:
            foundFragments = foundFragments + 1

        for tuple in search_results:
            results.append(tuple)

        fragmentAndSearchResults = FragmentAndSearchResults()
        fragmentAndSearchResults.fragment = f
        fragmentAndSearchResults.searchResults = search_results
        internetPlagiarismResult.results.append(fragmentAndSearchResults)
        time.sleep(CONFIG["SLEEP_TIME_WEB_SCRAPPING"])
        count = count + 1


    score = (foundFragments / len(fragments))*100
    ##print("found " + str(foundFragments))
    ##print("len" + str(len(fragments)))
    internetPlagiarismResult.score = score

def objectFromFile(path):
    file = open(path, "rb")
    return pickle.load(file)


plagiarismRegisters = []
preProcessorBuilder = PreProcessorBuilder()
preProcessor = preProcessorBuilder.build()



