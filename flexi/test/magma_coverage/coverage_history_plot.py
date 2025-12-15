import json
from matplotlib import pyplot as plt


with open('/tmp/coverage_history.json', 'r') as f:
    results = json.load(f)

def get_percentage(d):
    ok = sum(1 for r in d if isinstance(r[0], int))
    total = len(d)
    return ok / total * 100

def get_percentage_expl(d):
    ok = sum(1 for r in d if isinstance(r[0], int))
    total = len(d)
    return f'{ok}/{total} = {ok / total}'

def get_file_percentages(filename):
    print(filename)
    print('\n'.join([r['hash'] + ' ' + str(get_percentage_expl(r['results'][filename])) for r in results]))
    return [get_percentage(r['results'][filename]) for r in results]

plt.rcParams.update({'font.size': 14})

for filename in ['theorems_train.json', 'theorems_test.json', 'definitions_train.json', 'definitions_test.json']:
    percentages = get_file_percentages(filename)
    label = filename.split('_')[0].capitalize() + ' (' + filename.split('_')[1].split('.')[0] + ')'
    plt.plot(percentages, label=label, marker={'D': 's', 'T': '^'}[filename[0].upper()],
             **({} if 'test' in filename else dict(mfc='white')),
             linestyle='dotted'
             )

             # linestyle='dotted' if 'train' in filename else 'dashed')

plt.title('Coverage Growth as Grammar is Extended')
plt.ylim(bottom=0)

plt.xlabel('Number of grammar modifications')
plt.ylabel('Sentences parsed (%)')
plt.legend()
plt.savefig('/tmp/coverage_history.pdf', bbox_inches='tight')
plt.show()



