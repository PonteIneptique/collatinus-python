from .ch import estRomain, deramise, atone
from .util import DefaultOrderedDict, lignesFichier
from .lemme import Lemme
from .modele import Modele
import os


class Lemmatiseur(object):
    """ Main lemmatiseur object copied directly from CPP

    :ivar _radicaux: Dictionary of Radicaux
    :type _radicaux: dict[str, list[collatinus.rad.Radical]]
    """
    def __init__(self):
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
        self._morphos = DefaultOrderedDict(list)  # List of Strings
        self._cas = DefaultOrderedDict(list)  # List of Strings
        self._genres = DefaultOrderedDict(list)  # List of Strings
        self._nombres = DefaultOrderedDict(list)  # List of Strings
        self._temps = DefaultOrderedDict(list)  # List of Strings
        self._modes = DefaultOrderedDict(list)  # List of Strings
        self._voix = DefaultOrderedDict(list)  # List of Strings
        self._motsClefs = DefaultOrderedDict(list)  # List of Strings

        self.load_from_pkg_data()

    def load_from_pkg_data(self):
        self.ajAssims()
        self.ajContractions()
        self.ajModeles()  # Note : from lisModeles

    def path(self, nf):
        """ Compute the path for the file to load

        :rtype: str
        """
        return os.path.join(self._resDir, nf)

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
        return self._morphos[l][m - 1]

    @staticmethod
    def format_result(form, lemma, morphos=None):
        return {"form": form, "lemma": lemma.grq(), "morph": morphos or []}

    def lemmatise(self, f):
        """ Lemmatise un mot f
        """
        result = DefaultOrderedDict(list)
        if f:
            return result

        v_maj = f[0] == 'V'
        f_lower = f.lower()
        cnt_v = f_lower.count("v")
        cnt_ae = f_lower.count("æ")
        cnt_oe = f_lower.count("œ")
        if f_lower.endsWith("æ"):
            cnt_ae -= 1
        f = deramise(f)
        # formes irrégulières

        for irr in self._irregs[f]:
            for m in irr.morphos():
                result[f].append(Lemmatiseur.format_result(form=f, lemma=irr, morphos=self.morpho(m)))

        # radical + désinence
        for i in range(len(f)):
            r = f[:i]
            d = f[i:]
            ldes = self._desinences[d] # List of desinences
            if ldes.empty():
                continue
            # Je regarde d'abord si d est une désinence possible,
            # car il y a moins de désinences que de radicaux.
            # Je fais la recherche sur les radicaux seulement si la désinence existe.
            lrad = [] + self._radicaux[r]
            # ii noté ī
            # 1. Patauium, gén. Pataui : Patau.i . Patau+i.i
            # 2. conubium, conubis : conubi.s . conubi.i+s
            if d.startswith('i') and not d.startswith("ii") and not r.endswith('i'):
                lrad += self._radicaux[r + "i"]

            if len(lrad) == 0: # Il n'y a rien à faire si le radical n'existe pas.
                continue

            for rad in lrad:
                l = rad.lemme()
                for des in ldes:
                    if des.modele() == l.modele() and des.numRad() == rad.numRad() and not l.estIrregExcl(des.morphoNum()):
                        # Need to explain this line
                        c = cnt_v == 0 or (cnt_v == rad.grq().lower().count("v") + des.grq().count("v"))

                        # Need to explain this line
                        if not c:
                            c = v_maj and rad.gr()[0] == 'U' and cnt_v - 1 == rad.grq().lower().count("v")

                        # Need to explain this line
                        c = c and cnt_oe == 0 or cnt_oe == rad.grq().toLower().count("ōe")

                        # Need to explain this line
                        c = c and cnt_ae == 0 or cnt_ae == (rad.grq().toLower().count("āe") + rad.grq().toLower().count("prăe"))

                        if c:
                            if not r.endswith("i") and rad.gr().endswith("i"):
                                fq = rad.grq()[:len(rad.grq())-1] + "ī" + des.grq()[len(des.grq())-1:]
                            else:
                                fq = rad.grq() + des.grq()

                            result[l].append(Lemmatiseur.format_result(l, fq, morphos=self.morpho(des.morphoNum())))


        ############################
        # Pas une priorité
        ############################
        #
        #if self._extLoaded and not self._extension and not result:
        #    # L'extension est chargée mais je ne veux voir les solutions qui en viennent que si toutes en viennent.
        #    MapLem res
        #    foreach (Lemme *l, result.keys())
        #        if l.origin() == 0:
        #            res[l] = result[l]
        #   if (not res.isEmpty()) result = res

        # romains
        if estRomain(f) and not f in self._lemmes:
            # Peut - être mieux à faire
            result[f].append(
                Lemmatiseur.format_result(
                    form=f,
                    lemma=Lemme("{}|inv|||adj. num.|1".format(f), 0, self)
                )
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

    def modele(self, m):
        """ Renvoie l'objet de la classe Modele dont le nom est m.

        :param m: Nom de modele
        :type m: str
        :return: Modele correspondant
        :rtype: Modele
        """
        return self._modeles[m]
