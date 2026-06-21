from pathlib import Path

import flexi.workbench as wb
from flexi.config import TEST_FILE_DIR
from flexi.lexicon import Lexicon
from flexi.parsing.magma import MagmaGrammar
from flexi.parsing.mast import G, TermRef, Formula, MI, MT
from flexi.transform.substitution import substitute


def main():
    file = TEST_FILE_DIR / 'testmathhub' / 'goldbach' / 'source' / 'goldbach.en.html'
    l = Lexicon('GoldbachLexicon', 'Eng')
    l.extend_from_ftml(file)
    l.write_gf()
    grammar = MagmaGrammar('GoldbachLexicon', 'Eng')

    # divby2 = grammar.parse_ftml_to_sentences(
    #     etree.parse(StringIO(
    #         '<div data-ftml-head="http://mathhub.info?a=goldbach&m=goldbach&s=div">divisible</div> by <math><mn>2</mn></math>'
    #         ), parser=etree.HTMLParser()
    #     ).getroot()
    # )

    divby2 = G(
        'property2_to_property',
        [
            TermRef(
                'http://mathhub.info?a=goldbach&m=goldbach&s=div',
                [
                    G('verb_#1-divisible:A-by-#2_Property2')
                ],
                wrapfun='wrapped_property2'
            ),
            G('formula_term', [Formula([MI('mn', [MT('2')])], 'dollarmath')]),
        ]
    )

    with wb.new_workbench(Path('/tmp/goldbach.html'), 'Goldbach'):
        wb.set_default_grammar(grammar)
        # assert len(divby2) == 1
        # assert len(divby2[0]) == 1
        wb.push_html(f'<h1>Substituent</h1>')
        wb.push_sentence_mast(divby2)
        for i, sentence in enumerate(grammar.parse_ftml_to_sentences(file), start=1):
            wb.push_html(f'<h2>Sentence {i}</h2>')
            for mast in sentence:
                mast_new = substitute(
                    mast,
                    {
                        'http://mathhub.info?a=goldbach&m=goldbach&s=even' : [divby2]
                    },
                )
                wb.push_mast(mast_new)
                wb.push_sentence_mast(mast_new)



if __name__ == '__main__':
    main()
