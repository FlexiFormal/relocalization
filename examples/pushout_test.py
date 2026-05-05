from lxml import etree

from flexi.config import RECONTEXTUALIZATION_CORPUS, TEST_FILE_DIR
from flexi.lexicon_gen import augment_lexicon, Lexicon
from flexi.parsing.document import ftml_to_doc, DocText
from flexi.parsing.magma import MagmaGrammar
from flexi.transform.filtering import FilteringCtx, filter_readings
from flexi.transform.morphism import extract_from_extstructure_interpretmodule, MorphismExtractionContext

import flexi.workbench as wb
from flexi.transform.rewrite_guidance import greedy_rewriting, GREEDY_REWRITING_DEFAULT_RULES
from flexi.transform.rewrite_rules import RewritingContext
from flexi.transform.substitution import substitute
from flexi.treevis import mast_color_diff


def main():
    # stmt_path = TEST_FILE_DIR / 'smglom' / 'auto-reachable.en.html'
    # view_path = RECONTEXTUALIZATION_CORPUS / 'smglom' / 'views' / 'auto-to-tm_1.en.html'

    stmt_path = TEST_FILE_DIR / 'smglom' / 'quiver-path.en.html'
    view_path = RECONTEXTUALIZATION_CORPUS / 'smglom' / 'views' / 'elquiver-to-nts.en.html'


    augment_lexicon(
        (TEST_FILE_DIR / 'smglom' / 'automata.lexicon').read_text(),
        Lexicon('Automata', 'ftml'),
    ).write()

    grammar = MagmaGrammar('AutomataGrammar', 'Eng')
    doc = ftml_to_doc(stmt_path, grammar)

    view_html = etree.parse(str(view_path), parser=etree.HTMLParser()).getroot()
    extstruct = view_html.xpath('//div[@data-ftml-feature-structure]')[0]
    morphism = extract_from_extstructure_interpretmodule(extstruct, MorphismExtractionContext(grammar=grammar))

    with wb.new_workbench('/tmp/pushout_test.html', 'Pushout Test'):
        wb.set_default_grammar(grammar)
        wb.push_html('<h1>View</h1>')
        for concept, substitution in morphism.assignments.items():
            wb.push_html(f'<h2>{concept}</h2>')
            wb.push_mast(substitution[0])

        wb.push_html('<h1>Original Utterance</h1>')
        for i, textnode in enumerate(doc.find_children(lambda d: isinstance(d, DocText))):
            assert isinstance(textnode, DocText)
            for j, sentence in enumerate(textnode.sentences):
                wb.push_html(f'<h2>Sentence {i+1}.{j+1}</h2>')
                filtered_readings = list(filter_readings(sentence, FilteringCtx()))
                for k, mast in enumerate(filtered_readings):
                    wb.push_sentence_mast(mast)
                    new = substitute(mast, morphism.assignments)
                    wb.push_sentence_mast(new)
                    wb.push_html('<b>simplified</b>')
                    wb.push_sentence_mast(
                        greedy_rewriting(new, GREEDY_REWRITING_DEFAULT_RULES, RewritingContext()) or new
                    )
                    if k + 1 < len(filtered_readings):
                        # color diff so that we can improve filtering
                        mast_clone = mast.clone()
                        mast_color_diff(mast_clone, filtered_readings[k+1])
                        wb.push_mast(mast_clone)

                    wb.push_html('<hr/>')



if __name__ == '__main__':
    main()
