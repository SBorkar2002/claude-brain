"""Pixel cat sprite source, Cat v2 (17 Oct 2026).

48x48 frames, palette-indexed, one cat for every state. Proportions measured from Sejal's reference
(refs/sejal-reference-cat.png): head 22x19, eyes 8 px with a 2 px gap, legs 3 px x 10 rows, body 35 px long.
Faces right (her reference faces left; the site flips it when walking left).

Legend: '.' empty, '#' body, 'f' far-side legs (one shade off the body), 'Y' eye ring, 'p' pupil (black fill), 'w' eye shine,
        'm' mouth, 'M' mouth inner, 'z' Z, 'h' heart.
Shapes are hand-drawn ASCII stamps; only foot positions are computed. Run render.py to preview.
"""
W = H = 48
GROUND = 47


def blank():
    return [['.'] * W for _ in range(H)]


def put(g, r, c, ch='#'):
    if 0 <= r < H and 0 <= c < W:
        g[r][c] = ch


def stamp(g, art, top, left, flip=False):
    """Copy an ASCII stamp; '.' is transparent. flip mirrors it left to right."""
    for i, line in enumerate(art):
        if flip:
            line = line[::-1]
        for j, ch in enumerate(line):
            if ch != '.':
                put(g, top + i, left + j, ch)


def clear(g, cells):
    for r, c in cells:
        put(g, r, c, '.')


# ---------- eyes: 8x8 pixel circle, 1 px yellow ring, round black fill ----------
RING = ["..####..",
        ".######.",
        "########",
        "########",
        "########",
        "########",
        ".######.",
        "..####.."]


def disc(w, h):
    """Rounded fill, w x h, corners cut by 1 px."""
    return ['.' + '#' * (w - 2) + '.'] + ['#' * w] * (h - 2) + ['.' + '#' * (w - 2) + '.']


# look -> (fill w, fill h, row offset, col offset) inside the 8x8 eye
LOOK = {
    (0, 0): (6, 6, 1, 1),
    (-1, 0): (5, 6, 1, 1), (1, 0): (5, 6, 1, 2),
    (0, -1): (6, 5, 1, 1), (0, 1): (6, 5, 2, 1),
    (-1, -1): (5, 5, 1, 1), (1, -1): (5, 5, 1, 2),
    (-1, 1): (5, 5, 2, 1), (1, 1): (5, 5, 2, 2),
}

SQUEEZE = ["##....",   # '>' for the left eye; mirrored for the right
           "..##..",
           "....##",
           "..##..",
           "##...."]


def eye(g, top, left, mode='open', look=(0, 0), side='l', shine=True):
    """modes: open, wide (small fill), half, blink, sleep (lower arc), happy (upper arc), squeeze (> <)."""
    if mode in ('open', 'wide'):
        for i, line in enumerate(RING):
            for j, ch in enumerate(line):
                if ch == '#':
                    put(g, top + i, left + j, 'Y')
        if mode == 'open':
            fw, fh, ro, co = LOOK[look]
        else:
            fw, fh, ro, co = 4, 4, 2 + look[1], 2 + look[0]
        for i, line in enumerate(disc(fw, fh)):
            for j, ch in enumerate(line):
                if ch == '#':
                    put(g, top + ro + i, left + co + j, 'p')
        if shine and mode == 'open':
            put(g, top + ro + 1, left + co + 1, 'w')   # one pixel in from the fill's top-left, never on the ring
    elif mode == 'half':      # lid down to the middle: flat lid line, round bottom; fill slides with look
        art = {0: ["YYYYYYYY", "YppppppY", ".YppppY.", "..YYYY.."],
               1: ["YYYYYYYY", "YYpppppY", ".YYpppY.", "..YYYY.."],
               -1: ["YYYYYYYY", "YpppppYY", ".YpppYY.", "..YYYY.."]}[look[0]]
        stamp(g, art, top + 4, left)
    elif mode == 'blink':
        stamp(g, [".YYYYYY."], top + 5, left)
    elif mode == 'shut':      # squeezed shut for the yawn: full 8 px line, pushed up by the cheeks, clear of the whiskers
        stamp(g, ["YYYYYYYY"], top + 3, left)
    elif mode == 'sleep':     # lower arc of the ring
        stamp(g, ["Y......Y",
                  ".Y....Y.",
                  "..YYYY.."], top + 4, left)
    elif mode == 'happy':     # upper arc of the ring
        stamp(g, ["..YYYY..",
                  ".Y....Y.",
                  "Y......Y"], top + 3, left)
    elif mode == 'squeeze':
        art = [l.replace('#', 'Y') for l in SQUEEZE]
        stamp(g, art, top + 2, left + 1, flip=(side == 'r'))


# ---------- head: front-facing, 22 wide x 19 tall ----------
HEAD = ["#....................#",   # 0  ear tips
        "##..................##",   # 1
        "###................###",   # 2
        "#####............#####",   # 3  ear inner edge curves into the skull (runs 1,1,1,2)
        "######################",   # 4
        "######################",   # 5
        "######################",   # 6
        "######################",   # 7  eyes rows 7-14
        "######################",
        "######################",
        "######################",
        "######################",   # 11 whisker
        "######################",
        "######################",   # 13 whisker
        "######################",
        "######################",
        "######################",
        ".####################.",   # 17 cheeks round off (runs 1, 2)
        "..##################.."]   # 18

# ears pulled back (yawn, stretch): 1 px lower, tips blunt
HEAD_EARS_BACK = ["......................",
                  "##..................##",
                  "###................###",
                  "#####............#####"] + HEAD[4:]

WHISKERS = {11: 3, 13: 2}   # row in head -> length; upper is longer, like a hand-drawn pair (she kept them, 19 Oct)


BELL = [".YY.",     # yellow bell ('Y') on the lime belt ('g')
        "YYYY",
        ".pp."]


