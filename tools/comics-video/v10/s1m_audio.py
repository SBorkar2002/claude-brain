"""Cut the system-one-model VO into one file per line.

Edges come from the measured envelope (s1m/vo_src/*.json word order + 10ms RMS),
never from whisper's absolute times. Input-side seek only (-ss before -i), or
afade silences the clip. Interruptions get a 4ms fade, everything else 60ms."""
import os, subprocess, json
ROOT = os.path.expanduser("~/Documents/Work/comics-video")
SRC = os.path.join(ROOT, "s1m/vo_src")
OUT = os.path.join(ROOT, "public/s1m/vo")

# (out, source, in, out, fade_out)
CUTS = [
 ("ken_f01", "ken_all", 0.00, 4.95, 0.20),
 ("ken_f02", "ken_all", 6.18, 8.70, 0.08),
 ("ken_f04", "ken_all", 9.10, 10.55, 0.08),
 ("ken_f25", "ken_all", 11.50, 17.70, 0.08),
 ("ken_f29", "ken_all", 18.55, 19.98, 0.06),
 ("ken_f30", "ken_all", 20.15, 21.40, 0.08),
 ("ken_f56", "ken_all", 22.20, 22.92, 0.08),
 ("ken_f59", "ken_all", 23.75, 24.62, 0.08),
 ("ken_f61", "ken_all", 25.55, 28.68, 0.10),
 ("aj_f03", "aj_all", 0.03, 3.55, 0.06),
 ("aj_f07", "aj_all", 3.62, 4.55, 0.06),
 ("aj_f09", "aj_all", 4.73, 6.62, 0.06),
 ("aj_f14", "aj_all", 6.70, 8.80, 0.04),
 ("aj_f15", "aj_all", 8.84, 10.05, 0.06),
 ("aj_f16", "aj_all", 10.14, 11.15, 0.06),
 ("aj_f23", "aj_all", 11.41, 12.00, 0.06),
 ("aj_f28", "aj_all", 12.46, 15.55, 0.06),
 ("aj_f31", "aj_all", 16.19, 20.70, 0.06),
 ("aj_f36", "aj_all", 21.18, 22.95, 0.06),
 ("aj_f40", "aj_all", 23.36, 25.15, 0.06),
 ("aj_f44", "aj_all", 25.35, 26.69, 0.03),
 ("aj_f49", "aj_all", 26.71, 28.75, 0.06),
 ("aj_f54", "aj_all", 29.13, 30.42, 0.06),
 ("aj_f57", "aj_all", 30.51, 35.15, 0.06),
 ("aj_f60", "aj_all", 35.42, 37.48, 0.06),
 ("ai_f11", "ai_all", 0.00, 2.62, 0.06),
 ("ai_f13", "ai_all", 2.84, 3.44, 0.004),   # v7: "But without a-" (3 words; 3.46 already lets the l of "limit" in)
 ("ai_f33", "ai_all", 5.70, 15.05, 0.08),
 ("ai_f34", "ai_all", 15.46, 24.70, 0.08),
 ("ai_f37", "ai_all", 24.90, 33.10, 0.08),
 ("ai_f38", "ai_all", 33.47, 42.95, 0.08),
 ("ai_f39", "ai_all", 43.28, 49.35, 0.08),
 ("ai_f41", "ai_all", 49.67, 51.55, 0.08),
 ("ai_f43a", "ai_all", 52.08, 59.95, 0.08),
 ("ai_f43b", "ai_all", 60.25, 69.00, 0.08),
 ("ai_f43c", "ai_all", 69.48, 78.55, 0.08),
 ("ai_f46", "ai_all", 78.74, 81.05, 0.08),
 ("ai_f50", "ai_all", 81.67, 86.60, 0.08),
 ("ai_f52", "ai_all", 86.83, 90.95, 0.08),
 ("ai_f53", "ai_all", 91.22, 94.43, 0.10),
]

def cut(name, src, a, b, fo):
    d = b - a
    af = f"afade=t=in:st=0:d=0.010,afade=t=out:st={max(0, d - fo):.3f}:d={fo:.3f}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{d:.3f}",
                    "-i", os.path.join(SRC, src + ".wav"), "-af", af, "-ac", "1", "-ar", "44100",
                    "-c:a", "pcm_s16le", os.path.join(OUT, name + ".wav")], check=True)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for c in CUTS:
        cut(*c)
    print("cut", len(CUTS))

# ---------------------------------------------------------------- the customer-PDF version (9 Oct)
# Spliced from segments. Every join sits in a measured silence, except "a few | for" in f43c,
# which is a 15 ms crossfade inside continuous speech (re-record ai_f43c_pdf if it sounds clipped).
import wave as _wave
import numpy as _np

def _read(name):
    w = _wave.open(os.path.join(SRC, name + ".wav")); sr = w.getframerate()
    return _np.frombuffer(w.readframes(w.getnframes()), dtype=_np.int16).astype(_np.float64) / 32768, sr

def _active(x, sr):
    hop = int(sr * 0.01); n = len(x) // hop
    db = 20 * _np.log10(_np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    act = db[db > -45]
    return 10 * _np.log10(_np.mean(10 ** (act / 10))) if len(act) else -60

def splice(out, segs, xfade=0.015, fade_out=0.06, match_to=None):
    """segs: [(source, in, out)]. match_to: index of the segment whose level the others are matched to."""
    parts = []
    for src, a, b in segs:
        x, sr = _read(src); parts.append(x[int(a * sr):int(b * sr)].copy())
    if match_to is not None:
        ref = _active(parts[match_to], sr)
        for i, p in enumerate(parts):
            if i != match_to: parts[i] = p * 10 ** ((ref - _active(p, sr)) / 20)
    k = int(xfade * sr); y = parts[0]
    for p in parts[1:]:
        r = _np.linspace(0, 1, k)
        y = _np.concatenate([y[:-k], y[-k:] * (1 - r) + p[:k] * r, p[k:]])
    fi, fo = int(0.01 * sr), int(fade_out * sr)
    y[:fi] *= _np.linspace(0, 1, fi); y[-fo:] *= _np.linspace(1, 0, fo)
    w = _wave.open(os.path.join(OUT, out + ".wav"), "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((_np.clip(y, -1, 1) * 32767).astype(_np.int16).tobytes()); w.close()

PDF_SPLICES = [
    ("ken_f01", [("ken_pdf", 0.00, 2.66), ("ken_all", 2.75, 4.95)], dict(xfade=0.04, fade_out=0.20, match_to=1)),
    ("ai_f33",  [("ai_all", 5.70, 7.52), ("ai_all", 8.27, 15.05)], dict(fade_out=0.08)),
    ("ai_f43b", [("ai_all", 60.25, 63.32), ("ai_all", 66.46, 69.00)], dict(fade_out=0.08)),
    ("ai_f43c", [("ai_all", 69.48, 71.30), ("ai_all", 71.98, 78.55)], dict(fade_out=0.08)),
    ("ai_f53",  [("ai_all", 91.22, 93.38)], dict(fade_out=0.08)),
    # re-recorded 9 Oct: "Your doors are the four folders." The take ends on the "s" of
    # "folders" (decayed to -44 dB at the file edge), so the fade is short and lands on silence.
    ("ai_f39",  [("ai_f39_pdf", 0.45, 2.429)], dict(fade_out=0.02)),
]

if __name__ == "__main__":
    for name, segs, kw in PDF_SPLICES:
        splice(name, segs, **kw)
    print("pdf splices", len(PDF_SPLICES))
