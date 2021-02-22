import docs
import pickle
import mainFunctions
from config import CONFIG
import math
pathBase = CONFIG["DOCS_DB"] + "/"


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


class Topic:
    name = ""
    tokens = []

    @staticmethod
    def newTopic(name):
        obj = Topic()
        obj.name = name
        obj.tokens = []
        return obj

    def addToken(self, token):
        self.tokens.append(token)

    def count(self):
        i = 0
        for x in docsTraining:
            if x[1].name == self.name:
                i = i + 1
        return i


topics = []

domotica = Topic.newTopic("Domótica")
topics.append(domotica)
economiaExperiencia = Topic.newTopic("Economía de la experiencia")
topics.append(economiaExperiencia)
sistemasEmergentes = Topic.newTopic("Sistemas emergentes")
topics.append(sistemasEmergentes)
marketingEnInternetYNuevaEconomia = Topic.newTopic("Marketing en Internet y Nueva Economía")
topics.append(marketingEnInternetYNuevaEconomia)
definicionesEconomia = Topic.newTopic("Definiciones de Economía")
topics.append(definicionesEconomia)
comercioElectronicioArgentina = Topic.newTopic("Comercio electrónico en Argentina")
topics.append(comercioElectronicioArgentina)
wikinomics = Topic.newTopic("Wikinomics")
topics.append(wikinomics)
largaCola = Topic.newTopic("La Larga Cola")
topics.append(largaCola)
difusionAdopcion = Topic.newTopic("Difusion y adopción")
topics.append(difusionAdopcion)
sociedadcostoMarginalCero = Topic.newTopic("La sociedad del costo marginal cero")
topics.append(sociedadcostoMarginalCero)
plataformasModelosEBussiness = Topic.newTopic("Plataformas y modelos de e-business")
topics.append(plataformasModelosEBussiness)

docsTraining = [
    ("Domótica_Final.pptx.pptx", domotica),
    ("MKTG_TP0  - Definiciones Economia.pdf", definicionesEconomia),
    ("MKTG_TP4  - Suchecki - Comercio Electronico.pdf", comercioElectronicioArgentina),
    ("preguntas TP Wikinomics - Gariglio.doc", wikinomics),
    ("TP 0 Gabriela Gonzalez MKTG y NV Economía.doc", marketingEnInternetYNuevaEconomia),
    ("TP 1 - Wikinomics (1).pdf", wikinomics),
    ("TP 2 - Franco Zanette.docx", largaCola),
    ("TP 2 - Long Tail.docx", largaCola),
    ("TP 2 - Marketing en Internet y Nueva Economía - Lucas Corbo.docx", marketingEnInternetYNuevaEconomia),
    ("TP 3 - Economía de Experiencia - Andrés Basso (1).docx", economiaExperiencia),
    ("TP 3 - The experience economy - Joseph PINE II y James GILMORE - Juan Cruz Reines.pdf", economiaExperiencia),
    ("TP 4 - E-commerce - Juan Cruz Reines.pdf", comercioElectronicioArgentina),
    ("TP 4 Difusión y adopción - Hernan Noriega.docx", wikinomics),
    ("TP 4-Franco Zanette (1).docx", difusionAdopcion),
    ("TP 5 - La sociedad de costo marginal cero.docx", sociedadcostoMarginalCero),
    ("TP 5 - Rodrigo Campassi - Plataformas y modelos de ebusiness.docx", plataformasModelosEBussiness),
    ("TP 5 (2).docx", sociedadcostoMarginalCero),
    ("TP 5 La sociedad de costo cero - Hernan Noriega (1).docx", marketingEnInternetYNuevaEconomia),
    ("TP 6 - Joan Manuel do Carmo.docx", sistemasEmergentes),
    ("TP 6 - Sistemas emergentes.docx", sistemasEmergentes),
    ("TP Adopción TIC - ANTONUCCIO (1).doc", difusionAdopcion),
    ("TP Comercio electronico preguntas Gabriela Gonzalez.doc", comercioElectronicioArgentina),
    ("TP Johnson Sistemas emergentes - ANTONUCCIO.doc", sistemasEmergentes),
    ("TP Larga Cola.docx", largaCola),
    ("TP N° 3 – The Experience Economy - Hernán Kotler.docx", economiaExperiencia),
    ("TP N° 4 – Difusión y Adopción TIC - Hernán Kotler.docx", difusionAdopcion),
    ("TP N° 5 – La sociedad de costo marginal cero - Melanie Blejter.pdf", sociedadcostoMarginalCero),
    ("TP5 - Plataformas.docx", plataformasModelosEBussiness),
    ("TP 5 - Machine, Platform, Crowd.docx", plataformasModelosEBussiness)

]




def createVocabulary(tops):
    list = []
    for t in tops:
        for x in t.tokens:
            list.append(x)
    return list





'''
for t in topics:
    count = 0
    for x in docsTraining:
        if x[1] == t:
            count = count + 1
    print(t.name + "   " + str(count))
'''

def smoothLikelyhood(word, topic, vocabulary):
    i = 0
    for x in topic.tokens:
        if x.text == word.text:
            i = i + 1


    return (i + 1) / (len(topic.tokens) + len(vocabulary))


def createCacheProbabilisticTopicRecognition():
    for x in docsTraining:

        docName = x[0]
        topic = x[1]

        doc = docs.Doc.newDoc(pathBase + docName)

        for par in doc.paragraphs:
            for tok in par.metadata:
                topic.addToken(tok)

    for topic in topics:
        print("Guardando en caché: " + topic.name)
        topic_file = open("probabilistic_topic_recognition/" + topic.name + ".cache", 'wb')

        pickle.dump(topic, topic_file)



def containsToken(list, token):
    bool = False
    for x in list:
        if x.text == token.text:
            bool = True

    return bool


def logsumexp(x, y):
    sum = 0
    max_value = max(x, y)
    sum += math.exp(x - max_value)
    sum += math.exp(y - max_value)

    return math.log(sum) + max_value

def getTopicProbabilistic(doc):
    _topics = []
    files = docs.ls("probabilistic_topic_recognition/")

    for i in range(len(files)):
        _topics.append(mainFunctions.objectFromFile("probabilistic_topic_recognition/" + files[i]))

    tokens_doc = []
    for par in doc.paragraphs:
        for tok in par.metadata:
            bool = True
            for tok2 in tokens_doc:
                if tok == tok2:
                    bool = False
            if bool:
                tokens_doc.append(tok)

    maxProb = -10000000
    maxTopic = ""
    vocabulary = createVocabulary(_topics)
    for _topic in _topics:
        prob = 0
        prob += math.log(_topic.count()/len(topics)) / math.log(10)

        for word in tokens_doc:
            if containsToken(vocabulary, word):


                prob += math.log(smoothLikelyhood(word, _topic, vocabulary)) / math.log(10)



        if prob > maxProb:

            maxProb = prob
            maxTopic = _topic

    return maxTopic.name


