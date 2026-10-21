"""
Key a flat background out of generated art, and find where the head actually is.

Both of the generators we use hand back a solid-background raster -- ChatGPT's
heads come on light grey (246,243,244), the emoji frames on white -- and dropping
either straight into the film paints a rectangle over whatever is behind it. That
is exactly what happened: the disintegration cut a white hole through the race
track for a second and a half.

The tolerance band is tight on purpose. Dev 1's face fill is (227,225,225),
only 19 levels off his own background, so a generous ramp turns his cheeks
half-transparent. lo=5/hi=12 keeps the fill solid and still feathers the
antialiased outline.
"""
import numpy as np
from PIL import Image

LO, HI = 5, 12


def background(a):
    """The flat colour the art was generated on, read off the four corners."""
    h, w = a.shape[:2]
    return np.median(np.stack([a[2, 2], a[2, w - 3], a[h - 3, 2], a[h - 3, w - 3]]),
                     axis=0)


def key(im, lo=LO, hi=HI):
    """RGBA copy with the background colour taken to alpha, feathered."""
    rgb = np.array(im.convert("RGB")).astype(np.int16)
    d = np.abs(rgb - background(rgb).astype(np.int16)).max(axis=-1)
    alpha = np.clip((d - lo) / (hi - lo), 0, 1) * 255
    out = np.dstack([rgb.astype(np.uint8), alpha.astype(np.uint8)])
    return Image.fromarray(out, "RGBA")


def trim(im):
    """Crop to the visible content."""
    box = im.split()[-1].point(lambda v: 255 if v > 12 else 0).getbbox()
    return im.crop(box) if box else im


def head(im):
    """
    (width, centre_x, centre_y) of the head, in pixels.

    Measured as the widest unbroken run of opaque pixels per row: the head is
    the one wide blob, and the ZZZ marks floating beside it are narrow. Without
    this the sleeping pose renders with its face smaller and lower than the
    awake one, because the ZZZ stretch the bounding box up and to the right --
    so the swap reads as the head changing size rather than as him falling
    asleep.
    """
    a = np.array(im.convert("RGBA"))
    solid = a[..., 3] > 40
    runs = np.zeros(solid.shape[0], dtype=int)
    centres = np.zeros(solid.shape[0], dtype=int)
    for y in range(solid.shape[0]):
        row = solid[y]
        if not row.any():
            continue
        best = cur = start = beststart = 0
        for x, v in enumerate(row):
            if v:
                if cur == 0:
                    start = x
                cur += 1
                if cur > best:
                    best, beststart = cur, start
            else:
                cur = 0
        runs[y], centres[y] = best, beststart + best // 2
    w = int(runs.max())
    rows = np.flatnonzero(runs >= 0.55 * w)
    return w, int(centres[runs.argmax()]), int((rows[0] + rows[-1]) / 2)
