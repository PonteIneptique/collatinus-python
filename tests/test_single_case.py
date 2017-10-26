from unittest import TestCase
from pycollatinus import Lemmatiseur
from pycollatinus.lemme import Lemme
from pycollatinus.modele import Modele


class TestSpecificCases(TestCase):
    """ Class where we mock up a lemmatizer instance """
    def test_invariables(self):
        x = Lemmatiseur(load=False)
        x.ajMorphos()
        m = Modele([
            "modele:inv",
            "R:0:0,0",
            "des:416:0:-"
        ], parent=x)
        x._modeles[m.gr()] = m
        nec = Lemme("nĕc|inv|||adv.|6689", origin=0, parent=x)
        ergo = Lemme("ergō=ērgō|inv|||conj.|1450", origin=0, parent=x)
        x._lemmes[nec.cle()] = nec
        x._lemmes[ergo.cle()] = ergo
        self.assertEqual(x.lemmatise("nec"), [{'lemma': 'nec', 'morph': '-', 'form': 'nec'}])
        self.assertEqual(x.lemmatise("ergo"), [{'lemma': 'ergo', 'morph': '-', 'form': 'ergo'}])
