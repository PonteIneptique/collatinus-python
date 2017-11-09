from .ch import atone, communes
import re
from .util import DefaultOrderedDict
from .modele import Modele


class Radical(object):
    def __init__(self, g, n, parent=None):
        """ Représentation d'un radical

        :param g: Forme canonique du radical avec quantité
        :type g: str
        :param n: Numéro du radical
        :type n: int
        """
        self._lemme = parent
        self._grq = communes(g)
        self._gr = atone(g)
        self._numero = n

    def gr(self):
        """ Renvoie la graphie du radical dépourvue de diacritiques.

         :return: Graphie du radical dépourvue de diacritiques.
        :rtype: str
        """
        return self._gr

    def grq(self):
        """ Renvoie la graphie du radical pourvue de ѕes diacritiques.

        :return: raphie du radical pourvue de ѕes diacritiques.
        :rtype: str
        """
        return self._grq

    def lemme(self):
        """ Le lemme auquel appartient le radical.

        :return: Le lemme auquel appartient le radical.
        :rtype: Lemme
        """
        return self._lemme

    def set_lemme(self, lemme):
        """ Set the parent lemme

        :param lemme: Lemme
        :type lemme: Lemme
        """

        self._lemme = lemme

    def modele(self):
        """ Le modèle de flexion du radical

        :return: Le modèle de flexion du radical
        :rtype: str
        """
        return self._lemme.modele()

    def numRad(self):
        """ Le numéro du radical.

        :return: Le numéro du radical.
        :rtype: int
        """
        return self._numero

    def __repr__(self):
        return "<pycollatinus.lemme.Radical[{}:{}]>".format(self.gr(), self.numRad())


