from collections import OrderedDict, Callable
from .ch import clean_double_diacritic


class DefaultOrderedDict(OrderedDict):
    # Source: http://stackoverflow.com/a/6190500/562769
    def __init__(self, default_factory=None, *a, **kw):
        if (default_factory is not None and
           not isinstance(default_factory, Callable)):
            raise TypeError('first argument must be callable')
        OrderedDict.__init__(self, *a, **kw)
        self.default_factory = default_factory

    def __getitem__(self, key):
        try:
            return OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = self.default_factory,
        return type(self), args, None, None, iter(self.items())

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return type(self)(self.default_factory, self)

    def __deepcopy__(self, memo):
        import copy
        return type(self)(self.default_factory,
                          copy.deepcopy(self.items()))

    def __repr__(self):
        return 'OrderedDefaultDict(%s, %s)' % (self.default_factory, OrderedDict.__repr__(self))


def lignesFichier(nf):
    """ L'ensemble de lignes du fichier qui ne sont ni vides ni commentées.

        * Les fichiers de Collatinus ont adopté le point d'exclamation
        * en début de ligne pour introduire un commentaire.
        * Ces lignes doivent être ignorées par le programme.

    :param nf: Nom du fichier
    :type nf: str
    :yield: Ligne de fichier si ce n'est pas un commentaire
    :ytype: str
    """
    with open(nf) as file:
        for line in file.readlines():
            line = line.strip()
            if line and not line.startswith("!") and not line.startswith("! --- "):
                if "!" in line:
                    line, _ = tuple(line.split("!"))  # Suprimer les commentaires
                yield clean_double_diacritic(line)


def flatten(liste):
    return [x for y in liste for x in y]