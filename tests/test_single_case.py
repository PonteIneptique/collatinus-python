from unittest import TestCase
from pycollatinus import Lemmatiseur
from pycollatinus.lemme import Lemme
from pycollatinus.modele import Modele


def load_mod_vars(lemmatiseur):
    lines = [
        "$compar=ŏr;ŏr;ōrĕm;ōrĭs;ōrī;ōrĕ;ōrēs;ōrēs;ōrēs;ōrŭm;ōrĭbŭs;ōrĭbŭs",
        "$em=ĕm;ēs;ĕt;ēmŭs;ētĭs;ēnt",
        "$ens=ēns;ēns;ēntĕm;ēntĭs;ēntī;ēntĕ;ēntēs;ēntēs;ēntēs;ēntĭŭm,ēntŭm;ēntĭbŭs;ēntĭbŭs",
        "$im=ĭm;īs;ĭt;īmŭs;ītĭs;īnt",
        "$lupus=ŭs;ĕ;ŭm;ī;ō;ō;ī;ī;ōs;ōrŭm;īs;īs",
        "$templum=ŭm;ŭm;ŭm;ī;ō;ō;ă;ă;ă;ōrŭm;īs;īs",
        "$se=sē,sēsē;sŭī;sĭbī;sē,sēsē",
        "$tu=ū;ē;ŭī;ĭbĭ;ē",
        "$uita=ă;ă;ăm;āe;āe;ā;āe;āe;ās;ārŭm;īs;īs"
    ]
    for l in lines:
        if l.startswith('$'):
            varname, value = tuple(l.split("="))
            lemmatiseur._variables[varname] = value
            continue
    return lemmatiseur


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

        x._parse_lemme("nĕc|inv|||adv.|6689", orig=0)
        x._parse_lemme("ergō=ērgō|inv|||conj.|1450", orig=0)

        self.assertEqual(list(x.lemmatise("nec")), [{'lemma': 'nec', 'morph': '-', 'form': 'nec'}])
        self.assertEqual(list(x.lemmatise("ergo")), [{'lemma': 'ergo', 'morph': '-', 'form': 'ergo'}])

    def test_romanorum(self):
        x = Lemmatiseur(load=False)
        x.ajMorphos()
        load_mod_vars(x)
        lupus = Modele([
            "modele:lupus",
            "R:1:2,0",
            "des:1-12:1:$lupus"
        ], parent=x)
        x._modeles[lupus.gr()] = lupus

        doctus = Modele([
            "modele:doctus",
            "R:0:2,0",
            "R:1:2,ĭ",
            "R:2:2,īssĭm",
            "des:13-48:0:$lupus;$uita;$templum",
            "des:49-84:1:$compar;$compar;ŭs;ŭs;ŭs;ōrĭs;ōrī;ōrĕ;ōră;ōră;ōră;ōrŭm;ōrĭbŭs",
            "des:85-120:2:$lupus;$uita;$templum"
        ], parent=x)
        x._modeles[doctus.gr()] = doctus

        liberi = Modele([
            "modele:liberi",
            "pere:lupus",
            "R:1:1,0",
            "abs:1-6"
        ], parent=x)
        x._modeles[liberi.gr()] = liberi

        x._parse_lemme("Rōmānus|doctus|||a, um|2392", orig=0)
        x._parse_lemme("Rōmānus2|lupus|||i, m.|8", orig=0)
        x._parse_lemme("Rōmāni|liberi|||orum, m.|262", orig=0)

        self.assertEqual(
            sorted(list(set([r["lemma"]+"|"+r["pos"] for r in x.lemmatise("Romanorum", pos=True)]))),
            ["Romani|n", "Romanus|a", "Romanus|n"]
        )
        self.assertEqual(
            sorted(list(set([r["lemma"]+"|"+r["pos"] for r in x.lemmatise("Romana", pos=True)]))),
            ["Romanus|a"]
        )
