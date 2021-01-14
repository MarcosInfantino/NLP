import pytest
import mainFunctions
import docs

def test_method1(): ##1.	Dos textos idénticos deben dar similitud >= 99%
    doc1 = doc2 = docs.Doc.newDoc("C:/dataset-nlp-plagio-utn/Trabajo Práctico 1 - Hernan Dalle Nogare.docx")
    assert mainFunctions.JaccardScorePlainText(doc1.text, doc2.text) > 99

def test_method2():##Dos textos completamente diferentes dan una similitud menor al 10%
    s1 = "Rodrigo estaba paseando a su perro, cuando de repente vio un cerdo volar."
    s2 = "A juan le gustan mucho las hamburguesas y las papas fritas."
    assert mainFunctions.JaccardScorePlainText(s1, s2) < 10

def test_method3():##Una cita sin referencia correspondiente penaliza el score final
    s1 = "Rodrigo estaba paseando a su perro, cuando de repente vio un cerdo volar."
    s1CopyWithCitation = "Rodrigo estaba paseando a su perro (Sentence1, 2021)."
    s1CopyWithoutCitation = "Rodrigo estaba paseqando a su perro."

    assert mainFunctions.JaccardScorePlainText(s1, s1CopyWithoutCitation) > mainFunctions.JaccardScorePlainText(s1, s1CopyWithCitation)

def test_method4():##El algoritmo debe comprender las distintas formas validas de citar una referencia externa
    s1 = "Rodrigo estaba paseando a su perro, cuando de repente vio un cerdo volar"
    apaCitations = []
    citationIso = "Según [1], "
    apaCitations.append("(Despotovic-Zrakic et al., 2012)")
    apaCitations.append("(Anónimo, 2010)")
    apaCitations.append("(Sabbagh, 2010a)")
    apaCitations.append("(Sabbagh, 2010b)")
    apaCitations.append("(\"Barcelona to Ban Burqa\", 2010)")


    assert docs.hasCitations(citationIso + s1)
    for s in apaCitations:
        assert(docs.hasCitations(s))

def test_method5():##Dos oraciones identicas en textos distintos aumentan la similitud
    doc1 = docs.Doc.newDoc("C:/dataset-nlp-plagio-utn/Trabajo Práctico 1 - Hernan Dalle Nogare.docx")
    doc2 = docs.Doc.newDoc("C:/dataset-nlp-plagio-utn/TP 3 The experience economy (1).docx")
    addedSentence = "Esta es una nueva oración para testear si aumenta la similitud entre ambos documentos."
    assert mainFunctions.JaccardScorePlainText(doc1.text + addedSentence, doc2.text + addedSentence) > mainFunctions.JaccardScorePlainText(doc1.text, doc2.text)

def test_method6():##una copia parcial de una oracion penaliza la oracion, aunque menos que si la copia fuera total
    s1 = "Spiderman salvó a la mujer que estaba atrapada bajo los escombros del edificio en llamas."
    s1PartialCopy = "Ironman salvó al hombre que estaba atrapado dentro del edifico en llamas."
    s1FullCopy = s1

    assert mainFunctions.JaccardScorePlainText(s1, s1PartialCopy) > 0 and \
           (mainFunctions.JaccardScorePlainText(s1, s1FullCopy) > mainFunctions.JaccardScorePlainText(s1, s1PartialCopy))


def test_method7():
    doc1 = docs.Doc.newDoc("C:/dataset-nlp-plagio-utn/Marketing - TP 0.docx")

    assert mainFunctions.compareDocuments(doc1, doc1) > 99