def collar(g, mask):
    """Yellow belt all the way round the neck: under every head column that has body within 3 rows below
    (closing any gap), so it never stops partway when the head bobs or turns. Green bell at the neck's centre."""
    cols = {}
    for r, c in mask:
        cols[c] = max(cols.get(c, -1), r)
    belt = []
    for c, rb in sorted(cols.items()):
        if not (0 <= c < W) or rb + 1 >= H:
            continue
        below = [g[rr][c] if rr < H else '.' for rr in (rb + 1, rb + 2, rb + 3)]
        if any(ch in '#fl' for ch in below):
            for k, ch in enumerate(below):          # close a gap between head and body
                if ch in '#fl':
                    break
                if k > 0:
                    g[rb + 1 + k][c] = '#'
            g[rb + 1][c] = 'g'
            belt.append((c, rb + 1))
    if len(belt) >= 4:
        cx = round(sum(c for c, _ in belt) / len(belt))
        r = max(rr for c, rr in belt if abs(c - cx) <= 1)
        stamp(g, BELL, r + 1, cx - 1)
        if 'tie' in ACC:                                 # only on the body, never in the air
            for i, line in enumerate(TIE):
                for j, ch in enumerate(line):
                    rr, cc = r + 1 + i, cx - 2 + j
                    if ch != '.' and 0 <= rr < H and 0 <= cc < W and g[rr][cc] not in '.sg':
                        g[rr][cc] = ch


# ---------- wardrobe (20 Oct): overlay accessories, drawn only when ACC asks for them ----------
# Keys: 'H' hat and tie purple, 'b' light purple band, 'k' glasses (the colour opposite the body),
# 'h' bow pink, 'M' bow knot. accessories.py builds every frame once per accessory and keeps the difference.
ACC = set()          # which accessories to draw: any of 'hat', 'tie', 'glasses', 'bow'
NOFACE = False       # talk() redraws the head itself, so the sit under it skips the face accessories
HAT = ["...........HHH........",      # witch hat (20 Oct): pointed cone, tip droops right, wide flat brim
       "..........HHHHH.......",      # rows -7..3 from the head top; the brim sits on the ear bases so the
       "..........HHH.HH......",      # ear tips stay readable either side; lime buckle on the band
       ".........HHHH...H.....",
       "........HHHHHH........",
       "........HHHHHH........",
       ".......HHHHHHHH.......",
       "......bbbbggbbbb......",
       "......HHHHHHHHHH......",
       "....HHHHHHHHHHHHHH....",
       "..HHHHHHHHHHHHHHHHHH.."]
BOW = ["hh...hh",              # clipped beside the right ear, knot on the ear's outer edge
       "hhh.hhh",
       "hhhMhhh",
       "hhh.hhh",
       "hh...hh"]
TIE = [".HHHH.",               # knot sits over the bell, the blade hangs down the chest
       "..HH..",
       ".HHHH.",
       ".HbHH.",
       "HHbHHH",
       "HHHbHH",
       ".HHHH.",
       "..HH.."]
GLASS = ["..######..",          # 1 px outside the 8 px eye ring, so the yellow eye shows through
         ".#......#.",
         "#........#",
         "#........#",
         "#........#",
         "#........#",
         "#........#",
         "#........#",
         ".#......#.",
         "..######.."]
GLASS_NARROW = [".######.",       # around the narrow far eye (3/4) or the profile eye
                "#......#",
                "#......#",
                "#......#",
                "#......#",
                "#......#",
                "#......#",
                "#......#",
                "#......#",
                ".######."]


def _ink(art, ch):
    return [l.replace('#', ch) for l in art]


def wear(g, view, top, left):
    """Face accessories for a head stamped at (top, left). view: 'front', '34' (turned right), 'back', 'profile'."""
    if NOFACE:
        return
    if 'bow' in ACC:
        if view == 'profile':
            stamp(g, BOW, top + 1, left + 14)
        else:
            stamp(g, BOW, top + 1, left + 18)
    if 'hat' in ACC:
        stamp(g, HAT, top - 7, left + {'profile': -2, '34': 1}.get(view, 0))
    if 'glasses' in ACC and view != 'back':
        if view == 'front':
            stamp(g, _ink(GLASS, 'k'), top + 6, left + 1)
            stamp(g, _ink(GLASS, 'k'), top + 6, left + 11)
            put(g, top + 9, left, 'k'); put(g, top + 9, left + 21, 'k')
        elif view == '34':
            stamp(g, _ink(GLASS, 'k'), top + 6, left + 3)
            stamp(g, _ink(GLASS_NARROW, 'k'), top + 6, left + 13)
            put(g, top + 9, left + 2, 'k'); put(g, top + 9, left + 1, 'k')
        else:
            stamp(g, _ink(GLASS_NARROW, 'k'), top + 5, left + 11)
            for c in range(left + 7, left + 11):
                put(g, top + 8, c, 'k')


def head(g, top, left, mode='open', look=(0, 0), whisk='both', ears='up', shine=True, belt=True):
    art = HEAD_EARS_BACK if ears == 'back' else HEAD
    mask = {(top + i, left + j) for i, line in enumerate(art) for j, ch in enumerate(line) if ch == '#'}
    stamp(g, art, top, left)
    if mode == 'squeeze':
        eye(g, top + 7, left + 2, 'squeeze', side='l')
        eye(g, top + 7, left + 12, 'squeeze', side='r')
    else:
        eye(g, top + 7, left + 2, mode, look, shine=shine)
        eye(g, top + 7, left + 12, mode, look, shine=shine)
    for r, n in WHISKERS.items():
        if whisk in ('both', 'left'):
            for k in range(1, n + 1):
                put(g, top + r, left - k)
        if whisk in ('both', 'right'):
            for k in range(1, n + 1):
                put(g, top + r, left + 21 + k)
    if belt:
        collar(g, mask)
    wear(g, 'front', top, left)


MARKS = ["...Y",     # yellow marks beside the head (yawn, react), like her reference
         "..Y.",
         "....",
         "YYY.",
         "....",
         "..Y.",
         "...Y"]


def marks(g, top, left):
    stamp(g, MARKS, top, left)


def mouth(g, top, left, size):
    """Mouth centred under the eyes. Only the yawn uses it. A small V with two fangs reads as a cat's open
    mouth; tall pink ovals and wide pink shapes read as tongues or lips (tested side by side, see research.md)."""
    cx = left + 11   # head centre line falls between cols 10 and 11
    if size == 'small':      # the yawn starting or closing
        stamp(g, ["wMMw",
                  ".MM."], top + 15, cx - 2)
    elif size == 'big':      # wide open: fangs at the top corners, a little tongue at the bottom
        stamp(g, ["wMMMMw",
                  ".MMMM.",
                  ".MmmM.",
                  "..MM.."], top + 14, cx - 3)


