from flexi.config import TEST_FILE_DIR
from flexi.lexicon_gen import augment_lexicon, Lexicon
from flexi.parsing.document import forthel_to_doc, DocText
from flexi.parsing.magma import MagmaGrammar
from flexi.parsing.mast import MAst, mast_to_gfxml
from flexi.transform.filtering import filter_readings, FilteringCtx


def main():
    augment_lexicon(
        (TEST_FILE_DIR / 'naproche' / 'cantor.lexicon').read_text(),
        Lexicon('cantor', 'forthel'),
    ).write()

    path = TEST_FILE_DIR / 'naproche' / 'cantor.ftl'
    grammar = MagmaGrammar('cantorGrammar', 'Eng')
    doc = forthel_to_doc(path.read_text(), grammar)

    for text in doc.find_children(lambda node: isinstance(node, DocText)):
        for sentence in text.sentences:
            filtered = list(filter_readings(sentence, FilteringCtx()))
            print(len(sentence), 'filtered:', len(filtered))

            s = sentence[0]
            assert isinstance(s, MAst)
            print(grammar.linearize_mast(s))

            if len(filtered) > 1:
                print(mast_to_gfxml(filtered[0]).to_gf()[1])
                print(mast_to_gfxml(filtered[1]).to_gf()[1])


if __name__ == '__main__':
    main()
