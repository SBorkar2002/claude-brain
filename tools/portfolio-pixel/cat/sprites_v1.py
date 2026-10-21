"""Pixel cat sprite source. 32x32 frames, palette-indexed.
Legend: '.' empty, '#' body, 'Y' eye, 'p' pupil, 'w' eye shine, 'm' mouth (pink), 'M' mouth inner, 'z' sleep Z, 'h' heart
Edit the builders below; run render.py to preview and export.
"""
W = H = 32

def blank():
    return [['.'] * W for _ in range(H)]

def fill(g, r, c0, c1, ch='#'):
    if 0 <= r < H:
        for c in range(max(0, c0), min(W - 1, c1) + 1):
            g[r][c] = ch

def rows(g, spans, dy=0, dx=0, ch='#'):
    for r, c0, c1 in spans:
        fill(g, r + dy, c0 + dx, c1 + dx, ch)

# ---------- eyes ----------
EYE_OPEN = [".YYY.", "YYYYY", "YYYYY", "YYYYY", "YYYYY", ".YYY."]

def eye(g, top, left, look=(0, 0), mode='open'):
    """look=(dx,dy) in {-1,0,1}. mode: open, half, closed, happy, sleep, wide"""
    if mode == 'open' or mode == 'wide':
        for i, line in enumerate(EYE_OPEN):
            for j, ch in enumerate(line):
                if ch != '.':
                    g[top + i][left + j] = 'Y'
        dx, dy = look
        if mode == 'wide':
            # small round pupil, eyes wide
            pr, pc = top + 2 + dy, left + 2 + dx
            g[pr][pc] = 'p'; g[pr + 1][pc] = 'p'
        else:
            pc = left + 2 + dx
            for r in range(top + 1 + dy, top + 5 + dy):
                if 0 <= r - top < 6 and EYE_OPEN[r - top][pc - left] != '.':
                    g[r][pc] = 'p'
            # shine: top-left of pupil
            sr, sc = top + 1, left + 1 if dx >= 0 else left + 3
            if g[sr][sc] == 'Y':
                g[sr][sc] = 'w'
    elif mode == 'half':
        for i, line in enumerate([".....", ".....", "YYYYY", "YYYYY", ".YYY.", "....."]):
            for j, ch in enumerate(line):
                if ch != '.': g[top + i][left + j] = 'Y'
        g[top + 2 + 0][left + 2 + look[0]] = 'p'; g[top + 3][left + 2 + look[0]] = 'p'
    elif mode == 'closed':
        fill(g, top + 3, left, left + 4, 'Y')
    elif mode == 'happy':  # ^ ^ arcs
        for (r, c) in [(2, 1), (2, 2), (2, 3), (3, 0), (3, 4)]:
            g[top + r][left + c] = 'Y'
    elif mode == 'sleep':
        fill(g, top + 4, left + 1, left + 3, 'Y')
        g[top + 3][left] = 'Y'; g[top + 3][left + 4] = 'Y'

def eyes(g, top, l1, l2, look=(0, 0), mode='open'):
    eye(g, top, l1, look, mode)
    eye(g, top, l2, look, mode)

# ---------- front sitting cat (Sit, Look, Yawn, React, Inspect, Peek) ----------
HEAD = [  # (row, c0, c1)
    (3, 9, 9), (3, 22, 22),
    (4, 9, 10), (4, 21, 22),
    (5, 9, 11), (5, 20, 22),
    (6, 9, 22),
    (7, 8, 23), (8, 8, 23), (9, 8, 23), (10, 8, 23), (11, 8, 23), (12, 8, 23), (13, 8, 23), (14, 8, 23),
    (15, 9, 22), (16, 10, 21),
]
BODY_SIT = [
    (17, 9, 22), (18, 8, 23), (19, 7, 24), (20, 7, 24), (21, 7, 24), (22, 7, 24), (23, 7, 24),
    (24, 7, 24), (25, 7, 24), (26, 7, 24), (27, 7, 24), (28, 8, 23),
    (29, 9, 13), (29, 18, 22),  # front paws
    (29, 14, 17),
]
TAIL_SIT = [(23, 27, 28), (24, 28, 29), (25, 28, 29), (26, 28, 29), (27, 27, 29), (28, 25, 28), (29, 23, 26)]

