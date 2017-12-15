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
                [{'lemma': 'cogo', 'morph': '2ème singulier impératif futur actif', 'form': 'cogito',
                  'radical': 'cog', 'desinence': 'ito'},
                 {'lemma': 'cogo', 'morph': '3ème singulier impératif futur actif', 'form': 'cogito',
                  'radical': 'cog', 'desinence': 'ito'},
                 {'lemma': 'cogito', 'morph': '1ère singulier indicatif présent actif', 'form': 'cogito',
                  'radical': 'cogit', 'desinence': 'o'},
                 {'lemma': 'cogito', 'morph': '1ère singulier indicatif présent actif', 'form': 'cogito',
                  'radical': 'cogit', 'desinence': 'o'}],
                [{'lemma': 'ergo', 'morph': '1ère singulier indicatif présent actif', 'form': 'ergo',
                  'radical': 'erg', 'desinence': 'o'},
                 {'lemma': 'ergo', 'morph': 'positif', 'form': 'ergo',
                  'radical': 'ergo', 'desinence': ''},
                 {'lemma': 'ergo', 'morph': '-', 'form': 'ergo',
                  'radical': 'ergo', 'desinence': ''}],
                [{'lemma': 'sum', 'morph': '1ère singulier indicatif présent actif', 'form': 'sum',
                  'radical': 's', 'desinence': 'um'}]
            ],
            "Ergo, sum and cogito should be recognized"
        )

    def test_ego_romanus(self):
        results = TestSentences.lemmatizer.lemmatise_multiple("mihi Romanorum", pos=True)
        self.maxDiff = 5000
        self.assertLemmatisationMultipleEqual(results, [
            [
                {'form': 'mihi', 'morph': 'datif féminin singulier', 'lemma': 'ego', 'pos': 'p', "radical": "", "desinence": "mihi"},
                {'form': 'mihi', 'morph': 'datif masculin singulier', 'lemma': 'ego', 'pos': 'p', "radical": "", "desinence": "mihi"}
            ],
            [
                {'form': 'romanorum', 'pos': 'n', 'morph': 'génitif pluriel', 'lemma': 'Romani', "radical": "Roman", "desinence": "orum"},
                {'form': 'romanorum', 'pos': 'n', 'morph': 'génitif pluriel', 'lemma': 'Romanus', "radical": "Roman", "desinence": "orum"},
                {'form': 'romanorum', 'pos': 'a', 'morph': 'génitif masculin pluriel', 'lemma': 'Romanus', "radical": "Roman", "desinence": "orum"},
                {'form': 'romanorum', 'pos': 'a', 'morph': 'génitif neutre pluriel', 'lemma': 'Romanus', "radical": "Roman", "desinence": "orum"},
            ]
        ])

    def test_nec_aliud_sequenti_quadriduo(self):
        """ Check that aliud, an irregular form, is well behaving as well as nec, an invariable """
        results = TestSentences.lemmatizer.lemmatise_multiple("nec aliud sequenti quadriduo")
        expected = [
            [{'lemma': 'nec', 'morph': '-', 'form': 'nec', 'radical': 'nec', 'desinence': ''}],
            [
                {'form': 'aliud', 'morph': 'nominatif neutre singulier', 'lemma': 'aliud',
                                                                                  'radical': None, 'desinence': None},
                {'form': 'aliud', 'morph': 'vocatif neutre singulier', 'lemma': 'aliud',
                                                                                  'radical': None, 'desinence': None},
                {'form': 'aliud', 'morph': 'accusatif neutre singulier', 'lemma': 'aliud',
                                                                                  'radical': None, 'desinence': None},
            ],
            [
                {'form': 'sequenti', 'morph': 'datif masculin singulier participe présent actif', 'lemma': 'sequor',
                 'radical': 'sequ', 'desinence': 'enti'},
                {'form': 'sequenti', 'morph': 'datif féminin singulier participe présent actif', 'lemma': 'sequor',
                 'radical': 'sequ', 'desinence': 'enti'},
                {'form': 'sequenti', 'morph': 'datif neutre singulier participe présent actif', 'lemma': 'sequor',
                 'radical': 'sequ', 'desinence': 'enti'},
                {'form': 'sequenti', 'morph': 'datif masculin singulier participe présent actif', 'lemma': 'sequo',
                 'radical': 'sequ', 'desinence': 'enti'},
                {'form': 'sequenti', 'morph': 'datif féminin singulier participe présent actif', 'lemma': 'sequo',
                 'radical': 'sequ', 'desinence': 'enti'},
                {'form': 'sequenti', 'morph': 'datif neutre singulier participe présent actif', 'lemma': 'sequo',
                 'radical': 'sequ', 'desinence': 'enti'},
                {'form': 'sequenti', 'morph': 'datif masculin singulier', 'lemma': 'sequens',
                 'radical': 'sequent', 'desinence': 'i'},
                {'form': 'sequenti', 'morph': 'ablatif masculin singulier', 'lemma': 'sequens',
                 'radical': 'sequent', 'desinence': 'i'},
                {'form': 'sequenti', 'morph': 'datif féminin singulier', 'lemma': 'sequens',
                 'radical': 'sequent', 'desinence': 'i'},
                {'form': 'sequenti', 'morph': 'ablatif féminin singulier', 'lemma': 'sequens',
                 'radical': 'sequent', 'desinence': 'i'},
                {'form': 'sequenti', 'morph': 'datif neutre singulier', 'lemma': 'sequens',
                 'radical': 'sequent', 'desinence': 'i'},
                {'form': 'sequenti', 'morph': 'ablatif neutre singulier', 'lemma': 'sequens',
                 'radical': 'sequent', 'desinence': 'i'},
            ],
            [
                {'form': 'quadriduo', 'morph': 'datif singulier', 'lemma': 'quadriduum'
                    , 'radical': 'quadridu', 'desinence': 'o'},
                {'form': 'quadriduo', 'morph': 'ablatif singulier', 'lemma': 'quadriduum'
                    , 'radical': 'quadridu', 'desinence': 'o'}
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
                [{'lemma': 'apprehendo', 'form': 'apprehendant', 'morph': '3ème pluriel subjonctif présent actif',
                  "radical": "apprehend", "desinence": "ant"}],
                [{'lemma': 'exspecto', 'form': 'exspectari', 'morph': 'infinitif présent passif', "radical": "exspect",
                  "desinence": "ari"}]
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
                     'lemma': TestSentences.lemmatizer.lemme("exspiro"),
                     'radical': 'exspirav', 'desinence': 'isset'}
                ],
                [
                    {'lemma': TestSentences.lemmatizer.lemme("lego2"),
                     'morph': '3ème singulier indicatif PQP actif', 'form': 'legauerat',
                     'radical': 'legav', 'desinence': 'erat'}
                ],
                [
                    {'lemma': TestSentences.lemmatizer.lemme("lego"),
                     'morph': '3ème singulier indicatif PQP actif', 'form': 'legerat',
                     'radical': 'leg', 'desinence': 'erat'}
                ]
            ],
            _lemma_obj=True
        )

    def test_lower_case(self):
        results = TestSentences.lemmatizer.lemmatise("Christi", get_lemma_object=True)
        self.assertLemmatisationEqual(
            results,
            [
                {'lemma': TestSentences.lemmatizer.lemme("Christus"), 'form': 'christi', 'morph': 'génitif singulier',
                 'radical': 'Christ', 'desinence': 'i'},
                {'lemma': TestSentences.lemmatizer.lemme("Christus"), 'form': 'christi', 'morph': 'nominatif pluriel',
                 'radical': 'Christ', 'desinence': 'i'},
                {'lemma': TestSentences.lemmatizer.lemme("Christus"), 'form': 'christi', 'morph': 'vocatif pluriel',
                 'radical': 'Christ', 'desinence': 'i'},
                {'lemma': TestSentences.lemmatizer.lemme("christus2"), 'form': 'christi', 'morph': 'génitif masculin singulier',
                 'radical': 'christ', 'desinence': 'i'},
                {'lemma': TestSentences.lemmatizer.lemme("christus2"), 'form': 'christi', 'morph': 'nominatif masculin pluriel',
                 'radical': 'christ', 'desinence': 'i'},
                {'lemma': TestSentences.lemmatizer.lemme("christus2"), 'form': 'christi', 'morph': 'vocatif masculin pluriel',
                 'radical': 'christ', 'desinence': 'i'},
                {'lemma': TestSentences.lemmatizer.lemme("christus2"), 'form': 'christi', 'morph': 'génitif neutre singulier',
                 'radical': 'christ', 'desinence': 'i'}
            ], _lemma_obj=True
        )

    def test_roman_num(self):
        results = TestSentences.lemmatizer.lemmatise_multiple("XIV MDCXXIV xiv", get_lemma_object=True, as_list=True)
        self.assertLemmatisationMultipleEqual(
            results,
            [
                [
                    {'lemma': TestSentences.parser.parse_lemme("XIV|inv|||adj. num.|1", 0, _deramise=False),
                     'form': 'XIV', 'morph': '', 'radical': None, 'desinence': None},
                ],
                [
                    {'lemma': TestSentences.parser.parse_lemme("MDCXXIV|inv|||adj. num.|1", 0, _deramise=False),
                     'form': 'MDCXXIV', 'morph': '', 'radical': None, 'desinence': None},
                ],
                [
                    {'lemma': TestSentences.parser.parse_lemme("XIV|inv|||adj. num.|1", 0, _deramise=False),
                     'form': 'XIV', 'morph': '', 'radical': None, 'desinence': None},
                ]
            ], _lemma_obj=True
        )

    def test_when_there_is_a_non_word_char(self):
        results = TestSentences.lemmatizer.lemmatise_multiple(
            "Qui, quae , quod ! ", pos=True
        )
        self.assertEqual(len(results), 3, "Splitting should be operational")

    def test_when_there_is_a_suffixe(self):
        results = TestSentences.lemmatizer.lemmatise_multiple(
            "Et flavescit haphe gravesque draucis ", pos=True
        )
        self.assertLemmatisationMultipleEqual(
            results,
            [[{'pos': 'cd', 'form': 'et', 'lemma': 'et', 'morph': '-'}],
             [{'pos': 'v', 'form': 'flauescit', 'lemma': 'flavesco', 'morph': '3ème singulier indicatif présent actif'}],
             [{'pos': 'n', 'form': 'haphe', 'lemma': 'haphe', 'morph': 'nominatif singulier'},
              {'pos': 'n', 'form': 'haphe', 'lemma': 'haphe', 'morph': 'vocatif singulier'},
              {'pos': 'n', 'form': 'haphe', 'lemma': 'haphe', 'morph': 'ablatif singulier'}],
             [{'pos': 'a', 'form': 'graues', 'lemma': 'gravis', 'morph': 'nominatif masculin pluriel'},
              {'pos': 'a', 'form': 'graues', 'lemma': 'gravis', 'morph': 'vocatif masculin pluriel'},
              {'pos': 'a', 'form': 'graues', 'lemma': 'gravis', 'morph': 'accusatif masculin pluriel'},
              {'pos': 'a', 'form': 'graues', 'lemma': 'gravis', 'morph': 'nominatif féminin pluriel'},
              {'pos': 'a', 'form': 'graues', 'lemma': 'gravis', 'morph': 'vocatif féminin pluriel'},
              {'pos': 'a', 'form': 'graues', 'lemma': 'gravis', 'morph': 'accusatif féminin pluriel'},
              {'pos': 'v', 'form': 'graues', 'lemma': 'grauo', 'morph': '2ème singulier subjonctif présent actif'}],
             [{'pos': 'n', 'form': 'draucis', 'lemma': 'Draucus', 'morph': 'datif pluriel'},
              {'pos': 'n', 'form': 'draucis', 'lemma': 'Draucus', 'morph': 'ablatif pluriel'},
              {'pos': 'n', 'form': 'draucis', 'lemma': 'draucus', 'morph': 'datif pluriel'},
              {'pos': 'n', 'form': 'draucis', 'lemma': 'draucus', 'morph': 'ablatif pluriel'}],
             [{'pos': 'a', 'form': '', 'lemma': '', 'morph': ''}]]
        )
