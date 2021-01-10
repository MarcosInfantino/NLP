import nltk as nl
import logging
from config import CONFIG
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import docs


logging.basicConfig(level = logging.INFO, filename = CONFIG["LOG_FILE"])

stopwordsSpanish = stopwords.words('spanish')
spanishStemmer = nl.stem.SnowballStemmer("spanish")

class Log:
    def info(self, string):
       print(string)
       logging.info(string)

log = Log()

class Tokenizer:
    def ejecutar(self, string):
        return nl.word_tokenize(string)

class PunctuationRemover:
    def ejecutar(self, string_array):
        return [x for x in string_array if x.isalnum()]

class StopWordsRemover:
    def ejecutar(self, string_array):
        return [x for x in string_array if x not in stopwordsSpanish]

class LowerCaseConverter:
    def ejecutar(self, stringArray):
        return [x.lower() for x in stringArray]

class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: (spanishStemmer.stem(w) for w in analyzer(doc) if w not in stopwordsSpanish)

stemVectorizer = StemmedCountVectorizer(min_df=1)
stemAnalize = stemVectorizer.build_analyzer()

class Stemmer:
    def ejecutar(self, string):
        return [x for x in stemAnalize(string)]

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

            if i == 0:
                stringRet = self.preProcessors[i].ejecutar(stringTok)
            else:
                stringRet = self.preProcessors[i].ejecutar(stringRet)

        return stringRet

    def crearMetadata(self, string):
        tokensAdmitidos = self.preProcesar(string)
        metaText = [PosTaggedWord.newPosTaggedWord(tok.pos_, tok.text) for tok in docs.nlpSpanish(string)]
        metaFinal = [x for x in metaText if x.text.lower() in tokensAdmitidos]

        if(CONFIG["LOWER_CASE_CONVERTION"]):
            metaFinal = [PosTaggedWord.newPosTaggedWord(x.pos, x.text.lower()) for x in metaFinal]

        return metaFinal



class PreProcessorBuilder:
    varPreProcessor = PreProcessor()

    def build(self):
        if CONFIG["STEMMING"]:
            log.info("STEMMING ACTIVADO")
            self.varPreProcessor.preTokenizer = stemmer
            return self.varPreProcessor
        else:
            log.info("TOKENIZER ACTIVADO")
            self.varPreProcessor.preTokenizer = tokenizer
            if CONFIG["PUNCTUATION_REMOVAL"]:
                log.info("PUNCTUATION REMOVAL ACTIVADO")
                self.varPreProcessor.preProcessors.append(punctuationRemover)
            if CONFIG["LOWER_CASE_CONVERTION"]:
                log.info("LOWER CASE CONVERTION ACTIVADO")
                self.varPreProcessor.preProcessors.append(lowerCaseConverter)
            if CONFIG["STOPWORD_REMOVAL"]:
                log.info("STOPWORD REMOVAL ACTIVADO")
                self.varPreProcessor.preProcessors.append(stopWordsRemover)
            return self.varPreProcessor


def repeticionesNGramas(stringTok1, stringTok2): ##cuantos ngramas del string 1 estan en el string 2
    return len( [x for x in filter (lambda x: x in stringTok2, stringTok1  )])

def repeticionesNGramasClip(stringTok1, stringTok2):
    return min([repeticionesNGramas(stringTok1, stringTok2), repeticionesNGramas(stringTok2, stringTok1)])

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

    def equals(self, otherWord):
        return self.pos == otherWord.pos and self.text == otherWord.text

    @staticmethod
    def newPosTaggedWord(pos, text):
        obj = PosTaggedWord()
        obj.pos = pos
        obj.text = text
        return obj


'''def JaccardScore(text1, text2):
    
    metaText1 = [PosTaggedWord.newPosTaggedWord() for tok in docs.nlpSpanish(text1)]
    metaText2 = [PosTaggedWord.newPosTaggedWord() for tok in docs.nlpSpanish(text2)]
    print()'''








ejemplo = "La detección de plagios en los trabajos entregados por los alumnos es un problema que ha existido tradicionalmente cuando se entregaban en formato papel pero que en los últimos años se ha incrementado debido a la gran cantidad de información que existe en Internet, a la facilidad para encontrarla usando buscadores y a la entrega electrónica de los trabajos o actividades (ciberplagio). Incluso existen plataformas en Internet que estructuran y ofrecen gratuitamente los trabajos para que se puedan descargar."






preProcessorBuilder = PreProcessorBuilder()
preProcessor = preProcessorBuilder.build()




oracion1="the the the the the the the"
oracion2="the cat is on the mat"


sTok1 = tokenizer.ejecutar(oracion1)
sTok2 = tokenizer.ejecutar(oracion2)

log.info(repeticionesNGramasClip(sTok1, sTok2))


log.info(NGramas.puntaje(sTok1, sTok2))


for x in preProcessor.crearMetadata(ejemplo):
    print(x.text + "-" + x.pos)

