"""EP003 -- key the shivering-dog meme off its green screen.

A photoreal dog dropped into flat line art is the joke, so the matte has to be
clean: any green fringe against the pale background reads as a mistake rather
than a gag. Alpha comes from GREENNESS (G above the red/blue average), with a
soft ramp so the fur edge is not stair-stepped, and every pixel that still
leans green is pulled back to neutral (despill).

Writes public/rc/dog/NNN.png, cropped to the dog and nothing else.
"""
import subprocess, numpy as np, os, shutil
from PIL import Image

SRC = "/Users/sejal/Downloads/Dog Shivering Green Screen - Green Screens by CreatorSet (608p).mp4"
OUT = "public/rc/dog"
W, H, N = 608, 1080, 142
HI, LO = 90.0, 25.0          # fully green -> fully keyed, below LO -> opaque

raw = subprocess.run(["ffmpeg","-v","error","-i",SRC,"-f","rawvideo","-pix_fmt","rgb24","-"],
                     capture_output=True).stdout
v = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(np.float32)
print("decoded %d frames" % len(v))

r, g, b = v[...,0], v[...,1], v[...,2]
green = g - (r + b) / 2
a = np.clip((HI - green) / (HI - LO), 0, 1)
# despill: a pixel that is still greener than its neighbours goes neutral
cap = np.maximum((r + b) / 2, 0)
g2 = np.where(g > cap, cap, g)
rgb = np.stack([r, g2, b], -1)

# one crop box for the whole clip, so the dog does not drift in its own frame
m = (a > 0.35).any(0)
ys, xs = np.where(m)
y0, y1, x0, x1 = ys.min(), ys.max()+1, xs.min(), xs.max()+1
print("dog occupies x %d-%d  y %d-%d  (%dx%d)" % (x0, x1, y0, y1, x1-x0, y1-y0))

if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
SCALE = 0.55
tw, th = int((x1-x0)*SCALE), int((y1-y0)*SCALE)
for i in range(len(v)):
    px = np.dstack([rgb[i, y0:y1, x0:x1], a[i, y0:y1, x0:x1]*255]).astype(np.uint8)
    Image.fromarray(px, "RGBA").resize((tw, th), Image.LANCZOS).save(OUT+"/%03d.png" % i)
print("wrote %d frames at %dx%d -> %s" % (len(v), tw, th, OUT))
open(OUT+"/meta.txt","w").write("%d %d %d\n" % (len(v), tw, th))
