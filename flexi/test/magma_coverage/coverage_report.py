from pathlib import Path

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
        'theorems_train.json',
        'definitions_train.json',
        'theorems_test.json',
        'definitions_test.json',
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

def main():
    ok = {}
    total = {}
    for file in COVERAGE_FILES:
        is_train = 'train' in file.name
        total[file] = 0
        ok[file] = 0
        print(f'Processing {file}...')
        with file.open() as f:
            paragraphs = json.load(f)
        for paranum, para in enumerate(paragraphs[:NUMBER_OF_PARAGRAPHS]):
            print(f'Processing {para["paper"]}')
            for sentence in para['sentences']:
                total[file] += 1
                print('---', '' if is_train else '\033[48;2;255;0;255m', file.name, f'({paranum}) \033[0m')
                print(f'Sentence: \033[48;2;255;255;0m{sentence}\033[0m')
                try:
                    number = len(process_sentence_pgf(sentence))
                    if number < 100:
                        if is_train:
                            print('\033[30;42m' + f'OK: {number} readings' + '\033[0m')
                        ok[file] += 1
                    else:
                        if is_train:
                            print('\033[30;41m' + f'ERROR: more than 100 readings' + '\033[0m')
                except pgf.ParseError as e:
                    if is_train or 'Unexpected token' in str(e):
                        print('\033[30;41m' + f'ERROR: {e}' + '\033[0m')

                # shell_output = process_sentence_shell(sentence)
                # if shell_output.startswith('The parser failed at token') or \
                #         shell_output.startswith('The sentence is not complete'):
                #     print('ERROR:', shell_output)
                # else:
                #     ok[file] += 1
                #     print('OK:', len(shell_output.splitlines()), 'readings')

    print('Coverage results:')
    for file in COVERAGE_FILES:
        print(f'{file.name}: {ok[file]} / {total[file]} = {ok[file] / total[file] * 100:.2f} %')


if __name__ == "__main__":
    main()
