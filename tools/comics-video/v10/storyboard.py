#!/usr/bin/env python3
"""Export the episode as two storyboard frame sets, for the Drive archive.

  out/sb_nocap/f01.png ...   the clean Figma plates, exactly as exported
  out/sb_cap/f01_cap.png ... the same plates with the FULL caption laid in

The video reveals captions one word at a time, so no single video frame ever
shows a whole caption -- a still pulled from the render would show one word.
These are rebuilt instead: same font, same box, same wrap, same 38px line
boxes as Figma, but every word visible at once, which is what a storyboard
frame is for.

Two captions deliberately DON'T match the Figma node they came from, because
two meta rules override it: frame 18 inherits frame 17's box (caption
continuity on a shared shot) and frame 46 inherits frame 1's (loop caption
position). The shipped cut is the record, not the Figma file.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spec, captions

BASE   = os.path.dirname(os.path.abspath(__file__))
NOCAP  = os.path.join(BASE, "out", "sb_nocap")
CAP    = os.path.join(BASE, "out", "sb_cap")
DY     = captions.DY
N      = 46


# ---------- FIGMA ORIGINALS ----------
# Two captions were deliberately MOVED off their Figma node in the cut, because
# two meta rules beat the Figma file: frame 18 inherits frame 17's box (caption
# continuity on a shared shot) and frame 46 inherits frame 1's (loop caption
# position). Both target boxes are sized for ONE WORD at a time, which is all
# the video ever shows -- far too narrow to hold the whole line. A storyboard
# frame does show the whole line, so it uses the original Figma node here.
FIGMA_ORIG = {
    18: (79, 103, 159, 152),      # x, y, box_w, box_h
    46: (22, 265, 176, 114),
}

# Figma node widths are fractional; spec.py stores them as ints, so a line that
# fits in Figma can miss by a pixel here and wrap. H is the reliable record of
# how many lines Figma laid out, so grow the box by up to a few px until the
# wrap agrees with it.
SLACK = 8


def fit_width(text, bw, want_lines, fnt):
    for extra in range(SLACK + 1):
        if len(captions.wrap(text, bw + extra, fnt)) == want_lines:
            return bw + extra
    return bw


def draw_full(frame):
    """The plate for `frame` with its whole caption drawn in Figma's layout."""
    plate = Image.open(os.path.join(spec.PLATES, f"p{frame:02d}.png")).convert("RGB")
    if frame not in spec.C:
        return plate, 0, 0
    text, x, y, bw, align, hexc, ital, *_ = spec.C[frame]
    box_h = spec.H[frame]
    if frame in FIGMA_ORIG:
        x, y, bw, box_h = FIGMA_ORIG[frame]

    fnt   = captions.font(spec.SIZE)
    want  = box_h // spec.LINE_H
    bw    = fit_width(text, bw, want, fnt)
    lines = captions.wrap(text, bw, fnt)
    col   = tuple(int(hexc[i:i+2], 16) for i in (0, 2, 4))

    lay = Image.new("RGBA", plate.size, (0, 0, 0, 0))
    d   = ImageDraw.Draw(lay)
    for li, line in enumerate(lines):
        if not line:
            continue
        lw = fnt.getlength(line)
        lx = x + (bw - lw) / 2.0 if align == "C" else x
        cy = y + li * spec.LINE_H + spec.LINE_H / 2.0 + DY
        d.text((lx, cy), line, font=fnt, fill=col + (255,), anchor="lm")
    if ital:
        s = captions.SHEAR
        lay = lay.transform(lay.size, Image.AFFINE,
                            (1, s, -s * (y + box_h / 2.0), 0, 1, 0),
                            resample=Image.BICUBIC)
    plate.paste(lay, (0, 0), lay)
    return plate, len(lines), want


if __name__ == "__main__":
    os.makedirs(NOCAP, exist_ok=True)
    os.makedirs(CAP,   exist_ok=True)
    bad = []
    for fr in range(1, N + 1):
        src = os.path.join(spec.PLATES, f"p{fr:02d}.png")
        Image.open(src).convert("RGB").save(os.path.join(NOCAP, f"f{fr:02d}.png"))
        img, nl, want = draw_full(fr)
        img.save(os.path.join(CAP, f"f{fr:02d}_cap.png"))
        if fr in spec.C and nl != want:
            bad.append((fr, nl, want))
    print(f"wrote {N} clean + {N} captioned")
    if bad:
        print("LINE COUNT MISMATCH (wrapped lines vs Figma box height):")
        for fr, got, want in bad:
            print(f"  f{fr:02d}: wrapped {got} lines, Figma laid out {want}")
    else:
        print("every caption's wrap matches its Figma box height")
