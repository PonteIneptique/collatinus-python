from .ch import deramise, atone, listeI, allonge, simplified
from .util import lignesFichier, flatten, DefaultOrderedDict
from .lemme import Lemme, Radical
from .irregs import Irreg
from .modele import Modele, Desinence
from .error import UnknownModeleConfigurationKey, MissingRadical
import os
import warnings
import re


SPACES = re.compile("\W")

MODELE_CLEFS = [
    "pere",  # 0
    "des",  # 1
    "des+",  # 2
    "R",  # 3
    "abs",  # 4
    "suf",  # 5
    "sufd",  # 6
    "abs+",  # 7
    "pos",  # 8
]


class Parser(object):
    """ Parser object that fills the Lemmatiseur

    :param lemmatiseur: Lemmatiseur object to fill
    :param path: Path in which we find Collatinus data
    :param cible: Language for morphology
    """
    def __init__(self, lemmatiseur, path=None, cible="fr"):
        """"""
        self.__lemmatiseur__ = lemmatiseur
        self.__data_directory__ = path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        self.__cible__ = cible

    @property
    def data_directory(self):
        return self.__data_directory__

    @property
    def lemmatiseur(self):
        return self.__lemmatiseur__

    def parse(self):
        self.ajAssims()
        self.ajContractions()
        self.ajMorphos(self.__cible__)  # Note : from lisModeles
        self.ajModeles()  # Note : from lisModeles
        self.ajLexiques()  # Note : from lisLexique
        self.ajExtensions()  # Note : from lisLexique
        self.ajIrreguliers()

    def path(self, nf):
        """ Compute the path for the file to load

        :rtype: str
        """
        return os.path.join(self.data_directory, nf)

    def ajMorphos(self, lang="fr"):
        for ligne in lignesFichier(self.path("morphos." + lang)):
            if ":" not in ligne:
                break
            morph_id, morph_str = tuple(ligne.split(":"))
            self.lemmatiseur._morphos[lang][int(morph_id)] = morph_str

    def ajIrreguliers(self):
        """ Chargement des formes irrégulières du fichier data/irregs.la
        """
        lignes = lignesFichier(self.path("irregs.la"))
        for lin in lignes:
            try:
                irr = self.parse_irreg(lin)
                self.lemmatiseur._irregs[deramise(irr.gr())].append(irr)
            except Exception as E:
                warnings.warn("Erreur au chargement de l'irrégulier\n" + lin + "\n" + str(E))
                raise E

        for irr in flatten(self.lemmatiseur._irregs.values()):
            irr.lemme().ajIrreg(irr)

    def ajAssims(self):
        """ Charge et définit les débuts de mots non-assimilés, associe à chacun sa forme assimilée.
        """
        for lin in lignesFichier(self.path("assimilations.la")):
            ass1, ass2 = tuple(lin.split(':'))
            self.lemmatiseur._assims[ass1] = ass2
            self.lemmatiseur._assimsq[atone(ass1)] = atone(ass2)

    def ajContractions(self):
        """ Charge et établit une liste qui donne, chaque contraction, forme non contracte qui lui correspond.
        """
        for lin in lignesFichier(self.path("contractions.la")):
            ass1, ass2 = tuple(lin.split(':'))
            self.lemmatiseur._contractions[ass1] = ass2

    def lisFichierLexique(self, filepath):
        """ Lecture des lemmes, et enregistrement de leurs radicaux

        :param filepath: Chemin du fichier à charger
        :type filepath: str
        """
        orig = int(filepath.endswith("ext.la"))
        lignes = lignesFichier(filepath)
        for ligne in lignes:
            self.parse_lemme(ligne, orig)

    def parse_lemme(self, linea: str, origin: int=0, _deramise: bool=True):
        """ Constructeur de la classe Lemme à partir de la ligne linea.

        Exemple de linea avec numéro d'éclat:
            # cădo|lego|cĕcĭd|cās|is, ere, cecidi, casum|687
            #   0 | 1  | 2   | 3 |     4                | 5

        :param linea: Ligne à parser
        :type linea: str
        :param origin: 0 for original curated lemma, 1 for automatic import from Gaffiot
        :type origin: int
        :param _deramise: Force the deramisation of the normalized graphie
        :type _deramise: bool
        """
        eclats = linea.split('|')
        lg = eclats[0].split('=')

        if _deramise:
            cle = atone(deramise(lg[0]))
        else:
            cle = atone(lg[0])

        # Some lemma have homonyms, we have a number do differentiate them
        nh = 0
        if cle[-1].isnumeric():
            nh = int(cle[-1])
            grd = cle[:-1]
        else:
            grd = cle

        # We setup the accentuated graphie
        if len(lg) == 1:
            grq = grd
        else:
            grq = lg[1]
        # Pour l'affichage des dictionnaires, élimine les doubles de la forme canonique
        gr = atone(grq.split(",")[0])
        grModele = eclats[1]
        modele = self.lemmatiseur.modele(grModele)

        # contrôle de format. la liste doit avoir 6 items
        if len(eclats) < 6:
            warnings.warn("Ligne mal formée : " + gr + "\n ---Dernier champ " + eclats[-1] + "\n ---" + linea)

        radicaux = DefaultOrderedDict(list)
        # lecture des radicaux, 2 et 3
        for i in range(2, 4):
            if eclats[i]:
                lrad = eclats[i].split(',')
                for rad in lrad:
                    radicaux[i - 1].append(Radical(rad, i - 1))

        # Gros doute sur le fonctionnement ici
        indMorph = eclats[4]
        match_renvoi = Lemme.RENVOI.match(indMorph)
        if match_renvoi is not None:
            renvoi = match_renvoi.group(1)
        else:
            renvoi = ""

        pos = ""
        if "adj." in indMorph:
            pos += 'a'
        if "conj" in indMorph:
            pos += 'c'
        if "excl." in indMorph:
            pos += 'e'
        if "interj" in indMorph:
            pos += 'i'
        if "num." in indMorph:
            pos += 'm'
        if "pron." in indMorph:
            pos += 'p'
        if "prép" in indMorph:
            pos += 'r'
        if "adv" in indMorph:
            pos += 'd'
        if " nom " in indMorph:
            pos += 'n'
        if "npr." in indMorph:
            pos += 'n'
        if not pos:
            pos = modele.pos()  # Je prends le POS du modèle
            if pos == "d" and renvoi:
                pos = ""
                # S'il y a un renvoi (cf.) et que le modèle a donné le POS "d" (adverbe),
                # je prendrai le pos du renvoi (les indéclinables ont le POS par défaut "d").
                # Je ne peux pas le faire maintenant !

        # Nombre d'occurrences
        if len(eclats[5]):
            nbOcc = int(eclats[5])
        else:
            nbOcc = 1

        lemma = Lemme(
            cle=cle,
            graphie=gr, graphie_accentuee=grq,
            modele=modele, radicaux=radicaux,
            parent=self.lemmatiseur,
            nombre_homonymie=nh, nbOcc=nbOcc,
            origin=origin, pos=pos
        )
        # We register the lemma for each radical
        for radNum in lemma._radicaux:
            for rad in lemma._radicaux[radNum]:
                rad.set_lemme(lemma)
        self._register_lemme(lemma)
        return lemma

    def register_modele(self, modele: Modele):
        """ Register a modele onto the lemmatizer

        :param modele: Modele to register
        """
        self.lemmatiseur._modeles[modele.gr()] = modele

    def parse_modele(self, list_of_lines: list):
        """ Chaque item de la liste list_of_lines est constitué de champs séparé par le caractère ':'. Le premier champ est un mot clé. Le parent est le lemmatiseur.
        Pour le format du fichier data/modeles.la, la documentation utilisateur.

        :param list_of_lines: Liste de champs séparés par le caractère ":". Le premier champ est un mot-clef
        :return: model
        :rtype: Modele
        """
        grq = list_of_lines[0].split(":")[1]
        gr = atone(grq)
        modele = Modele(graphie=gr, graphie_accentuee=grq, parent=self.lemmatiseur)
        pere = None

        for original_l in list_of_lines[1:]:
            # remplacement des variables par leur valeur
            l = "" + original_l

            # TODO : Ajouté * pour la premiere capture pour rendre le prefix optionnel...
            for pre, v in Modele.RE.findall(l):
                var = self.lemmatiseur.variable(v)
                if pre:
                    var = var.replace(";", ";" + pre)
                l = l.replace(v, var)

            eclats = simplified(l).split(":")
            # type_of_line -> pere des  des+  R   abs
            #                  0    1    2    3    4
            type_of_line = MODELE_CLEFS.index(eclats[0])
            if type_of_line == 0:  # père
                modele._pere = pere = self.lemmatiseur.modele(eclats[1])
            elif type_of_line == 1 or type_of_line == 2:
                # des+: désinences s'ajoutant à celles du père
                # des: désinences écrasant celles du père
                index_morphologies = listeI(eclats[1])  # Anciennement li
                radical = int(eclats[2])  # Anciennement "r"
                liste_desinences = eclats[3].split(';')  # Anciennement "ld"
                for i in range(len(index_morphologies)):
                    if i < len(liste_desinences):
                        liste_desinences_definitives = liste_desinences[i].split(',')  # Anciennement "ldd"
                    else:
                        liste_desinences_definitives = liste_desinences[-1].split(',')

                    for graphie in liste_desinences_definitives:
                        nd = Desinence(graphie, index_morphologies[i], nr=radical, parent=modele)
                        modele._desinences[nd.morphoNum()].append(nd)
                        self.ajDesinence(nd)

                # si des+, chercher les autres désinences chez le père :
                if type_of_line == 2:
                    for i in index_morphologies:
                        for dp in pere.desinences(i):
                            dh = modele.clone(dp)  # cloner la désinence
                            modele._desinences[i].append(dh)
                            self.ajDesinence(dh)

            elif type_of_line == 3:  # R:n: radical n
                modele._genRadicaux[int(eclats[1])] = eclats[2]
            elif type_of_line == 4:  # abs
                modele._absents = listeI(eclats[1])
            elif type_of_line == 7:  # abs+
                modele._absents += listeI(eclats[1])
            elif type_of_line == 5:  # suffixes suf:<intervalle>:valeur
                lsuf = listeI(eclats[1])
                gr = eclats[2]  # TODO verif : bien formée ?
                for m in lsuf:
                    modele.msuff[gr].append(m)
            elif type_of_line == 6:  # sufd: les désinences du père, suffixées
                if pere:
                    suf = eclats[1]
                    ld = pere.desinences()
                    for d in ld:
                        if d.morphoNum() in modele._absents:
                            continue
                        nd = allonge(d.grq())
                        dsuf = Desinence(nd+suf, d.morphoNum(), d.numRad(), modele)
                        modele._desinences[dsuf.morphoNum()].append(dsuf)
                        self.ajDesinence(dsuf)
            elif type_of_line == 8:  # POS
                modele.set_pos(eclats[1])
            else:
                warnings.warn("Modele : Erreur pour " + l, UnknownModeleConfigurationKey)

        # père
        if pere:
            if not modele.pos():  # Small difference with original codebase : we inherit the pos if the parent has it
                modele.set_pos(pere.pos())
            for m in pere.morphos():
                # héritage des désinence
                if modele.deja(m):
                    continue
                ld = pere.desinences(m)
                for d in ld:
                    if d.morphoNum() in modele._absents:  # morpho absente chez le descendant
                        continue
                    dh = modele.clone(d)
                    modele._desinences[dh.morphoNum()].append(dh)
                    self.ajDesinence(dh)

            # héritage des radicaux
            for numRad in set([d.numRad() for d in flatten(modele._desinences.values())]):
                if numRad not in modele._genRadicaux:
                    if pere.hasRadical(numRad):
                        modele._genRadicaux[numRad] = pere.genRadical(numRad)
                    else:
                        warnings.warn(gr + " has no radical {}".format(numRad), MissingRadical)

            # héritage des absents
            modele._absents = pere.absents()

        # génération des désinences suffixées
        ldsuf = []
        clefsSuff = set(list(modele.msuff.keys()))
        for suff in clefsSuff:
            for d in flatten(modele._desinences.values()):
                if d.morphoNum() in modele.msuff[suff]:
                    gq = d.grq()
                    if gq == "-":
                        gq = ""
                    gq += suff
                    dsuf = Desinence(gq, d.morphoNum(), d.numRad(), modele)
                    ldsuf.append(dsuf)

        for dsuf in ldsuf:
            modele._desinences[dsuf.morphoNum()].append(dsuf)
            self.ajDesinence(dsuf)

        return modele

    def _register_lemme(self, lemma):
        """ Register a lemma into the Lemmatiseur

        :param lemma: Lemma to register
        :return:
        """
        if lemma.cle() not in self.lemmatiseur._lemmes:
            self.ajRadicaux(lemma)
            self.lemmatiseur._lemmes[lemma.cle()] = lemma

    def ajExtensions(self):
        """ Lecture du fichier de lemmes étendus """
        self.lisFichierLexique(self.path("lem_ext.la"))

    def ajLexiques(self):
        """ Lecture du fichier de lemmes de base """
        self.lisFichierLexique(self.path("lemmes.la"))

    def ajModeles(self):
        """ Lecture des modèles, et enregistrement de leurs désinences
        """
        sl = []
        lines = [line for line in lignesFichier(self.path("modeles.la"))]
        max = len(lines) - 1
        for i, l in enumerate(lines):
            if l.startswith('$'):
                varname, value = tuple(l.split("="))
                self.lemmatiseur._variables[varname] = value
                continue

            eclats = l.split(":")
            if (eclats[0] == "modele" or i == max) and len(sl) > 0:
                m = self.parse_modele(sl)
                self.register_modele(m)
                sl = []
            sl.append(l)

    def ajRadicaux(self, lemme):
        """ Calcule tous les radicaux du lemme l,
            *  en se servant des modèles, ajoute à ce lemme,
            *  et ensuite à la map *  des radicaux de la classe Lemmat.

        Ligne type de lemme
        # ablŭo=ā̆blŭo|lego|ā̆blŭ|ā̆blūt|is, ere, lui, lutum
        #      0        1    2    3         4

        :param lemme: Lemme
        :type lemme: Lemme
        """
        m = self.lemmatiseur.modele(lemme.grModele())
        ''' insérer d'abord les radicaux définis dans lemmes.la
        qui sont prioritaires '''

        for i in lemme.cles_radicaux():
            radical_list = lemme.radical(i)
            for radical in radical_list:
                self.lemmatiseur._radicaux[deramise(radical.gr()).lower()].append(radical)

        # pour chaque radical du modèle
        for indice_radical in m.cles_radicaux():
            # Si le radical a été défini par le lemme
            if indice_radical in lemme.cles_radicaux():
                continue
            gs = lemme.grq().split(',')
            for graphie in gs:
                gen = m.genRadical(indice_radical)
                # si gen == 'K', radical est la forme canonique
                if gen == "-":
                    continue
                if gen != "K":
                    # sinon, la règle de formation du modèle
                    oter, ajouter = 0, "0"
                    if "," in gen:
                        oter, ajouter = tuple(gen.split(","))
                        oter = int(oter)
                    else:
                        oter = int(gen)

                    if oter == len(graphie):
                        graphie = ""
                    elif oter != 0:
                        graphie = graphie[:-oter]
                    if ajouter != "0":
                        graphie += ajouter
                r = Radical(graphie, indice_radical, lemme)

                # Doute si cela n'appartient pas à graphe in gs
                lemme.ajRadical(indice_radical, r)
                self.lemmatiseur._radicaux[deramise(r.gr()).lower()].append(r)

    def ajDesinence(self, d):
        """ Ajoute la désinence d dans la map des désinences. """
        self.lemmatiseur._desinences[deramise(d.gr())].append(d)

    def parse_irreg(self, l):
        """ Constructeur de la classe Irreg.

        :param l: Ligne de chargement des irréguliers
        :type l: str
        """
        ecl = l.split(':')
        grq = ecl[0]
        exclusif = False
        if grq.endswith("*"):
            grq = grq[:-1]
            exclusif = True
        return Irreg(
            graphie_accentuee=grq, graphie=atone(grq),
            exclusif=exclusif,
            morphos=listeI(ecl[2]),
            lemme=self.lemmatiseur.lemme(ecl[1]),
            parent=self.lemmatiseur
        )
