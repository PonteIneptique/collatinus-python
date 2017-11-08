from .ch import estRomain, deramise, atone
from .util import DefaultOrderedDict, lignesFichier, flatten
from .lemme import Lemme, Radical
from .irregs import Irreg
from .modele import Modele
import os
import warnings
from pickle import dump, load
import re


SPACES = re.compile("\W")


class Lemmatiseur(object):
    """ Main lemmatiseur object copied directly from CPP

    :ivar _radicaux: Dictionary of Radicaux
    :type _radicaux: dict[str, list[pycollatinus.rad.Radical]]
    """
    def __init__(self, load=True):
        """"""
        self._resDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        self._cible = "fr"  # Langue cible
        self._modeles = {}  # Modeles
        self._cibles = {}
        self._lemmes = {}  # Lemmes

        self._assims = {}  # str -> str
        self._assimsq = {}  # str -> str
        self._contractions = {}  # str -> str
        self._variables = {}  # str -> str # Where key starts with $

        self._radicaux = DefaultOrderedDict(list)  # List of Radicaux
        self._desinences = DefaultOrderedDict(list)  # List of Desinence
        self._irregs = DefaultOrderedDict(list)  # List of Irreg
        self._morphos = {"fr":{}}  # List of Strings
        self._cas = DefaultOrderedDict(list)  # List of Strings
        self._genres = DefaultOrderedDict(list)  # List of Strings
        self._nombres = DefaultOrderedDict(list)  # List of Strings
        self._temps = DefaultOrderedDict(list)  # List of Strings
        self._modes = DefaultOrderedDict(list)  # List of Strings
        self._voix = DefaultOrderedDict(list)  # List of Strings
        self._motsClefs = DefaultOrderedDict(list)  # List of Strings

        if load is True:
            self.load_from_pkg_data()

    def compile(self):
        """ Compile le lemmatiseur localement
        """
        with open(self.path("compiled.pickle"), "wb") as file:
            dump(self, file)

    @staticmethod
    def load(path=None):
        """ Compile le lemmatiseur localement
        """
        if path is None:
            path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"))
            path = os.path.join(path, "compiled.pickle")
        with open(path, "rb") as file:
            return load(file)

    def load_from_pkg_data(self):
        self.ajAssims()
        self.ajContractions()
        self.ajMorphos("fr")  # Note : from lisModeles
        self.ajModeles()  # Note : from lisModeles
        self.ajLexiques()  # Note : from lisLexique
        self.ajExtensions()  # Note : from lisLexique
        self.ajIrreguliers()

    def path(self, nf):
        """ Compute the path for the file to load

        :rtype: str
        """
        return os.path.join(self._resDir, nf)

    def ajMorphos(self, lang="fr"):
        for ligne in lignesFichier(self.path("morphos." + lang)):
            if ":" not in ligne:
                break
            morph_id, morph_str = tuple(ligne.split(":"))
            self._morphos[lang][int(morph_id)] = morph_str

    def ajIrreguliers(self):
        """ Chargement des formes irrégulières du fichier data/irregs.la
        """
        lignes = lignesFichier(self.path("irregs.la"))
        for lin in lignes:
            try:
                irr = Irreg(lin, self)
                self._irregs[deramise(irr.gr())].append(irr)
            except Exception as E:
                print(len(self._lemmes), list(self._lemmes.keys())[0:10])
                warnings.warn("Erreur au chargement de l'irrégulier\n" + lin + "\n"+ str(E))
                raise E

        for irr in flatten(self._irregs.values()):
            irr.lemme().ajIrreg(irr)

    def ajAssims(self):
        """ Charge et définit les débuts de mots non-assimilés, associe à chacun sa forme assimilée.
        """
        for lin in lignesFichier(self.path("assimilations.la")):
            ass1, ass2 = tuple(lin.split(':'))
            self._assims[ass1] = ass2
            self._assimsq[atone(ass1)] = atone(ass2)

    def ajContractions(self):
        """ Charge et établit une liste qui donne, chaque contraction, forme non contracte qui lui correspond.
        """
        for lin in lignesFichier(self.path("contractions.la")):
            ass1, ass2 = tuple(lin.split(':'))
            self._contractions[ass1] = ass2

    def assims(self, mot):
        """ Cherche si la chaîne a peut subir une assimilation, renvoie cette chaîne éventuellement assimilée.

        :param mot: Mot pour lequel on doit vérifier des assimilations
        :type mot: str
        :return: Mot assimilé
        :rtype: str
        """
        for replaced, replacement in self._assimsq.items():
            if mot.startswith(replaced):
                mot = mot.replace(replaced, replacement)
                return mot
        return mot

    def desassims(self, mot):
        """ Cherche si la chaîne a peut subir une assimilation inversée, renvoie cette chaîne éventuellement assimilée.

        :param mot: Mot pour lequel on doit vérifier des assimilations
        :type mot: str
        :return: Mot assimilé
        :rtype: str
        """
        for replacement, replaced in self._assimsq.items():
            if mot.startswith(replaced):
                mot = mot.replace(replaced, replacement)
                return mot
        return mot

    def lisFichierLexique(self, filepath):
        """ Lecture des lemmes, et enregistrement de leurs radicaux

        :param filepath: Chemin du fichier à charger
        :type filepath: str
        """
        orig = int(filepath.endswith("ext.la"))
        lignes = lignesFichier(filepath)
        for lin in lignes:
            lemma = Lemme(lin, origin=orig, parent=self)
            self._lemmes[lemma.cle()] = lemma

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
                self._variables[varname] = value
                continue

            eclats = l.split(":")
            if (eclats[0] == "modele" or i == max) and len(sl) > 0:
                m = Modele(sl, parent=self)
                self._modeles[m.gr()] = m
                sl = []
            sl.append(l)

    def modele(self, m):
        """ Retrouve le modele pour la clef m

        :param m: Nom du modele
        :type m: str
        :return: Modele trouvé
        :rtype: Modele
        """
        return self._modeles[m]

    def lemme(self, lemme):
        """ Retrouve le lemme pour la clef lemme

        :param lemme: Nom du lemme
        :type lemme: str
        :return: Lemme trouvé
        :rtype: Lemme
        """
        return self._lemmes[lemme]

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
        m = self.modele(lemme.grModele())
        ''' insérer d'abord les radicaux définis dans lemmes.la
        qui sont prioritaires '''

        for i in lemme.clesR():
            radical_list = lemme.radical(i)
            for radical in radical_list:
                self._radicaux[deramise(radical.gr()).lower()].append(radical)

        # pour chaque radical du modèle
        for indice_radical in m.clesR():
            # Si le radical a été défini par le lemme
            if indice_radical in lemme.clesR():
                continue
            gs = lemme.grq().split(',')
            for graphie in gs:
                r = ""
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
                self._radicaux[deramise(r.gr()).lower()].append(r)

    def ajDesinence(self, d):
        """ Ajoute la désinence d dans la map des désinences. """
        self._desinences[deramise(d.gr())].append(d)

    def morpho(self, m):
        """ Renvoie la chaîne de rang m dans la liste des morphologies donnée par le fichier data/morphos.la

        :param m: Indice de morphologie
        :type m: int
        :return: Chaîne de rang m dans la liste des morphologies donnée par le fichier data/morphos.la
        :rtype: str
        """
        l = "fr"

        # TODO : Si ajout langue de traduction, il faudra convertir ce qui suit
        ###################
        # if self._morphos.keys().contains(_cible.mid(0,2))) l = _cible.mid(0,2:
        # elif (_cible.size() > 4) and (_morphos.keys().contains(_cible.mid(3,2))):
        #    l = _cible.mid(3,2)
        ####################

        if m < 0 or m > len(self._morphos[l]):
            raise KeyError("Morphology %s requested but not found" % m)
        if m == len(self._morphos[l]):
            return "-"
        return self._morphos[l][m]

    @staticmethod
    def format_result(form, lemma, morphos=None, with_pos=False, raw_obj=False):
        r = {"form": form, "lemma": lemma.gr(), "morph": morphos or []}
        if raw_obj:
            r["lemma"] = lemma
        if with_pos:
            r["pos"] = lemma.pos()
        return r

    def lemmatise_multiple(self, string, pos=False, get_lemma_object=False, as_list=True):
        """ Lemmatise une liste complète

        :param string: Chaîne à lemmatiser
        :param pos: Récupère la POS
        :param get_lemma_object: Retrieve Lemma object instead of string representation of lemma
        :param as_list: Retrieve a list of generators instead of a list if set to false
        """
        mots = SPACES.split(string)
        resultats = [self.lemmatise(mot, pos=pos, get_lemma_object=get_lemma_object) for mot in mots]
        if as_list:
            resultats = [list(r) for r in resultats]
        return resultats

    def _lemmatise_assims(self, f, *args, **kwargs):
        """ Lemmatise un mot f avec son assimilation

        :param f: Mot à lemmatiser
        :param pos: Récupère la POS
        :param get_lemma_object: Retrieve Lemma object instead of string representation of lemma
        :param results: Current results
        """
        forme_assimilee = self.assims(f)
        if forme_assimilee != f:
            for proposal in self._lemmatise(forme_assimilee):
                yield proposal

    def _lemmatise_contractions(self, f, *args, **kwargs):
        """ Lemmatise un mot f avec sa contraction

        :param f: Mot à lemmatiser
        :yield: Match formated like in _lemmatise()
        """
        fd = f
        for contraction, decontraction in self._contractions.items():
            if fd.endswith(contraction):
                fd = f[:-len(contraction)]
                if "v" in fd or "V" in fd:
                    fd += decontraction
                else:
                    fd += deramise(decontraction)
                for proposal in self._lemmatise(fd, *args, **kwargs):
                    yield proposal

    def _lemmatise_desassims(self, f, *args, **kwargs):
        """ Lemmatise un mot f avec sa désassimilation

        :param f: Mot à lemmatiser
        :yield: Match formated like in _lemmatise()
        """
        forme_assimilee = self.desassims(f)
        if forme_assimilee != f:
            for proposal in self._lemmatise(forme_assimilee, *args, **kwargs):
                yield proposal

    def lemmatise(self, f, pos=False, get_lemma_object=False, lower=True):
        """ Lemmatise un mot f

        :param f: Mot à lemmatiser
        :param pos: Récupère la POS
        :param get_lemma_object: Retrieve Lemma object instead of string representation of lemma
        :param check_assims: Vérifie les assimilations.
        """
        if lower is True:
            if f.lower() != f:
                yield from self.lemmatise(f.lower(), pos, get_lemma_object, lower=False)

        f = deramise(f)
        for proposal in self._lemmatise(f, pos, get_lemma_object):
            yield proposal
        for proposal in self._lemmatise_assims(f, pos, get_lemma_object):
            yield proposal
        for proposal in self._lemmatise_desassims(f, pos, get_lemma_object):
            yield proposal
        for proposal in self._lemmatise_contractions(f, pos, get_lemma_object):
            yield proposal

    def _lemmatise(self, form, pos=False, get_lemma_object=False):
        """ Lemmatise un mot f

        :param f: Mot à lemmatiser
        :param pos: Récupère la POS
        :param get_lemma_object: Retrieve Lemma object instead of string representation of lemma
        :param check_assims: Vérifie les assimilations.
        """
        result = []
        if not form:
            return result

        # formes irrégulières
        for irr in self._irregs[form]:
            for m in irr.morphos():
                yield Lemmatiseur.format_result(
                    form=form, lemma=irr, morphos=self.morpho(m), with_pos=pos,
                    raw_obj=get_lemma_object
                )

        # radical + désinence
        for i in range(len(form)+1):
            if i == 0:
                radical = ""
                desinence = form
            else:
                radical = form[:i]
                desinence = form[i:]
            ldes = self._desinences.get(desinence, None)  # List of desinences
            if ldes is None:
                continue
            # Je regarde d'abord si d est une désinence possible,
            # car il y a moins de désinences que de radicaux.
            # Je fais la recherche sur les radicaux seulement si la désinence existe.
            lrad = [] + self._radicaux.get(radical, [])

            # ii noté ī
            # 1. Patauium, gén. Pataui : Patau.i . Patau+i.i
            # 2. conubium, conubis : conubi.s . conubi.i+s
            if desinence.startswith('i') and not desinence.startswith("ii") and not radical.endswith('i'):
                lrad += self._radicaux.get(radical + "i", [])

            if len(lrad) == 0:  # Il n'y a rien à faire si le radical n'existe pas.
                continue

            for rad in lrad:
                lemme = rad.lemme()
                for des in ldes:
                    if des.modele() == lemme.modele() and des.numRad() == rad.numRad() and not lemme.estIrregExcl(des.morphoNum()):
                        # Commented this part because we are not using quantity right now.
                        yield Lemmatiseur.format_result(
                                form, lemme, morphos=self.morpho(des.morphoNum()), with_pos=pos,
                                raw_obj=get_lemma_object
                            )

        # romains
        if estRomain(form) and form not in self._lemmes:
            # Peut - être mieux à faire
            yield Lemmatiseur.format_result(
                form=form,
                lemma=Lemme("{}|inv|||adj. num.|1".format(form), 0, self)
            )

        return result

    def variable(self, v):
        """ Permet de remplacer la métavariable v
            par son contenu. Ces métavariables sont
            utilisées par le fichier modeles.la, pour
            éviter de répéter des suites de désinences.
            Elles sont repérées comme en PHP, leur
            premier caractère $.

            :param v: Nom de la variable
            :type v: str
            :return: Valeur de variable
            :rtype: str
        """
        return self._variables[v]