# ---------- legs ----------
def leg(g, top, bottom, x_top, x_bot, width=5):
    """A straight 5 px leg (chunky, not a stick) with clean, even steps: rows split into |dx|+1 runs,
    longest runs in the middle. The heel corner of the foot is cut so it reads as a soft round paw."""
    n = bottom - top + 1
    dx = x_bot - x_top
    k = abs(dx) + 1
    base, extra = divmod(n, k)
    runs = [base] * k
    for i in sorted(range(k), key=lambda i: abs(i - (k - 1) / 2))[:extra]:
        runs[i] += 1
    step = (dx > 0) - (dx < 0)
    r, x = top, x_top
    for run in runs:
        for _ in range(run):
            for c in range(x, x + width):
                put(g, r, c)
            r += 1
        x += step
    put(g, bottom, x - step, '.')   # heel (rear corner of the paw)


# ---------- standing / walking: side body, head turned to camera ----------
HX, HY = 19, 11          # head position when standing (our HEAD stamp, same size as the reference head)
# Standing cat TRACED from Sejal's refined reference (inventory/refs/cat-reference.webp, 19 Oct): the big
# reference cat sampled to this grid (about 7.4 source px per sprite px, majority colour per cell), so the
# rounded rump, chest and tapering legs are hers, not redrawn by eye. Body + tail block below (rows 9-38,
# cols 2-35); the head is our HEAD stamp with our eyes and whiskers, placed where her head sits. Her
# reference separates head and body with a dark notch (col 18 and the row under the chin); kept as traced.
TAIL_UP, TAIL_SWAY = 0, 1
TRACE_BODY = [
    "..................................",
    "...####...........................",
    "..######...........#..............",
    "..######...........##.............",
    "..######...........###............",
    "..######...........#####..........",
    "..######...........###############",
    "..#####............###############",
    "..#####............###############",
    "..#####..........#################",
    "..#####..........#################",
    "..#####..........#################",
    ".#####...........#################",
    ".#####...........#################",
    ".#####...........#################",
    ".#####...........#################",
    ".#####.#########.#################",
    ".###############.#################",
    ".###############.#################",
    "..###############..###############",
    "..###############...##############",
    "...################...............",
    "...#############################..",
    "...#############################..",
    "...#############################..",
    "...#############################..",
    "..##############################..",
    "..#############################...",
    "..#############################...",
    "..#############################...",
]
TRACE_TOP, TRACE_LEFT = 9, 2
# legs traced from the same image, as (row, first col, last col) in sprite coordinates
NEAR_HIND = [(38, 4, 11), (39, 4, 11), (40, 4, 11), (41, 4, 9), (42, 4, 8), (43, 4, 7), (44, 4, 7), (45, 4, 7),
             (46, 4, 8), (47, 4, 8)]
FAR_HIND = [(38, 12, 15), (39, 12, 15), (40, 12, 16), (41, 11, 16), (42, 12, 14), (43, 11, 14), (44, 11, 14),
            (45, 11, 14), (46, 11, 16)]
NEAR_FRONT = [(38, 23, 27), (39, 23, 27), (40, 23, 27), (41, 23, 27), (42, 23, 27), (43, 23, 27), (44, 23, 27),
              (45, 23, 27), (46, 24, 28), (47, 24, 28)]
FAR_FRONT = [(38, 29, 32), (39, 29, 32), (40, 29, 32), (41, 29, 32), (42, 29, 32), (43, 30, 33), (44, 30, 33),
             (45, 30, 33), (46, 31, 33)]
LEGS = {'near_hind': (NEAR_HIND, False), 'far_hind': (FAR_HIND, True),
        'near_front': (NEAR_FRONT, False), 'far_front': (FAR_FRONT, True)}


def torso(g, dy=0, breathe=0, tail_lean=0, tail_dy=0):
    for i, line in enumerate(TRACE_BODY):
        r = TRACE_TOP + i + dy
        for j, ch in enumerate(line):
            if ch == '.':
                continue
            c = TRACE_LEFT + j
            if tail_lean and i <= 7 and c <= 10:      # tail top sways 1 px forward
                c += 1
            put(g, r, c, '#' if ch != 'f' else 'f')
    if breathe:                                       # back rises 1 px between the tail and the head
        for c in range(10, 18):
            put(g, TRACE_TOP + 15 + dy, c)


def limb(g, prof, dx=0, lift=0, ch='#', up=0):
    """A traced leg: rows below the hip (row 39) shift progressively toward dx at the paw; lift raises the
    paw; up raises the hip (body bob) and stretches the leg by repeating its top row."""
    rows = list(prof)
    bottom = rows[-1][0] - lift
    if up:
        rows = [(rows[0][0] - k, rows[0][1], rows[0][2]) for k in range(up, 0, -1)] + rows
    for r, c0, c1 in rows:
        if r > bottom:
            continue
        hip = 39 - up
        shift = round(dx * max(0, r - hip) / max(1, bottom - hip))
        span(g, r, c0 + shift, c1 + shift, ch)


def side(legs, dy=0, look=(0, 0), mode='open', tail=TAIL_UP, breathe=0, head_dy=0, tail_dy=0):
    """legs: {name: (dx, lift)}. Far legs are drawn behind the body in the lilac far shade."""
    g = blank()
    for name, (dx, lift) in legs.items():
        prof, far = LEGS[name]
        if far:
            limb(g, prof, dx, lift, 'f', up=-dy)
    torso(g, dy, breathe, tail_lean=tail)
    for name, (dx, lift) in legs.items():
        prof, far = LEGS[name]
        if not far:
            limb(g, prof, dx, lift, '#', up=-dy)
    head(g, HY + dy + head_dy, HX, mode, look, whisk='right')
    return g


STAND = {'near_hind': (0, 0), 'far_hind': (0, 0), 'near_front': (0, 0), 'far_front': (0, 0)}


def walk_feet(phase):
    """Diagonal-pair stride like her reference: near front + far back reach together, then far front + near
    back. Cycle per leg: +3 contact, 0 support, -3 push, 0 swing lifted 2 px."""
    pos = [(+3, 0), (0, 0), (-3, 0), (0, 2)]
    a, b = pos[phase % 4], pos[(phase + 2) % 4]
    return {'far_hind': a, 'far_front': b, 'near_hind': b, 'near_front': a}


