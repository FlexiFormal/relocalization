"""
Simple demonstration of using the workbench to visualize a parsed sentence
"""

import sys
import webbrowser
from pathlib import Path

# ensure flexi is in path, even if not installed
sys.path.append(str(Path(__file__).parent.parent))

from flexi.parsing.magma import MagmaGrammar
from flexi.config import TEST_FILE_DIR
import flexi.workbench as wb


result_file = Path('/tmp/simple-def-exp.html')
# input_file = TEST_FILE_DIR / 'ftml' / 'positive-integer.en.html'

grammar = MagmaGrammar('EnglishFtmlTestGrammar', 'Eng')

with wb.new_workbench(result_file, 'Parsing example sentences'):
    for input_file in [
        TEST_FILE_DIR / 'ftml' / 'positive-integer.en.html',
        TEST_FILE_DIR / 'ftml' / 'quiver-walk.en.html',
        TEST_FILE_DIR / 'ftml' / 'comprehension-reduction-minimal.en.html',
        TEST_FILE_DIR / 'ftml' / 'inner-product-minimal.en.html',
    ] if len(sys.argv) == 1 else [Path(arg) for arg in sys.argv[1:]]:

        wb.set_default_grammar(grammar)
        wb.push_html(f'<h1>Original definition (<code>{input_file.name}</code>)</h1>')
        wb.push_html(input_file.read_text())
        for i, sentence in enumerate(grammar.parse_ftml_to_sentences(input_file), start=1):
            wb.push_html(f'<h2>Sentence {i}</h2>')
            for mast in sentence:
                wb.push_sentence_mast(mast)

webbrowser.open(str(result_file))
