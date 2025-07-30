import sys
from pathlib import Path

# ensure flexi is in path, even if not installed
sys.path.append(str(Path(__file__).parent.parent))

from flexi.parsing.document import ftml_to_doc
from flexi.parsing.magma import MagmaGrammar
from flexi.config import TEST_FILE_DIR

grammar = MagmaGrammar('XLTenMagma', 'Eng')

definition_file = TEST_FILE_DIR / 'ftml' / 'positive-integer.en.html'
definition_doc = ftml_to_doc(definition_file, grammar)


# result_file = Path('/tmp/simple-parse-wb.html')
#
#
# with wb.new_workbench(result_file, 'Example: Parsing the definition of positive integers'):
#     wb.set_default_grammar(grammar)
#     wb.push_html('<h1>Original definition</h1>')
#     wb.push_html(input_file.read_text())
#     for i, sentence in enumerate(grammar.parse_ftml_to_sentences(input_file), start=1):
#         wb.push_html(f'<h2>Sentence {i}</h2>')
#         for mast in sentence:
#             wb.push_sentence_mast(mast)
#
# webbrowser.open(str(result_file))
#
