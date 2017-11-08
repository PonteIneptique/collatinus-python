from pycollatinus.lemmatiseur import Lemmatiseur

l = Lemmatiseur.load()

print(l.lemmatise("exspirasset"))
print(l.lemmatise("adprehendant"))
print(l.lemmatise(""))
print(l.lemmatise("exspectari"))
print(l.lemmatise("vexassent"))
print(l.lemmatise("vexavissent"))