def sit(look=(0, 0), mode='open', head_dy=0, body_wide=0, dy=0):
    g = blank()
    rows(g, HEAD, dy=head_dy + dy)
    body = [(r, c0 - (body_wide if 19 <= r <= 27 else 0), c1 + (body_wide if 19 <= r <= 27 else 0)) for r, c0, c1 in BODY_SIT]
    rows(g, body, dy=dy)
    rows(g, TAIL_SIT, dy=dy)
    eyes(g, 8 + head_dy + dy, 10, 17, look, mode)
    return g

def yawn(stage):
    # stage 1 squint, 2 mouth small, 3 mouth wide + stretch, 4 closing
    if stage == 1:
        return sit(mode='half')
    head_dy = -1 if stage == 3 else 0
    g = sit(mode='happy', head_dy=head_dy)
    top = 8 + head_dy
    if stage in (2, 4):
        for r, c0, c1 in [(top + 5, 14, 17), (top + 6, 14, 17)]:
            fill(g, r, c0, c1, 'm')
    if stage == 3:
        fill(g, top + 9, 9, 22, '#'); fill(g, top + 10, 10, 21, '#'); fill(g, top + 11, 11, 20, '#')
        for r, c0, c1 in [(top + 5, 14, 17), (top + 6, 13, 18), (top + 7, 13, 18), (top + 8, 13, 18), (top + 9, 14, 17)]:
            fill(g, r, c0, c1, 'm')
        fill(g, top + 6, 14, 17, 'M'); fill(g, top + 7, 14, 17, 'M')
    return g

def react(stage):
    if stage == 1:   # squash
        g = blank()
        rows(g, HEAD, dy=2); rows(g, [(r, c0 - 1, c1 + 1) for r, c0, c1 in BODY_SIT if r >= 19], dy=0)
        rows(g, [(r, c0, c1) for r, c0, c1 in BODY_SIT if r < 19], dy=1)
        rows(g, TAIL_SIT)
        eyes(g, 10, 10, 17, mode='happy'); return g
    if stage == 2:   # airborne, stretched, eyes wide
        g = blank()
        rows(g, HEAD, dy=-2)
        rows(g, [(r, c0 + 1, c1 - 1) for r, c0, c1 in BODY_SIT if r <= 28], dy=-2)
        fill(g, 27, 10, 12); fill(g, 27, 19, 21)  # dangling paws
        rows(g, [(r, c0, c1) for r, c0, c1 in TAIL_SIT], dy=-4)
        eyes(g, 6, 10, 17, mode='wide')
        for (r, c) in [(0, 26), (0, 28), (1, 25), (1, 26), (1, 27), (1, 28), (1, 29), (2, 26), (2, 27), (2, 28), (3, 27)]:
            g[r][c] = 'h'
        return g
    return sit(mode='open', look=(0, 0), body_wide=1, head_dy=1)  # land

def peek(rows_visible, look=(0, 0)):
    """Head rising from behind a ledge at the bottom of the frame."""
    g = blank()
    shift = (H - rows_visible) - 3  # HEAD starts at row 3
    rows(g, HEAD, dy=shift)
    rows(g, [(r, 8, 23) for r in range(17, 40)], dy=shift)  # neck/body continues below the ledge
    top = 8 + shift
    if top + 6 <= H:
        eyes(g, top, 10, 17, look)
    elif top + 3 < H:
        # half the eyes above the ledge
        for l in (10, 17):
            for i, line in enumerate(EYE_OPEN):
                r = top + i
                if 0 <= r < H:
                    for j, ch in enumerate(line):
                        if ch != '.': g[r][l + j] = 'Y'
            for r in range(top + 1, min(H, top + 5)):
                g[r][l + 2 + look[0]] = 'p'
    return g