# ---------- sitting, front view ----------
SX, SY = 13, 14          # head position when sitting (cols 13-34, rows 14-32)
SIT_BODY = [              # 26 wide at cols 11-36, rows 33-47: a soft pear. Convex shoulders (steps 2,1,1,
    "......##############......",   # 33 neck      then 1 every 2 rows), round haunches, chunky round paws
    "....##################....",   # 34
    "...####################...",   # 35
    "..######################..",   # 36
    "..######################..",   # 37
    ".########################.",   # 38
    ".########################.",   # 39
    "##########################",   # 40 haunches
    "##########################",
    "##########################",
    "##########################",
    "##########################",   # 44
    "##########################",   # 45 paws tucked together: one solid, soft base
    "##########################",   # 46 (separate limbs read as a cat holding itself apart)
    ".########################."]   # 47 rounded outer corners
SIT_TAIL = [".####..",  # drawn for the right side, stamped flipped on the left (the rear): a plump '?'
            "######.",
            "######.",
            ".######",
            "..#####",
            "..#####",
            "..#####",
            ".#####.",
            ".#####.",
            "#####..",
            "#####..",
            "####..."]
REACH = ["...###.",    # right front paw raised toward the artwork (Inspect): round chunky paw on a 1:1 arm
         "..#####",
         "..#####",
         ".####..",
         "####...",
         "###...."]


def sit_body(lift=0, drop=0, widen=0):
    """lift: chest grows by `lift` rows (head rises); drop: chest loses `drop` rows.
    widen: +1 adds a pixel to each side of every row below the neck (squash keeps its mass),
    -1 takes one away (stretch). Breathing uses lift alone, so it never changes width."""
    rows = list(SIT_BODY)
    for _ in range(lift):
        rows.insert(1, rows[1])
    for i in range(drop):
        del rows[2 + i]
    if widen:
        n = abs(widen)
        out = []
        for i, row in enumerate(rows):
            row = list('.' * n + row + '.' * n)
            if i > 0:
                first = next(j for j, ch in enumerate(row) if ch == '#')
                last = max(j for j, ch in enumerate(row) if ch == '#')
                for k in range(1, n + 1):
                    if widen > 0:
                        row[first - k] = '#'
                        row[last + k] = '#'
                    else:
                        row[first + k - 1] = '.'
                        row[last - k + 1] = '.'
            out.append(''.join(row))
        rows = out
    return rows


def sit(mode='open', look=(0, 0), lift=0, drop=0, widen=0, dy=0, head_dx=0, ears='up', mouth_size=None, reach=False,
        tail=True, shine=True):
    g = blank()
    body = sit_body(lift, drop, widen)
    top = H - len(body) + dy
    if tail:
        stamp(g, SIT_TAIL, top - 2 + lift, 4 - abs(widen), flip=True)
    stamp(g, body, top, SX - 2 - abs(widen))
    if reach:
        clear(g, [(r, c) for r in range(45 + dy, 48 + dy) for c in range(SX + 12, SX + 18)])
        stamp(g, REACH, 32 + dy, SX + 21)
    htop = top - 19
    head(g, htop, SX + head_dx, mode, look, ears=ears, shine=shine)
    if mouth_size:
        mouth(g, htop, SX + head_dx, mouth_size)
    return g


# ---------- yawn: sleepy, small mouth, big stretch, close, two eyes again ----------
def yawn(stage):
    if stage == 1:
        return sit(mode='half')
    if stage == 2:
        return sit(mode='blink', mouth_size='small', lift=1)
    if stage == 3:
        g = sit(mode='shut', mouth_size='big', ears='back', lift=2)
        marks(g, (H - len(sit_body(2))) - 19 + 3, SX + 24)
        return g
    if stage == 4:
        return sit(mode='blink', mouth_size='small', lift=1)
    return sit(mode='sleep')


# ---------- sleep: front-facing loaf, head lowered onto it ----------
LOAF = ["........##################........",   # 33 a soft dome (steps 3,2,1,1,0,1), 34 wide
        ".....########################.....",   # 34
        "...############################...",   # 35
        "..##############################..",   # 36
        ".################################.",   # 37
        ".################################.",   # 38
        "##################################",   # 39
        "##################################",
        "##################################",
        "##################################",
        "##################################",
        "##################################",   # 44
        ".################################.",   # 45
        ".################################.",   # 46
        "...############################..."]   # 47
TAIL_REST = [".....###",   # plump tail lies along the ground and curls up at the tip
             "....#####",
             "....#####",
             ".....####",
             "########.",
             "#######.."]
Z = ["#####",
     "...#.",
     "..#..",
     ".#...",
     "#####"]
Z_SMALL = ["####",
           "..#.",
           ".#..",
           "####"]


def sleep(stage):
    g = blank()
    up = 1 if stage in (2, 4) else 0
    loaf = LOAF if not up else [LOAF[0]] + LOAF
    stamp(g, loaf, H - len(loaf), 6)
    stamp(g, TAIL_REST, 42, 37)
    head(g, 27 - up, SX, 'sleep', shine=False)
    zs = [l.replace('#', 'z') for l in Z_SMALL]
    zb = [l.replace('#', 'z') for l in Z]
    if stage == 2:
        stamp(g, zs, 22, 37)
    elif stage == 3:
        stamp(g, zs, 19, 38)
        stamp(g, zb, 12, 42)
    elif stage == 4:
        stamp(g, zb, 9, 43)
    return g


# ---------- mid-air: the landing pose (Fall, Land, React) ----------
def span(g, r, c0, c1, ch='#'):
    for c in range(c0, c1 + 1):
        put(g, r, c, ch)


def slant(g, top, bottom, x_top, x_bot, width=4):
    """A straight limb with even steps (1:2 for a 30 degree splay)."""
    leg(g, top, bottom, x_top, x_bot, width)


