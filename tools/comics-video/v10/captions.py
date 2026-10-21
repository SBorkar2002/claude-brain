#!/usr/bin/env python3
"""Draw Figma captions back onto the clean plates, one word at a time.

Layout has to match Figma exactly or the words move when they appear, so the
wrap / centring / line height below reproduce Figma's text engine: word-break
wrapping inside the node's box width, 38px line boxes, first line box top at
the node's y. DY is the one empirical number -- the offset from a line box's
top to where PIL's ascender anchor has to sit -- and calibrate() pins it by
diffing against the v9 frames that still had the caption baked in.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spec

BASE = os.path.dirname(os.path.abspath(__file__))
DY = -1                    # set by calibrate()
SCALE = 1.0                # plates are 720x1280; render at 1.5 for a 1080x1920 master
                           # so caption glyphs are drawn at output size, not upscaled
SHEAR = 0.21               # faux oblique: Lato Italic isn't on this machine

_fonts = {}
def font(size=spec.SIZE):
    if size not in _fonts:
        _fonts[size] = ImageFont.truetype(os.path.join(BASE, spec.FONT_R), size)
    return _fonts[size]

def wrap(text, box_w, f):
    """Figma-style wrap: honour explicit newlines, then break on words."""
    lines = []
    for para in text.split("\n"):
        if not para:
            lines.append("")
            continue
        cur = ""
        for w in para.split(" "):
            trial = w if not cur else cur + " " + w
            if f.getlength(trial) <= box_w or not cur:
                cur = trial
            else:
                lines.append(cur); cur = w
        lines.append(cur)
    return lines

def balanced(text, box_w, f, maxw):
    """wrap(), then even the lines out so the last one isn't a lone word.

    Greedy wrapping leaves widows, and a widow is worse here than anywhere else
    because a line is a reveal step: "Okay. Fix every failing test / in this
    file, stop when they / pass." put "pass." alone on screen for 0.23s, which
    is a flash rather than a word. Rebalancing to roughly equal line widths
    fixed 8 of 10 of them and reads better besides -- "Long night. / Left a loop
    running." instead of "Long night. Left a loop / running."

    Explicit newlines are left alone: those are the author's line breaks.
    Falls back to the greedy wrap if rebalancing would change the line count or
    overrun maxw, so it can never push a caption outside the safe area.
    """
    lines = [l for l in wrap(text, box_w, f) if l]
    if "\n" in text or len(lines) < 2 or len(lines[-1].split(" ")) > 1:
        return lines
    n = len(lines)
    words = text.split()
    target = f.getlength(" ".join(words)) / n
    out, cur = [], ""
    for wd in words:
        trial = wd if not cur else cur + " " + wd
        if cur and f.getlength(trial) > target and len(out) < n - 1:
            out.append(cur); cur = wd
        else:
            cur = trial
    out.append(cur)
    if len(out) != n or any(f.getlength(l) > maxw for l in out):
        return lines
    return out


def word_positions(text, box_w, align, x0):
    """(word, x, line_index) for every word, in its final laid-out position."""
    f = font(int(round(spec.SIZE * SCALE)))
    box_w *= SCALE; x0 *= SCALE
    out = []
    for li, line in enumerate(wrap(text, box_w, f)):
        if not line: continue
        lw = f.getlength(line)
        lx = x0 + (box_w - lw) / 2 if align == "C" else x0
        cx = lx
        for w in line.split(" "):
            out.append((w, cx, li))
            cx += f.getlength(w + " ")
    return out

def render(frame, k, plate=None):
    """Plate for `frame` showing ONLY word k of its caption (1-based; 0 = none).

    Every word is drawn at the same point -- the centre of the Figma text box --
    so the caption never spreads sideways along the line. One word, one place.
    """
    if plate is None:
        plate = Image.open(os.path.join(spec.PLATES, f"p{frame:02d}.png")).convert("RGB")
    else:
        plate = plate.copy()
    if SCALE != 1.0:
        plate = plate.resize((int(720*SCALE), int(1280*SCALE)), Image.LANCZOS)
    if frame not in spec.C or k <= 0:
        return plate
    text, x, y, bw, align, hexc, ital, *_ = spec.C[frame]
    wl = text.replace("\n", " ").split()
    if k > len(wl):
        return plate
    word = wl[k-1]
    col = tuple(int(hexc[i:i+2], 16) for i in (0, 2, 4))
    fnt = font(int(round(spec.SIZE * SCALE)))
    cx = (x + bw / 2.0) * SCALE
    cy = (y + spec.H[frame] / 2.0) * SCALE + DY * SCALE
    if not ital:
        ImageDraw.Draw(plate).text((cx, cy), word, font=fnt, fill=col, anchor="mm")
        return plate
    lay = Image.new("RGBA", plate.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((cx, cy), word, font=fnt, fill=col + (255,), anchor="mm")
    lay = lay.transform(lay.size, Image.AFFINE,
                        (1, SHEAR, -SHEAR * cy, 0, 1, 0), resample=Image.BICUBIC)
    plate.paste(lay, (0, 0), lay)
    return plate


def calibrate(frames=(1, 27, 30, 32)):
    """DY is pinned at -1. It was found by diffing against the v9 frames that
    still had the caption baked in; those frames are gone, so this is now a
    constant. Re-derive only if the font or the line height changes."""
    return (-1, 0)


if __name__ == "__main__":
    dy, err = calibrate()
    print(f"DY = {dy}  (residual {err})")

_edges = {}
def busy_mask(frame):
    """Edge density of a plate. Line art and faces are dense with edges; flat
    paper and the flat dark night office are not.

    Darkness is the wrong test -- the night office plate is almost entirely
    dark and a white outlined caption sits on it perfectly. What a caption must
    not cover is BUSY-ness.
    """
    if frame in _edges:
        return _edges[frame]
    import numpy as np
    g = np.array(Image.open(os.path.join(spec.PLATES, f"p{frame:02d}.png"))
                 .convert("L")).astype(int)
    e = (np.abs(np.diff(g, axis=0))[:, :-1]
         + np.abs(np.diff(g, axis=1))[:-1, :]) > 28
    _edges[frame] = e
    return e


def busy_at(frame, l, t, r, b):
    """Fraction of the given box that is busy artwork."""
    m = busy_mask(frame)
    l, t, r, b = (int(round(v)) for v in (l, t, r, b))
    l, t = max(l, 0), max(t, 0)
    r, b = min(r, m.shape[1]), min(b, m.shape[0])
    return float(m[t:b, l:r].mean()) if r > l and b > t else 0.0


def clean_lines(text, frame, box, sub, tol=0.015):
    """Wrap so the caption stays off the artwork, using as few lines as it can.

    The Figma boxes are narrow because they were placed in narrow columns of
    clean paper -- measured, every one sits on 0.0% busy pixels. Letting a short
    sentence run to one wide line therefore put five captions straight across a
    character's face, at 3-6% busy.

    Preference order: fewest lines first, then least movement, and staying off
    the art is the hard requirement. A caption may slide horizontally as far as
    it must to stay inside the safe area -- that is usually a few pixels and
    only matters for the ones anchored near an edge -- but it will never sit on
    the artwork to avoid moving, and it will never gain a line it does not need.

    Returns (lines, sx, sy) -- where the block ends up after clamping.
    """
    x, y, bw, _al = box
    cx, cy = x + bw / 2.0, y + spec.H[frame] / 2.0
    f = font(sub["size"])
    ref = busy_at(frame, x, y, x + bw, y + spec.H[frame])

    def block(w):
        lines = []
        for para in text.split("\n"):
            para = para.strip()
            if not para:
                continue
            if f.getlength(para) <= w:
                lines.append(para)
            else:
                lines += [l for l in balanced(para, w, f, sub["maxw"]) if l]
        return lines

    fallback = None
    for w in (sub["maxw"], 500, 440, 380, 320, 270, 230, max(bw, 110)):
        lines = block(w)
        if not lines:
            continue
        lw = max(f.getlength(l) for l in lines)
        h = len(lines) * sub["line"]
        lo, hi = sub["safe_l"] + lw / 2, sub["safe_r"] - lw / 2
        sx = (sub["safe_l"] + sub["safe_r"]) / 2 if lo > hi else min(max(cx, lo), hi)
        # and the same vertically, against the Shorts chrome. Horizontal-only
        # clamping let a caption land at y=96, under the top overlay.
        tlo, thi = sub["safe_t"] + h / 2, sub["safe_b"] - h / 2
        sy = (sub["safe_t"] + sub["safe_b"]) / 2 if tlo > thi else min(max(cy, tlo), thi)
        got = busy_at(frame, sx - lw / 2, sy - h / 2, sx + lw / 2, sy + h / 2)
        if fallback is None:
            fallback = (lines, sx, sy)
        if got <= ref + tol:
            return lines, sx, sy
    return fallback
