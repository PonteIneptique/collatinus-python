from unittest import TestCase


class ExtendedTestCase(TestCase):
    def assertLemmatisationEqual(self, origin, result, message=None, _lemma_obj=False):
        if _lemma_obj:
            _origin = sorted(list(origin), key=lambda x: x["morph"]+x["lemma"].cle()+x.get("pos", "-"))
            _result = sorted(result, key=lambda x: x["morph"]+x["lemma"].cle()+x.get("pos", "-"))
        else:
            _origin = sorted(list(origin), key=lambda x: x["morph"]+x["lemma"]+x.get("pos", "-"))
            _result = sorted(result, key=lambda x: x["morph"]+x["lemma"]+x.get("pos", "-"))

        self.assertEqual(
            _origin, _result, message
        )

    def assertLemmatisationMultipleEqual(self, origin, result, message=None, _lemma_obj=False):
        if _lemma_obj:
            _origin = [
                sorted(list(token), key=lambda x:x["morph"]+x["lemma"].cle()+x.get("pos", "-"))
                for token in origin
            ]
            _result = [
                sorted(token, key=lambda x:x["morph"]+x["lemma"].cle()+x.get("pos", "-"))
                for token in result
            ]
        else:
            _origin = [
                sorted(list(token), key=lambda x:x["morph"]+x["lemma"]+x.get("pos", "-"))
                for token in origin
            ]
            _result = [
                sorted(token, key=lambda x:x["morph"]+x["lemma"]+x.get("pos", "-"))
                for token in result
            ]
        for index, token in enumerate(_origin):
            self.assertEqual(
                token,
                _result[index],
                "Token {} should have the results than expected ".format(index)
            )