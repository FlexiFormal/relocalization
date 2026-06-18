import flexi.workbench as wb
from flexi.config import TEST_FILE_DIR
from flexi.old_lexicon_gen import augment_lexicon, Lexicon
from flexi.parsing.document import ftml_to_doc, DocText
from flexi.parsing.magma import MagmaGrammar
from flexi.transform.filtering import FilteringCtx, filter_readings


def main():
    # stmt_path = TEST_FILE_DIR / 'smglom' / 'quiver-path.en.html'
    stmt_path = TEST_FILE_DIR / 'smglom' / 'nts.en.html'


    augment_lexicon(
        (TEST_FILE_DIR / 'smglom' / 'automata.lexicon').read_text(),
        Lexicon('Automata', 'ftml'),
    ).write()

    grammar = MagmaGrammar('AutomataGrammar', 'Eng')
    doc = ftml_to_doc(stmt_path, grammar)
    print(doc)

    with wb.new_workbench('/tmp/tmp_bw.html', 'Pushout Test'):
        wb.set_default_grammar(grammar)
        readings = []
        for i, textnode in enumerate(doc.find_children(lambda d: isinstance(d, DocText))):
            assert isinstance(textnode, DocText)
            for sentence in textnode.sentences:
                filtered_readings = list(filter_readings(sentence, FilteringCtx()))
                readings.append(filtered_readings)

        for i, reading in enumerate(readings[0]):
            wb.push_sentence_mast(reading)


if __name__ == '__main__':
    main()
