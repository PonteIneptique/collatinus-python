from .ch import estRomain, deramise
from .util import DefaultOrderedDict
from .lemme import Lemme
from .modele import Modele
from .parser import Parser
import os
import re
from pickle import dump, load


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
        self._morphos = {"fr": {}}  # List of Strings
        self._cas = DefaultOrderedDict(list)  # List of Strings
        self._genres = DefaultOrderedDict(list)  # List of Strings
        self._nombres = DefaultOrderedDict(list)  # List of Strings
        self._temps = DefaultOrderedDict(list)  # List of Strings
        self._modes = DefaultOrderedDict(list)  # List of Strings
        self._voix = DefaultOrderedDict(list)  # List of Strings
        self._motsClefs = DefaultOrderedDict(list)  # List of Strings

        if load is True:
            Parser(self, path=self._resDir).parse()

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

    def path(self, nf):
        """ Compute the path for the file to load

        :rtype: str
        """
        return os.path.join(self._resDir, nf)

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
        r = {"form": form, "lemma": lemma.gr(), "morph": morphos or ""}
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
            for proposal in self._lemmatise(forme_assimilee, *args, **kwargs):
                yield proposal

    def _lemmatise_roman_numerals(self, form, pos=False, get_lemma_object=False):
        """ Lemmatise un mot f si c'est un nombre romain

        :param form: Mot à lemmatiser
        :param pos: Récupère la POS
        :param get_lemma_object: Retrieve Lemma object instead of string representation of lemma
        """
        if estRomain(form):
            _lemma = Lemme(
                cle=form, graphie_accentuee=form, graphie=form, parent=self, origin=0, pos="a",
                modele=self.modele("inv")
            )
            yield Lemmatiseur.format_result(
                form=form,
                lemma=_lemma,
                with_pos=pos,
                raw_obj=get_lemma_object
            )

        if form.upper() != form:
            yield from self._lemmatise_roman_numerals(form.upper(), pos=pos, get_lemma_object=get_lemma_object)

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
                yield from self._lemmatise(fd, *args, **kwargs)

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
        :param lower: Need to check lowercase version
        """
        if lower:
            # We do not run numeral on lower
            yield from self._lemmatise_roman_numerals(f, pos=pos, get_lemma_object=get_lemma_object)

            # We run on the lower version
            if f.lower() != f:
                yield from self.lemmatise(f.lower(), pos=pos, get_lemma_object=get_lemma_object, lower=False)

        f = deramise(f)
        yield from self._lemmatise(f, pos=pos, get_lemma_object=get_lemma_object)
        yield from self._lemmatise_assims(f, pos=pos, get_lemma_object=get_lemma_object)
        yield from self._lemmatise_desassims(f, pos=pos, get_lemma_object=get_lemma_object)
        yield from self._lemmatise_contractions(f, pos=pos, get_lemma_object=get_lemma_object)

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
