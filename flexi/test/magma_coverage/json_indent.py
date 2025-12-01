import json
import sys

for fn in sys.argv[1:]:
    with open(fn) as f:
        data = json.load(f)

    with open(fn, 'w') as f:
        json.dump(data, f, indent=2)
