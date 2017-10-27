import re
import warnings
from .ch import simplified, allonge, atone
from .util import DefaultOrderedDict, flatten
from .error import MissingRadical, UnknownModeleConfigurationKey


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
    RE = re.compile("[:;]*([\\w]*)\\+{0,1}(\\$\\w+)")
    CLEFS = [
            "modele",  # 0
            "pere",    # 1
            "des",     # 2
            "des+",    # 3
            "R",       # 4
            "abs",     # 5
            "suf",     # 6
            "sufd",    # 7
            "abs+",    # 8
    ]

    def __repr__(self):
        return "<pyollatinus.modele.Modele[{}]>".format(self.gr())

    def __init__(self, ll, parent=None):
        """ Constructeur de la classe modèle. 

        Chaque item de la liste ll est constitué de champs séparé par le caractère ':'. Le premier champ est un mot clé. Le parent est le lemmatiseur. 
        Pour le format du fichier data/modeles.la, la documentation utilisateur.

        :param ll: Liste de champs séparés par le caractère ":". Le premier champ est un mot-clef
        :param parent: Lemmatiseur
        :type parent: pycollatinus.lemmatiseur.Lemmatiseur

        :ivar _desinences: Dictionnaire de liste de désinences pour les morpho KEY
        :type _desinences: dict of list of Desinence
        """
        self._lemmatiseur = parent
        self._pere = 0
        self._desinences = DefaultOrderedDict(list)
        self.msuff = DefaultOrderedDict(list)  # list of int
        self._absents = []  # List of int
        self._genRadicaux = {}  # int -> str
        self._gr = ""
        self._grq = ""

        for original_l in ll:
            # remplacement des variables par leur valeur
            l = "" + original_l

            # TODO : Ajouté * pour la premiere capture pour rendre le prefix optionnel...
            for pre, v in Modele.RE.findall(l):
                var = self._lemmatiseur.variable(v)
                if pre:
                    var = var.replace(";", ";" + pre)
                l = l.replace(v, var)

            eclats = simplified(l).split(":")
            # modele pere des des  R   abs
            #  0      1    2   3   4   5

            p = Modele.CLEFS.index(eclats[0])
            if p == 0:  # modèle
                self._gr = eclats[1]
            elif p == 1:  # père
                self._pere = self._lemmatiseur.modele(eclats[1])
            elif p == 2 or p == 3:
                # des+: désinences s'ajoutant à celles du père
                # des: désinences écrasant celles du père
                index_morphologies = Modele.listeI(eclats[1])  # Anciennement li
                radical = int(eclats[2])  # Anciennement "r"
                liste_desinences = eclats[3].split(';')  # Anciennement "ld"
                for i in range(len(index_morphologies)):
                    if i < len(liste_desinences):
                        liste_desinences_definitives = liste_desinences[i].split(',')  # Anciennement "ldd"
                    else:
                        liste_desinences_definitives = liste_desinences[-1].split(',')

                    for graphie in liste_desinences_definitives:
                        nd = Desinence(graphie, index_morphologies[i], nr=radical, parent=self)
                        self._desinences[nd.morphoNum()].append(nd)
                        self._lemmatiseur.ajDesinence(nd)

                # si des+, chercher les autres désinences chez le père :
                if p == 3:
                    for i in index_morphologies:
                        for dp in self._pere.desinences(i):
                            dh = self.clone(dp)  # cloner la désinece
                            self._desinences[i].append(dh)
                            self._lemmatiseur.ajDesinence(dh)

            elif p == 4:  # R:n: radical n
                nr = int(eclats[1])
                self._genRadicaux[nr] = eclats[2]
            elif p == 8:  # abs+
                self._absents += Modele.listeI(eclats[1])
            elif p == 5:  # abs
                self._absents = Modele.listeI(eclats[1])
            elif p == 6:  # suffixes suf:<intervalle>:valeur
                lsuf = Modele.listeI(eclats[1])
                gr = eclats[2]  # TODO verif : bien formée ?
                for m in lsuf:
                    self.msuff[gr].append(m)
            elif p == 7:  # sufd: les désinences du père, suffixées
                if self._pere != 0:
                    suf = eclats[1]
                    ld = self._pere.desinences()
                    for d in ld:
                        if d.morphoNum() in self._absents:
                            continue
                        nd = allonge(d.grq())
                        dsuf = Desinence(nd+suf, d.morphoNum(), d.numRad(), self)
                        self._desinences[dsuf.morphoNum()].append(dsuf)
                        self._lemmatiseur.ajDesinence(dsuf)
            else:
                warnings.warn("Modele : Erreur pour " + l, UnknownModeleConfigurationKey)

        # père
        if self._pere:
            for m in self._pere.morphos():
                # héritage des désinence
                if self.deja(m):
                    continue
                ld = self._pere.desinences(m)
                for d in ld:
                    if d.morphoNum() in self._absents:  # morpho absente chez le descendant
                        continue
                    dh = self.clone(d)
                    self._desinences[dh.morphoNum()].append(dh)
                    self._lemmatiseur.ajDesinence(dh)

            # héritage des radicaux
            for numRad in set([d.numRad() for d in flatten(self._desinences.values())]):
                if numRad not in self._genRadicaux:
                    if self._pere.hasRadical(numRad):
                        nr = self._pere.genRadical(numRad)
                        self._genRadicaux[numRad] = nr
                    else:
                        warnings.warn(self.__repr__() + " has no radical {}".format(numRad), MissingRadical)

            # héritage des absents
            self._absents = self._pere.absents()

        # génération des désinences suffixées
        ldsuf = []
        clefsSuff = set(list(self.msuff.keys()))
        for suff in clefsSuff:
            for d in flatten(self._desinences.values()):
                if d.morphoNum() in self.msuff[suff]:
                    gq = d.grq()
                    if gq == "-":
                        gq = ""
                    gq += suff
                    dsuf = Desinence(gq, d.morphoNum(), d.numRad(), self)
                    ldsuf.append(dsuf)

        for dsuf in ldsuf:
            self._desinences[dsuf.morphoNum()].append(dsuf)
            self._lemmatiseur.ajDesinence(dsuf)

    def hasRadical(self, numRad):
        """ Vérifie que l'objet à le radical donné

        :param numRad: Identifiant de radical
        :type numRad: int
        :return: Si l'objet à la radical
        :rtype: bool
        """
        return numRad in self._genRadicaux

    @staticmethod
    def listeI(l):
        """ Fonction importante permettant de renvoyer
                une liste d'entiers à partir d'une chaîne.
                La chaîne est une liste de sections séparées
                par des virgules. Une section peut être soit
                un entier, soit un intervalle d'entiers. On
                donne alors les limites inférieure et supérieure
                de l'intervale, séparées par le caractère '-'.
                Nombreux exemples d'intervalles dans le fichier
                data/modeles.la.

        :param l: Chaîne à transformer
        :type l: str
        :return: Liste des sections étendues
        :rtype: list of int
        """
        result = []
        lvirg = l.split(',')
        for virg in lvirg:
            if "-" in virg:
                deb, fin = tuple(virg.split("-"))
                result += [i for i in range(int(deb), int(fin)+1)]
            else:
                result.append(int(virg))

        return result

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

    def clesR(self): 
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
        if self._pere == 0:
            return False
        return self._pere.estUn(m)

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

    def pos(self):
        """ Retourne la catégorie du modèle, utilisant les ancêtres du modèle.

        :return: Catégorie du modèle
        :rtype: str
        """
        if self.estUn("uita") or self.estUn("lupus") or self.estUn("miles") or self.estUn("manus") or self.estUn("res") or self.estUn("perseus"):
            return 'n'
        if self.estUn("doctus") or self.estUn("fortis"):
            return 'a'
        if self.estUn("amo") or self.estUn("imitor"):
            return 'v'
        return 'd'
