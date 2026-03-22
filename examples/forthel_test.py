from flexi.config import TEST_FILE_DIR
from flexi.parsing.document import forthel_to_doc
from flexi.parsing.magma import MagmaGrammar


def main():
    path = TEST_FILE_DIR / 'naproche' / 'cantor.ftl'
    doc = forthel_to_doc(path.read_text(), MagmaGrammar('ForthelTestGrammar', 'Eng'))


if __name__ == '__main__':
    main()
