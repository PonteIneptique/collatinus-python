from .ch import atone, deramise, communes, clean_double_diacritic
import warnings
import re
from .util import DefaultOrderedDict


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

    def __init__(self, linea, origin, parent):
        """ Constructeur de la classe Lemme à partire de la ligne linea.
            *parent est le lemmatiseur (classe Lemmat).

        Exemple de linea avec numéro d'éclat:
            # cădo|lego|cĕcĭd|cās|is, ere, cecidi, casum|687
            #   0 | 1  | 2   | 3 |     4                | 5

        :param linea: Ligne à parser
        :type linea: str
        :param origin: NO FUCKING IDEA
        :type origin: ?
        :param parent: Lemmatiseur
        :type parent: pycollatinus.Lemmatiseur
        """
        self._lemmatiseur = parent
        self._radicaux = DefaultOrderedDict(list)
        self._irregs = []  # list of Irreg
        self._morphosIrrExcl = []  # list of int

        eclats = linea.split('|')
        lg = eclats[0].split('=')

        self._cle = atone(deramise(lg[0]))
        self._nh = 0
        self._grd = self.oteNh(lg[0])  # TODO: Cette ligne pose un problè : d'ou vient le _nh

        if len(lg) == 1:
            self._grq = self._grd
        else:
            self._grq = lg[1]

        # pour l'affichage des dictionnaires, élimine les doubles de la forme canonique
        self._gr = atone(self._grq.split(",")[0])  # TODO : À verifier
        self._grModele = eclats[1]
        self._modele = self._lemmatiseur.modele(self._grModele)
        self._hyphen = ""
        self._origin = origin

        # Tous les lemmes doivent avoir été rencontrés une fois
        self._nbOcc = 1

        # contrôle de format. la liste doit avoir 6 items
        if len(eclats) < 6:
            warnings.warn("Ligne mal formée : " + self._gr + "\n ---Dernier champ " + eclats[-1] + "\n ---" +linea)

        # lecture des radicaux, 2 et 3
        for i in range(2, 4):
            if eclats[i]:
                lrad = eclats[i].split(',')
                for rad in lrad:
                    self._radicaux[i-1].append(Radical(rad, i-1, self))

        self._lemmatiseur.ajRadicaux(self)

        # Gros doute sur le fonctionnement ici
        self._indMorph = eclats[4]
        match_renvoi = Lemme.RENVOI.match(self._indMorph)
        if match_renvoi is not None:
            self._renvoi = match_renvoi.group(1)
        else:
            self._renvoi = ""

        self._pos = ""
        if "adj." in self._indMorph:
            self._pos += 'a'
        if "conj" in self._indMorph:
            self._pos += 'c'
        if "excl." in self._indMorph:
            self._pos += 'e'
        if "interj" in self._indMorph:
            self._pos += 'i'
        if "num." in self._indMorph:
            self._pos += 'm'
        if "pron." in self._indMorph:
            self._pos += 'p'
        if "prép" in self._indMorph:
            self._pos += 'r'
        if "adv" in self._indMorph:
            self._pos += 'd'
        if " nom " in self._indMorph:
            self._pos += 'n'
        if "npr." in self._indMorph:
            self._pos += 'n'
        if not self._pos:
            self._pos = self._modele.pos()
            # Je prends le POS du modèle
            if self._pos == "d" and self._renvoi:
                self._pos = ""
            # S'il y a un renvoi (cf.) et que le modèle a donné le POS "d" (adverbe),
            # je prendrai le pos du renvoi (les indéclinables ont le POS par défaut "d").
            # Je ne peux pas le faire maintenant !

        # nombre d'occurrences
        if len(eclats[5]):
            self._nbOcc = int(eclats[5])
        else:
            self._nbOcc = 0

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

    def ajNombre(self, n):
        """ Ajoute l'entier n au nombre d'occurrences du lemme.

        :note: Un lemme de Collatinus peut être associé à plusieurs lemmes du LASLA, d'où la somme.
        """
        self._nbOcc += n
        # Un lemme de Collatinus peut être associé à plusieurs lemmes du LASLA.
        # D'où la somme.

    def ajRadical(self, i, r=None):
        """ Ajoute le radical r de numéro i à la map des radicaux du lemme.

        :param i: Index de radical
        :type i: int
        :param r: Radical à ajouter
        :type r: Radical
        """
        if r:
            self._radicaux[i] = r

    def ajTrad(self, t, l):
        """ Ajoute la traduction t de langue l à la map des traductions du lemme."""
        pass

    def ambrogio(self):
        """ Renvoie dans une chaîne un résumé de la traduction du lemme dans toutes les langues cibles disponibles."""
        pass

    def cle(self):
        """ Renvoie la clé sous laquel le lemme est enregistré dans le lemmatiseur parent.

        :return:
        :rtype:
        """
        return self._cle

    def clesR(self):
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

    def oteNh(self, g):
        """ Supprime le dernier caractère de g si c'est un nombre et
        renvoie le résultat après avoir donné la valeur de ce nombre à nh.

        :param g: Chaîne
        :type g: str
        :return: Chaîne sans le numéro
        :rtype: str
        """

        c = g[-1]
        if c.isnumeric():
            self._nh = int(c)
            g = g[:-1]
        return g

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
                forms.append(self.radical(desinence.numRad()).gr() + desinence.gr())
        return list(set(forms))
