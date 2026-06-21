import unittest

from flexi.config import TEST_FILE_DIR
from flexi.lexicon import VerbalizationRecord, Lexicon
from flexi.parsing.magma import MagmaGrammar


class TestLexicon(unittest.TestCase):
    def test_spec_parsing(self):
        r = VerbalizationRecord.from_spec('N2', '#1 finite:A subset:N of #2')
        self.assertEqual(r.typ, 'Kind2')
        self.assertEqual(r.main_argument, 1)
        self.assertEqual(r.gf_lin, "mkKind2 (makeCN 'finite:A' 'subset:N') of_Prep")
        self.assertEqual(r.depends_on_words, ['finite:A', 'subset:N'])

    def test_ftml_import(self):
        l = Lexicon('GoldbachLexicon', 'Eng')
        l.extend_from_ftml(
            TEST_FILE_DIR / 'testmathhub' / 'goldbach' / 'source' / 'goldbach.en.html'
        )
        l.write_gf()
        grammar = MagmaGrammar('GoldbachLexicon', 'Eng')
        grammar.parse_to_aststr(
            'there is an even integer .',
            category='Sentence'
        )
