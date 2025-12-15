import json
from matplotlib import pyplot as plt
from collections import defaultdict

plt.rcParams.update({'font.size': 14})


with open('/tmp/coverage_results.json', 'r') as f:  # history has wrong sentence lengths
    cr = json.load(f)

with open('/tmp/coverage_history.json', 'r') as f:
    results = json.load(f)


totals = defaultdict(int)

for f, v in results[0]['results'].items():
    if 'train' in f:
        continue
    for i, e in enumerate(v):
        totals[cr[f][i][1]] += 1


keys = list(range(19))


plt.plot(keys, [totals[k] for k in keys], label='All sentences (test dataset)', marker='o', mfc='black', color='black')



for nn in [0, 12, 43]:
    totals = defaultdict(int)

    for f, v in results[nn]['results'].items():
        if 'train' in f:
            continue
        for i, e in enumerate(v):
            if isinstance(e[0], int):
                totals[e[1]] += 1


    plt.plot(keys, [totals[k] for k in keys], marker='o',
             mfc='white', linestyle='dashed', label=f'Parsed after {nn} modifications')

plt.ylim(bottom=0)
plt.title('Coverage by Sentence Length')
plt.legend(prop={'size': 12})
plt.xlabel('Sentence length (in words)')
plt.ylabel('Number of sentences')
plt.xticks(keys[::2])

plt.savefig('/tmp/coverage_by_sentence_length.pdf', bbox_inches='tight')

plt.show()
