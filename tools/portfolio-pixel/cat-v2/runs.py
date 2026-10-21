"""Export Cat v2 as merged rectangles per colour layer, for building vectors in Figma.
Usage: python3 runs.py out.json
Output: {"size": 48, "layers": [...], "frames": {state: [{key: [[x, y, w, h], ...]}, ...]}, "timings": {...}}
Each run of same-colour pixels in a row is extended downward while the next rows repeat it exactly,
so a layer becomes a handful of rectangles instead of one per pixel.
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sprites import FRAMES, TIMINGS, W

KEYS = 'sf#lYgpwmMzh'
LAYER_NAMES = {'s': 'shadow', 'l': 'body-top', 'f': 'body-far', '#': 'body', 'Y': 'eyes', 'g': 'bell', 'p': 'pupils', 'w': 'shine', 'm': 'mouth', 'M': 'mouth-inner', 'z': 'zzz', 'h': 'heart'}


def rects(g, k):
    H = len(g)
    runs = []
    for r, row in enumerate(g):
        c = 0
        while c < len(row):
            if row[c] == k:
                c0 = c
                while c < len(row) and row[c] == k:
                    c += 1
                runs.append((r, c0, c - c0))
            else:
                c += 1
    used = set()
    out = []
    runset = set(runs)
    for r, c0, n in runs:
        if (r, c0, n) in used:
            continue
        h = 1
        while (r + h, c0, n) in runset and (r + h, c0, n) not in used:
            used.add((r + h, c0, n))
            h += 1
        out.append([c0, r, n, h])
    return out


if __name__ == '__main__':
    data = {'size': W, 'layers': [[k, LAYER_NAMES[k]] for k in KEYS], 'frames': {}, 'timings': TIMINGS}
    for state, frames in FRAMES.items():
        data['frames'][state] = []
        for g in frames:
            layers = {}
            for k in KEYS:
                rs = rects(g, k)
                if rs:
                    layers[k] = rs
            data['frames'][state].append(layers)
    s = json.dumps(data, separators=(',', ':'))
    open(sys.argv[1], 'w').write(s)
    print(len(s), 'bytes,', sum(len(v) for v in data['frames'].values()), 'frames')
