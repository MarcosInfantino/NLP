import spacy
import docs
import random
from config import CONFIG


def tuplaInicioFinSubString(string, sub):
    x0 = string.find(sub)
    return (x0, x0 + len(sub))


pathBase = CONFIG["DOCS_DB"] + "/"


muchosAlumnos = ("", {"entities": []})
docAlumno = [
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

TRAINING_DATA = [ ]


def generarTrainingData():
    for x in docAlumno:
        nombreDoc = x[0]
        nombreAlumno = x[1].lower()
        docText = nombreDoc + '/n' + docs.Doc.newDoc(pathBase + nombreDoc).text.lower()
        tuplaInicioFin = tuplaInicioFinSubString(docText, nombreAlumno)
        print(tuplaInicioFin)
        sub0 = tuplaInicioFin[0]
        subf = tuplaInicioFin[1]
        if len(nombreAlumno) > 0:
            obj = (docText, {"entities": [(sub0, subf, "TEMATICA")]})
        else:
            obj = (docText, {"entities": []})
        TRAINING_DATA.append(obj)

generarTrainingData()
##("", {"entities": []})
TRAINING_DATA2 = [
    ("1)	¿Cómo define Anderson a “La larga cola”?  ¿Por qué asegura que es el presente y futuro de la economía minorista? Grafique.", {"entities": []}),
    ("1)	Anderson define a la Larga Cola como la teoría que indica que Internet desafía el Principio de Pareto (el 20% de las cosas son vitales y el 80% son triviales o inútiles) y en esta nueva economía los productos y servicios para minorías tienen un amplísimo espectro de oportunidades mediante el comercio electrónico. Internet es un medio que revoluciona el modo de consumo gracias a que la tecnología ahorra costos de almacenaje y de distribución de algunos productos.", {"entities": []}),
    ("Ése era el mundo de la escasez. Ahora, con la llegada de Internet la distribución y la venta digital,  se comienza a entrar en un mundo de abundancia donde las diferencias son más profundas.", {"entities": []}),
    ("Uber es una aplicación que no necesita grandes recursos económicos para poder instalarse en un mercado. Sólo basta con que haya conductores con vehículos (que cumplan ciertos requisitos) pero no mucho más que eso. Por eso, Uber puede desembarcar en países emergentes sin mayores inconvenientes. Permite a los conductores independientes convivir en el mercado con empresas de taxis o transporte y que su negocio aun sea rentable.", {"entities": []}),



]

'''for x in TRAINING_DATA2:
    TRAINING_DATA.append(x)'''


nlp = spacy.blank("es")
ner = nlp.create_pipe("ner")
nlp.add_pipe(ner)
ner.add_label("TEMATICA")

nlp.begin_training()

for i in range(600):
    random.shuffle(TRAINING_DATA)
    for batch in spacy.util.minibatch(TRAINING_DATA):
        print(i)
        texts = [text for text, annotation in batch]
        annotations = [annotation for text, annotation in batch]
        nlp.update(texts, annotations)

nlp.to_disk("C:/respositorios_git/tp_nlp/TP/models/tematica")