def midair_front(top=8, mode='open', look=(0, 1), tail_side='l', eyes_on=True):
    """Front view, falling upright like a cat about to land: four legs splayed about 30 degrees
    (1:2 steps), tail straight and raised, angled up and out behind the head. top = head top row."""
    g = blank()
    t = top
    # tail first (it sits behind the head)
    if tail_side == 'l':
        slant(g, t - 2, t + 9, 4, 9, 5)
        span(g, t - 3, 5, 7)
    else:
        slant(g, t - 2, t + 9, 39, 34, 5)
        span(g, t - 3, 40, 42)
    # belly, seen from the front: soft and full under the chin
    for dr, c0, c1 in [(16, 15, 32), (17, 14, 33), (18, 14, 33), (19, 14, 33), (20, 14, 33), (21, 14, 33),
                       (22, 14, 33), (23, 14, 33), (24, 15, 32), (25, 16, 31), (26, 18, 29)]:
        span(g, t + dr, c0, c1)
    # hind legs splay out from the hips, front legs reach down and out from the chest: four chunky limbs,
    # each stretched about 30 degrees from the body, 1 px apart, round paws
    slant(g, t + 18, t + 25, 11, 7, 5)
    slant(g, t + 18, t + 25, 32, 36, 5)
    slant(g, t + 22, t + 29, 17, 13, 5)
    slant(g, t + 22, t + 29, 26, 30, 5)
    if eyes_on:
        head(g, t, SX, mode, look)
    else:   # back of the head: same shape and whiskers, no face
        stamp(g, HEAD, t, SX)
        for r, n in WHISKERS.items():
            for k in range(1, n + 1):
                put(g, t + r, SX - k); put(g, t + r, SX + 21 + k)
        wear(g, 'back', t, SX)
    return g


PROFILE = ["...#......#.........",   # head in profile, facing right: far ear behind, near ear in front
           "...##....###........",
           "..###...#####.......",
           "..####.#######......",
           "..###############...",
           ".#################..",
           ".##################.",
           "####################",
           "####################",
           "####################",
           "####################",
           "####################",
           "####################",
           "###################.",
           "##################..",
           "#################...",
           ".###############....",
           "..#############.....",
           "...##########......."]
PROFILE_RING = [".####.", "######", "######", "######", "######", "######", "######", ".####."]


def profile_head(g, top, left, look=(0, 1)):
    stamp(g, PROFILE, top, left)
    collar(g, {(top + i, left + j) for i, l in enumerate(PROFILE) for j, ch in enumerate(l) if ch == '#'})
    for i, line in enumerate(PROFILE_RING):           # one eye, a narrower O near the front
        for j, ch in enumerate(line):
            if ch == '#':
                put(g, top + 6 + i, left + 12 + j, 'Y')
    dy = 1 if look[1] > 0 else 0
    for i, line in enumerate(disc(4, 5)):
        for j, ch in enumerate(line):
            if ch == '#':
                put(g, top + 7 + dy + i, left + 13 + j, 'p')
    put(g, top + 8 + dy, left + 14, 'w')
    for r, n in WHISKERS.items():                      # near-side whiskers point forward
        for k in range(1, n + 1):
            put(g, top + r, left + 19 + k)
    wear(g, 'profile', top, left)


def midair_side(top=8, look=(0, 1)):
    """Profile facing right: body level, front legs reaching forward-down, hind legs back-down (each about
    30 degrees, each on its own hip), tail straight out the back and a little up."""
    g = blank()
    t = top
    for dr, c0, c1 in [(8, 14, 27), (9, 12, 27), (10, 11, 27)] + [(d, 11, 27) for d in range(11, 18)] + \
                      [(18, 12, 27), (19, 14, 26)]:
        span(g, t + dr, c0, c1)
    for dr, c0, c1 in [(6, 1, 4), (7, 0, 6), (8, 0, 8), (9, 1, 10), (10, 3, 12), (11, 5, 12), (12, 7, 12)]:
        span(g, t + dr, c0, c1)                        # tail: straight, 2 across for 1 up, round tip
    slant(g, t + 17, t + 24, 11, 7, 5)                 # far hind
    slant(g, t + 18, t + 25, 17, 13, 5)                # near hind
    slant(g, t + 17, t + 24, 20, 24, 5)                # far front
    slant(g, t + 18, t + 25, 27, 31, 5)                # near front
    profile_head(g, t, 24, look)
    return g


def midair_34(top=8, look=(1, 1), back=False):
    """Three-quarter view turning right. Front: the face slides toward the turn, the far eye narrows.
    Back: the back of the head, the body nearer, the tail big on the left."""
    g = blank()
    t = top
    slant(g, t - 1, t + 9, 6, 11, 5)                   # tail up and out, behind (front) or nearer (back)
    span(g, t - 2, 7, 9)
    for dr, c0, c1 in [(16, 13, 31), (17, 12, 32)] + [(d, 11, 32) for d in range(18, 24)] + \
                      [(24, 12, 31), (25, 14, 30), (26, 16, 28)]:
        span(g, t + dr, c0, c1)
    slant(g, t + 18, t + 25, 11, 6, 5)                 # hind legs trail toward the back (left)
    slant(g, t + 18, t + 25, 17, 15, 5)
    slant(g, t + 21, t + 28, 23, 24, 5)                # front legs reach toward the turn
    slant(g, t + 21, t + 28, 29, 33, 5)
    L = SX + 2
    stamp(g, HEAD, t, L)
    collar(g, {(t + i, L + j) for i, l in enumerate(HEAD) for j, ch in enumerate(l) if ch == '#'})
    for r, n in WHISKERS.items():
        for k in range(1, n + 1):
            put(g, t + r, L + 21 + k)
            if not back:
                put(g, t + r, L - k)
    if not back:
        eye(g, t + 7, L + 4, 'open', look)            # near eye, full O
        for i, line in enumerate(PROFILE_RING):       # far eye, narrower, near the edge
            for j, ch in enumerate(line):
                if ch == '#':
                    put(g, t + 7 + i, L + 14 + j, 'Y')
        for i, line in enumerate(disc(4, 5)):
            for j, ch in enumerate(line):
                if ch == '#':
                    put(g, t + 8 + (1 if look[1] > 0 else 0) + i, L + 15 + j, 'p')
    wear(g, 'back' if back else '34', t, L)
    return g


def mirror(g):
    return [row[::-1] for row in g]


def hop_front(top=10, mode='wide', look=(0, 0), grounded=False):
    """Front view with all four legs straight down under the body (a hop, or standing up):
    front legs inside, hind legs just outside and 3 px higher (further back), never splayed; tail up."""
    g = blank()
    t = top
    slant(g, t - 2, t + 9, 4, 9, 5)                    # tail straight up and out, behind the head
    span(g, t - 3, 5, 7)
    for dr, c0, c1 in [(16, 15, 32), (17, 14, 33)] + [(d, 14, 33) for d in range(18, 24)] + \
                      [(24, 15, 32), (25, 16, 31), (26, 18, 29)]:
        span(g, t + dr, c0, c1)
    hind_end = t + 28 if grounded else t + 27
    front_end = t + 31
    for x in (13, 30):                                 # hind legs, straight
        leg(g, t + 18, hind_end, x, x, 5)
    for x in (19, 24):                                 # front legs, straight, a 1 px gap between
        leg(g, t + 20, front_end, x, x, 4)
    head(g, t, SX, mode, look)
    return g


