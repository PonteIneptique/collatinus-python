from pycollatinus import Lemmatiseur
from pycollatinus.parser import Parser
from tests.util import ExtendedTestCase


class TestSentences(ExtendedTestCase):
    lemmatizer = Lemmatiseur()
    parser = Parser(lemmatizer)

    def test_cogito_ergo_sum(self):
        results = TestSentences.lemmatizer.lemmatise_multiple("cogito ergo sum")
        self.assertLemmatisationMultipleEqual(
            results,
            [
                [{'lemma': 'cogo', 'morph': '2ème singulier impératif futur actif', 'form': 'cogito'},
                 {'lemma': 'cogo', 'morph': '3ème singulier impératif futur actif', 'form': 'cogito'},
                 {'lemma': 'cogito', 'morph': '1ère singulier indicatif présent actif', 'form': 'cogito'},
                 {'lemma': 'cogito', 'morph': '1ère singulier indicatif présent actif', 'form': 'cogito'}],
                [{'lemma': 'ergo', 'morph': '1ère singulier indicatif présent actif', 'form': 'ergo'},
                 {'lemma': 'ergo', 'morph': 'positif', 'form': 'ergo'},
                 {'lemma': 'ergo', 'morph': '-', 'form': 'ergo'}],
                [{'lemma': 'sum', 'morph': '1ère singulier indicatif présent actif', 'form': 'sum'}]
            ],
            "Ergo, sum and cogito should be recognized"
        )

    def test_ego_romanus(self):
        results = TestSentences.lemmatizer.lemmatise_multiple("mihi Romanorum", pos=True)
        self.maxDiff = 5000
        self.assertLemmatisationMultipleEqual(results, [
            [
                {'form': 'mihi', 'morph': 'datif féminin singulier', 'lemma': 'ego', 'pos': 'p'},
                {'form': 'mihi', 'morph': 'datif masculin singulier', 'lemma': 'ego', 'pos': 'p'}
            ],
            [
                {'form': 'romanorum', 'pos': 'n', 'morph': 'génitif pluriel', 'lemma': 'Romani'},
                {'form': 'romanorum', 'pos': 'n', 'morph': 'génitif pluriel', 'lemma': 'Romanus'},
                {'form': 'romanorum', 'pos': 'a', 'morph': 'génitif masculin pluriel', 'lemma': 'Romanus'},
                {'form': 'romanorum', 'pos': 'a', 'morph': 'génitif neutre pluriel', 'lemma': 'Romanus'},
            ]
        ])

    def test_nec_aliud_sequenti_quadriduo(self):
        """ Check that aliud, an irregular form, is well behaving as well as nec, an invariable """
        results = TestSentences.lemmatizer.lemmatise_multiple("nec aliud sequenti quadriduo")
        expected = [
            [{'lemma': 'nec', 'morph': '-', 'form': 'nec'}],
            [
                {'form': 'aliud', 'morph': 'nominatif neutre singulier', 'lemma': 'aliud'},
                {'form': 'aliud', 'morph': 'vocatif neutre singulier', 'lemma': 'aliud'},
                {'form': 'aliud', 'morph': 'accusatif neutre singulier', 'lemma': 'aliud'}
            ],
            [
                {'form': 'sequenti', 'morph': 'datif masculin singulier participe présent actif', 'lemma': 'sequor'},
                {'form': 'sequenti', 'morph': 'datif féminin singulier participe présent actif', 'lemma': 'sequor'},
                {'form': 'sequenti', 'morph': 'datif neutre singulier participe présent actif', 'lemma': 'sequor'},
                {'form': 'sequenti', 'morph': 'datif masculin singulier participe présent actif', 'lemma': 'sequo'},
                {'form': 'sequenti', 'morph': 'datif féminin singulier participe présent actif', 'lemma': 'sequo'},
                {'form': 'sequenti', 'morph': 'datif neutre singulier participe présent actif', 'lemma': 'sequo'},
                {'form': 'sequenti', 'morph': 'datif masculin singulier', 'lemma': 'sequens'},
                {'form': 'sequenti', 'morph': 'ablatif masculin singulier', 'lemma': 'sequens'},
                {'form': 'sequenti', 'morph': 'datif féminin singulier', 'lemma': 'sequens'},
                {'form': 'sequenti', 'morph': 'ablatif féminin singulier', 'lemma': 'sequens'},
                {'form': 'sequenti', 'morph': 'datif neutre singulier', 'lemma': 'sequens'},
                {'form': 'sequenti', 'morph': 'ablatif neutre singulier', 'lemma': 'sequens'}
            ],
            [
                {'form': 'quadriduo', 'morph': 'datif singulier', 'lemma': 'quadriduum'},
                {'form': 'quadriduo', 'morph': 'ablatif singulier', 'lemma': 'quadriduum'}
            ]
        ]
        self.assertLemmatisationMultipleEqual(
            results, expected, "Invar should be correctly recognized"
        )

    def test_possible_forms(self):
        self.assertEqual(
            sorted(list(self.lemmatizer.lemmatise("bellus", get_lemma_object=True))[0]["lemma"].possible_forms()),
            sorted([
                'belliora',
                'bellae',
                'bellam',
                'bellissimis',
                'bellioris',
                'bellissimarum',
                'bellissime',
                'bellorum',
                'bellissimum',
                'belliori',
                'bellissimorum',
                'bellissima',
                'bellum',
                'bellus',
                'bellissimae',
                'bellis',
                'belli',
                'belliores',
                'bellissimo',
                'bellissimas',
                'bellioribus',
                'bellas',
                'bellior',
                'belliore',
                'bellarum',
                'bella',
                'bellissimus',
                'bellissimos',
                'belliorum',
                'belle',
                'bellos',
                'belliorem',
                'bellissimam',
                'bello',
                'bellissimi',
                'bellius'
            ])
        )

    def test_assimilations(self):
        """ Check that lemmatizer handles correctly assimilations """
        results = TestSentences.lemmatizer.lemmatise_multiple("adprehendant expectari")
        self.assertLemmatisationMultipleEqual(
            results,
            [
                [{'lemma': 'apprehendo', 'form': 'apprehendant', 'morph': '3ème pluriel subjonctif présent actif'}],
                [{'lemma': 'exspecto', 'form': 'exspectari', 'morph': 'infinitif présent passif'}]
            ]
        )

    def test_contractions(self):
        """ Check that the lemmatizer handles correctly contractions """
        results = TestSentences.lemmatizer.lemmatise_multiple("exspirasset legarat legerat", get_lemma_object=True)
        self.assertLemmatisationMultipleEqual(
            results,
            [
                [
                    {'form': 'exspirauisset', 'morph': '3ème singulier subjonctif PQP actif',
                     'lemma': TestSentences.lemmatizer.lemme("exspiro")}
                ],
                [
                    {'lemma': TestSentences.lemmatizer.lemme("lego2"),
                     'morph': '3ème singulier indicatif PQP actif', 'form': 'legauerat'}
                ],
                [
                    {'lemma': TestSentences.lemmatizer.lemme("lego"),
                     'morph': '3ème singulier indicatif PQP actif', 'form': 'legerat'}
                ]
            ],
            _lemma_obj=True
        )

    def test_lower_case(self):
        results = TestSentences.lemmatizer.lemmatise("Christi", get_lemma_object=True)
        self.assertLemmatisationEqual(
            results,
            [
                {'lemma': TestSentences.lemmatizer.lemme("Christus"), 'form': 'christi', 'morph': 'génitif singulier'},
                {'lemma': TestSentences.lemmatizer.lemme("Christus"), 'form': 'christi', 'morph': 'nominatif pluriel'},
                {'lemma': TestSentences.lemmatizer.lemme("Christus"), 'form': 'christi', 'morph': 'vocatif pluriel'},
                {'lemma': TestSentences.lemmatizer.lemme("christus2"), 'form': 'christi', 'morph': 'génitif masculin singulier'},
                {'lemma': TestSentences.lemmatizer.lemme("christus2"), 'form': 'christi', 'morph': 'nominatif masculin pluriel'},
                {'lemma': TestSentences.lemmatizer.lemme("christus2"), 'form': 'christi', 'morph': 'vocatif masculin pluriel'},
                {'lemma': TestSentences.lemmatizer.lemme("christus2"), 'form': 'christi', 'morph': 'génitif neutre singulier'}
            ], _lemma_obj=True
        )

    def test_roman_num(self):
        results = TestSentences.lemmatizer.lemmatise_multiple("XIV MDCXXIV xiv", get_lemma_object=True, as_list=True)
        self.assertLemmatisationMultipleEqual(
            results,
            [
                [
                    {'lemma': TestSentences.parser.parse_lemme("XIV|inv|||adj. num.|1", 0, _deramise=False), 'form': 'XIV', 'morph': ''},
                ],
                [
                    {'lemma': TestSentences.parser.parse_lemme("MDCXXIV|inv|||adj. num.|1", 0, _deramise=False), 'form': 'MDCXXIV', 'morph': ''},
                ],
                [
                    {'lemma': TestSentences.parser.parse_lemme("XIV|inv|||adj. num.|1", 0, _deramise=False), 'form': 'XIV', 'morph': ''},
                ]
            ], _lemma_obj=True
        )
