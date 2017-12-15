from pycollatinus import Lemmatiseur
from tests.util import ExtendedTestCase


class TestDump(ExtendedTestCase):
    def test_dump_and_load(self):
        lemmatizer = Lemmatiseur()
        lemmatizer.compile()

        del lemmatizer

        lemmatizer = Lemmatiseur.load()
        results = lemmatizer.lemmatise_multiple("mihi Romanorum", pos=True)
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