def fall_frames(top=8):
    """One full turn around the vertical axis, 8 frames: front, 3/4, side, 3/4 back, back, then mirrored."""
    F = midair_front(top)
    Q = midair_34(top)
    S = midair_side(top)
    QB = midair_34(top, back=True)
    B = mirror(midair_front(top, eyes_on=False))
    return [F, Q, S, QB, B, mirror(QB), mirror(S), mirror(Q)]


def land_front(top=16, mode='open', look=(0, 1), squash=0):
    """Front view standing on four straight legs, the same body as the hop. Lower `top` = knees bent:
    the body drops, the legs get shorter and splay 1 px, and the belly widens 1 px (mass kept)."""
    g = blank()
    t = top
    slant(g, t - 2, t + 9, 4, 9, 5)                    # tail still up from the fall
    span(g, t - 3, 5, 7)
    w = 1 if squash else 0
    for dr, c0, c1 in [(16, 15, 32), (17, 14, 33)] + [(d, 14, 33) for d in range(18, 24)] + \
                      [(24, 15, 32), (25, 16, 31), (26, 18, 29)]:
        if t + dr <= GROUND:
            span(g, t + dr, c0 - w, c1 + w)
    splay = 1 if squash else 0
    for x, d in ((13, -splay), (30, splay)):           # hind legs to the ground
        leg(g, min(t + 18, GROUND), GROUND - 1, x, x + d, 5)
    for x, d in ((19, -splay), (24, splay)):           # front legs to the ground
        leg(g, min(t + 20, GROUND), GROUND, x, x + d, 4)
    head(g, t, SX, mode, look)
    return g


def land(stage):
    """Paws reach down, the body compresses on impact, stays low to recover, rises, then sits once."""
    return {1: lambda: land_front(16, look=(0, 1)),                    # legs straight down, paws touch
            2: lambda: land_front(21, mode='happy', squash=1),         # impact: knees bend, eyes squeezed
            3: lambda: land_front(21, mode='blink', squash=1),         # stays low, recovering
            4: lambda: land_front(20, look=(0, 1), squash=1),          # eyes open, looking down
            5: lambda: land_front(17, look=(0, 0)),                    # rises, looks up
            6: lambda: sit(drop=1),                                    # settles into a sit
            7: lambda: sit()}[stage]()


# ---------- react: squash, hop with one heart, land ----------
HEART = [".##.##.",
         "#######",
         "#######",
         ".#####.",
         "..###..",
         "...#..."]


def react(stage):
    if stage == 1:     # anticipation: 2 rows shorter, 2 px wider each side
        return sit(mode='happy', drop=2, widen=2)
    if stage == 2:     # push off: legs straight down, tail up
        return hop_front(14)
    if stage == 3:     # top of the hop, yellow surprise marks beside the head (her reference)
        g = hop_front(9)
        marks(g, 9 + 2, SX + 24)
        return g
    if stage == 4:     # coming down
        return hop_front(15, mode='open', look=(0, 1))
    return sit(drop=1, widen=1)   # soft landing squash, then back to Sit


# ---------- peek: rises from behind an edge (the frame's bottom), paws over it ----------
PAW = [".####.",
       "######",
       "######"]


def peek(visible, look=(0, 0), paws=False, mode='open'):
    g = blank()
    top = H - visible
    head(g, top, SX, mode, look, whisk='both' if visible > 13 else 'none')
    if paws:   # hooked over the edge either side of the face
        stamp(g, PAW, H - 3, SX - 7)
        stamp(g, PAW, H - 3, SX + 23)
    return g


# ---------- inspect: notices the artwork (right), sinks into a pounce crouch, wiggles, holds ----------
def stalk(level=2, wiggle=0, look=(1, 0), mode='open'):
    """Inspect, from her reference: a low, long stalking crouch. The head stays forward and highest, the back
    slopes down to the rump, the tail stands straight up, and the legs fold short under the body, the white
    near paws a little forward. level 1 is halfway down. wiggle +1 / -1: the rump bobs 1 px, the tail tip
    twitches the other way and the back paws tread."""
    g = blank()
    d = 0 if level == 2 else -4                  # level 1 sits 4 rows higher
    ht, hx = 21 + d, 23 - (1 if level == 1 else 0)
    rump = (1 if wiggle == 1 else 0)
    tip = {0: 0, 1: -1, -1: 1}[wiggle]
    # far legs first, in the far shade
    for r in range(43 + d, 47 - (1 if wiggle == -1 else 0)):
        span(g, r, 12, 15, 'f')
    for r in range(43 + d, 47):
        span(g, r, 33, 36, 'f')
    # tail straight up from the rump, round top
    top = 14 + d - rump
    span(g, top, 6 + tip, 9 + tip)
    for r in range(top + 1, top + 5):
        span(g, r, 5 + tip, 10 + tip)
    for r in range(top + 5, 33 + d):
        span(g, r, 5, 10)
    # back slopes up from the rump to the head
    for r, c0, c1 in [(29, 18, 23), (30, 14, 23), (31, 10, 23), (32, 5, 23)]:
        span(g, r + d, c0, c1)
        if rump and c0 < 14:                     # rump bobs up 1 px; the body under it stays filled
            span(g, r + d - 1, c0, min(c1, 13))
    for r in range(33 + d, 42 + d):
        span(g, r, 5, 37)
    span(g, 42 + d, 6, 37)
    # near legs folded short; paws a little forward
    lift = 1 if wiggle == 1 else 0
    for r in range(40 + d, 47 - lift):
        span(g, r, 5, 11)
    span(g, 47 - lift, 6, 12)
    for r in range(43 + d, 47):
        span(g, r, 28, 31)
    span(g, 47, 28, 33)
    head(g, ht, hx, mode, look, whisk='right')
    return g