# ---------- side body (Idle standing, Walk) ----------
def side(legs, look=(1, 0), body_dy=0, tail_tip=0, mode='open', breathe=0, head_dx=-1):
    """legs: list of (c0, bottom_row) for 4 legs, each 2 wide, top at row 23.
    The head is front-facing and symmetric: 2px margin, 5px eye, 2px gap, 5px eye, 2px margin (same as the sitting head)."""
    g = blank()
    DX = -2
    # tail rising from the back (left)
    tail = [(6, 3, 4), (7, 2, 3), (8, 2, 3), (9, 2, 3), (10, 2, 3), (11, 2, 3), (12, 2, 4), (13, 3, 4), (14, 3, 5), (15, 4, 6)]
    if tail_tip:
        tail = [(6, 4, 5), (7, 3, 4)] + tail[2:]
    rows(g, tail, dy=body_dy, dx=DX + 2)
    # body
    body = [(15, 6, 21), (16, 5, 22), (17, 4, 22), (18, 4, 22), (19, 4, 22), (20, 4, 22), (21, 4, 22), (22, 5, 22), (23, 6, 21)]
    if breathe:
        body = [(r, c0, c1) for r, c0, c1 in body] + [(14, 8, 18)]
    rows(g, body, dy=body_dy, dx=DX)
    # head, front facing, on the right
    head = [(5, 17, 17), (5, 30, 30), (6, 17, 18), (6, 29, 30), (7, 17, 19), (7, 28, 30), (8, 17, 30),
            (9, 16, 31), (10, 16, 31), (11, 16, 31), (12, 16, 31), (13, 16, 31), (14, 16, 31), (15, 16, 31), (16, 17, 30), (17, 18, 29)]
    rows(g, head, dy=body_dy, dx=DX + head_dx)
    eyes(g, 10 + body_dy, 18 + DX + head_dx, 25 + DX + head_dx, look, mode)
    for c0, bottom in legs:
        for r in range(23 + body_dy, bottom + 1):
            fill(g, r, c0 + DX, c0 + DX + 1)
    return g

IDLE_LEGS = [(6, 28), (9, 28), (17, 28), (20, 28)]
WALK = [
    [(4, 28), (10, 27), (16, 28), (21, 27)],   # contact, far paws lifted
    [(7, 27), (9, 28), (18, 28), (20, 27)],    # passing
    [(5, 27), (11, 28), (17, 27), (22, 28)],   # contact, other pair
    [(8, 28), (10, 27), (19, 27), (21, 28)],   # passing
]

# ---------- sleep (loaf) ----------
def sleep(stage):
    g = blank()
    up = 0 if stage == 1 else 1
    body = [(17, 8, 20), (18, 6, 22), (19, 5, 23), (20, 4, 24), (21, 4, 24), (22, 4, 24), (23, 4, 24), (24, 4, 24), (25, 4, 24), (26, 4, 24), (27, 5, 24), (28, 6, 25)]
    rows(g, body)
    if up:
        fill(g, 16, 10, 18)
    head = [(15, 17, 17), (15, 29, 29), (16, 17, 18), (16, 28, 29), (17, 17, 29), (18, 16, 30), (19, 16, 30), (20, 16, 30), (21, 16, 30), (22, 16, 30), (23, 16, 30), (24, 16, 30), (25, 17, 29), (26, 18, 28)]
    rows(g, head, dy=2)
    eyes(g, 19, 17, 24, mode='sleep')
    rows(g, [(28, 2, 6), (27, 1, 3), (26, 1, 2), (25, 2, 3)])  # tail wrapped
    # one Z at a time, small then large
    Z4 = ["####", "..#.", ".#..", "####"]
    Z5 = ["#####", "...#.", "..#..", ".#...", "#####"]
    glyph, (r0, c0) = (Z4, (10, 25)) if stage == 1 else (Z5, (3, 26))
    for i, line in enumerate(glyph):
        for j, ch in enumerate(line):
            if ch == '#':
                g[r0 + i][c0 + j] = 'z'
    return g

FRAMES = {
    'Idle':    [side(IDLE_LEGS, look=(0, 0)), side(IDLE_LEGS, look=(0, 0), breathe=1), side(IDLE_LEGS, look=(1, 0)), side(IDLE_LEGS, mode='closed')],
    'Walk':    [side(WALK[0], body_dy=0, tail_tip=0), side(WALK[1], body_dy=-1, tail_tip=1), side(WALK[2], body_dy=0, tail_tip=0), side(WALK[3], body_dy=-1, tail_tip=1)],
    'Look':    [sit(look=(-1, 0)), sit(look=(1, 0)), sit(look=(0, -1)), sit(look=(0, 1)), sit(look=(-1, -1)), sit(look=(1, 1))],
    'Yawn':    [yawn(1), yawn(2), yawn(3), yawn(4)],
    'Sit':     [sit(), sit(head_dy=1, body_wide=1), sit(mode='closed')],
    'Sleep':   [sleep(1), sleep(2)],
    'React':   [react(1), react(2), react(3)],
    'Peek':    [peek(3), peek(7), peek(11), peek(16, look=(-1, 0)), peek(16, look=(1, 0))],
    'Inspect': [sit(look=(1, 0)), sit(look=(1, 1)), sit(look=(1, 1), mode='half'), sit(look=(1, 0))],
}
