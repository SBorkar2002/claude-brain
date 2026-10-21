"""Wardrobe overlays (20 Oct): hat, tie, glasses, bow. Each accessory is drawn into every frame of every
state by the same code that draws the cat (sprites.ACC), then only the pixels it changed are kept. So each
overlay already follows the head through bobs, turns, mirrors, the tumble rotation and the upside-down peek.

Export (added to preview/frames.json by render.py), in the code chat's format:
  accessories[name] = {"sprites": [rows, ...], "anchors": {state: [[x, y, v] or null per frame]}}
  rows use the cat legend: H hat/tie purple, b light purple band, k glasses (opposite of body), h bow, M knot,
  # body (only where the hat shades the top-light rim). Code draws them over the cat; hat on top.
  icons[name] = 16x16 rows, '#' filled, tinted by the button text colour.
"""
import sprites

NAMES = ['tie', 'glasses', 'bow', 'hat']
KEYS = set('HbkhMg')

ICONS = {
    'hat': ["................",
            ".........###....",
            "........#####...",
            "........###.##..",
            ".......####..#..",
            ".......####.....",
            "......######....",
            "......######....",
            ".....########...",
            ".....########...",
            "....##########..",
            "................",
            "....##########..",
            ".##############.",
            "################",
            "................"],
    'tie': ["................",
            "......HHHH......",
            "......HHHH......",
            ".......HH.......",
            "......HHHH......",
            "......HbHH......",
            ".....HHbHHH.....",
            ".....HHHbHH.....",
            ".....HHHHbH.....",
            ".....HHHHHH.....",
            ".....HbHHHH.....",
            "......HbHH......",
            "......HHHH......",
            ".......HH.......",
            "................",
            "................"],
    'glasses': ["................",
                "................",
                "................",
                "................",
                "..####....####..",
                ".#....#..#....#.",
                "#......##......#",
                "#......##......#",
                "#......##......#",
                "#......##......#",
                ".#....#..#....#.",
                "..####....####..",
                "................",
                "................",
                "................",
                "................"],
    'bow': ["................",
            "................",
            "................",
            "..hhh......hhh..",
            "..hhhh....hhhh..",
            "..hhhhh..hhhhh..",
            "..hhhhhMMhhhhh..",
            "..hhhhhMMhhhhh..",
            "..hhhhh..hhhhh..",
            "..hhhh....hhhh..",
            "..hhh......hhh..",
            "................",
            "................",
            "................",
            "................",
            "................"],
}


def frames_with(acc):
    sprites.ACC = set(acc)
    try:
        return sprites.build()
    finally:
        sprites.ACC = set()


def overlay(base, worn):
    cells = []
    for r in range(sprites.H):
        for c in range(sprites.W):
            a, b = worn[r][c], base[r][c]
            if a != b and (a in KEYS or (a == '#' and b == 'l')):
                cells.append((r, c, a))
    return cells


def boxed(cells):
    if not cells:
        return None
    r0 = min(r for r, _, _ in cells); r1 = max(r for r, _, _ in cells)
    c0 = min(c for _, c, _ in cells); c1 = max(c for _, c, _ in cells)
    rows = [['.'] * (c1 - c0 + 1) for _ in range(r1 - r0 + 1)]
    for r, c, ch in cells:
        rows[r - r0][c - c0] = ch
    return {'x': c0, 'y': r0, 'rows': [''.join(l) for l in rows]}


def compute():
    base = frames_with([])
    cells = {n: {} for n in NAMES}
    for n in NAMES:
        worn = frames_with([n])
        for st, fr in base.items():
            cells[n][st] = [overlay(b, w) for b, w in zip(fr, worn[st])]
    clash = {}
    for st in base:
        row = []
        for i in range(len(base[st])):
            hat = {(r, c) for r, c, _ in cells['hat'][st][i]}
            bow = {(r, c) for r, c, _ in cells['bow'][st][i]}
            near = {(r + dr, c + dc) for r, c in hat for dr in (-1, 0, 1) for dc in (-1, 0, 1)}
            row.append(bool(near & bow))
        clash[st] = row
    return base, cells, clash


def mono(rows):
    """Button icons are tinted by the code: '#' filled, '.' empty. Detail colours (band, stripe, knot) become gaps."""
    return [''.join('#' if ch in 'H#kh' else '.' for ch in l) for l in rows]


def export_into(data):
    """Code chat format (20 Oct): accessories[name] = {sprites: [rows...], anchors: {state: [[x, y, v] or null]}}.
    Identical overlays share one sprite. Shadow (not a cat pose) is left out, so it means hidden."""
    base, cells, clash = compute()
    acc = {}
    for n in NAMES:
        sprites_, index, anchors = [], {}, {}
        for st, fr in cells[n].items():
            if st == 'Shadow':
                continue
            row = []
            for c in fr:
                b = boxed(c)
                if b is None:
                    row.append(None)
                    continue
                key = tuple(b['rows'])
                if key not in index:
                    index[key] = len(sprites_)
                    sprites_.append(b['rows'])
                row.append([b['x'], b['y'], index[key]])
            anchors[st] = row
        acc[n] = {'sprites': sprites_, 'anchors': anchors}
    data['accessories'] = acc
    data['icons'] = {n: mono(r) for n, r in ICONS.items()}
    return data


def composite(g, cells_list):
    out = [row[:] for row in g]
    for cells in cells_list:
        for r, c, ch in cells:
            out[r][c] = ch
    return out