def inspect(stage):
    """Notices the artwork, sinks into a stalking crouch, wiggles twice, rises."""
    return {1: lambda: side(STAND, look=(1, 0)),
            2: lambda: stalk(1),
            3: lambda: stalk(2),
            4: lambda: stalk(2, wiggle=1),
            5: lambda: stalk(2, wiggle=-1),
            6: lambda: stalk(2, wiggle=1),
            7: lambda: stalk(2, wiggle=-1),
            8: lambda: stalk(1)}[stage]()


# ---------- round 8 (19 Oct): run, tumble, side/top peek, talk, shadow, top light ----------
def run(stage):
    """Gallop for chasing the laser cursor: extend, float, gather, push. Front and back pairs move together."""
    legs = {1: {'near_front': (5, 0), 'far_front': (3, 1), 'near_hind': (-5, 0), 'far_hind': (-3, 1)},
            2: {'near_front': (2, 2), 'far_front': (1, 2), 'near_hind': (-1, 2), 'far_hind': (0, 2)},
            3: {'near_front': (-3, 0), 'far_front': (-2, 1), 'near_hind': (5, 0), 'far_hind': (4, 1)},
            4: {'near_front': (1, 0), 'far_front': (0, 1), 'near_hind': (2, 0), 'far_hind': (1, 1)}}[stage]
    dy = {1: 0, 2: -2, 3: -1, 4: 0}[stage]
    return side(legs, dy=dy, look=(1, 0), tail=(TAIL_SWAY if stage in (2, 3) else TAIL_UP))


def rotate(g, deg, cy=24.0, cx=23.5):
    """In-plane rotation, nearest neighbour, so every frame stays on the pixel grid (fall only)."""
    import math
    t = math.radians(deg)
    out = blank()
    for r in range(H):
        for c in range(W):
            y, x = r - cy, c - cx
            sr = round(cy + y * math.cos(t) - x * math.sin(t))
            sc = round(cx + y * math.sin(t) + x * math.cos(t))
            if 0 <= sr < H and 0 <= sc < W:
                out[r][c] = g[sr][sc]
    return out


def tumble_frames():
    """Extra fall spins in the picture plane (explicitly allowed for the fall only). Quarter turns are exact
    on the pixel grid, so the cat stays crisp; 45 degree steps smeared the eyes and were dropped."""
    base = midair_front(11)
    return [rotate(base, a) for a in (0, 90, 180, 270)]


def peek_side(show, look=(0, 0), paw=False):
    """Pokes out from behind a vertical edge on the left (the frame's left side is the edge)."""
    g = blank()
    left = show - 22
    head(g, 17, left, 'open', look, whisk='right')
    if paw:
        stamp(g, [".####", "#####", "#####", ".####"], 31, 0)
    return g


def flip_v(g):
    return [row[:] for row in g[::-1]]


def talk(stage):
    """3/4 head turn for the speech bubble: the face slides toward the viewer's right, the far eye narrows."""
    global NOFACE
    NOFACE = True
    g = sit()
    NOFACE = False
    top = (H - len(sit_body())) - 19
    L = SX + 2
    for i, line in enumerate(HEAD):
        for j, ch in enumerate(line):
            if ch == '#':
                put(g, top + i, SX + j)
                put(g, top + i, L + j)
    for r, n in WHISKERS.items():
        for k in range(1, n + 1):
            put(g, top + r, L + 21 + k)
    mode = 'blink' if stage == 2 else 'open'
    lk = (1, 0) if stage == 3 else (0, 0)
    eye(g, top + 7, L + 4, mode, lk)
    if mode == 'open':
        for i, line in enumerate(PROFILE_RING):
            for j, ch in enumerate(line):
                if ch == '#':
                    put(g, top + 7 + i, L + 14 + j, 'Y')
        for i, line in enumerate(disc(4, 6)):
            for j, ch in enumerate(line):
                if ch == '#':
                    put(g, top + 8 + i, L + 15 + j, 'p')
    else:
        stamp(g, [".YYYY."], top + 12, L + 14)
    wear(g, '34', top, L)
    return g


SHADOW = [".........##########################.........",
          ".....##################################.....",
          "...######################################...",
          ".....##################################....."]


def shadow():
    g = blank()
    stamp(g, [l.replace('#', 's') for l in SHADOW], 44, 2)
    return g


def top_light(g):
    """2.5D: a 1 px lighter rim ('l') on every upward-facing body edge, where light from above would land."""
    out = [row[:] for row in g]
    for r in range(1, H - 1):
        for c in range(W):
            if g[r][c] == '#' and g[r - 1][c] in '.zh' and g[r + 1][c] == '#':
                out[r][c] = 'l'
    return out


def pounce(stage):
    """Pounce at a target on the right: anticipation (crouch, wiggle), coil, leap (body stretched, front legs
    reaching forward, back legs trailing, all off the ground), front paws land first, absorb, stand."""
    if stage <= 3:
        return stalk(2, wiggle={1: 0, 2: 1, 3: -1}[stage])
    if stage == 4:                                   # coil: rump drops back, hind legs loaded
        return stalk(2, wiggle=-1)
    if stage == 5:                                   # take-off: back legs push, front legs lift
        return side({'near_front': (5, 3), 'far_front': (4, 4), 'near_hind': (-4, 0), 'far_hind': (-3, 1)},
                    dy=-3, look=(1, 0))
    if stage == 6:                                   # in the air: stretched out, four legs off the ground
        return side({'near_front': (6, 5), 'far_front': (5, 6), 'near_hind': (-6, 5), 'far_hind': (-5, 6)},
                    dy=-7, look=(1, 0))
    if stage == 7:                                   # front paws touch down first
        return side({'near_front': (3, 0), 'far_front': (2, 1), 'near_hind': (-5, 4), 'far_hind': (-4, 5)},
                    dy=-2, look=(1, 1))
    if stage == 8:                                   # absorb the landing
        return stalk(1, look=(1, 1))
    return side(STAND, look=(1, 1))


