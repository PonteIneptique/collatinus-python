from .ch import atone
from .modele import Modele


class Irreg(object):
    def __init__(self, l, parent=None):
        """ Constructeur de la classe Irreg.

        :param l: Ligne de chargement des irréguliers
        :type l: str
        :param parent: Lemmatiseur
        :type parent: pycollatinus.lemmatiseur.Lemmatiseur
        """
        if parent:
            self._lemmat = parent
        ecl = l.split(':')
        self._grq = ecl[0]
        self._exclusif = False
        if self._grq.endswith("*"):
            self._grq = self._grq[:-1]
            self._exclusif = True

        self._gr = atone(self._grq)
        self._lemme = self._lemmat.lemme(ecl[1])
        self._morphos = Modele.listeI(ecl[2])

    def exclusif(self):
        """ True si le lemmes est exclusif, c'est à dire si la forme régulière calculée par le modèle est inusitée, remplace par la forme irrégulière.

        :return: si le lemmes est exclusif
        :rtype: bool
        """
        return self._exclusif

    def gr(self):
        """ Graphie ramiste sans diacritique.

        :return: Graphie ramiste sans diacritique.
        :rtype: str
        """
        return self._gr

    def grq(self):
        """ Graphie ramiste avec diacritiques.

        :return: Graphie ramiset avec diacritiques.
        :rtype: str
        """
        return self._grq

    def lemme(self):
        """ Le lemme de l'irrégulier.

        :return: Le lemme de l'irrégulier.
        :rtype: pycollatinus.lemme.Lemme
        """
        return self._lemme

    def morphos(self):
        """  Liste des numéros de morphos que peut prendre l'irrégulier, en tenant compte des quantités.

        :return: Liste des numéros de morphos que peut prendre l'irrégulier, en tenant compte des quantités.
        :rtype: list of int
        """
        return self._morphos

    def pos(self):
        """ Return the pos of the parent

        :rtype: str
        """
        return self.lemme().pos()

    def cle(self):
        return self.lemme().cle()

    def possible_forms(self):
        """ Generate a list of possible forms for the current lemma

        :returns: List of possible forms for the current lemma
        :rtype: [str]
        """
        return list(set(self.lemme().possible_forms() + [self.gr()]))

