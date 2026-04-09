from flexi.config import RECONTEXTUALIZATION_CORPUS, TEST_FILE_DIR
from flexi.lexicon_gen import augment_lexicon, Lexicon
from flexi.parsing.document import ftml_to_doc
from flexi.parsing.magma import MagmaGrammar


def main():
    stmt_path = RECONTEXTUALIZATION_CORPUS / 'smglom'/'statements'/'auto-reachable.en.html'


    augment_lexicon(
        (TEST_FILE_DIR / 'smglom' / 'automata.lexicon').read_text(),
        Lexicon('Automata', 'ftml'),
    ).write()

    grammar = MagmaGrammar('AutomataGrammar', 'Eng')
    doc = ftml_to_doc(stmt_path, grammar)


if __name__ == '__main__':
    main()
