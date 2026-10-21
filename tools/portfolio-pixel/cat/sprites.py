"""Pixel cat sprite source, v2 (17 Oct): style from Sejal's reference cat.
Big front-facing head, round O eyes with a black fill, short whiskers, upright tail, longer legs.
32x32 frames, palette-indexed.
Legend: '.' empty, '#' body, 'Y' eye ring, 'p' pupil (black fill), 'w' eye shine, 'm' mouth, 'M' mouth inner, 'z' Z, 'h' heart
Edit the builders below; run render.py to preview and export.
"""
W = H = 32

def blank():
    return [['.'] * W for _ in range(H)]

def put(g, r, c, ch='#'):
    if 0 <= r < H and 0 <= c < W:
        g[r][c] = ch

def fill(g, r, c0, c1, ch='#'):
    for c in range(c0, c1 + 1):
        put(g, r, c, ch)

def rows(g, spans, dy=0, dx=0, ch='#'):
    for r, c0, c1 in spans:
        fill(g, r + dy, c0 + dx, c1 + dx, ch)

# ---------- round eyes (6x6) ----------
MASK = [".####.", "######", "######", "######", "######", ".####."]

def eye(g, top, left, look=(0, 0), mode='open'):
    """look=(dx,dy) in {-1,0,1}. modes: open, wide, half, closed, happy, sleep"""
    dx, dy = look
    if mode in ('open', 'wide'):
        for i in range(6):
            for j in range(6):
                if MASK[i][j] == '#':
                    put(g, top + i, left + j, 'Y')
        if mode == 'open':
            # black fill; looking shrinks it to 3px toward the look side so the ring never breaks
            r0, r1 = {-1: (1, 3), 0: (1, 4), 1: (2, 4)}[dy]
            c0, c1 = {-1: (1, 3), 0: (1, 4), 1: (2, 4)}[dx]
        else:
            r0, r1 = 2 + dy, 3 + dy
            c0, c1 = 2 + dx, 3 + dx
        for i in range(r0, r1 + 1):
            for j in range(c0, c1 + 1):
                put(g, top + i, left + j, 'p')
        if mode == 'open':
            put(g, top + r0, left + c0, 'w')  # shine, top-left of the pupil
    elif mode == 'half':
        fill(g, top + 3, left, left + 5, 'Y')
        put(g, top + 4, left, 'Y'); put(g, top + 4, left + 5, 'Y'); fill(g, top + 4, left + 1 + max(dx, 0), left + 4 + min(dx, 0), 'p')
        fill(g, top + 5, left + 1, left + 4, 'Y')
    elif mode in ('squeeze-l', 'squeeze-r'):   # > and <, used for the big yawn
        pts = [(2, 1), (2, 2), (3, 3), (3, 4), (4, 1), (4, 2)]
        for r, c in pts:
            put(g, top + r, left + (c if mode == 'squeeze-l' else 5 - c), 'Y')
    elif mode == 'closed':
        fill(g, top + 3, left, left + 5, 'Y')
    elif mode == 'happy':   # ∩
        fill(g, top + 2, left + 1, left + 4, 'Y'); put(g, top + 3, left, 'Y'); put(g, top + 3, left + 5, 'Y')
    elif mode == 'sleep':   # ∪
        put(g, top + 3, left, 'Y'); put(g, top + 3, left + 5, 'Y'); fill(g, top + 4, left + 1, left + 4, 'Y')

# ---------- front-facing head (16 wide, 14 tall) ----------
HEAD = [(0, 0, 0), (0, 15, 15), (1, 0, 1), (1, 14, 15), (2, 0, 2), (2, 13, 15)] + \
       [(r, 0, 15) for r in range(3, 13)] + [(13, 1, 14)]

