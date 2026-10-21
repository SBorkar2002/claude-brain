import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from sprites import FRAMES
KEYS = '#YpwmMzh'
out = {}
for state, frames in FRAMES.items():
    out[state] = []
    for g in frames:
        layers = {}
        for k in KEYS:
            runs = []
            for r, row in enumerate(g):
                c = 0
                while c < len(row):
                    if row[c] == k:
                        c0 = c
                        while c < len(row) and row[c] == k: c += 1
                        runs.append([r, c0, c - c0])
                    else:
                        c += 1
            if runs: layers[k] = runs
        out[state].append(layers)
s = json.dumps(out, separators=(',', ':'))
open(sys.argv[1], 'w').write(s)
print(len(s), sum(len(v) for v in out.values()))
