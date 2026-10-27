from flexi.config import TEST_FILE_DIR
from flexi.old_lexicon_gen import augment_lexicon, Lexicon
from flexi.parsing.document import forthel_to_doc, DocText
from flexi.parsing.magma import MagmaGrammar
from flexi.parsing.mast import MAst, mast_to_gfxml
from flexi.transform.filtering import filter_readings, FilteringCtx
from flexi.transform.rewrite_guidance import greedy_rewriting, GREEDY_REWRITING_DEFAULT_RULES
from flexi.transform.rewrite_rules import RewritingContext
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--print-all-asts", action="store_true", help="print all ASTs instead of only the first one")
parser.add_argument("-i", "--input", help="input file")

def main():
    do_print_all_asts = False
    input_file = TEST_FILE_DIR / 'naproche' / 'cantor.ftl'

    args = parser.parse_args()

    if args.print_all_asts:
        do_print_all_asts = True
    if args.input is not None:
        input_file = Path(args.input).resolve()

    augment_lexicon(
        (TEST_FILE_DIR / 'naproche' / 'cantor.lexicon').read_text(),
        Lexicon('cantor', 'forthel'),
    ).write()

    grammar = MagmaGrammar('cantorGrammar', 'Eng')
    doc = forthel_to_doc(input_file.read_text(), grammar)

    for text in doc.find_children(lambda node: isinstance(node, DocText)):
        for sentence in text.sentences:
            filtered = list(filter_readings(sentence, FilteringCtx()))
            print('\n', len(sentence), 'filtered:', len(filtered))

            s = sentence[0]
            assert isinstance(s, MAst)
            # print(grammar.linearize_mast(s))
            # if grammar.linearize_mast(s) != 'For all v0 , ( if v0 is a class then for all v1 , ( ( v1 is a subclass of v0 ) iff ( v1 is a class and for all v2 , ( if v2 is an element of v1 then v2 is an element of v0 ) ) ) ).':
            #     continue

            if len(filtered) >= 1:
                for ast in filtered:
                    print('\n', mast_to_gfxml(ast).to_gf()[1])
                    print('LINEARIZATION:', grammar.linearize_mast(ast))

                    try:
                        # m = next(iter(RewritePullKindIntoUnivQuant().apply_somewhere(filtered[0], RewritingContext())))
                        m = mast if (mast := greedy_rewriting(ast, GREEDY_REWRITING_DEFAULT_RULES, RewritingContext())) is not None else ast
                        # print('SIMPLIFIED:', mast_to_gfxml(m).to_gf()[1])
                        print('SIMPLIFIED:   ', grammar.linearize_mast(m))
                    except StopIteration:
                        print('Not applicable')
                    if not do_print_all_asts:
                        break


            # import sys
            # sys.exit(0)


if __name__ == '__main__':
    main()
