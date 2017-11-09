from .ch import atone, listeI


class Irreg(object):

    def __repr__(self):
        return "<pycollatinus.irregs.Irreg[{}]>".format(self._gr)

    def __init__(self, graphie_accentuee: str, graphie: str, lemme, morphos: list,
                 exclusif: bool = False, parent=None):
        """

        :param graphie_accentuee: Graphie accentuee
        :param graphie: Graphie
        :param lemme: Lemma
        :type lemme: pycollatinus.lemme.Lemme
        :param morphos: List of morphologies matched by this form
        :param exclusif: si la forme régulière calculée par le modèle est inusitée, remplace par la forme irrégulière.
        :param parent: Lemmatiseur
        :type parent: pycollatinus.lemmatiseur.Lemmatiseur
        """
        self._lemmat = parent
        self._grq = graphie_accentuee
        self._exclusif = exclusif
        self._gr = graphie
        self._lemme = lemme
        self._morphos = morphos

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

