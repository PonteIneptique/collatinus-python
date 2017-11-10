import re
from .ch import atone
from .util import DefaultOrderedDict


class Desinence(object):
    def __repr__(self):
        return "<pycollatinus.modele.Desinence[{};{};{}]>".format(self.gr(), self.morphoNum(), self.numRad())

    def __init__(self, d, morph, nr, parent=None):
        """ Desinence

        :param d: Graphie avec quantités 
        :type d: str
        :param morph: Numéro de morphologie
        :type morph: int
        :param nr: Numéro de radical accepté par la désinence
        :type nr: int
        :param parent: modèle du lemme et du radical qui utilisent cette désinence
        :type parent: Modele
        """

        # der, dernier caractère de d, s'il est un nombre, le degré de
        # rareté de la désinence, est 10 par défaut.

        self._rarete = 10
        if d and d[-1].isdigit():
            der = int(d[-1])
            self._rarete = der
            d = d[:-1]

        # '-' est la désinence zéro
        if d == "-":
            d = ""
        self._grq = d
        self._gr = atone(self._grq)
        self._morpho = morph
        self._numR = nr
        self._modele = parent

    def gr(self):
        """ Graphie de la désinence, et sans quantités.

        :return: Graphie de la désinence, et sans quantités.
        :rtype: str
        """
        return self._gr

    def grq(self):
        """ Graphie ramiste avec quantités.

        :return: Graphie ramiste avec quantités.
        :rtype: str
        """
        return self._grq

    def modele(self):
        """ Modèle de la désinence.

        :return: Modèle de la désinence.
        :rtype: Modele
        """
        return self._modele

    def rarete(self):
        """ Rareté de la désinence, est 10 par défaut.

        :return: rareté de la désinence, est 10 par défaut.
        :rtype: int
        """
        return self._rarete

    def morphoNum(self):
        """ Numéro de morpho de la désinence.

        :return: Numéro de morpho de la désinence.
        :rtype: int
        """
        return self._morpho

    def numRad(self):
        """ Numéro de radical de la désinence.

        :return: Numéro de radical de la désinence.
        :rtype: int
        """
        return self._numR

    def setModele(self, *m):
        """ Attribue un modèle à la désinence.

        :param m: Modele à attribuer
        :type m: Modele
        """
        self._modele = m


class Modele(object):
    """ Constructeur de la classe modèle.

    :param graphie: Graphie du modele
    :param graphie_accentuee: Graphie accentuée du modèle
    :param parent: Lemmatiseur
    :type parent: pycollatinus.lemmatiseur.Lemmatiseur
    :param pere: Modele from which the modele derive
    :type pere: Modele
    """
    RE = re.compile("[:;]*([\\w]*)\\+{0,1}(\\$\\w+)")

    def __repr__(self):
        return "<pycollatinus.modele.Modele[{}]>".format(self.gr())

    def __init__(self, graphie: str, graphie_accentuee: str, parent=None, pere=None, pos=""):
        self._lemmatiseur = parent
        self._pere = pere
        self._desinences = DefaultOrderedDict(list)
        self.msuff = DefaultOrderedDict(list)  # list of int
        self._absents = []  # List of int
        self._genRadicaux = {}  # int -> str
        self._gr = graphie
        self._grq = graphie_accentuee
        self._pos = pos

    def hasRadical(self, numRad):
        """ Vérifie que l'objet à le radical donné

        :param numRad: Identifiant de radical
        :type numRad: int
        :return: Si l'objet à la radical
        :rtype: bool
        """
        return numRad in self._genRadicaux

    def absent(self, a):
        """ Renvoie True si la morpho de rang a n'existe pas dans le modèle. 

        Certains modèles, exemple, n'ont pas de singulier, certains verbes n'ont pas de passif.

        :return: Si la morpho de rang a n'existe pas dans le modèle
        :rtype: bool
        """
        return a in self._absents

    def absents(self):
        """ Retourne la liste des numéros des morphos absentes.

        :return: Liste des numéros des morphos absentes.
        :rtype: list of int
        """
        return self._absents

    def cles_radicaux(self):
        """ Liste des numéros de radicaux utilisés, et rangés dans la map _genRadicaux.

        :return: Liste des numéros de radicaux utilisés, et rangés dans la map _genRadicaux.
        :rtype: list of int
        """
        return sorted(list(self._genRadicaux.keys()))

    def clone(self, d):
        """ Crée une Désinence copiée sur la désinence d.

        :param d: Desinence à copier
        :type d: Desinence 
        :return: Désinence copiée sur la désinence d.
        :rtype: Desinence
        """
        return Desinence(d.grq(), d.morphoNum(), d.numRad(), self)

    def deja(self, m):
        """ Renvoie True si la désinence a une morpho de rang m. 

        Permet de savoir s'il faut aller chercher la désinence de morpho m chez le modèle père.

        :return: Si la désinence a une morpho de rang m. 
        :rtype: bool
        """
        return m in self._desinences

    def desinences(self, d=None):
        """ Renvoie la liste des désinence de morpho d du modèle.

        :param d: Identifant de morphologie
        :type d: int
        :return: Liste des désinence de morpho d du modèle ou toutes les désinences du modèle (Applaties en python, doute sur original)
        :rtype: list of Desinence
        """
        if d:
            return self._desinences[d]
        return [x for morpho_values in self._desinences.values() for x in morpho_values]

    def estUn(self, m):
        """ Renvoie True si le modèle se nomme m, si l'un de ses ancêtre se nomme m

        :param m: Nom de modele
        :type m: str
        :return: si le modèle se nomme m, si l'un de ses ancêtre se nomme m
        :rtype: bool
        """
        if self._gr == m:
            return True
        if self._pere is not None:
            return self._pere.estUn(m)
        return False

    def gr(self):
        """ Nom du modèle

        :return: Nom du modèle.
        :rtype: str
        """
        return self._gr

    def genRadical(self, r):
        """ Chaîne permettant de calculer un radical à partir de la forme canonique d'un lemme. 

        :param r: Numéro du radical
        :type r: int
        :return: Chaîne permettant de calculer un radical à partir de la forme canonique d'un lemme. 
        :rtype: str
        """
        return self._genRadicaux[r]

    def morphos(self):
        """ Liste des numéros des désinences définies par le modèle.

        :return: Liste des numéros des désinences définies par le modèle.
        :rtype: list of int
        """
        return list(self._desinences.keys())

    def set_pos(self, pos: str):
        """ Change la POS du modele

        :param pos: Part Of Speech of the modele
        :type pos: str
        """
        self._pos = pos

    def pos(self):
        """ Retourne la catégorie du modèle, utilisant les ancêtres du modèle.

        :return: Catégorie du modèle
        :rtype: str
        """
        return self._pos