def sphinx(paw=0, mode='open', look=(1, 0)):
    """Lying like the Egyptian sphinx: haunches folded, chest up, forelegs flat forward, head up.
    paw > 0 lifts the near front paw that many px (the tap)."""
    g = blank()
    for r, c0, c1 in [(44, 25, 41), (45, 25, 42), (46, 25, 42)]:   # far foreleg, behind
        span(g, r, c0, c1, 'f')
    for r, c0, c1 in [(30, 6, 12), (31, 4, 15), (32, 3, 18)] + [(r, 2, 20) for r in range(33, 36)] + \
                      [(r, 2, 34) for r in range(36, 46)] + [(46, 3, 34), (47, 4, 33)]:
        span(g, r, c0, c1)                                         # folded haunch and low body
    stamp(g, SIT_TAIL, 21, 0, flip=True)                            # tail up behind, a plump '?'
    for r, c0, c1 in [(32, 1, 5), (33, 1, 4)]:
        span(g, r, c0, c1)
    for r, c0, c1 in [(45 - paw, 28, 45), (46 - paw, 28, 46), (47 - paw, 29, 46)]:   # near foreleg forward
        span(g, r, c0, c1)
    if paw:
        for r in range(45 - paw, 45):
            span(g, r, 28, 31)                                     # leg stays joined while the paw lifts
    head(g, 19, 20, mode, look, whisk='right')
    return g


def ground_shadow(g):
    """Soft pixel shadow on the bottom two rows, behind the cat, sized to the cat and smaller when it is
    off the ground. Drawn into every grounded frame, so it always follows the feet."""
    cols = [c for c in range(W) for r in range(H) if g[r][c] not in '.s']
    rows = [r for r in range(H) for c in range(W) if g[r][c] not in '.s']
    if not cols:
        return g
    lift = 47 - max(rows)
    c0, c1 = min(cols) + 2 + lift, max(cols) - 2 - lift
    if c1 - c0 < 6:
        return g
    out = [row[:] for row in g]
    for r, inset in ((46, 3), (47, 0)):
        for c in range(c0 + inset, c1 - inset + 1):
            if out[r][c] == '.':
                out[r][c] = 's'
    return out


NO_SHADOW = {'Fall', 'Tumble', 'Peek', 'PeekSide', 'PeekTop'}


def build():
    """Every state's frames, drawn with whatever ACC currently asks for."""
    FRAMES = {
        # blink = open, closed, nearly open, open (research.md section 4)
        'Sit':     [sit(), sit(lift=1), sit(mode='blink'), sit(mode='half')],
        'Idle':    [side(STAND), side(STAND, breathe=1), side(STAND, look=(1, 0), tail=TAIL_SWAY),
                    side(STAND, mode='blink'), side(STAND, mode='half')],
        # shoulders up (head -1) while the hips drop (tail +1) on the frames where the front legs pass
        # body rises 1 px on the passing frames (legs under the body), drops on the contact frames
        'Walk':    [side(walk_feet(p), dy=(-1 if p % 2 else 0), tail=(TAIL_SWAY if p >= 2 else TAIL_UP)) for p in range(4)],
        # look around in the standing pose, as in her reference: left, right, up, down, up-left, down-right
        'Look':    [side(STAND, look=lk) for lk in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1)]],
        'Inspect': [inspect(i) for i in range(1, 9)],
        'Yawn':    [yawn(1), yawn(2), yawn(3), yawn(4), yawn(5)],
        'Sleep':   [sleep(1), sleep(2), sleep(3), sleep(4)],
        # ears, a quick rise that overshoots 2 px, a 1 px dip, rest, then slow looks each way
        'Peek':    [peek(4), peek(10), peek(21, paws=True), peek(18, paws=True), peek(19, paws=True),
                    peek(19, look=(-1, 0), paws=True), peek(19, look=(1, 0), paws=True)],
        'React':   [react(i) for i in range(1, 6)],
        'Fall':    fall_frames(),
        'Land':    [land(i) for i in range(1, 8)],
        'Run':     [run(i) for i in range(1, 5)],
        'Tumble':  tumble_frames(),
        'PeekSide': [peek_side(5), peek_side(11), peek_side(19), peek_side(17),
                     peek_side(17, look=(1, 0)), peek_side(17, look=(0, -1))],
        'PeekTop': [flip_v(g) for g in [peek(4), peek(10), peek(21, paws=True), peek(18, paws=True), peek(19, paws=True),
                                        peek(19, look=(-1, 0), paws=True), peek(19, look=(1, 0), paws=True)]],
        'Talk':    [talk(1), talk(2), talk(3)],
        'Pounce':  [pounce(i) for i in range(1, 10)],
        # sphinx: tap the target three times, then rest; loops
        'Sphinx':  [sphinx(), sphinx(mode='blink'), sphinx(look=(1, 1))],     # resting loop
        'SphinxTap': [sphinx(paw=3), sphinx(paw=0)],                         # one tap; play 2 or 3 times
    }
    FRAMES = {k: [top_light(g if k in NO_SHADOW else ground_shadow(g)) for g in v] for k, v in FRAMES.items()}
    FRAMES['Shadow'] = [shadow()]
    return FRAMES


FRAMES = build()

# seconds each frame holds before the next (After-delay in Figma); see research.md section 9
TIMINGS = {
    'Sit':     [1.2, 1.4, 0.15, 0.08],
    'Idle':    [1.0, 0.9, 1.2, 0.15, 0.08],
    'Walk':    [0.14, 0.14, 0.14, 0.14],
    'Look':    [0.6] * 6,
    'Inspect': [0.8, 0.12, 0.6, 0.12, 0.12, 0.12, 0.12, 0.15],
    'Yawn':    [1.2, 0.25, 0.9, 0.25, 0.5],
    'Sleep':   [0.7, 0.7, 0.7, 0.7],
    'Peek':    [1.0, 0.06, 0.08, 0.08, 0.5, 1.0, 1.0],
    'React':   [0.08, 0.1, 0.3, 0.08, 0.15],
    'Fall':    [0.09] * 8,
    'Land':    [0.08, 0.14, 0.5, 0.4, 0.16, 0.12, 0.6],
    'Run':     [0.07, 0.07, 0.07, 0.07],
    'Tumble':  [0.08] * 4,
    'PeekSide': [0.8, 0.06, 0.08, 0.1, 0.9, 0.9],
    'PeekTop': [1.0, 0.06, 0.08, 0.08, 0.5, 1.0, 1.0],
    'Talk':    [0.5, 0.12, 0.6],
    'Pounce':  [0.5, 0.12, 0.12, 0.25, 0.07, 0.14, 0.08, 0.2, 0.4],
    'Sphinx':  [2.0, 0.15, 1.2],
    'SphinxTap': [0.12, 0.12],
    'Shadow':  [1.0],
}
