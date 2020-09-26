import nltk
#nl.download()
#nl.download("punkt")
from nltk.book import*

moby_dick=text1
wall_street=text7
tokens_moby_dick=moby_dick.tokens
moby_sin_puntuacion=[word for word in tokens_moby_dick if word.isalnum()]
moby_lower=[token.lower() for token in moby_sin_puntuacion]

tokens_wall_street=wall_street.tokens
wall_street_sin_puntuacion=[word for word in tokens_wall_street if word.isalnum()]
wall_street_lower=[token.lower() for token in wall_street_sin_puntuacion]


print("-------------------PUNTO 1------------------")
cant_tokens_moby=len(moby_lower)
cant_tokens_wall_street=len(wall_street_lower)
print("Cantidad de tokens en Moby Dick: {}".format(cant_tokens_moby)) # 218619
print("-------------------PUNTO 2------------------")
types_moby = len(set(moby_lower))
types_wall_street = len(set(wall_street_lower))
print("Cantidad de types en Moby Dick: {}".format(types_moby)) # 17139
print("-------------------PUNTO 3------------------")
print("type-token ratio para Moby Dick: {}".format(types_moby/cant_tokens_moby)) # 0.07839666268714064
print("-------------------PUNTO 4------------------")
print("type-token ratio para Wall Street: {}".format(types_wall_street/cant_tokens_wall_street)) # 0.12080105848651843
print("-------------------PUNTO 5------------------")
print("El Wall Street Journal posee mayor diversidad léxica")
print("-------------------PUNTO 6------------------")
print("El Wall Street Journal posee mayor diversidad léxica porque es un periódico, mientras que Moby Dick es una novela literaria.")
print("-------------------PUNTO 7------------------")


def mle(word, corpus):
    tokens = corpus.tokens
    tokens_sin_puntuacion = [word for word in tokens if word.isalnum()]
    tokens_to_lower = [token.lower() for token in tokens_sin_puntuacion]
    return corpus.count(word)/len(tokens_to_lower)


print("MLE de la palabra whale en Moby Dick = {}".format(mle("whale", moby_dick))) # 0.004144196067130487

print("-------------------PUNTO 8------------------")
print("MLE de la palabra whale en Wall Street Journal = {}".format(mle("whale", wall_street)))# 0.0


