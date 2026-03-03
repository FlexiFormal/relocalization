import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from flexi.semconstr.conversion import convert, Context
from flexi.parsing.magma import MagmaGrammar
from flexi.config import TEST_FILE_DIR


grammar = MagmaGrammar('EnglishFtmlTestGrammar', 'Eng')

for input_file in [
    TEST_FILE_DIR / 'ftml' / 'positive-integer.en.html',
    # TEST_FILE_DIR / 'ftml' / 'quiver-walk.en.html',
] if len(sys.argv) == 1 else [Path(arg) for arg in sys.argv[1:]]:
        print(input_file.name)
        for i, sentence in enumerate(grammar.parse_ftml_to_sentences(input_file), start=1):
            print(f'<h2>Sentence {i}</h2>')
            for mast in sentence:
                # print(mast)
                try:
                    decls, r = convert(mast, Context())
                    print('RESULT:\n', decls, str(r))
                    print('SIMPLIFIED:')
                    print(str(r.beta_reduced()))
                    print(str(r.simplified()))
                except Exception as e:
                    # print error and stack trace, but continue with the next sentence
                    print(f'Error converting sentence {i}: {e}')
                    import traceback
                    traceback.print_exc()
                    break
