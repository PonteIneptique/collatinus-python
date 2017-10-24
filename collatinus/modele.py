import re
import warnings
from .ch import simplified, allonge
from .util import DefaultOrderedDict

class Desinence(object):
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
        der = -1
        if d:
            der = int(d[len(d)-1])
        if der > 0:
            self._rarete = der
            d = d[:-1]

        
        # '-' est la désinence zéro
        if d == "-":
            d = ""
        self._grq = d
        self._gr = atone(_grq)
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
    RE = re.compile("[:;]([\\w]*)\\+{0,1}(\\$\\w+)")
    CLEFS = [
            "modele",  # 0
            "pere"  ,  # 1
            "des"   ,  # 2
            "des+"  ,  # 3
            "R"     ,  # 4
            "abs"   ,  # 5
            "suf"   ,  # 6
            "sufd"  ,  # 7
            "abs+" ,  # 8
    ]

    def __init__(self, ll, parent=None):
        """ Constructeur de la classe modèle. 

        Chaque item de la liste ll est constitué de champs séparé par le caractère ':'. Le premier champ est un mot clé. Le parent est le lemmatiseur. 
        Pour le format du fichier data/modeles.la, la documentation utilisateur.

        :param ll: Liste de champs séparés par le caractère ":". Le premier champ est un mot-clef
        :param parent: Lemmatiseur

        :ivar _desinences: Dictionnaire de liste de désinences pour les morpho KEY
        :type _desinences: dict of list of Desinence
        """
        self._lemmatiseur = parent
        self._pere = 0
        self._desinences = DefaultOrderedDict(list)
        self._absents = []  # List of int
        self._genRadicaux = {}
        self._gr = ""
        self._grq = ""

        for original_l in ll:
            # remplacement des variables par leur valeur
            l = "" + original_l

            ## TODO : A REVOIR car assez compliqué
            while (Modele.RE.indexIn(l) > -1)
                v = Modele.RE.cap(2)
                var = _lemmatiseur.variable(v)
                pre = MODELE.RE.cap(1)
                if pre:
                    var = var.replace(";", ";") + pre
                l = l.replace(v, var)

            eclats = simplified(l).split(":")
            # modele pere des des  R   abs
            #  0      1    2   3   4   5

            p = MODELE.CLEFS.index(eclats[0])
            if p == 0:  # modèle
                self._gr = eclats[1]
            elif p == 1:  # père
                self._pere = parent.modele(eclats[1])
            elif p == 2 or p == 3:
                # des+: désinences s'ajoutant à celles du père
                # des: désinences écrasant celles du père
                li = Modele.listeI(eclats[1])
                r = int(eclats[2])
                ld = eclats[3].split(';')
                for i in range(len(li)):
                    if i < ld.count():
                        ldd = ld[1].split(',')
                    else:
                        ldd = ld[-1].split(',')
                    for g in ldd:
                        nd = Desinence(g, li[i], r, self)
                        self._desinences[nd.morphoNum()].append(nd)
                        self._lemmatiseur.ajDesinence(nd)

                # si des+, chercher les autres désinences chez le père :
                if p == 3:
                    for i in li:
                        ldp = self._pere.desinences(i) # Liste de desinences au numéro i
                        for dp in ldp:
                            # cloner la désinece
                            h = self.clone(dp)
                            self._desinences[i].append(dh)
                            self._lemmatiseur.ajDesinence(dh)

            elif p == 4:  # R:n: radical n
                nr = int(eclats[1])
                self._genRadicaux[nr] = eclats.at(2)
            elif p == 8: # abs+
                self._absents.append(Modele.listeI(eclats[1]))
            elif p == 5: # abs
                self._absents = Modele.listeI(eclats[1])
            elif p == 6:  # suffixes suf:<intervalle>:valeur
                lsuf = Modele.listeI(eclats[1])
                gr = eclats[2]  # TODO verif : bien formée ?
                for m in lsuf:
                    msuff.insert(gr, m)
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
                warnings.warn("Modele : Erreur pour " + l)

        # père
        if self._pere != 0:
            for m in self._pere.morphos():
                # héritage des désinence
                if self.deja(m):
                    continue
                ld = self._pere.desinences(m)
                for d in ld:
                    if d.morphoNum() in self._absents: # morpho absente chez le descendant
                        continue
                    dh = self.clone(d)
                    self._desinences[dh.morphoNum()].append(dh)
                    self._lemmatiseur.ajDesinence(dh)

            # héritage des radicaux
            for d in self._desinences:
                if d.numRad() not in self._genRadicaux:
                    nr = self._pere.genRadical(d.numRad())
                    self._genRadicaux[d.numRad()] = nr

            # héritage des absents
            self._absents = self._pere.absents()

        # génération des désinences suffixées
        ldsuf = []
        clefsSuff = msuff.keys()
        clefsSuff.removeDuplicates()
        for suff in clefsSuff:
            for d in self._desinences:
                if d.morphoNum() in msuff[suff]:
                    gq = d.grq()
                    if gq == "-":
                        gq.clear()
                    gq.append(suff)
                    dsuf = Desinence(gq, d.morphoNum(), d.numRad(), self)
                    ldsuf.insert(dsuf.morphoNum(), dsuf)

        for dsuf in ldsuf:
            self._desinences[dsuf.morphoNum()].append(dsuf)
            self._lemmatiseur.ajDesinence(dsuf)

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
            if virg.contains('-'):
                deb, fin = tuple(virg.split("-"))
                result += [i for i in range(int(deb), int(fin))]
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

    
    '''*
     * \fn QList<Desinence*> Modele.desinences (int d)
     * \brief 
     '''
    def desinences(self, d):
        """ Renvoie la liste des désinence de morpho d du modèle.

        :param d: Identifant de morphologie
        :type d: int
        :return: Liste des désinence de morpho d du modèle.
        :rtype: list of Desinence
        """
        return self._desinences[d]

    def desinences(self):
        """ Renvoie toutes les désinences du modèle.

        :return: toutes les désinences du modèle (Applaties en python, doute sur original)
        :rtype: list of Desinence
        """
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
        return _gr

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
