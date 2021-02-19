import docs
import pickle
import mainFunctions
from config import CONFIG

pathBase = CONFIG["DOCS_DB"]

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

        for x in self.tokens:
            if x == token:
                return 0
        self.tokens.append(token)
        return 0



topics = []

domotica = Topic.newTopic("Domótica")
topics.append(domotica)
economiaExperiencia = Topic.newTopic("Economía de la experiencia")
topics.append(economiaExperiencia)
rifkin = Topic.newTopic("Rifkin")
topics.append(rifkin)
sistemasEmergentes = Topic.newTopic("Sistemas emergentes")
topics.append(sistemasEmergentes)
marketingEnInternetYNuevaEconomia = Topic.newTopic("Marketing en Internet y Nueva Economía")
topics.append(marketingEnInternetYNuevaEconomia)
definicionesEconomia = Topic.newTopic("Definiciones de Economía")
topics.append(definicionesEconomia)
comercioElectronicioArgentina = Topic.newTopic("Comercio electrónico en Argentina")
topics.append(comercioElectronicioArgentina)
##machinePlatform = Topic.newTopic("Machine, Platform, Crowd: Harnessing Our Digital Future")
#topics.append(machinePlatform)
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
    ("Economía de experiencia.pdf", economiaExperiencia),
    ("K5071 - Matias David Choren - TP N°5 Rifkin.pdf", rifkin),
    ("K5071 - Matias David Choren - TP N6 Sistemas Emergentes.pdf", sistemasEmergentes),
    ("K5071.pdf", marketingEnInternetYNuevaEconomia),
    ("Marketing - TP 0.docx", marketingEnInternetYNuevaEconomia),
    ("Marketing - TP 2.docx", marketingEnInternetYNuevaEconomia),
    ("Marketing en Internet y Nueva Economía - TP0.docx", marketingEnInternetYNuevaEconomia),
    ("MKT 2016 - Alan Szpigiel - TP4 (2).pdf", marketingEnInternetYNuevaEconomia),
    ("MKT 2016 - Alan Szpigiel - TP4.pdf", marketingEnInternetYNuevaEconomia),
    ("MKTG_TP0  - Definiciones Economia.pdf", definicionesEconomia),
    ("MKTG_TP4  - Suchecki - Comercio Electronico.pdf", comercioElectronicioArgentina),
    ("Preguntas TP Economía de experiencia - Gabriela Gonzalez.docx", economiaExperiencia),
    ##("PREGUNTAS TP Machine, Platform, Crowd.docx", machinePlatform),
    ("preguntas TP Wikinomics - Gariglio.doc", wikinomics),
    ("SCHMID TP N°3 Experience Economy.pdf", marketingEnInternetYNuevaEconomia),
    ("TP - 4.docx", marketingEnInternetYNuevaEconomia),
    ("TP 0 Gabriela Gonzalez MKTG y NV Economía.doc", marketingEnInternetYNuevaEconomia),
    ("TP 1 - Larga Cola - Campassi Rodrigo .docx", marketingEnInternetYNuevaEconomia),
    ("TP 1 - Wikinomics (1).pdf", wikinomics),
    ("TP 1 - Wikinomics.pdf", wikinomics),
    ("TP 1 Wikinomics.doc", wikinomics),
    ("TP 2 - Franco Zanette.docx", largaCola),
    ("TP 2 - Long Tail.docx", largaCola),
    ("TP 2 - Marketing en Internet y Nueva Economía - Lucas Corbo.docx", marketingEnInternetYNuevaEconomia),
    ("TP 2 LargaCola - Hernan Noriega .docx", largaCola),
    ("TP 3 - Economía de Experiencia - Andrés Basso (1).docx", economiaExperiencia),
    ("TP 3 - Economia de la experiencia.docx", economiaExperiencia),
    ("TP 3 - The experience economy - Joseph PINE II y James GILMORE - Juan Cruz Reines.pdf", economiaExperiencia),
    ("TP 3 (1).doc", economiaExperiencia),
    ("TP 3 Experience Economy - Hernan Noriega  (1).docx", economiaExperiencia),
    ("TP 3 Experience Economy.docx", economiaExperiencia),
    ("TP 3 The experience economy (2).docx", economiaExperiencia),
    ("TP 3 The experience economy.docx", economiaExperiencia),
    ("TP 3.docx", economiaExperiencia),
    ("TP 4 - E-commerce - Juan Cruz Reines.pdf", comercioElectronicioArgentina),
    ("TP 4 - Wikinomía.docx", wikinomics),
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
    ("TP La Larga Cola  - ANTONUCCIO.doc", largaCola),
    ("TP La Larga Cola - Gabriela Gonzalez.doc", largaCola),
    ("TP Larga Cola.docx", largaCola),
    ("TP N° 1 – WIKINOMICS - Melanie Blejter.pdf", wikinomics),
    ("TP N° 3 – The Experience Economy - Hernán Kotler.docx", economiaExperiencia),
    ("TP N° 4 – Difusión y Adopción TIC - Hernán Kotler.docx", difusionAdopcion),
    ("TP N° 5 – La sociedad de costo marginal cero - Melanie Blejter.pdf", sociedadcostoMarginalCero),
    ("TP N°1 - Wikinomics (1).pdf", wikinomics),
    ("TP N°02 (1).pdf", largaCola),
    ("TP N°2 - La Larga Cola de Chris Anderson corto (1).doc", largaCola),
    ("TP N°2 Larga Cola.pdf", largaCola)

    ## ("", ""),

]


def createCacheProbabilisticTopicRecognition():

    for x in docsTraining:
        print(x)
        docName = x[0]
        topic = x[1]
        print(topic.name)
        print(len(topic.tokens))
        doc = docs.Doc.newDoc(pathBase + docName)

        for par in doc.paragraphs:
            for tok in par.metadata:
                topic.addToken(tok)

    for topic in topics:
        print("Guardando en caché: " + topic.name)
        topic_file = open("probabilistic_topic_recognition/" + topic.name + ".cache", 'wb')
        print(len(topic.tokens))
        pickle.dump(topic, topic_file)


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

    maxProb = -1
    maxTopic = ""

    for _topic in _topics:

        intersection = len(mainFunctions.intersectionStringTok(tokens_doc, _topic.tokens))
        union = len(mainFunctions.unionStringTok(tokens_doc, _topic.tokens))


        prob = (intersection / union) * 100


        if prob > maxProb:
            maxProb = prob
            maxTopic = _topic

    return maxTopic.name


