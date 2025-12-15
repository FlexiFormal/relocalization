import json
from matplotlib import pyplot as plt
from collections import defaultdict

plt.rcParams.update({'font.size': 14})


with open('/tmp/coverage_history.json', 'r') as f:
    results = json.load(f)[10:]


readings_history = {}  # file -> list of list of readings

for filename in results[0]['results'].keys():
    if 'train' in filename:
        continue

    # step 1: find sentences that can be parsed at every modification
    okay = [True] * len(results[0]['results'][filename])

    # for i, r in enumerate(results):
    #     if any(x[0] == 'TOO MANY' for x in r['results'][filename]):
    #         print('OOPs', i, filename)

    for r in results:
        for i, outcome in enumerate(r['results'][filename]):
            if not isinstance(outcome[0], int):
                okay[i] = False

    print(f'{filename}: {sum(okay)} sentences parsed at every modification')


    # step 2: extract number of readings for those sentences
    history = []
    for r in results:
        readings = []
        for i, outcome in enumerate(r['results'][filename]):
            if okay[i]:
                readings.append(outcome[0])
        history.append(readings)

    readings_history[filename] = history

with open('/tmp/readings_history.json', 'w') as f:
    json.dump(readings_history, f)

plain_readings_history = []
for a, b in zip(*readings_history.values()):
    plain_readings_history.append(a + b)

with open('/tmp/play_readings_history.json', 'w') as f:
    json.dump(plain_readings_history, f)

n = len(plain_readings_history[0])

plt.plot(
    range(len(plain_readings_history)),
    [
        sum(readings) / n
        for readings in plain_readings_history
    ],
    label='Average'
)

plt.plot(
    range(len(plain_readings_history)),
    [
        sorted(readings)[n // 2] for readings in plain_readings_history
    ],
    label='Median',
)

plt.plot(
    range(len(plain_readings_history)),
    [
        sorted(readings)[int(n * 0.95)] for readings in plain_readings_history
    ],
    label='95th percentile',
)

plt.plot(
    range(len(plain_readings_history)),
    [
        sorted(readings)[int(n * 0.98)] for readings in plain_readings_history
    ],
    label='98th percentile',
)

plt.plot(
    range(len(plain_readings_history)),
    [
        max(readings) for readings in plain_readings_history
    ],
    label='Max',
)

plt.ylim(bottom=0)
plt.title('Syntactic Ambiguity')
plt.legend(prop={'size': 12})
plt.xlabel('Number of grammar modifications')
plt.ylabel('Average number of readings per sentence')

plt.savefig('/tmp/coverage_by_sentence_length.pdf', bbox_inches='tight')

plt.show()