def head(g, top, left, look=(0, 0), mode='open', whiskers=True, chin=0):
    rows(g, HEAD, dy=top, dx=left)
    for k in range(chin):
        fill(g, top + 14 + k, left + 2 + k, left + 13 - k)
    if mode == 'squeeze':
        eye(g, top + 5, left + 1, look, 'squeeze-l'); eye(g, top + 5, left + 9, look, 'squeeze-r')
    else:
        eye(g, top + 5, left + 1, look, mode); eye(g, top + 5, left + 9, look, mode)
    if whiskers:
        for r in (top + 9, top + 11):
            fill(g, r, left - 3, left - 1); fill(g, r, left + 16, left + 18)

# ---------- sitting (front) ----------
def sit(look=(0, 0), mode='open', dy=0, head_dy=0, wide=0, tail=True, mouth=None, chin=0):
    g = blank()
    hx, hy = 8, 4 + head_dy + dy
    # body
    body = [(17, 10, 21), (18, 9, 22)] + [(r, 8 - (wide if 19 <= r <= 27 else 0), 23 + (wide if 19 <= r <= 27 else 0)) for r in range(19, 29)]
    rows(g, body, dy=dy)
    fill(g, 29 + dy, 9, 13); fill(g, 29 + dy, 18, 22)   # front paws
    if tail:  # upright tail beside the body, below the whiskers
        rows(g, [(18, 26, 26), (19, 25, 27)] + [(r, 25, 26) for r in range(20, 27)] + [(26, 24, 26), (27, 24, 25)], dy=dy)
    head(g, hy, hx, look, mode, chin=chin)
    if mouth:
        for r, c0, c1, ch in mouth:
            fill(g, hy + r, hx + c0, hx + c1, ch)
    return g

# ---------- standing / walking (side body, front head) ----------
def side(legs, look=(1, 0), dy=0, tail_dx=0, mode='open', breathe=0):
    """legs: list of (top_col, bottom_col, bottom_row); each leg is 2px wide and starts at row 23."""
    g = blank()
    # upright tail at the back (left), 3px wide with a rounded tip
    tail = [(6, 4 + tail_dx, 4 + tail_dx), (7, 3 + tail_dx, 5 + tail_dx), (8, 3 + tail_dx, 5 + tail_dx), (9, 3 + tail_dx, 5 + tail_dx),
            (10, 3, 5), (11, 3, 5), (12, 3, 5), (13, 3, 5), (14, 3, 5), (15, 3, 6)]
    rows(g, tail, dy=dy)
    body = [(16, 4, 18), (17, 3, 19), (18, 3, 19), (19, 3, 19), (20, 3, 19), (21, 3, 19), (22, 4, 18)]
    if breathe:
        body = [(15, 7, 14)] + body
    rows(g, body, dy=dy)
    for top_c, bot_c, bottom in legs:
        n = bottom - 23
        for i, r in enumerate(range(23, bottom + 1)):
            c = round(top_c + (bot_c - top_c) * (i / n if n else 0))
            fill(g, r + dy, c, c + 1)
    head(g, 4 + dy, 13, look, mode)
    return g

IDLE_LEGS = [(4, 4, 29), (8, 8, 29), (14, 14, 29), (18, 18, 29)]
WALK = [
    [(4, 2, 29), (8, 9, 28), (14, 13, 28), (18, 20, 29)],   # contact, far paws lifted
    [(5, 5, 28), (7, 7, 29), (15, 15, 29), (17, 17, 28)],   # passing, body up
    [(4, 5, 28), (8, 7, 29), (14, 15, 29), (18, 17, 28)],   # contact, other pair
    [(5, 5, 29), (7, 7, 28), (15, 15, 28), (17, 17, 29)],   # passing, body up
]

# ---------- yawn ----------
def yawn(stage):
    if stage == 1:
        return sit(mode='half')
    if stage in (2, 4):
        return sit(mode='closed', mouth=[(11, 7, 8, 'm'), (12, 7, 8, 'm')])
    # wide yawn: head stretches 1px up, chin drops, small round mouth below the eyes
    return sit(mode='squeeze', head_dy=-1, chin=2,
               mouth=[(11, 6, 9, 'm'), (12, 5, 10, 'm'), (13, 5, 10, 'm'), (14, 6, 9, 'm'), (12, 6, 9, 'M'), (13, 6, 9, 'M')])

