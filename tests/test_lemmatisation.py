from unittest import TestCase
from pycollatinus import Lemmatiseur


class TestSentences(TestCase):
    lemmatizer = Lemmatiseur()

    def assertLemmatisationEqual(self, origin, result, message=None):
        _origin = [
            sorted(token, key=lambda x:x["morph"]+x["lemma"]+x.get("pos", "-"))
            for token in origin
        ]
        _result = [
            sorted(token, key=lambda x:x["morph"]+x["lemma"]+x.get("pos", "-"))
            for token in result
        ]
        self.assertEqual(len(origin), len(result), "There should be as many token in origin as in result")
        for index, token in enumerate(origin):
            self.assertEqual(len(token), len(result[index]),
                             "Token {} should have the same size than its result".format(index)
                             )

        self.assertEqual(
            _origin, _result, message
        )

    def test_cogito_ergo_sum(self):
        results = TestSentences.lemmatizer.lemmatise_multiple("cogito ergo sum")
        self.assertLemmatisationEqual(
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
        self.assertLemmatisationEqual(results, [
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
        self.assertLemmatisationEqual(
            results, expected, "Invar should be correctly recognized"
        )

    def test_possible_forms(self):
        self.assertEqual(
            sorted(self.lemmatizer.lemmatise("bellus", get_lemma_object=True)[0]["lemma"].possible_forms()),
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
