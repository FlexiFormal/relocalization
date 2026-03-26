from flexi.config import TEST_FILE_DIR
from flexi.lexicon_gen import augment_lexicon, Lexicon
from flexi.parsing.document import forthel_to_doc
from flexi.parsing.magma import MagmaGrammar


def main():
    augment_lexicon(
        (TEST_FILE_DIR / 'naproche' / 'cantor.lexicon').read_text(),
        Lexicon('cantor', 'forthel'),
    ).write()

    path = TEST_FILE_DIR / 'naproche' / 'cantor.ftl'
    doc = forthel_to_doc(path.read_text(), MagmaGrammar('cantorGrammar', 'Eng'))


if __name__ == '__main__':
    main()
