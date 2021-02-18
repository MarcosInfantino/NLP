import docs
import pickle
import mainFunctions

pathBase = "C:/dataset-nlp-plagio-utn/"


class Topic:
    name = ""
    tokens = []

    @staticmethod
    def newTopic(name):
        obj = Topic()
        obj.name = name
        return obj

    def addToken(self, token):

        for x in self.tokens:
            if x == token:
                return
        self.tokens.append(token)
        return


topics = []

domotica = Topic.newTopic("Domótica")
topics.append(domotica)
economiaExperiencia = Topic.newTopic("Economía de la experiencia")
rifkin = Topic.newTopic("Rifkin")
sistemasEmergentes = Topic.newTopic("Sistemas emergentes")
marketingEnInternetYNuevaEconomia = Topic.newTopic("Marketing en Internet y Nueva Economía")
definicionesEconomia = Topic.newTopic("Definiciones de Economía")
comercioElectronicioArgentina = Topic.newTopic("Comercio electrónico en Argentina")
machinePlatform = Topic.newTopic("Machine, Platform, Crowd: Harnessing Our Digital Future")
wikinomics = Topic.newTopic("Wikinomics")

docsTraining = [
    ("Domótica_Final.pptx.pptx", "DOMÓTICA"),
    ("Economía de experiencia.pdf", "Economía de experiencia"),
    ("K5071 - Matias David Choren - TP N°5 Rifkin.pdf", "Rifkin"),
    ("K5071 - Matias David Choren - TP N6 Sistemas Emergentes.pdf", "Sistemas Emergentes"),
    ("K5071.pdf", "MARKETING EN INTERNET Y NUEVA ECONOMÍA"),
    ("Marketing - TP 0.docx", "Marketing en Internet y Nueva Economía"),
    ("Marketing - TP 2.docx", "Marketing en Internet y Nueva Economía"),
    ("Marketing en Internet y Nueva Economía - TP0.docx", "Marketing en Internet y Nueva Economía"),
    ("MKT 2016 - Alan Szpigiel - TP4 (2).pdf", "Marketing en Internet"),
    ("MKT 2016 - Alan Szpigiel - TP4.pdf", "Marketing en Internet"),
    ("MKTG_TP0  - Definiciones Economia.pdf", "Definiciones Economia"),
    ("MKTG_TP4  - Suchecki - Comercio Electronico.pdf", "COMERCIO ELECTRONICO EN ARGENTINA"),
    ("Preguntas TP Economía de experiencia - Gabriela Gonzalez.docx", "The experience economy "),
    ("PREGUNTAS TP Machine, Platform, Crowd.docx", "Machine, Platform, Crowd: Harnessing Our Digital Future "),
    ("preguntas TP Wikinomics - Gariglio.doc", "Wikinomics"),

    ("SCHMID TP N°3 Experience Economy.pdf", "MARKETING EN INTERNET Y NUEVA ECONOMÍA"),
    ("TP - 4.docx", "Marketing en Internet y Nueva Economía"),
    ("TP 0 Gabriela Gonzalez MKTG y NV Economía.doc", "MKTG y NV Economía"),
    ("TP 1 - Larga Cola - Campassi Rodrigo .docx", "Marketing en Internet y Nueva Economía"),
    ("TP 1 - Wikinomics (1).pdf", "Wikinomics"),
    ("TP 1 - Wikinomics.pdf", "Wikinomics"),
    ("TP 1 Wikinomics.doc", "Wikinomics"),
    ("TP 2 - Franco Zanette.docx", "La larga cola"),
    ("TP 2 - Long Tail.docx", "La larga cola"),
    ("TP 2 - Marketing en Internet y Nueva Economía - Lucas Corbo.docx", "Marketing en Internet y Nueva Economía"),
    ("TP 2 (1).doc", ""),
    ("TP 2 LargaCola - Hernan Noriega .docx", "La Larga Cola"),
    ("TP 3 - Economía de Experiencia - Andrés Basso (1).docx", "Economía de Experiencia"),
    ("TP 3 - Economia de la experiencia.docx", "Economía de Experiencia"),
    ("TP 3 - The experience economy - Joseph PINE II y James GILMORE - Juan Cruz Reines.pdf", "The experience economy"),
    ("TP 3 (1).doc", "economía de experiencia"),
    ("TP 3 Experience Economy - Hernan Noriega  (1).docx", "economía de experiencia"),
    ("TP 3 Experience Economy.docx", "economía de experiencia"),
    ("TP 3 The experience economy (2).docx", "economía de experiencia"),
    ("TP 3 The experience economy.docx", "economía de experiencia"),
    ("TP 3.docx", "economía de experiencia"),
    ("TP 4 - E-commerce - Juan Cruz Reines.pdf", "E-commerce"),
    ("TP 4 - Wikinomía.docx", "Wikinomics"),
    ("TP 4 Difusión y adopción - Hernan Noriega.docx", "Wikinomics"),
    ("TP 4-Franco Zanette (1).docx", "Difusión y adopción"),
    ("TP 5 - La sociedad de costo marginal cero.docx", "La sociedad de costo marginal cero"),
    ("TP 5 - Rodrigo Campassi - Plataformas y modelos de ebusiness.docx", "Plataformas y modelos de ebusiness"),
    ("TP 5 (2).docx", "La sociedad de costo marginal cero"),
    ("TP 5 La sociedad de costo cero - Hernan Noriega (1).docx", "Marketing en Internet"),
    ("TP 6 - Joan Manuel do Carmo.docx", "Sistemas Emergentes"),
    ("TP 6 - Sistemas emergentes.docx", "Sistemas emergentes"),
    ("TP Adopción TIC - ANTONUCCIO (1).doc", "Adopción TIC"),
    ("TP Comercio electronico preguntas Gabriela Gonzalez.doc", "Comercio electronico"),
    ("TP Johnson Sistemas emergentes - ANTONUCCIO.doc", "Sistemas emergentes"),
    ("TP La Larga Cola  - ANTONUCCIO.doc", "La Larga Cola"),
    ("TP La Larga Cola - Gabriela Gonzalez.doc", "La Larga Cola"),
    ("TP Larga Cola.docx", "Larga Cola"),
    ("TP N° 1 – WIKINOMICS - Melanie Blejter.pdf", "WIKINOMICS"),
    ("TP N° 3 – The Experience Economy - Hernán Kotler.docx", "economía de experiencia"),
    ("TP N° 4 – Difusión y Adopción TIC - Hernán Kotler.docx", "Difusión y Adopción TIC"),
    ("TP N° 5 – La sociedad de costo marginal cero - Melanie Blejter.pdf", "La sociedad de costo marginal cero"),
    ("TP N°1 - Wikinomics (1).pdf", "Wikinomics"),
    ("TP N°02 (1).pdf", "LA LARGA COLA"),
    ("TP N°2 - La Larga Cola de Chris Anderson corto (1).doc", "La Larga Cola"),
    ("TP N°2 Larga Cola.pdf", "Larga Cola")

    ## ("", ""),

]

for (docName, topic) in docsTraining:
    doc = docs.Doc.newDoc(pathBase + docName)
    tokensDoc = []
    for par in doc.paragraphs:
        for tok in par.metadata:
            topic.addToken(tok)

for topic in topics:
    print("Guardando en caché: " + topic.name)
    topic_file = open("probabilistic_topic_recognition/" + topic.name + ".cache", 'wb')
    pickle.dump(topic, topic_file)


def objectFromFile(path):
    file = open(path, "rb")
    return pickle.load(file)



