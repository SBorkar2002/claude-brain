"""Check a rendered `system one model` cut: one still per panel, and the mix."""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
ROOT = os.path.expanduser("~/Documents/Work/comics-video")
mp4 = sys.argv[1]
cut = json.load(open(os.path.join(ROOT, "src/s1m_cut.json")))
out = os.path.join(ROOT, "out/s1m/verify"); os.makedirs(out, exist_ok=True)
# one frame at 70% through every panel
ims = []
for n, p in enumerate(cut["panels"]):
    t = (p["startF"] + p["durF"] * 0.7) / cut["fps"]
    f = os.path.join(out, f"p{n:02d}.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", mp4, "-frames:v", "1", "-vf", "scale=216:384", f], check=True)
    ims.append(Image.open(f))
cols = 10
sheet = Image.new("RGB", (cols * 220, ((len(ims) + cols - 1) // cols) * 388), "black")
for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * 220, (i // cols) * 388))
sheet.save(os.path.join(out, "sheet.png"))
# the mix
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", mp4, "-ac", "1", "-ar", "44100", "-f", "f32le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
db = lambda s: 20 * np.log10(np.sqrt(np.mean(s ** 2)) + 1e-12)
seg = lambda a, b: x[int(a * 44100):int(b * 44100)]
print("duration %.2fs  peak %.1f dBFS" % (len(x) / 44100, 20 * np.log10(np.abs(x).max() + 1e-12)))
voice = [db(seg(v["at"] + 0.1, v["end"])) for v in cut["vo"]]
print("voice segments: median %.1f  min %.1f  max %.1f dB" % (np.median(voice), min(voice), max(voice)))
for v, d in zip(cut["vo"], voice):
    if abs(d - np.median(voice)) > 4: print("   level outlier", v["name"], round(d, 1))
err = [s["at"] for s in cut["sfx"] if s["file"].endswith("ui_error.wav")]
night_end = min([cut["light_at"] - 0.1] + [e - 0.05 for e in err if cut["night_at"] < e < cut["light_at"]])
print("night bed (should be silent, before the error sound): %.1f dB" % db(seg(cut["night_at"] + 0.7, night_end)))
# a gap with no voice in daylight: bed only
gaps = []
vs = sorted((v["at"], v["at"] + v["dur"]) for v in cut["vo"])
for (a0, b0), (a1, b1) in zip(vs, vs[1:]):
    if a1 - b0 > 0.6 and not (cut["night_at"] - 1 < b0 < cut["light_at"] + 2):
        gaps.append(db(seg(b0 + 0.15, a1 - 0.15)))
print("bed in voice gaps: median %.1f dB  (target 20-25 dB under voice)" % np.median(gaps))
for s in cut["sfx"]:
    if "dur" in s:   # typing slices; the UI cues are short one-shots
        print("typing", s["file"], "%.1f dB" % db(seg(s["at"] + 0.1, s["at"] + s["dur"] - 0.1)))
