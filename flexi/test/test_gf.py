import unittest

from flexi.parsing.gf_ast import GfAst


class TestGF(unittest.TestCase):
    def test_ast_parser(self):
        GfAst.from_str("function arg")
        GfAst.from_str("(function arg)")
        self.assertRaises(ValueError, GfAst.from_str, "(function arg")

        # function names can be surrounded by single quotes
        a = GfAst.from_str("'abc def'")
        self.assertEqual(a.node, 'abc def')

