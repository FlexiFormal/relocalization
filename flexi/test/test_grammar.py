import unittest

from flexi.parsing.magma import MagmaGrammar


class TestGrammar(unittest.TestCase):
    def test_sentences(self):
        grammar = MagmaGrammar('EnglishTestGrammar', 'Eng')

        # pairs (sentence, number of readings)
        sentences = [
            ('There is an integer.', 1),
            ('There are integers.', 1),
            ('Let $ n $ be an even integer.', 1),
            ('$ n $ is an even integer.', 1),
            ('$ n $ is an even integer iff $ ? $.', 1),
            ('$ 1 $ divides every integer.', 1),
            ('Some integer $ n $ divides every integer.', 1),
        ]

        for sentence, num_readings in sentences:
            with self.subTest(sentence=sentence):
                readings = grammar.parse_to_gfast(sentence)
                self.assertEqual(len(readings), num_readings)
