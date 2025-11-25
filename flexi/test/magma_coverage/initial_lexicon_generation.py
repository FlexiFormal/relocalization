import stanza
import json
import re
import os
import gzip


CACHE_PATH = 'cache.json.gz'

# if the cache exists, load from it
if os.path.exists(CACHE_PATH):
    CACHE = json.load(gzip.open(CACHE_PATH, 'rt'))
else:
    CACHE = {}

time_since_last_save = 0

def save_cache():
    with gzip.open(CACHE_PATH, 'wt') as f:
        json.dump(CACHE, f, indent=4)

def query_llama32(message):
    global time_since_last_save
    if message in CACHE:
        return CACHE[message]
    from ollama import chat
    from ollama import ChatResponse
    response: ChatResponse = chat(model='llama3.2', messages=[
        {
            'role': 'user',
            'content': message,
        },
        ])
    CACHE[message] = response.message.content
    time_since_last_save += 1
    if time_since_last_save >= 50:
        save_cache()
        time_since_last_save = 0
    return response.message.content

def get_grammar_info(sentence, word):
    message = '''
Given a sentence and a word, tell me
* if the word is used as a technical term (and not a structural word) in the sentence
* the word type (noun, verb, adjective, name)
* the base form of the word

Only respond in JSON, nothing else.
Do not include any explanations.

Example 1:
    {"sentence": "Let X be the resulting Cartesian square.", "word": "Cartesian"}
Output:
    {"technical_term": true, "type": "adjective", "base_form": "Cartesian"}

Example 2:
    {"sentence": "X is said to be a circular code if for any X, we have X.", "word": "said"}
Output:
    {"technical_term": false, "type": "verb", "base_form": "say"}

Example 3:
    {"sentence": "Let X be the universal ring over X parametrising deformations of X as a X-representation.", "word": "deformations"}
Output:
    {"technical_term": true, "type": "noun", "base_form": "deformation"}

Here is your input:
    '''
    message += json.dumps({"sentence": sentence, "word": word})
    message = message.strip()
    response = query_llama32(message)
    print("LLama 3.2 response:", response)
    j = re.search(r'\{.*\}', response, re.DOTALL)
    if not j:
        return None
    try:
        return json.loads(j.group(0))
    except json.JSONDecodeError:
        return None


nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos')

non_technical_terms = set()

def get_sentences():
    for file in [
        'definitions_train.json',
        'definitions_test.json',
        'theorems_train.json',
        'theorems_test.json',
    ]:
        with open(file, 'r') as f:
            data = json.load(f)
            for i, entry in enumerate(data):
                print('-----------', i, '-----------')
                if not i % 100:
                    print(f'Processing {file}, entry {i}')
                # if i > 50:
                #     break
                yield from entry['sentences']

def prep_sentence(sentence):
    return re.sub(r'@(MathNode|MathGroup|MathEquation|LtxRef)@', 'X', sentence)


result = {
    'V': [],
    'N': [],
    'A': [],
    'PN': [],
}

processed = set()

for sentence in get_sentences():
    sentence = prep_sentence(sentence)
    doc = nlp(sentence)
    for sent in doc.sentences:
        for word in sent.words:
            if (word.text, word.upos) in processed:
                continue
            processed.add((word.text, word.upos))

            if word.upos in {'NOUN', 'VERB', 'ADJ', 'PROPN'}:
                grammar_info = get_grammar_info(sentence, word.text)
                if grammar_info is None:
                    print('OOPS')
                    print(sentence)
                    print(word.text)
                    print('---')
                    continue
                if not grammar_info.get('technical_term'):
                    print('Not a technical term:')
                    print(sentence)
                    print(word.text)
                    print('---')
                    continue

                k = {'verb': 'V', 'noun': 'N', 'adjective': 'A', 'name': 'PN'}.get(grammar_info['type'].lower())
                if k is not None and 'base_form' in grammar_info:
                    result[k].append(grammar_info['base_form']) # f'mk{k} "{grammar_info["base_form"]}"'
                    continue

                print('Unknown type:')
                print(sentence)
                print(word.text)
                print(grammar_info)
                print('---')

            # print(f"{word.text}\t{word.upos}\t{word.xpos}\t{word.lemma}")
            # if word.upos == 'NOUN':
            #     result['N'][word.lemma] = f'mkN "{word.lemma}"'
            # elif word.upos == 'VERB':
            #     result['V'][word.lemma] = f'mkV "{word.lemma}"'
            # elif word.upos == 'ADJ':
            #     result['A'][word.lemma] = f'mkA "{word.lemma}"'
            # elif word.upos == 'PROPN':
            #     result['PN'][word.lemma] = f'mkPN "{word.lemma}"'

with open('pre-lexicon.json', 'w') as f:
    json.dump(result, f, indent=4)



