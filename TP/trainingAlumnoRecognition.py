import spacy
import docs
import random
from config import CONFIG
def tuplaInicioFinSubString(string, sub):
    x0 = string.find(sub)
    return (x0, x0 + len(sub))


pathBase = CONFIG["DOCS_DB"]
''

muchosAlumnos = ("", {"entities": []})
docAlumno = [
    ("Domótica_Final.pptx.pptx", "Pedro León"),
    ("Economía de experiencia (1).pdf", "Gallazzi, Pablo Gabriel"),
    ("Economía de experiencia.pdf", "Gallazzi, Pablo Gabriel"),
    ("K5071 - Matias David Choren - TP N°5 Rifkin (1).pdf", "MATIAS DAVID CHOREN"),
    ("K5071 - Matias David Choren - TP N°5 Rifkin.pdf", "MATIAS DAVID CHOREN"),
    ##("K5071 - Matias David Choren - TP3 - Experience Economy.pdf", "MATÍAS DAVID CHOREN"),
    ("Lopez Tomas - TP 6 - Sistemas Emergentes.doc", "LÓPEZ, Tomas"),
    ("Marketing - TP 0.docx", "Ivo Ursino"),
    ("Marketing - TP 1.docx", "Ivo Ursino"),
    ("Marketing - TP 2.docx", "Ivo Ursino"),
    ##("Marketing en Internet y Nueva Economía - TP0 (1).docx","Lorena Gonzalez"), ##REVISAR
    ##("TP 1 - Marketing.docx", "Calvo, Luciano"),
    ("TP1 - La Larga Cola - Chris Anderson (1).doc", "Lorena Gonzalez"),
    ("MKT 2016 - Alan Szpigiel - TP4 (1).pdf", "Alan Szpigiel"),
    ("Mkt_JourdanMartin_Tp1.docx", "Jourdan Martin"),
    ("MKTG_TP0  - Definiciones Economia.pdf", "Suchecki, Emiliano G."),
    ("MKTG_TP4  - Suchecki - Comercio Electronico.pdf", "Suchecki, Emiliano G."),
    ("MKT-TP N° 3 The experience Economy - Diego Noya.docx", "Diego Noya"),
    ##("Preguntas TP Economía de experiencia - Gabriela Gonzalez.docx", "Gabriela Gonzalez"),
    ##("Preguntas TP Marketing 4.0 - Kotler  Gabriela Gonzalez.docx", "Kotler  Gabriela Gonzalez"),
    ##("preguntas TP Wikinomics - Gariglio.doc", "Gariglio"),
    ##("TP 1 - Larga Cola - Campassi Rodrigo  (1).docx", "Rodrigo Campassi"),
    ("TP 1 - Wikinomics.docx", "Rocchio, Claudio"),
    ("TP 2 - Cecilia Ramacciotti.doc", "Cecilia A. Ramacciotti "),
    ("TP 2 - Franco Zanette.docx", "Franco Zanette "),
    ##("TP 2 - La economía Long Tail.docx", "Gonzalo Fernandez"),
    ("TP 2 Larga Cola - Ezequiel Ogando .docx", "Ezequiel Ogando"),
    ##("TP 3 - Economía de Experiencia - Andrés Basso.docx", "Andrés Basso"),
    ##("TP 3 - the experience economy.docx", "Calvo, Luciano"),
    ("TP 3-Franco Zanette.docx", "Franco Zanette "),
    ("TP 6 - Joan Manuel do Carmo.docx", "JOAN MANUEL DO CARMO"),
    ("TP 6 - Sistemas emergentes.docx", "Levy Nazareno Isaac"),
    ("TP N3 - García Santillán.doc", "Camila García Santillán"),
    ("TP Rifkin La sociedad de costo Mg cero - ANTONUCCIO.doc", "Jorge Ignacio Antonuccio"),
    ("TP_3_Weiss_Gonzalo (1).pdf", "WEISS, GONZALO"),
    ("TP1PabloPallocchi.pdf", "Pablo Pallocchi"),
    ("TP3 - Ignacio Penacino - Marketing (1).docx", "Penacino Ignacio"),
    ##("TP4-Gariglio.docx", "Gariglio"),
    ("TpN6 Hernan.doc", "Hernán Suzuki Son"),
    ("TP04 - TP Prince Difusión y adopción TIC.doc", "Spadafora, Franco Luciano"),
    ("TP4 - Adopcion TIC - Joel Melamed.docx", "Joel Melamed"),
    ("TP4 - Adopcion.docx", ""),
    ("TP4 - Comercio Electronico - Marina Pross.docx", "Marina Pross"),
    ("TP4 - Comercio electronico.doc", "Lorena Gonzalez"),
    ("TP4 - Comercio electronico.docx", ""),
    ("TP4 - Difusión y adopción - Parte I y II - Santiago Peralta (1).doc", "Santiago Peralta"),
    ("TP4 - Difusión y adopción TIC - Ramirez Fernando 2017.pdf", "Ramirez Fernando"),
    ("TP4 - ecommerce.docx", ""),
    ("TP4 (1).pdf", "Agustín Ezequiel Brandoni"),
    ("TP4 Adopcion.docx", "Brian Daniel Leder"),
    ("Tp4 Filannino marketing en internet.docx", "Hernán Filannino"),
    ("TP4.pdf", "Ignacio Javier Fernández Soto"),
    ("TP4-Gariglio.docx", "Gariglio"),
    ("TP5 - La sociedad de MG Cero - Rifkin - Santiago Peralta.docx", "Santiago Peralta"),
    ("TP5 - La sociedad del costo marginal 0.docx", "Santiago Peralta"),
    ("TP5 - Machine, Platform, Cloud - Marina Pross.docx", "Marina Pross"),
    ("TP5 - Plataformas.docx", ""),
    ("TP5 - Rifkin.docx", "Brian Daniel Leder"),
    ("TP5-Franco Zanette.docx.docx", "Franco Zanette "),
    ("TP6  - Sistemas emergentes - Joel Melamed.docx", "Joel Melamed"),
    ("TP6 - Sistemas emergentes - Hernan Noriega.docx", "Hernan Noriega"),
    ("TP6 Johnson Sistemas emergentes.doc", "Hernan Noriega"),
    ("TP6.docx", "Agustín Ezequiel Brandoni"),
    ("TP7 Dominio de la informacion - Juan Facundo Obregon.pdf", "Juan Facundo Obregon"),
    ("Trabajo Práctico 2 - Hernan Dalle Nogare.docx", "Hernan Dalle Nogare"),

    ##("UTN Mktg 2016 - Modugno - TP1.pdf", "Agustín Modugno"),
   ## ("", ""),

]

