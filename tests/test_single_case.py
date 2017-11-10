from unittest import TestCase
from pycollatinus import Lemmatiseur
from pycollatinus.parser import Parser
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
        parser = Parser(x)
        parser.ajMorphos()
        m = parser.parse_modele(["modele:inv", "R:0:0,0", "des:416:0:-"])
        x._modeles[m.gr()] = m

        parser.parse_lemme("nĕc|inv|||adv.|6689", origin=0)
        parser.parse_lemme("ergō=ērgō|inv|||conj.|1450", origin=0)

        self.assertEqual(list(x.lemmatise("nec")), [{'lemma': 'nec', 'morph': '-', 'form': 'nec'}])
        self.assertEqual(list(x.lemmatise("ergo")), [{'lemma': 'ergo', 'morph': '-', 'form': 'ergo'}])

    def test_romanorum(self):
        x = Lemmatiseur(load=False)
        parser = Parser(x)
        parser.ajMorphos()
        load_mod_vars(x)

        lupus = parser.parse_modele(["modele:lupus", "R:1:2,0", "des:1-12:1:$lupus", "pos:n"])
        x._modeles[lupus.gr()] = lupus
        doctus = parser.parse_modele([
            "modele:doctus", "R:0:2,0", "R:1:2,ĭ", "R:2:2,īssĭm",
            "des:13-48:0:$lupus;$uita;$templum",
            "des:49-84:1:$compar;$compar;ŭs;ŭs;ŭs;ōrĭs;ōrī;ōrĕ;ōră;ōră;ōră;ōrŭm;ōrĭbŭs",
            "des:85-120:2:$lupus;$uita;$templum", "pos:a"
        ])
        x._modeles[doctus.gr()] = doctus
        liberi = parser.parse_modele(["modele:liberi", "pere:lupus", "R:1:1,0", "abs:1-6", "pos:n"])
        x._modeles[liberi.gr()] = liberi

        parser.parse_lemme("Rōmānus|doctus|||a, um|2392", origin=0)
        parser.parse_lemme("Rōmānus2|lupus|||i, m.|8", origin=0)
        Romani = parser.parse_lemme("Rōmāni|liberi|||orum, m.|262", origin=0)

        self.assertEqual(
            sorted(list(set([r["lemma"]+"|"+r["pos"] for r in x.lemmatise("Romanorum", pos=True)]))),
            ["Romani|n", "Romanus|a", "Romanus|n"]
        )
        self.assertEqual(
            sorted(list(set([r["lemma"]+"|"+r["pos"] for r in x.lemmatise("Romana", pos=True)]))),
            ["Romanus|a"]
        )

    def test_contraction(self):

        x = Lemmatiseur(load=False)
        parser = Parser(x)
        parser.ajMorphos()
        parser.ajContractions()
        parser.ajAssims()
        load_mod_vars(x)
        amo = parser.parse_modele("""modele:amo
R:0:1,0
R:1:1,āv
R:2:1,āt
des:121-126:0:ō̆;ās;ăt;āmŭs;ātĭs;ānt
des:127-132:0:ābăm;ābās;ābăt;ābāmŭs;ābātĭs;ābānt
des:133-138:0:ābō̆;ābĭs;ābĭt;ābĭmŭs;ābĭtĭs;ābūnt
des:139-144:1:ī;īstī;ĭt;ĭmŭs;īstĭs;ērūnt,ērĕ
des:145-150:1:ĕrăm;ĕrās;ĕrăt;ĕrāmŭs;ĕrātĭs;ĕrānt
des:151-156:1:ĕrō̆;ĕrī̆s;ĕrĭt;ĕrī̆mŭs;ĕrī̆tĭs;ĕrīnt
des:157-162:0:$em
des:163-168:0:ārĕm;ārēs;ārĕt;ārēmŭs;ārētĭs;ārēnt
des:169-174:1:ĕrĭm;ĕrī̆s;ĕrĭt;ĕrī̆mŭs;ĕrī̆tĭs;ĕrīnt
des:175-180:1:īssĕm;īssēs;īssĕt;īssēmŭs;īssētĭs;īssēnt
des:181-186:0:ā;ātĕ;ātō;ātō;ātōtĕ;āntō
des:187:0:ārĕ
des:188:1:īssĕ
des:188:0:āssĕ
des:189-200:0:āns;āns;āntĕm;āntĭs;āntī;āntĕ;āntēs;āntēs;āntēs;āntĭŭm,āntŭm;āntĭbŭs;āntĭbŭs
des:201-212:0:āns;āns;āntĕm;āntĭs;āntī;āntĕ;āntēs;āntēs;āntēs;āntĭŭm,āntŭm;āntĭbŭs;āntĭbŭs
des:213-224:0:āns;āns;āns;āntĭs;āntī;āntĕ;āntĭă;āntĭă;āntĭă;āntĭŭm,āntŭm;āntĭbŭs;āntĭbŭs
des:225-236:2:ūr$lupus
des:237-248:2:ūr$uita
des:249-260:2:ūr$templum
des:261-264:0:āndŭm;āndī;āndō;āndō
des:265,266:2:ŭm;ū
des:267-272:0:ŏr;ārĭs,ārĕ;ātŭr;āmŭr;āmĭnī;āntŭr
des:273-278:0:ābăr;ābārĭs,ābārĕ;ābātŭr;ābāmŭr;ābāmĭnī;ābāntŭr
des:279-284:0:ābŏr;ābĕrĭs,ābĕrĕ;ābĭtŭr;ābĭmŭr;ābĭmĭnī;ābūntŭr
des:285-290:0:ĕr;ērĭs,ērĕ;ētŭr;ēmŭr;ēmĭnī;ēntŭr
des:291-296:0:ārĕr;ārērĭs,ārērĕ;ārētŭr;ārēmŭr;ārēmĭnī;ārēntŭr
des:297,298:0:ārĕ;āmĭnī
des:299-301:0:ātŏr;ātŏr;āntŏr
des:302:0:ārī
des:303-314:2:$lupus
des:315-326:2:$uita
des:327-338:2:$templum
des:339-350:0:ānd$lupus
des:351-362:0:ānd$uita
des:363-374:0:ānd$templum""".split("\n"))
        x._modeles[amo.gr()] = amo
        moneo = parser.parse_modele("""modele:moneo
pere:amo
R:0:2,0
R:2:-
des:121-126:0:ĕō̆;ēs;ĕt;ēmŭs;ētĭs;ēnt
des:127-132:0:ēbăm;ēbās;ēbăt;ēbāmŭs;ēbātĭs;ēbānt
des:133-138:0:ēbō̆;ēbĭs;ēbĭt;ēbĭmŭs;ēbĭtĭs;ēbūnt
des:157-162:0:ĕăm;ĕās;ĕăt;ĕāmŭs;ĕātĭs;ĕānt
des:163-168:0:ērĕm;ērēs;ērĕt;ērēmŭs;ērētĭs;ērēnt
des:181-186:0:ē;ētĕ;ētō;ētō;ētōtĕ;ēntō
des:187:0:ērĕ
des:188:1:īssĕ
des:189-200:0:$ens
des:201-212:0:$ens
des:213-224:0:ēns;ēns;ēns;ēntĭs;ēntī;ēntĕ;ēntĭă;ēntĭă;ēntĭă;ēntĭŭm,ēntŭm;ēntĭbŭs;ēntĭbŭs
des:261-264:0:ēndŭm;ēndī;ēndō;ēndō
des:267-272:0:ĕŏr;ērĭs,ērĕ;ētŭr;ēmŭr;ēmĭnī;ēntŭr
des:273-278:0:ēbăr;ēbārĭs,ēbārĕ;ēbātŭr;ēbāmŭr;ēbāmĭnī;ēbāntŭr
des:279-284:0:ēbŏr;ēbĕrĭs,ēbĕrĕ;ēbĭtŭr;ēbĭmŭr;ēbĭmĭnī;ēbūntŭr
des:285-290:0:ĕăr;ĕārĭs,ĕārĕ;ĕātŭr;ĕāmŭr;ĕāmĭnī;ĕāntŭr
des:291-296:0:ērĕr;ērērĭs,ērērĕ;ērētŭr;ērēmŭr;ērēmĭnī;ērēntŭr
des:297,298:0:ērĕ;ēmĭnī
des:299-301:0:ētŏr;ētŏr;ēntŏr
des:302:0:ērī
des:339-350:0:ēndŭs;ēndĕ;ēndŭm;ēndī;ēndō;ēndō;ēndī;ēndī;ēndōs;ēndōrŭm;ēndīs;ēndīs
des:351-362:0:ēndă;ēndă;ēndăm;ēndāe;ēndāe;ēndā;ēndāe;ēndāe;ēndās;ēndārŭm;ēndīs;ēndīs
des:363-374:0:ēndŭm;ēndŭm;ēndŭm;ēndī;ēndō;ēndō;ēndă;ēndă;ēndă;ēndōrŭm;ēndīs;ēndīs""".split("\n"))
        x._modeles[moneo.gr()] = moneo
        lego = parser.parse_modele("""modele:lego
pere:moneo
R:0:1,0
des:121-126:0:ō̆;ĭs;ĭt;ĭmŭs;ĭtĭs;ūnt
des:133-138:0:ăm;ēs;ĕt;ēmŭs;ētĭs;ēnt
des:157-162:0:ăm;ās;ăt;āmŭs;ātĭs;ānt
des:163-168:0:ĕrĕm;ĕrēs;ĕrĕt;ĕrēmŭs;ĕrētĭs;ĕrēnt
des:181-186:0:ĕ;ĭtĕ;ĭtō;ĭtō;ĭtōtĕ;ūntō
des:187:0:ĕrĕ
des:267-272:0:ŏr;ĕrĭs,ĕrĕ;ĭtŭr;ĭmŭr;ĭmĭnī;ūntŭr
des:279-284:0:ăr;ērĭs,ērĕ;ētŭr;ēmŭr;ēmĭnī;ēntŭr
des:285-290:0:ăr;ārĭs,ārĕ;ātŭr;āmŭr;āmĭnī;āntŭr
des:291-296:0:ĕrĕr;ĕrērĭs,ĕrērĕ;ĕrētŭr;ĕrēmŭr;ĕrēmĭnī;ĕrēntŭr
des:297,298:0:ĕrĕ;ĭmĭnī
des:299-301:0:ĭtŏr;ĭtŏr;ūntŏr
des:302:0:ī""".split("\n"))
        x._modeles[lego.gr()] = lego

        parser.parse_lemme("lēgo2|amo|||as, are|34", origin=0)
        parser.parse_lemme("lĕgo|lego|lēg|lēct|is, ere, legi, lectum|619", origin=0)

        self.assertEqual(
            x.lemmatise_multiple("legarat legerat", get_lemma_object=True),
            [
                [{'lemma': x.lemme("lego2"),
                 'morph': '3ème singulier indicatif PQP actif', 'form': 'legauerat'}],
                [{'lemma': x.lemme("lego"),
                 'morph': '3ème singulier indicatif PQP actif', 'form': 'legerat'}]
            ]
        )

    def test_hierosylima(self):
        test = " Hierosolyma"
        x = Lemmatiseur(load=False)
        parser = Parser(x)
        parser.ajMorphos()
        parser.ajContractions()
        parser.ajAssims()
        load_mod_vars(x)
        parser.register_modele(parser.parse_modele("""modele:uita
R:1:1,0
des:1-12:1:$uita""".split("\n")))
        parser.register_modele(parser.parse_modele("""modele:roma
pere:uita
des:413:1:āe""".split("\n")))
        parser.register_modele(parser.parse_modele("""modele:doctus
R:0:2,0
R:1:2,ĭ
R:2:2,īssĭm
des:13-48:0:$lupus;$uita;$templum
des:49-84:1:$compar;$compar;ŭs;ŭs;ŭs;ōrĭs;ōrī;ōrĕ;ōră;ōră;ōră;ōrŭm;ōrĭbŭs
des:85-120:2:$lupus;$uita;$templum""".split("\n")))
        parser.register_modele(parser.parse_modele("""modele:aureus
pere:doctus
des:14:0:ŭs
abs:49-120""".split("\n")))

        parser.parse_lemme("Hĭĕrŏsŏlўma|roma|||ae, f.|5")
        parser.parse_lemme("Lўcāŏnĭus|aureus|||a, um|5")
        self.assertEqual(
            list(x.lemmatise("Hierosolymam")),
            [{'lemma': 'Hierosolyma', 'form': 'hierosolymam', 'morph': 'accusatif singulier'}]
        )
        self.assertEqual(
            list(x.lemmatise("Lycaonios")),
            [{'morph': 'accusatif masculin pluriel', 'lemma': 'Lycaonius', 'form': 'lycaonios'}]
        )

    def test_sequens(self):

        x = Lemmatiseur(load=False)
        parser = Parser(x)
        parser.ajMorphos()
        parser.ajContractions()
        parser.ajAssims()
        load_mod_vars(x)

        doctus = parser.parse_modele("""modele:doctus
R:0:2,0
R:1:2,ĭ
R:2:2,īssĭm
des:13-48:0:$lupus;$uita;$templum
des:49-84:1:$compar;$compar;ŭs;ŭs;ŭs;ōrĭs;ōrī;ōrĕ;ōră;ōră;ōră;ōrŭm;ōrĭbŭs
des:85-120:2:$lupus;$uita;$templum""".split("\n"))
        x._modeles[doctus.gr()] = doctus
        fortis = parser.parse_modele("""modele:fortis
pere:doctus
R:0:2,0
R:4:K
R:5:2,ĭ
des:13,14,25,26:4:-;-;-;-
des:15-24:1:ĕm;ĭs;ī;ī;ēs;ēs;ēs,īs;ĭŭm;ĭbŭs
des:27-36:1:ĕm;ĭs;ī;ī;ēs;ēs;ēs,īs;ĭŭm;ĭbŭs
des:37-48:1:ĕ;ĕ;ĕ;ĭs;ī;ī;ĭă;ĭă;ĭă;ĭŭm;ĭbŭs
des:49-84:1:ĭ$compar;ĭ$compar;ĭŭs;ĭŭs;ĭŭs;ĭōrĭs;ĭōrī;ĭōrĕ;ĭōră;ĭōră;ĭōră;ĭōrŭm;ĭōrĭbŭs
des:85-120:1:īssĭm$lupus;īssĭm$uita;īssĭm$templum""".split("\n"))
        x._modeles[fortis.gr()] = fortis
        infans = parser.parse_modele("""modele:infans
pere:fortis
des+:22,34,46:1:ŭm3""".split("\n"))
        x._modeles[infans.gr()] = infans
        lemma = parser.parse_lemme("sĕquens=sĕquēns|infans|sĕquēnt||entis|44")
        self.assertEqual(
            sorted(lemma.possible_forms()),
            sorted(['sequentioris', 'sequentissimae', 'sequentissimam', 'sequentissimum', 'sequentiores',
                    'sequentissimorum', 'sequentissimi', 'sequentissime', 'sequentis', 'sequentior', 'sequentem',
                    'sequentiori', 'sequentum', 'sequentissimas', 'sequentiorem', 'sequens', 'sequentiora',
                    'sequentius', 'sequentissimos', 'sequentibus', 'sequenti', 'sequentiorum', 'sequentissimis',
                    'sequentes', 'sequente', 'sequentioribus', 'sequentissimus', 'sequentiore', 'sequentissima',
                    'sequentissimarum', 'sequentia', 'sequentissimo', 'sequentium'])
        )