import unittest

from flexi.parsing.mast import GfSymb


class TestGrammar(unittest.TestCase):
    def test_gf_symb_eq(self):
        self.assertEqual(GfSymb('for_term_stmt'), '~for_term_stmt#')