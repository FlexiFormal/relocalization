import json
from pathlib import Path

from flexi.parsing.gf_shell import GFShellRaw

# only the first N paragraphs from each file are considered
NUMBER_OF_PARAGRAPHS = 5

BASE_PATH = Path(__file__).parent
REPO_PATH = BASE_PATH.parent.parent.parent

COVERAGE_FILES = [
    BASE_PATH / p for p in [
        'definitions_train.json',
        'theorems_train.json',
        'definitions_test.json',
        'theorems_test.json',
    ]
]

def get_shell():
    grammar_path =  REPO_PATH / 'magma' / 'combinations' / 'CoverageTestGrammarEng.gf'
    shell = GFShellRaw()
    print('importing grammar...')
    response = shell.handle_command(f'import {grammar_path}')
    print('Result:', repr(response))
    return shell

def process_sentence(shell, sentence):
    sentence = sentence.replace('@', ' $ ')
    if sentence[0].isalpha() and sentence[0].isupper():
        sentence = sentence[0].lower() + sentence[1:]
    if sentence[-1] == '.':
        sentence = sentence[:-1] + ' .'
    cmd = f'p -cat=Sentence "{sentence}"'
    response = shell.handle_command(cmd)
    print(response)
    return response


def main():
    shell = get_shell()
    for file in COVERAGE_FILES:
        print(f'Processing {file}...')
        with file.open() as f:
            paragraphs = json.load(f)
        for para in paragraphs[:NUMBER_OF_PARAGRAPHS]:
            print(f'Processing {para["paper"]}')
            for sentence in para['sentences']:
                print(f'Sentence: {sentence}')
                process_sentence(shell, sentence)
            print('---')


if __name__ == "__main__":
    main()
