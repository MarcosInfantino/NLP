from nltk.corpus import wordnet as wn

def mostrar_synsets_defs(palabra):
    synsets= wn.synsets(palabra)
    for i in range(len(synsets)-1):
        print("Synset: ", synsets[i],"/Definicion: ", synsets[i].definition())