TRAINING_DATA = [ ]

'''
def textoConMuchosAlumnos(nombreDoc, alumnos):
    docText = nombreDoc + '/n' + docs.Doc.newDoc(pathBase + nombreDoc).text.lower()
    tuplas = []
    for al in alumnos:
        tuplaInicioFin = tuplaInicioFinSubString(docText, al)
        sub0 = tuplaInicioFin[0]
        subf = tuplaInicioFin[1]
        tuplas.append((sub0, subf, "ALUMNO"))
        print(tuplaInicioFin)
    obj = (docText, {"entities": tuplas})
    TRAINING_DATA.append(obj)

textoConMuchosAlumnos("Domótica_Final.pptx.pptx", ["Pedro León", "Luis Sosa", "Martín Jourdan", "Diego Laib"])
'''



def generarTrainingData():
    for x in docAlumno:
        nombreDoc = x[0]
        nombreAlumno = x[1].lower()
        docText = nombreDoc + '/n' + docs.Doc.newDoc(pathBase + nombreDoc).text.lower()
        ##docText = docs.Doc.newDoc(pathBase + nombreDoc).text.lower()
        tuplaInicioFin = tuplaInicioFinSubString(docText, nombreAlumno)
        print(tuplaInicioFin)
        sub0 = tuplaInicioFin[0]
        subf = tuplaInicioFin[1]
        if len(nombreAlumno) > 0:
            obj = (docText, {"entities": [(sub0, subf, "ALUMNO")]})
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
    ("Alumno: Marcos Infantino", {"entities": [(8, 24, "ALUMNO")]}),
    ("Alumno: Alan Rodríguez", {"entities": [(8, 22, "ALUMNO")]}),
    ("Alumna: Lucila Passarini", {"entities": [(8, 24, "ALUMNO")]}),
    ("Alumno: Suchecki, Emiliano G.", {"entities": [(8, 29, "ALUMNO")]}),
    ("Alumna: Cecilia A. Ramacciotti", {"entities": [(8, 30, "ALUMNO")]}),
    ("Alumna: Marcela Fernández", {"entities": [(8, 25, "ALUMNO")]}),
    ("Alumno: Hernán Noriega", {"entities": [(8, 22, "ALUMNO")]}),
    ("Alumno: Levy Nazareno Isaac", {"entities": [(8, 27, "ALUMNO")]}),
    ("Alumna: Melanie Blejter", {"entities": [(8, 23, "ALUMNO")]}),


]

for x in TRAINING_DATA2:
    TRAINING_DATA.append(x)


nlp = spacy.blank("es")
ner = nlp.create_pipe("ner")
nlp.add_pipe(ner)
ner.add_label("ALUMNO")

nlp.begin_training()

for i in range(700):
    random.shuffle(TRAINING_DATA)
    for batch in spacy.util.minibatch(TRAINING_DATA):
        print(i)
        texts = [text for text, annotation in batch]
        annotations = [annotation for text, annotation in batch]
        nlp.update(texts, annotations)

nlp.to_disk("C:/respositorios_git/tp_nlp/TP/models/alumno")