# ---------- react ----------
def react(stage):
    if stage == 1:   # squash
        return sit(mode='happy', head_dy=2, wide=1)
    if stage == 2:   # hop, eyes wide, one heart
        g = blank()
        body = [(14, 10, 21), (15, 9, 22)] + [(r, 9, 22) for r in range(16, 25)] + [(25, 10, 21)]
        rows(g, body)
        fill(g, 26, 10, 12); fill(g, 27, 10, 11); fill(g, 26, 19, 21); fill(g, 27, 20, 21)   # dangling paws
        rows(g, [(14, 26, 26), (15, 25, 27)] + [(r, 25, 26) for r in range(16, 23)] + [(22, 23, 26), (23, 23, 24)])
        head(g, 1, 8, mode='wide')
        for r, c in [(0, 26), (0, 28), (1, 25), (1, 26), (1, 27), (1, 28), (1, 29), (2, 26), (2, 27), (2, 28), (3, 27)]:
            put(g, r, c, 'h')
        return g
    return sit(wide=1, head_dy=1)   # land

# ---------- peek ----------
def peek(visible, look=(0, 0)):
    g = blank()
    top = H - visible
    head(g, top, 8, look)
    rows(g, [(r, 9, 22) for r in range(top + 14, H)])
    return g

# ---------- sleep (loaf) ----------
def sleep(stage):
    g = blank()
    body = [(18, 7, 18), (19, 5, 20)] + [(r, 4, 21) for r in range(20, 29)] + [(29, 5, 20)]
    if stage == 2:
        body = [(17, 9, 16)] + body
    rows(g, body)
    rows(g, [(29, 2, 6), (28, 1, 3), (27, 1, 2), (26, 2, 3)])   # tail wrapped round the front
    head(g, 16, 13, mode='sleep', whiskers=False)
    for r in (25, 27):
        fill(g, r, 29, 31)   # whiskers on the open side only
    Z5 = ["#####", "...#.", "..#..", ".#...", "#####"]
    Z6 = ["######", "....#.", "...#..", "..#...", ".#....", "######"]
    glyph, (r0, c0) = (Z5, (9, 26)) if stage == 1 else (Z6, (2, 25))
    for i, line in enumerate(glyph):
        for j, ch in enumerate(line):
            if ch == '#':
                put(g, r0 + i, c0 + j, 'z')
    return g

FRAMES = {
    'Idle':    [side(IDLE_LEGS, look=(0, 0)), side(IDLE_LEGS, look=(0, 0), breathe=1), side(IDLE_LEGS, look=(1, 0)), side(IDLE_LEGS, mode='closed')],
    'Walk':    [side(WALK[0]), side(WALK[1], dy=-1, tail_dx=1), side(WALK[2]), side(WALK[3], dy=-1, tail_dx=1)],
    'Look':    [sit(look=(-1, 0)), sit(look=(1, 0)), sit(look=(0, -1)), sit(look=(0, 1)), sit(look=(-1, -1)), sit(look=(1, 1))],
    'Yawn':    [yawn(1), yawn(2), yawn(3), yawn(4)],
    'Sit':     [sit(), sit(head_dy=1, wide=1), sit(mode='closed')],
    'Sleep':   [sleep(1), sleep(2)],
    'React':   [react(1), react(2), react(3)],
    'Peek':    [peek(3), peek(7), peek(11), peek(17, look=(-1, 0)), peek(17, look=(1, 0))],
    'Inspect': [sit(look=(1, 0)), sit(look=(1, 1)), sit(look=(1, 0), mode='half'), sit(look=(1, 0))],
}
