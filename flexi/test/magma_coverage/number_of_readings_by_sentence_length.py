import json
from matplotlib import pyplot as plt
from collections import defaultdict

plt.rcParams.update({'font.size': 14})


with open('/tmp/coverage_results.json', 'r') as f:
    results = json.load(f)

readings_by_sentence_length = defaultdict(list)

for filename, data in results.items():
    if 'train' in filename:
        continue
    for v in data:
        if isinstance(v[0], int):
            readings_by_sentence_length[v[1]].append(v[0])

keys = list(range(1, 19))

plt.plot(
    keys,
    [
        sum(readings_by_sentence_length[k]) / len(readings_by_sentence_length[k])
        for k in keys
    ],
    label='Average'
)

plt.plot(
    keys,
    [
        max(readings_by_sentence_length[k])
        for k in keys
    ],
    label='Maximum'
)

plt.plot(
    keys,
    [
        sorted(readings_by_sentence_length[k])[int(0.95 * len(readings_by_sentence_length[k]))]
        for k in keys
    ],
    label='95th Percentile'
    )

plt.plot(
    keys,
    [
        sorted(readings_by_sentence_length[k])[int(0.5 * len(readings_by_sentence_length[k]))]
        for k in keys
    ],
    label='Median'
    )

plt.xticks(keys[::2])
plt.ylim(bottom=0)
plt.title('Syntactic Ambiguity')
plt.legend(prop={'size': 12})
plt.xlabel('Number of grammar modifications')
plt.ylabel('Average number of readings per sentence')

plt.savefig('/tmp/coverage_by_sentence_length.pdf', bbox_inches='tight')

plt.show()
