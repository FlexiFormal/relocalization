from flexi.config import TEST_FILE_DIR
from flexi.lexicon_gen import augment_lexicon, Lexicon
from flexi.parsing.document import forthel_to_doc, DocText
from flexi.parsing.magma import MagmaGrammar
from flexi.parsing.mast import MAst, mast_to_gfxml
from flexi.transform.filtering import filter_readings, FilteringCtx
from flexi.transform.rewriting import RewritePullKindIntoUnivQuant, RewritingContext


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
            if grammar.linearize_mast(s) != 'For all v0 , ( if v0 is a class then for all v1 , ( ( v1 is a subclass of v0 ) iff ( v1 is a class and for all v2 , ( if v2 is an element of v1 then v2 is an element of v0 ) ) ) ).':
                continue

            if len(filtered) >= 1:
                print(mast_to_gfxml(filtered[0]).to_gf()[1])
                print(grammar.linearize_mast(filtered[0]))

                try:
                    m = next(iter(RewritePullKindIntoUnivQuant().apply_somewhere(filtered[0], RewritingContext())))
                    print(mast_to_gfxml(m).to_gf()[1])
                    print(grammar.linearize_mast(m))
                except StopIteration:
                    print('Not applicable')

            import sys
            sys.exit(0)


if __name__ == '__main__':
    main()
