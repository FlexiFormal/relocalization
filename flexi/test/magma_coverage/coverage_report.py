import re
from pathlib import Path
from typing import Literal, Iterable

# only the first N paragraphs from each file are considered
NUMBER_OF_PARAGRAPHS = 1000

BASE_PATH = Path(__file__).parent
REPO_PATH = BASE_PATH.parent.parent.parent

import sys
sys.path.append(str(REPO_PATH))


import functools
import json

import pgf

from flexi.parsing.gf_shell import GFShellRaw
from flexi.parsing.magma import get_pgf


COVERAGE_FILES = [
    BASE_PATH / p for p in [
        'definitions_train.json',
        'theorems_train.json',
        'definitions_test.json',
        'theorems_test.json',
    ]
]

@functools.cache
def get_shell():
    grammar_path =  REPO_PATH / 'magma' / 'combinations' / 'CoverageTestGrammarEng.gf'
    shell = GFShellRaw()
    print('importing grammar...')
    response = shell.handle_command(f'import {grammar_path}')
    print('Result:', repr(response))
    return shell

def sentence_preprocess(sentence):
    sentence = sentence.replace('@', ' $ ')
    if sentence[0].isalpha() and sentence[0].isupper():
        sentence = sentence[0].lower() + sentence[1:]
    if sentence[-1] == '.':
        sentence = sentence[:-1] + ' .'
    if sentence.endswith('STATEMENT_ENUM_PLACEHOLDER'):
        sentence += ' .'
    sentence = sentence.replace('-', ' - ')
    sentence = sentence.replace(':', ' : ')
    sentence = sentence.replace(', ', ' , ')
    if sentence.endswith('MathGroup $ ') or sentence.endswith('MathEquation $ '):
        sentence += '.'
    return sentence

def process_sentence_shell(sentence):
    shell = get_shell()
    cmd = f'p -cat=Sentence "{sentence_preprocess(sentence)}"'
    print(cmd)
    response = shell.handle_command(cmd)
    # print(response)
    return response

def process_sentence_pgf(sentence):
    pgf = get_pgf('CoverageTestGrammar')
    cmd = f'p -cat=Sentence "{sentence_preprocess(sentence)}"'
    print(cmd)
    concrete = pgf.languages['CoverageTestGrammarEng']
    results = concrete.parse(sentence_preprocess(sentence), n=100)
    return list(results)


OUTCOME = Literal['NONE', 'TOO MANY'] | int


def process_sentence(sentence: str | list, is_train, separator, in_enum: bool = False) -> Iterable[OUTCOME]:
    if isinstance(sentence, list):
        is_plain_enum = all(isinstance(s, list) for s in sentence)
        for s in sentence:
            if isinstance(s, list):
                for ss in s:
                    yield from process_sentence(ss, is_train, separator + f'\033[48;2;255;0;255m+\033[0m', in_enum=True)
        if is_plain_enum:
            return
        else:  # enum is embedded in sentence
            sentence_actual = ' '.join(
                item if isinstance(item, str) else 'STATEMENT_ENUM_PLACEHOLDER'
                for item in sentence
            )
    else:
        sentence_actual = sentence

    if in_enum:  # potentially remove enumeration marker
        parts = [
            r'•',
            r'(\(?[0-9][0-9.]*\)?)',
            r'\(?[a-z]\)',
            r'((i|ii|iii|iv|v|vi|vii|viii|ix|x|xi|xii)\.)',
            r'(\(?(i|ii|iii|iv|v|vi|vii|viii|ix|x|xi|xii)\))',
            ]
        for part in parts:  # iirc, '|' is not commutative in re, and I don't want to deal with that :D
            if m := re.match('^(' + part + ') ', sentence_actual):
                sentence_actual = sentence_actual[len(m.group(0)):].lstrip()
                break

    print(separator)

    print(f'Sentence: \033[48;2;255;255;0m{sentence_actual}\033[0m')
    try:
        number = len(process_sentence_pgf(sentence_actual))
        if number < 100:
            if is_train:
                print('\033[30;42m' + f'OK: {number} readings' + '\033[0m')
            yield number
        else:
            if is_train:
                print('\033[30;41m' + f'ERROR: more than 100 readings' + '\033[0m')
            yield 'TOO MANY'
    except pgf.ParseError as e:
        if is_train or 'Unexpected token' in str(e):
            print('\033[30;41m' + f'ERROR: {e}' + '\033[0m')
        yield 'NONE'


def main():
    results: dict[Path, list[OUTCOME]] = {}
    for file in COVERAGE_FILES:
        is_train = 'train' in file.name
        results[file] = []
        print(f'Processing {file}...')

        with file.open() as f:
            paragraphs = json.load(f)

        for paranum, para in enumerate(paragraphs[:NUMBER_OF_PARAGRAPHS]):
            print(f'Processing {para["paper"]}')
            for sentence in para['sentences']:
                results[file].extend(process_sentence(
                    sentence,
                    is_train,
                    separator = '---' + ('' if is_train else '\033[48;2;255;0;255m') + ' ' + file.name + ' ' + f'({paranum}) \033[0m'
                ))

    print('Coverage results:')
    for file in COVERAGE_FILES:
        ok = sum(1 for r in results[file] if isinstance(r, int))
        total = len(results[file])
        print(f'{file.name}: {ok} / {total} = {ok / total * 100:.2f} %')


if __name__ == "__main__":
    main()
