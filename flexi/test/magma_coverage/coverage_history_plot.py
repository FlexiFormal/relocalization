import json
from matplotlib import pyplot as plt


with open('/tmp/coverage_history.json', 'r') as f:
    results = json.load(f)

def get_percentage(d):
    ok = sum(1 for r in d if isinstance(r[0], int))
    total = len(d)
    return ok / total * 100

def get_file_percentages(filename):
    return [get_percentage(r['results'][filename]) for r in results]


for filename in ['definitions_train.json', 'theorems_train.json', 'definitions_test.json', 'theorems_test.json']:
    percentages = get_file_percentages(filename)
    plt.plot(percentages, label=filename)

plt.legend()
plt.show()



