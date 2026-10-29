"""EP005 -- key banana cat (walking + crying) and happy-happy cat off their green screens.

The patients in the triage explainer are these cats:
  banana walk  -> every patient walking into the queue (frozen on a frame while they wait)
  banana cry   -> the one the nurse is not sure about, on the waiting bench
  happy        -> the one that gets picked and goes through the door

Key: alpha from how much GREEN beats the stronger of red/blue (g - max(r, b)), not
g - mean(r, b) -- the banana suit is yellow, and yellow has a lot of green in it, so the
mean-based key from rc_dog.py would eat the banana. Despill pulls any leftover green
back to neutral. One crop box per segment so a cat never drifts inside its own frame.

Writes public/s1m/cats/{walk,cry,happy}/NNN.png + meta.json, and the clips' own audio
(kept, never stripped -- Sejal decides later whether it plays) as wav slices.
"""
import json, os, shutil, subprocess
import numpy as np
from PIL import Image

ROOT = os.path.expanduser("~/Documents/Work/comics-video")
SRC = os.path.join(ROOT, "s1m/cats")
OUT = os.path.join(ROOT, "public/s1m/cats")
HI, LO = 70.0, 22.0               # green margin: >= HI fully keyed, <= LO fully opaque
TARGET_H = 260                    # px; drawn at ~125 px in 720-space, 1.5x scaled at render

def decode(path, w, h):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)

def key(frames):
    v = frames.astype(np.float32)
    r, g, b = v[..., 0], v[..., 1], v[..., 2]
    margin = g - np.maximum(r, b)
    a = np.clip((HI - margin) / (HI - LO), 0, 1)
    g2 = np.minimum(g, np.maximum(r, b) + 6)          # despill
    return np.stack([r, g2, b], -1), a

def write(name, rgb, a, idx):
    d = os.path.join(OUT, name)
    if os.path.isdir(d): shutil.rmtree(d)
    os.makedirs(d)
    m = (a[idx] > 0.5).any(0)
    ys, xs = np.where(m)
    y0, y1, x0, x1 = max(0, ys.min() - 4), ys.max() + 5, max(0, xs.min() - 4), xs.max() + 5
    s = TARGET_H / (y1 - y0)
    tw, th = int(round((x1 - x0) * s)), TARGET_H
    for n, i in enumerate(idx):
        px = np.dstack([rgb[i, y0:y1, x0:x1], a[i, y0:y1, x0:x1] * 255]).astype(np.uint8)
        Image.fromarray(px).resize((tw, th), Image.LANCZOS).save(os.path.join(d, "%03d.png" % n))
    # where the feet are: the lowest opaque row, as a fraction of the crop height
    feet = (np.where((a[idx][:, y0:y1, x0:x1] > 0.5).any(0).any(1))[0].max() + 1) / (y1 - y0)
    return {"frames": len(idx), "w": tw, "h": th, "feet": round(float(feet), 3), "box": [int(x0), int(y0), int(x1), int(y1)]}

meta = {}
# ---- banana cat: find where walking turns into crying (the figure jumps in size)
ban = decode(os.path.join(SRC, "banana_src.mp4"), 1280, 720)
rgb, a = key(ban)
heights, widths = [], []
for i in range(len(a)):
    m = a[i] > 0.5
    ys = np.where(m.any(1))[0]; xs = np.where(m.any(0))[0]
    heights.append(ys.max() - ys.min() if len(ys) else 0)
    widths.append(xs.max() - xs.min() if len(xs) else 0)
widths = np.array(widths, float)
blank = [i for i, h in enumerate(heights) if h == 0]                 # the source has a stray empty frame
# walking -> crying is where the figure suddenly gets wide (the tears arc out)
jump = next(i for i in range(1, len(widths)) if widths[i] > 1.8 * widths[i - 1] and widths[i - 1] > 0)
print("banana: %d frames, walk->cry at frame %d (%.2fs), width %d -> %d, blank frames %s"
      % (len(a), jump, jump / 30, widths[jump - 1], widths[jump], blank))
walk = [i for i in range(0, jump) if i not in blank]
cry = [i for i in range(jump, len(a)) if i not in blank]
meta["walk"] = write("walk", rgb, a, walk)
meta["cry"] = write("cry", rgb, a, cry)
meta["walk"]["fps"] = meta["cry"]["fps"] = 30
meta["switch_s"] = jump / 30
# ---- happy cat
hap = decode(os.path.join(SRC, "happy_src.mp4"), 1280, 720)
rgb, a = key(hap)
meta["happy"] = write("happy", rgb, a, list(range(len(a))))
meta["happy"]["fps"] = 29.97
# ---- the clips' own audio, kept
def audio(src, out, ss=None, t=None):
    cmd = ["ffmpeg", "-v", "error", "-y"]
    if ss is not None: cmd += ["-ss", "%.3f" % ss]
    if t is not None: cmd += ["-t", "%.3f" % t]
    cmd += ["-i", os.path.join(SRC, src), "-vn", "-ac", "1", "-ar", "44100", "-c:a", "pcm_s16le", os.path.join(OUT, out)]
    subprocess.run(cmd, check=True)
audio("banana_src.mp4", "banana_walk.wav", 0, jump / 30)
audio("banana_src.mp4", "banana_cry.wav", jump / 30, None)
audio("happy_src.mp4", "happy.wav")
json.dump(meta, open(os.path.join(OUT, "meta.json"), "w"), indent=1)
print(json.dumps(meta))
