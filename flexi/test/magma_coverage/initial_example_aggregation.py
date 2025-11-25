# quick-and-dirty script to aggregate data

from pathlib import Path
import re
import json
import random
from nltk.tokenize import sent_tokenize
from nltk.classify.textcat import TextCat
import stanza

# stanza gives significantly better sentence segmentation than nltk
# (possibly because formulae mess up nltk's punkt model)
nlp = stanza.Pipeline(lang='en', processors='tokenize')


def sentence_tokenize(text):
    doc = nlp(text)
    return [
        text[sent.tokens[0].start_char:sent.tokens[-1].end_char]
        for sent in doc.sentences
            ]
    # return sent_tokenize(text)


tc = TextCat()


paper_prefix = 'Paper: https://ar5iv.org/abs/'


for type_, dir_ in [
        ('definition', '~/5kdefs'),
        ('theorem', '~/5kthms'),
]:
    print('type_:', type_)
    result = []
    for path in Path(dir_).expanduser().glob('*.txt'):
        for line in path.open():
            if line.startswith(paper_prefix):
                result.append(
                        {
                            'paper': line[len('Paper: '):].strip(),
                            'identifier': None,
                            'sentences': [],
                        }
                )
            elif re.match(r'^(Definition|Theorem) [0-9]', line) and not result[-1]['sentences']:
                if not result[-1]['identifier']:
                    result[-1]['identifier'] = line.strip()
                # if result[-1]['sentences']:
                #     print('OOPS', result[-1]['id'])
                #     result[-1]['sentences'].append('NEW_PARAGRAPH')
                continue
            elif not line.strip():
                if result and result[-1]['sentences']:
                    # new paragraph
                    result.append({
                        'paper': result[-1]['paper'],
                        'identifier': None,
                        'sentences': [],
                    })
                continue
            else:
                result[-1]['sentences'].extend(
                        sentence_tokenize(line.strip())
                )

    # for r in result:
        # if r['sentences'] and tc.guess_language(' '.join(r['sentences'])) != 'eng':
        #     print('Non-English:', r['sentences'])
        #     print('is ' + tc.guess_language(' '.join(r['sentences'])))

    result = [r for r in result if r['sentences']] # and tc.guess_language(' '.join(r['sentences'])) == 'eng']


    random.seed(42)
    random.shuffle(result)
    print(len(result))

    with open('/tmp/' + type_ + 's_train.json', 'w') as f:
        json.dump(result[:1100], f, indent=2)
    with open('/tmp/' + type_ + 's_test.json', 'w') as f:
        json.dump(result[1100:2200], f, indent=2)


