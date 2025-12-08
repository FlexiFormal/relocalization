from subprocess import run
from pathlib import Path
import coverage_report
import json


run(['rm', '-rf', '/tmp/relocalization'])
run(['git', '-C', '/tmp', 'clone', 'https://github.com/FlexiFormal/relocalization.git'])
logs = run(['git', '-C', '/tmp/relocalization', 'log', '--one-line'], capture_output=True, text=True).stdout.splitlines()


hashes = []
for log in logs:
    if 'grammar extension' in log:
        hashes.append(log.split()[0])

hashes.reverse()

results = []

for h in hashes:
    run(['git', '-C', '/tmp/relocalization', 'checkout', h])
    magma_tmp = Path('/tmp/relocalization/magma')
    magma_me = coverage_report.REPO_PATH / 'magma'
    assert magma_tmp.exists()
    # reset (just in case)
    run(['git', '-C', str(coverage_report.REPO_PATH), 'checkout', str(magma_me)])

    for d in ['combinations', 'magma', 'formulae', 'other']:
        run(['cp', '-r', str(magma_tmp / d), str(magma_me / d)])


    sub_results: dict[Path, list[coverage_report.OUTCOME]] = {}
    for file in coverage_report.COVERAGE_FILES:
        is_train = 'train' in file.name
        sub_results[file] = []
        print(f'Processing {file}...')

        with file.open() as f:
            paragraphs = json.load(f)

        for paranum, para in enumerate(paragraphs[:coverage_report.NUMBER_OF_PARAGRAPHS]):
            print(f'Processing {para["paper"]}')
            for sentence in para['sentences']:
                sub_results[file].extend(coverage_report.process_sentence(
                    sentence,
                    is_train,
                    separator = '---' + ('' if is_train else '\033[48;2;255;0;255m') + ' ' + file.name + ' ' + f'({paranum}) \033[0m'
                ))
    results.append({
        'hash': h,
        'results': sub_results
    })

with open(coverage_report.REPO_PATH / 'test' / 'magma_coverage' / 'coverage_history.json', 'w') as f:


