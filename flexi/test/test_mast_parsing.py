import unittest
from io import StringIO

from lxml import etree

from flexi.config import TEST_FILE_DIR
from flexi.parsing.magma import MagmaGrammar


class TestGrammar(unittest.TestCase):
    def test_basic(self):
        grammar = MagmaGrammar('EnglishFtmlTestGrammar', 'Eng')
        masts = grammar.parse_ftml_to_sentences(
            etree.parse(
                StringIO(
                    '<p>There is a <emph>node</emph>.</p>'
                )
            ).getroot()
        )
        self.assertEqual(len(masts), 1)
        self.assertGreaterEqual(len(masts[0]), 1)
        mast = masts[0][0]
        string = grammar.linearize_mast(mast)
        # some polishing is still needed
        self.assertEqual(string, 'There is a <emph > node </emph>.')

    def test_ftml_files_parsability(self):
        grammar = MagmaGrammar('EnglishFtmlTestGrammar', 'Eng')
        for testfile in ['positive-integer.en.html']:
            with self.subTest(testfile=testfile):
                ftml = etree.parse(
                    TEST_FILE_DIR / 'ftml' / testfile,
                )
                masts = grammar.parse_ftml_to_sentences(ftml.getroot())
                self.assertGreater(len(masts), 0, f'No MASTs parsed from {testfile}')
