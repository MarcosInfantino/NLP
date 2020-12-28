##NLTK environment
import nltk
import numpy as np
##nltk.download()
from nltk.book import *

##Part of speech tagsets
print("---------------------------------------------------------------TAGSET UPENN COMPLETO---------------------------------------------------------------")
nltk.help.upenn_tagset(".*")
print("---------------------------------------------------------------TAGS DE NOUNS UPENN---------------------------------------------------------------")
nltk.help.upenn_tagset("NN*")
print("---------------------------------------------------------------TAGS DE VERBS UPENN---------------------------------------------------------------")
nltk.help.upenn_tagset("VB")

# Hay cuatro categorias de sustantivos y una de verbos en UPENN

## Categorias de NOUNS en  Upenn
##NN: son aquellos sustantivos comunes en singular
##NNP: son aquellos sustantivos propios en singular
##NNPS: son aquellos sustantivos propios en plural
##NNS: son aquellos sustantivos comunes en plural

print("---------------------------------------------------------------TAGSET BROWN COMPLETO---------------------------------------------------------------")
nltk.help.brown_tagset(".*")
print("---------------------------------------------------------------TAGS DE NOUNS BROWN---------------------------------------------------------------")
nltk.help.brown_tagset("NN*")
print("---------------------------------------------------------------TAGS DE VERBS BROWN--------------------------------------------------------------")
nltk.help.brown_tagset("VB")

##Explorando el tagged corpora

from nltk.corpus import treebank
treebank.fileids()
print("---------------------------------------------------------------ÄRCHIVO wsj_0001.mrg ENTERO CON TAGS---------------------------------------------------------------")

wsj_0001_TAGGED=treebank.tagged_words("wsj_0001.mrg")[0:]

for x in wsj_0001_TAGGED:
    print(x)

print("---------------------------------------------------------------PRIMERAS 100 PALABRAS DEL ÄRCHIVO wsj_0003.mrg CON TAGS---------------------------------------------------------------")

wsj_0003_TAGGED=treebank.tagged_words("wsj_0003.mrg")[0:100]

for x in wsj_0003_TAGGED:
    print(x)

##Contando desde un corpora
race_noun = nltk.tag.str2tuple("race/NN")
race_verb = nltk.tag.str2tuple("race/VB")

from nltk.corpus import brown

len_tagged_words=len(brown.tagged_words())

count_race_noun=brown.tagged_words().count(race_noun)
count_race_verb=brown.tagged_words().count(race_verb)

frecuencia_uso_noun= count_race_noun/len_tagged_words
frecuencia_uso_verb= count_race_verb/len_tagged_words

print("Frecuencia uso de la palabra race como NOUN:", frecuencia_uso_noun)
print("Frecuencia uso de la palabra race como VERB:", frecuencia_uso_verb)

if(frecuencia_uso_noun > frecuencia_uso_verb):
    print("SE UTILIZA MAS COMO NOUN")
elif(frecuencia_uso_noun < frecuencia_uso_verb):
        print("SE UTILIZA MAS COMO VERB")
else:
    print("SE UTLIZA TANTO EN FORMA DE VERB COMO EN FORMA DE NOUN")

##El POS tagger HMM que se detalla en las diapositivas de la clase, usa dos fuentes de
##información. Una es la probabilidad de una palabra dado un tag particular, p(w i |t i ).
##La otra es la probabilidad de aparicion de un tag i habiendo aparecido antes un tag i-1, p(t i| t i-1)

## Aplicando POS tagging a una nueva oración
unigram_tagger = nltk.tag.UnigramTagger(brown.tagged_sents(categories="news")[:5000])

from nltk import word_tokenize
from nltk.tag import hmm

cadena = "The Secretariat is expected to race tomorrow."

cadena_tok = word_tokenize(cadena)

cadena_tag_unigram=unigram_tagger.tag(cadena_tok)

hmm_tagger =hmm.HiddenMarkovModelTrainer().train_supervised(brown.tagged_sents(categories="news")[:5000])

cadena_tag_hmm=hmm_tagger.tag(cadena_tok)

print("Oracion: ",cadena)
print("Taggeada con UNIGRAM tagger:")

for x in cadena_tag_unigram:
    print(x)

print("Taggeada con HMM tagger:")

for x in cadena_tag_hmm:
    print(x)



cadena2= "Juvenile Court to Try Shooting Defendant"

cadena2_tok = word_tokenize(cadena2)
cadena2_tag_hmm=hmm_tagger.tag(cadena2_tok)

print("Oracion: ", cadena2)

print("Taggeada con HMM tagger:")

for x in cadena2_tag_hmm:
    print(x)

