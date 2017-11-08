from pycollatinus.lemmatiseur import Lemmatiseur

l = Lemmatiseur.load()

_print = lambda x: print(list(x))

_print(l.lemmatise("exspirasset"))
_print(l.lemmatise("adprehendant"))
_print(l.lemmatise("legarat"))
_print(l.lemmatise("exspectari"))
_print(l.lemmatise("vexassent"))
_print(l.lemmatise("vexavissent"))