class Lemme(object):
    RENVOI = re.compile("cf\\.\\s(\\w+)$")

    def __repr__(self):
        return "<pycollatinus.lemme.Lemme[{}:modele-{}]>".format(self.cle(), self.grModele())

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __init__(self,
                 cle: str, graphie: str, graphie_accentuee: str,
                 modele: Modele, parent,
                 radicaux: DefaultOrderedDict=None, origin: int =0, pos: str="-",
                 nombre_homonymie: int=0, nbOcc: int=0):
        """  Generate a lemma object

        :param cle: Unique Identifier of the Lemma
        :type cle: str
        :param graphie: Graphie
        :type graphie: str
        :param graphie_accentuee: Accentuated Graphie
        :type graphie_accentuee: str
        :param modele: Modele of the Lemma
        :type modele: pycollatinus.modele.Modele
        :param parent: Lemmatiseur
        :type parent: pycollatinus.Lemmatiseur
        :param radicaux: Dictionary of list of radicaux
        :type radicaux: DefaultOrderedDict(list)
        :param origin: Origin of the lemma (0 curated, 1 automatic import)
        :type origin: int
        :param pos: POS tag
        :type pos: str
        :param nombre_homonymie: Number to distinguish homonyms
        :type nombre_homonymie: int
        :param nbOcc: Number of known occurences
        :type nbOcc: int
        """
        self._lemmatiseur = parent
        self._radicaux = radicaux or DefaultOrderedDict(list)
        self._irregs = []  # list of Irreg
        self._morphosIrrExcl = []  # list of int
        self._nh = nombre_homonymie
        self._nbOcc = nbOcc
        self._cle = cle
        self._grq = graphie_accentuee
        self._gr = graphie
        self._grModele = modele.gr()
        self._modele = modele
        self._indMorph = ""
        self._renvoi = None
        self._origin = origin
        self._pos = pos

    def ajIrreg(self, irr):
        """ Ajoute au lemme l'obet irr, représente
                 une forme irrégulière. Lorsque les formes irrégulières
                 sont trop nombreuses, lorsque plusieurs lemmes
                 ont des formes analogues, vaut ajouter un modèle
                 dans data/modeles.la.

        :param irr: Irrégulier
        :type irr: pycollatinus.irregs.Irreg
        """
        self._irregs.append(irr)
        # ajouter les numéros de morpho à la liste
        # des morphos irrégulières du lemme :
        if irr.exclusif():
            self._morphosIrrExcl += irr.morphos()

    def ajRadical(self, i, r=None):
        """ Ajoute le radical r de numéro i à la map des radicaux du lemme.

        :param i: Index de radical
        :type i: int
        :param r: Radical à ajouter
        :type r: Radical
        """
        if r:
            self._radicaux[i].append(r)

    def cle(self):
        """ Renvoie la clé sous laquel le lemme est enregistré dans le lemmatiseur parent.

        :return:
        :rtype:
        """
        return self._cle

    def cles_radicaux(self):
        """ Retourne toutes les clés (formes non-ramistes sans diacritiques) de la map des radicaux du lemme.
        """
        return self._radicaux.keys()

    def estIrregExcl(self, nm):
        """ Renvoie vrai si la forme irrégulière avec le n° nm remplace celle construite sur le radical , si la forme régulière existe aussi.

        :param nm: Numéro de morpho
        :type nm: int
        :return: Statut de forme irrégulière
        :rtype: bool
        """
        return nm in self._morphosIrrExcl

    def genre(self):
        """ Cette routine convertit les indications morphologiques, données dans le fichier lemmes.la, pour exprimer le genre du mot dans la langue courante.

        :return: Genre
        :rtype: str
        """
        _genre = ""
        if " m." in self._indMorph:
            _genre += "m"
        if " f." in self._indMorph:
            _genre += "f"
        if " n." in self._indMorph:
            _genre += "n"
        _genre = _genre.strip()
        if self._renvoi and not _genre:
            lr = self._lemmatiseur.lemme(self._renvoi)
            if lr:
                return lr.genre()

        return _genre

    def gr(self):
        """ Retourne la graphie ramiste du lemme sans diacritiques.

        :return: Graphie ramiste du lemme sans diacritiques.
        :rtype: str
        """
        return self._gr

    def grq(self):
        """ Retourne la graphie ramiste du lemme sans diacritiques.

        :return: Graphie ramiste du lemme sans diacritiques.
        :rtype: str
        """
        return self._grq

    def grModele(self):
        """ Retourne la graphie du modèle du lemme.

        :return: Graphie du modèle du lemme.
        :rtype: ???
        """
        return self._grModele

    def indMorph(self):
        """ Returne l'index de morphologie
        """
        return self._indMorph

    def irreg(self, i):
        """ Renvoie la forme irrégulière de morpho i. excl devient True si elle est exclusive, sinon.

        :return: Forme irrégulière de morpho i, Exclusivité
        :rtype: tuple.<str, bool>
        """
        excl = False
        for ir in self._irregs:
            if i in ir.morphos():
                return ir.grq(), ir.exclusif
        return "", excl

    def modele(self):
        """ Renvoie l'objet modèle du lemme.

        :return: Modèle du lemme
        :rtype: pycollatinus.modele.Modele
        """
        return self._modele

    def nbOcc(self):
        """ Renvoie le nombre d'occurrences du lemme dans les textes du LASLA.

        :return: Nombre d'occurrences du lemme dans les textes du LASLA.
        :rtype: int
        """
        return self._nbOcc

    def clearOcc(self):
        """ Initialise le nombre d'occurrences. """
        self._nbOcc = 1

    def nh(self):
        """ Renvoie le numéro d'homonymie du lemme.

        :return: Numéro d'homonymie du lemme.
        :rtype: int
        """
        return self._nh

    def origin(self):
        """ Renvoie l'origine du lemme : 0 pour le lexique de base, pour l'extension. 

        :return: Origine du lemme : 0 pour le lexique de base, pour l'extension. 
        :rtype: int
        """
        return self._origin

    def pos(self):
        """ Renvoie un caractère représentant la catégorie (part of speech, orationis) du lemme.

        :return: Caractère représentant la catégorie (part of speech, orationis) du lemme.
        :rtype: str
        """
        if not self._pos and self._renvoi:
            lr = self._lemmatiseur.lemme(self._renvoi)
            if lr:
                return lr.pos()
        return self._pos

    def radical(self, r):
        """  Renvoie le radical numéro r du lemme.
        
        :param r: Numéro de radical
        :type r: int
        :return: Radicaux enregistré au numéro R
        :rtype: list of Radical
        """
        return self._radicaux[r]

    def renvoi(self):
        """ Renvoie True si le lemme est une forme alternative renvoyant à une autre entrée du lexique.

        :return: Statut forme alternative renvoyant à une autre entrée du lexique
        :rtype: bool
        """
        return "cf. " in self._indMorph

    def traduction(self, l):
        """ Renvoie la traduction du lemme dans la langue cible l (2 caractères, plus
         pour donner l'ordre des langues de secours). J'ai opté pour un format "l1.l2.l3" où les trois langues sont en 2 caractères.
        """
        pass

    def __lt__(self, l):
        """ Vrai si la fréquence du lemme de gauche est inférieure à celle de celui de droite. 

        commenté : vrai si la graphie du lemme de gauche précède celle de celui de droite dans l'ordre alphabétique.

        :param l: Other lemma
        :type l: Lemme
        :return: Fréquence du lemme de gauche est inférieure à celle de celui de droite. 
        :rtype: Bool
        """
        return self._nbOcc < l.nbOcc()

    def setHyphen(self, h):
        """ Stocke l'information sur la césure étymologique du lemme

        :param h: indique où se fait la césure. 
        :type h: int
        """
        self._hyphen = h

    def getHyphen(self):
        """ Retourne la césure étymologique du lemme

        :return: Césure étymologique du lemme
        """
        return self._hyphen

    def possible_forms(self):
        """ Generate a list of possible forms for the current lemma

        :returns: List of possible forms for the current lemma
        :rtype: [str]
        """
        forms = []
        for morph in self.modele().morphos():
            for desinence in self.modele().desinences(morph):
                radicaux = self.radical(desinence.numRad())
                if isinstance(radicaux, Radical):
                    forms.append(radicaux.gr() + desinence.gr())
                else:
                    for rad in radicaux:
                        forms.append(rad.gr() + desinence.gr())
        return list(set(forms))
