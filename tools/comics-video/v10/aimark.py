#!/usr/bin/env python3
"""Render the AI mark as a standalone transparent asset.

The mark is the AI's one body across the whole series -- centred on every blank
monitor, small in the corner where a screen is busy, and the thing that moves in
any diagram. Geometry here is the same as the SVG in src/LoopV10.tsx, so the
exported asset and the animated one cannot drift.

Six petals + one eye. Not a face (the AIs never have faces) and not a four-point
sparkle (every AI product on the market already uses one). The eye is what lets
it express: it shifts to look, narrows under effort, widens when it lands. The
exported asset is the NEUTRAL pose -- eye centred, nothing narrowed.
"""
import math, os
from PIL import Image, ImageDraw

TEAL = (3, 166, 207)
OUT  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# the SVG's own numbers, in its 100x100 user space
PETAL = dict(cx=50, cy=25, rx=14.5, ry=25)
EYE_R, PUPIL_R = 17.0, 11.0
PAD = 6                       # viewBox is -6 -6 112 112: petals reach past 100


def render(size=1024, color=TEAL, gaze=1.0, squint=0.0, wide=0.0, ss=4):
    """Transparent RGBA render of the mark. gaze=1 is the resting pose.

    ss = supersample factor.
    """
    span = 100 + PAD * 2
    S = size * ss / span                     # user units -> supersampled px
    def P(x, y):                             # user space -> pixel space
        return ((x + PAD) * S, (y + PAD) * S)

    img = Image.new("RGBA", (size * ss, size * ss), (0, 0, 0, 0))

    # six petals, each an ellipse rotated about the centre
    for i in range(6):
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        x0, y0 = P(PETAL["cx"] - PETAL["rx"], PETAL["cy"] - PETAL["ry"])
        x1, y1 = P(PETAL["cx"] + PETAL["rx"], PETAL["cy"] + PETAL["ry"])
        ImageDraw.Draw(lay).ellipse([x0, y0, x1, y1], fill=color + (255,))
        # PIL rotates counter-clockwise, SVG clockwise -- hence the minus
        lay = lay.rotate(-i * 60, resample=Image.BICUBIC, center=P(50, 50))
        img.alpha_composite(lay)

    d = ImageDraw.Draw(img)
    ex = 50 + gaze * 9
    for r, fill in ((EYE_R, (255, 255, 255, 255)), (None, color + (255,))):
        if r is None:
            rx = PUPIL_R * (1 + wide * 0.25)
            ry = rx * (1 - squint * 0.62)
        else:
            rx = ry = r
        x0, y0 = P(ex - rx, 50 - ry)
        x1, y1 = P(ex + rx, 50 + ry)
        d.ellipse([x0, y0, x1, y1], fill=fill)

    return img.resize((size, size), Image.LANCZOS)


def svg(color="#03A6CF", gaze=1.0):
    span = 100 + PAD * 2
    petals = "\n".join(
        f'  <ellipse cx="50" cy="25" rx="14.5" ry="25" fill="{color}" '
        f'transform="rotate({i * 60} 50 50)"/>' for i in range(6))
    ex = 50 + gaze * 9
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-PAD} {-PAD} {span} {span}">\n'
            f'{petals}\n'
            f'  <circle cx="{ex:g}" cy="50" r="{EYE_R}" fill="#ffffff"/>\n'
            f'  <circle cx="{ex:g}" cy="50" r="{PUPIL_R}" fill="{color}"/>\n'
            f'</svg>\n')


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    render(1024).save(os.path.join(OUT, "ai-mark.png"))
    render(256).save(os.path.join(OUT, "ai-mark-256.png"))
    open(os.path.join(OUT, "ai-mark.svg"), "w").write(svg())
    for f in sorted(os.listdir(OUT)):
        print(f"  {f}  {os.path.getsize(os.path.join(OUT, f)) / 1024:.0f}K")
