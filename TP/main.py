import nltk as nl
import logging
from config import CONFIG
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer


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
    def ejecutar(self, string):
        stringTok = self.preTokenizer.ejecutar(string)

        stringRet = stringTok

        for i in range(len(self.preProcessors)):

            if i == 0:
                stringRet = self.preProcessors[i].ejecutar(stringTok)
            else:
                stringRet = self.preProcessors[i].ejecutar(stringRet)

        return stringRet


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

















preProcessorBuilder = PreProcessorBuilder()
preProcessor = preProcessorBuilder.build()




oracion1="the the the the the the the"
oracion2="the cat is on the mat"


sTok1 = tokenizer.ejecutar(oracion1)
sTok2 = tokenizer.ejecutar(oracion2)

log.info(repeticionesNGramasClip(sTok1, sTok2))

log.info(preProcessor.ejecutar( oracion1))

log.info(NGramas.puntaje(sTok1, sTok2))

