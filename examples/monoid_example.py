import itertools
import os
from pathlib import Path

from lxml import etree

from flexi.config import TEST_FILE_DIR
from flexi.lexicon import Lexicon
from flexi.parsing.magma import MagmaGrammar, Sentence

import flexi.workbench as wb
from flexi.parsing.mast import MAst
from flexi.semconstr.conversion import convert, ConversionContext, finalized_convert
from flexi.semconstr.logic import expr_to_tptp, TptpConvCtx, Expr, Const, Apply, tptp_verify
from flexi.transform.filtering import FilteringCtx, filter_readings
from flexi.transform.rewrite_rules import RewriteEliminateRedundantInfo, RewritingContext
from flexi.treevis import mast_color_diff


def main():
    path = TEST_FILE_DIR / 'testmathhub' / 'monoid' / 'source'
    l = Lexicon('MonoidLexicon', 'Eng')
    l.extend_from_ftml(path / 'commutative-monoid.en.html')
    l.extend_from_ftml(path / 'invertible-in-monoid.en.html')
    l.add_word_list(Path(os.environ['MATHHUB']) / 'smglom' / 'meta-inf' / 'source' / 'verbalization-words.en.txt')
    l.write_gf()
    grammar = MagmaGrammar('MonoidLexicon', 'Eng')

    with wb.new_workbench(Path('/tmp/monoid.html'), 'Monoid'):
        wb.set_default_grammar(grammar)

        com_mon_def = etree.parse(path / 'commutative-monoid.en.html', parser=etree.HTMLParser())
        context_sentences: list[list[MAst]] = []
        for node in com_mon_def.xpath('//div[@data-ftml-assertion]'):
            context_sentences.extend(
                [
                    list(filter_readings(sentence, FilteringCtx()))
                    for sentence in grammar.parse_ftml_to_sentences(node)
                ]
            )
        axioms: list[Expr] = []

        for i, sentence in enumerate(context_sentences):
            wb.push_html(f'<h1>Context [{i}]</h1>')
            axiom = Const.Falsehood
            for mast in sentence:
                wb.push_sentence_mast(mast)
                r = finalized_convert(mast, ConversionContext())
                axiom = Apply.multi(Const.Disjunction, axiom, r.simplified())
                wb.push_html(f'''
<pre>
Result: {str(r)}
Reduced: {str(r.beta_reduced())}
Simplified: {str(r.simplified())}
TPTP FOF: {expr_to_tptp(r.simplified(), TptpConvCtx())}
</pre>
''')
            axioms.append(axiom)
        # tptp_verify(
        #     axiom, [], TptpConvCtx()
        # )

        for i, sentence in enumerate(grammar.parse_ftml_to_sentences(path / 'invertible-in-monoid.en.html'), start=1):
            wb.push_html(f'<h1>Sentence {i}</h1>')
            for k, reading in enumerate(sentence):
                wb.push_html(f'<h2>Reading [{k}]</h2>')
                wb.push_sentence_mast(reading)
                r = finalized_convert(reading, ConversionContext())
                wb.push_html(f'''
                <pre>
Result: {str(r)}
Reduced: {str(r.beta_reduced())}
Simplified: {str(r.simplified())}
TPTP FOF: {expr_to_tptp(r.simplified(), TptpConvCtx())}
                </pre>
                ''')
                if k + 1 < len(sentence):
                    # color diff so that we can improve filtering
                    mast_clone = reading.clone()
                    mast_color_diff(mast_clone, sentence[k + 1])
                    wb.push_mast(mast_clone)
                ctx = RewritingContext(axioms=axioms)
                for simplified in itertools.chain(
                        RewriteEliminateRedundantInfo(0).apply_somewhere(reading, ctx),
                        RewriteEliminateRedundantInfo(1).apply_somewhere(reading, ctx),
                ):
                    wb.push_html('<h3>Simplified</h3>')
                    wb.push_sentence_mast(simplified)

if __name__ == '__main__':
    main()
