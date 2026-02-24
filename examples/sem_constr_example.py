import sys
from pathlib import Path

from flexi.semconstr.conversion import convert_1

sys.path.append(str(Path(__file__).parent.parent))

from flexi.parsing.magma import MagmaGrammar
from flexi.config import TEST_FILE_DIR


grammar = MagmaGrammar('EnglishFtmlTestGrammar', 'Eng')

for input_file in [
    TEST_FILE_DIR / 'ftml' / 'positive-integer.en.html',
] if len(sys.argv) == 1 else [Path(arg) for arg in sys.argv[1:]]:
        print(input_file.name)
        for i, sentence in enumerate(grammar.parse_ftml_to_sentences(input_file), start=1):
            print(f'<h2>Sentence {i}</h2>')
            for mast in sentence:
                print(mast)
                try:
                    print('RESULT:\n', convert_1(mast))
                except Exception as e:
                    # print error and stack trace, but continue with the next sentence
                    print(f'Error converting sentence {i}: {e}')
                    import traceback
                    traceback.print_exc()
