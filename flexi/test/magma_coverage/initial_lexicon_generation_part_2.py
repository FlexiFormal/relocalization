import stanza
import json
import re
import os
import gzip


CACHE_PATH = 'cache2.json.gz'

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


def keyify(s):
    return s.replace(' ', '_').replace('-', '_')


with open('pre-lexicon.json', 'r') as fp:
    prelexicon = json.load(fp)

result = {}

for verb in prelexicon['V']:
    message = '''
Given a verb, tell me its past form.

Only respond in JSON, nothing else.
Do not include any explanations.

Example 1:
    {"verb": "run"}
Output:
    {"past_form": "ran"}

Example 2:
    {"verb": "divide"}
Output:
    {"past_form": "divided"}

Your input:
    {"verb": "%s"}
    ''' % verb
    response = query_llama32(message).strip()

    j = re.search(r'\{.*\}', response, re.DOTALL)
    if not j:
        continue
    try:
        jp = json.loads(j.group(0))
    except json.JSONDecodeError:
        continue
    if 'past_form' not in jp or not isinstance(jp['past_form'], str):
        continue

    result.setdefault('V', {})[keyify(verb)] = [verb, jp['past_form']]


for noun in prelexicon['N']:
    message = '''
Given a noun, tell me its plural form

Only respond in JSON, nothing else.
Do not include any explanations.

Example 1:
    {"noun": "matrix"}
Output:
    {"plural_form": "matrices"}

Example 2:
    {"noun": "set"}
Output:
    {"plural_form": "sets"}

Your input:
    {"noun": "%s"}
    ''' % noun
    response = query_llama32(message).strip()

    j = re.search(r'\{.*\}', response, re.DOTALL)
    if not j:
        continue
    try:
        jp = json.loads(j.group(0))
    except json.JSONDecodeError:
        continue
    if 'plural_form' not in jp:
        continue

    result.setdefault('N', {})[keyify(noun)] = [noun, jp['plural_form']]

for pn in prelexicon['PN']:
    result.setdefault('PN', {})[keyify(pn)] = [pn]

for adj in prelexicon['A']:
    result.setdefault('A', {})[keyify(adj)] = [adj]

save_cache()

with open('lexicon.json', 'w') as fp:
    json.dump(result, fp, indent=4)
