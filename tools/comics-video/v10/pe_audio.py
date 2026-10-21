"""Cut the four ElevenLabs takes for `prompt engineering` into one wav per line.

  Peter = Eric   (public/pe/vo_src/peter.mp3)
  AJ    = Jet    (public/pe/vo_src/aj.mp3)
  AI    = David  (public/pe/vo_src/ai.mp3)  -- both AIs, screens only
  ai_card.mp3    = David again, the card read ("GOAL what done looks like ...").
                   It REPLACES 37.3-46.7 of ai.mp3, where "constraints" came out wrong.

Cut points: a requested boundary snaps into the silence that contains it, then sits
>= 0.4s after the last voiced frame (the decay tail; feedback-vo-cut-tails) and
>= 0.08s before the next onset. Input-side seek (-ss before -i), 30 ms fade in,
60 ms fade out. Every clip is checked with volumedetect afterwards.
"""
import os, subprocess, json
import numpy as np

ROOT = os.path.expanduser("~/Documents/comics-video")
SRC = os.path.join(ROOT, "public/pe/vo_src")
OUT = os.path.join(ROOT, "public/pe/vo")

def env(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "44100", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float32); h = 441; n = len(x) // h
    return 20 * np.log10(np.sqrt((x[:n * h].reshape(n, h) ** 2).mean(1)) + 1e-9), len(x) / 44100

def snap(db, t, dur):
    """move a requested cut into the silence around it, leaving the tail"""
    v = db > -40
    k = int(t * 100)
    a = k
    while a > 0 and not v[a - 1]: a -= 1          # last voiced frame before
    b = k
    while b < len(v) and not v[b]: b += 1          # next onset after
    if v[min(k, len(v) - 1)]:
        raise SystemExit(f"cut at {t:.2f}s lands inside a word")
    lo, hi = a / 100 + 0.40, b / 100 - 0.08
    return round(min(max((a + b) / 200, lo), hi) if lo <= hi else (a + b) / 200, 3)

# (name, take, from, to); "end" = end of the take. Requested times are whisper mid-gaps.
LINES = [
    ("aj_f02", "aj", 0.0, 2.23),        # Huh? A hackathon?
    ("aj_f03", "aj", 2.23, 3.34),       # Bet.
    ("aj_f07", "aj", 3.34, 4.92),       # Okay, okay.
    ("aj_f08", "aj", 4.92, 17.2),       # Goal. ... Not sure? Ask me.
    ("aj_f09", "aj", 17.2, 19.9),       # One shot. Not typing this twice.
    ("aj_f11", "aj", 19.9, 21.25),      # New here.
    ("aj_f21", "aj", 21.25, "end"),     # ty. Just prompt engineered it, lol.
    ("pe_f05", "peter", 0.0, 1.25),     # My time to shine.
    ("pe_f06", "peter", 1.25, 7.95),    # Build an app ... Make no mistakes.
    ("pe_f16", "peter", 7.95, 10.4),    # Now that's a platform.
    ("pe_f20", "peter", 10.4, 12.85),   # Nice work, AJ.
    ("pe_f22", "peter", 12.85, 15.35),  # Right. Obviously.
    ("pe_f23", "peter", 15.35, 19.0),   # I have no idea what that means.
    ("pe_f27", "peter", 19.0, 24.5),    # Okay. His worked. Mine didn't. Why?
    ("pe_f34", "peter", 24.5, 26.6),    # I was going to say that.
    ("pe_f35", "peter", 26.6, "end"),   # You know what? I'm winning the next hackathon.
    ("ai_f10", "ai", 0.0, 4.55),        # One question. Explain it like ...
    ("ai_f13", "ai", 4.55, 6.62),       # Done. One link.
    ("ai_f15", "ai", 6.62, 10.6),       # Done. Two hundred and twelve features.
    ("ai_f26", "ai", 10.6, 15.7),       # Prompt engineering: telling the AI ...
    ("ai_f28", "ai", 15.7, 22.25),      # 'Amazing.' 'No mistakes.' ...
    ("ai_f29", "ai", 22.25, 31.45),     # His had four boxes ...
    ("ai_f30", "ai", 31.45, 37.4),      # He said what to skip ...
    # 37.4 - 46.9 of ai.mp3 is the card read with the bad "constraints": NOT USED
    ("ai_f32", "ai_card", 0.0, "end"),  # the card, from the re-record
    ("ai_f33", "ai", 46.9, "end"),      # Fill these four before you hit enter.
]

def main():
    os.makedirs(OUT, exist_ok=True)
    cache = {}
    report = {}
    for name, take, a, b in LINES:
        path = os.path.join(SRC, take + ".mp3")
        if take not in cache: cache[take] = env(path)
        db, total = cache[take]
        s = 0.0 if a == 0.0 else snap(db, a, total)
        e = total if b == "end" else snap(db, b, total)
        d = e - s
        pad = 0.45 if b == "end" else 0.0               # a take that ends on the word gets room to decay
        af = f"afade=t=in:st=0:d=0.03,afade=t=out:st={max(0, d - 0.06):.3f}:d=0.06"
        if pad: af += f",apad=pad_dur={pad}"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.3f}", "-t", f"{d:.3f}", "-i", path,
                        "-af", af, "-ac", "1", "-ar", "44100", "-c:a", "pcm_s16le",
                        os.path.join(OUT, name + ".wav")], check=True)
        r = subprocess.run(["ffmpeg", "-v", "info", "-i", os.path.join(OUT, name + ".wav"), "-af", "volumedetect",
                            "-f", "null", "-"], capture_output=True, text=True).stderr
        mean = float(r.split("mean_volume:")[1].split("dB")[0])
        assert mean > -60, f"{name} is silent ({mean} dB)"
        report[name] = {"take": take, "from": s, "to": round(e, 3), "dur": round(d + pad, 3), "mean_db": mean}
        print(f"  {name:8s} {take:8s} {s:6.2f} -> {e:6.2f}  {d + pad:5.2f}s  mean {mean:6.1f} dB")
    json.dump(report, open(os.path.join(ROOT, "public/pe/vo_src/cuts.json"), "w"), indent=1)

main()
