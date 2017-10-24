from .ch import communes, atone
from .lemme import Lemme


class Radical(object):
    def __init__(self, g, n, *parent):
        """ Représentation d'un radical

        :param g: Forme canonique du radical avec quantité
        :type g: str
        :param n: Numéro du radical
        :type n: int
        """
        self._lemme = Lemme(parent)
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
        return _grq


    def lemme(self):
        """ Le lemme auquel appartient le radical.

        :return: Le lemme auquel appartient le radical.
        :rtype: Lemme
        """
        return self._lemme;

    def modele(self):
        """ Le modèle de flexion du radical

        :return: Le modèle de flexion du radical
        :rtype: str
        """
        return self._lemme.modele();

    def numRad(self):
        """ Le numéro du radical.

        :return: Le numéro du radical.
        :rtype: int
        """
        return self._numero;