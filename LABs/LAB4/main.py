import nltk
##nltk.download()
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

##lemas para el segundo sentido de dog
print("Lemas para el segundo sentido de dog:")
print(wn.synset("dog.n.02").lemmas())

print("--------------------------------------------------------------------------------------")
print("Definición de flag.n.07:")
print(wn.synset("flag.n.07").definition())
print("--------------------------------------------------------------------------------------")
print("Definición de canis.n.01:")
print(wn.synset("canis.n.01").definition())
print("--------------------------------------------------------------------------------------")
print("Definición de pack.n.06:")
print(wn.synset("pack.n.06").definition())
print("--------------------------------------------------------------------------------------")
print("flag es merónimo de dog porque se refiere a la cola, que es una subparte del perro")
print("canis es holónimo de dog porque se refiere a la especie a la cual el perro pertenece")
print("pack es holónimo de dog porque se refiere a la jauría, un grupo de perros")
print("--------------------------------------------------------------------------------------")
synsets_bank_nouns = [x for x in wn.synsets("bank") if x.pos() == "n"]
synsets_bank = wn.synsets("bank")
print("synsets de bank(nouns):")
print(synsets_bank_nouns)
print("definiciones de synsets de bank (nouns):")
print([x.definition() for x in synsets_bank_nouns])
print("Existen ", len(synsets_bank), " synsets de bank")
print("Existen ", len(synsets_bank_nouns), " synsets de bank que son sustantivos")
print("El synset correcto, en mi opinión, para la oracion mencionada, es Synset('bank.n.02'), cuya definicion es: ", synsets_bank[1].definition())

S = "The bank can guarantee deposits will eventually cover future tuition costs because it invests in adjustable-rate mortgage securities."
S_tok = word_tokenize(S)
print("El synset elegio por Lesk es: ", lesk(S_tok, "bank", "n"), ", cuya deifnicion es: ", lesk(S_tok, "bank", "n").definition())

l = word_tokenize((wn.synset("bank.n.05").definition()))
m = word_tokenize((wn.synset("bank.n.02").definition()))

k = set(S_tok)
print("Elementos que intersectan a la oracion con bank.n.05: ", k.intersection(l))
print("Elementos que intersectan a la oracion con bank.n.02: ", k.intersection(m))
print("Como bank.n.05 posee mayor cantidad de elementos en la interseccion, el mismo es elegido por lesk")

print("------------------------------------------PRUEBA DE LESK CON ORACIONES--------------------------------------------")

def mostrar_oracion_lesk(oracion, palabra, pos, sentido):

    print("Oracion: ", oracion)
    print("Palabra: ", palabra)
    synset_sugerido = wn.synset(sentido)
    print("Sentido correcto: ", synset_sugerido, ". Y su definicion es: ", synset_sugerido.definition())
    synset_lesk = lesk(word_tokenize(oracion), palabra, pos)
    print("Sentido obtenido por lesk: ", synset_lesk, ". Y su definicion es: ", synset_lesk.definition())

    if(synset_lesk == synset_sugerido):
        print("PRECISION CORRECTA")
    else:
        print("PRECISION INCORRECTA")
    print(" ")




mostrar_oracion_lesk("I went to the bank to deposit some money.", "bank", "n", "bank.n.02")

mostrar_oracion_lesk("She created a big mess of the birthday cake.", "mess", "n", "mess.n.01")

mostrar_oracion_lesk("In the interest of your safety, please wear your seatbelt.", "safety", "n", "safety.n.01")

mostrar_oracion_lesk("I drank some ice cold water.", "water", "n","water.n.06")


print("------------------------------------------ALGORITMO DE INTERSECCION UTILIZANDO LEMMATIZER--------------------------------------------")

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wn.ADJ
    elif treebank_tag.startswith('V'):
        return wn.VERB
    elif treebank_tag.startswith('N'):
        return wn.NOUN
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        return wn.NOUN

def matching_words (sentence1, sentence2):
    lemmatizer = WordNetLemmatizer()
    s1_tok = [x for x in word_tokenize(sentence1) if x.isalnum()]
    s1_tok = nltk.pos_tag(s1_tok)

    s2_tok = [x for x in word_tokenize(sentence2) if x.isalnum()]
    s2_tok = nltk.pos_tag(s2_tok)

    s1_lemma = [lemmatizer.lemmatize(x[0], get_wordnet_pos(x[1])) for x in s1_tok]
    s2_lemma = [lemmatizer.lemmatize(x[0], get_wordnet_pos(x[1])) for x in s2_tok]
    return set(s1_lemma).intersection(s2_lemma)

def mostrar_prueba(num, s1, s2):
    print("CASO DE PRUEBA ", num, " :")
    print("Oracion 1: ", s1)
    print("Oracion 2:", s2)
    print("Resultado interseccion: ", matching_words(s1,s2))
    print(" ")


s1 = "He was walking his dog."
s2 = "He was walking three dogs."
mostrar_prueba(1,s1,s2)

s1 = "Rodrigo has two cars and a house."
s2 = "Rodrigo has a car and two houses."
mostrar_prueba(2,s1,s2)

s1 = "Holiday from Green Day is one of my favourite songs."
s2 = "I do not know how to compose a song."
mostrar_prueba(3,s1,s2)


