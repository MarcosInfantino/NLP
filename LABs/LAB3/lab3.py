import nltk.stem
import PyPDF2
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords

stopwords_spanish = stopwords.words('spanish')
spanish_stemmer = nltk.stem.SnowballStemmer("spanish")



class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: (spanish_stemmer.stem(w) for w in analyzer(doc) if w not in stopwords_spanish)

stem_vectorizer = StemmedCountVectorizer(min_df=1)
stem_analyze = stem_vectorizer.build_analyzer()

def analizar_oracion(oracion, mostrar_nombre):
    if(mostrar_nombre):
        print("------------------------------------------Analisis de la oración: ", oracion, "------------------------------------------")
    oracion_tok=stem_analyze(oracion)
    for tok in oracion_tok:
        print(tok)

def leer_pdf(archivo):
    reader = PyPDF2.PdfFileReader(archivo)
    cant_pags=reader.getNumPages()
    string_lectura= reader.getPage(0).extractText()
    print(cant_pags)
    for i in range(cant_pags):
        string_lectura = string_lectura + reader.getPage(i).extractText()

    return string_lectura


oracion1="Juan se compró dos perro, cinco ornitorrincos y un gato. A Juan no le gustan los gatos ni los ortnitorrincos, pero venían de oferta con los perros."
oracion2="Rodrigo estaba sentado en el patio, recordando cuando jugaba allí con sus amigos, cuando eran chicos. Rodrigo disfrutaba sus bellos recuerdos."

analizar_oracion(oracion1, True)

analizar_oracion(oracion2, True)
corpus_file = open("El gato negro.pdf", "rb")
string_cuento = leer_pdf(corpus_file)

print("------------------------------------------Análisis de un cuento de Edgar Allan Poe------------------------------------------")
analizar_oracion(string_cuento,False)






