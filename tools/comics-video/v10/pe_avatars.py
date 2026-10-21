"""Leaderboard avatars for `prompt engineering` (f17).

  aj.png     AJ's head cropped from Sejal's full-body sheet (dog_src/aj_full.webp)
  peter.png  Peter's drooling head (dog_src/peter_head.webp, already transparent)
  dog/NNN    the crying-dog meme keyed off its green screen, cropped to the head,
             no audio (Sejal: "dog crying + no audio"). Same g - max(r, b) key as the cats.
All square, drawn into one grey circle in PeScreens so the swap Peter -> dog is a hard cut
inside the same frame.
"""
import os, shutil, subprocess
import numpy as np
from PIL import Image

ROOT = os.path.expanduser("~/Documents/comics-video")
SRC = os.path.join(ROOT, "public/pe/dog_src")
OUT = os.path.join(ROOT, "public/pe")
SIZE = 240

aj = Image.open(os.path.join(SRC, "aj_full.webp")).convert("RGBA")
aj.crop((280, 335, 490, 545)).resize((SIZE, SIZE), Image.LANCZOS).save(os.path.join(OUT, "avatars/aj.png"))

pe = Image.open(os.path.join(SRC, "peter_head.webp")).convert("RGBA")
a = np.asarray(pe)[..., 3]; ys, xs = np.where(a > 10)
cx, cy = (xs.min() + xs.max()) // 2, (ys.min() + ys.max()) // 2 + 20
half = int(max(xs.max() - xs.min(), ys.max() - ys.min()) * 0.47)
pe.crop((cx - half, cy - half, cx + half, cy + half)).resize((SIZE, SIZE), Image.LANCZOS).save(os.path.join(OUT, "avatars/peter.png"))

HI, LO = 70.0, 22.0
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(SRC, "dog.mp4"), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                     capture_output=True, check=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, 720, 1280, 3)
FROM, N = 60, 120                     # 2.0s in: the whimpering stretch; 4s is more than the panel needs
BOX = (420, 20, 760, 360)             # one box for every frame: the head moves inside it, never the crop
d = os.path.join(OUT, "dog")
shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
for n, i in enumerate(range(FROM, FROM + N)):
    v = fr[i, BOX[1]:BOX[3], BOX[0]:BOX[2]].astype(np.float32)
    r, g, b = v[..., 0], v[..., 1], v[..., 2]
    alpha = np.clip((HI - (g - np.maximum(r, b))) / (HI - LO), 0, 1)
    g2 = np.minimum(g, np.maximum(r, b) + 6)
    px = np.dstack([r, g2, b, alpha * 255]).astype(np.uint8)
    Image.fromarray(px).resize((SIZE, SIZE), Image.LANCZOS).save(os.path.join(d, "%03d.png" % n))
print("aj, peter, dog frames:", N)
