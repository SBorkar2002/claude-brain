"""Emit the /insights cut. One source of truth: frames, plates, audio, flap."""
import json, os, wave
import numpy as np

FPS = 30
ROOT = os.path.expanduser("~/Documents/Work/comics-video")
VO   = os.path.join(ROOT, "public/ins")

def load(name):
    w = wave.open(os.path.join(VO, name + ".wav"))
    sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768.0
    return x, sr

# per-line level trims, measured against the median VO
GAINS = {"aj_p21": 0.62}   # the shout sits 5dB over everything else

def dur(name):
    x, sr = load(name)
    return len(x) / sr

def flap_track(name, nframes):
    """Per-video-frame mouth-open flags, measured off the take's own envelope.
    Never inferred: open where the voice is loud, shut where it is not."""
    x, sr = load(name)
    step = sr / FPS
    db = []
    for i in range(nframes):
        seg = x[int(i * step):int((i + 1) * step)]
        db.append(20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-12) if len(seg) else -120)
    db = np.array(db)
    thr = np.percentile(db[db > -60], 38) if (db > -60).any() else -44
    on = [bool(v > thr) for v in db]
    # a mouth that shuts on a decaying vowel reads as the word being swallowed
    out = list(on)
    for i, v in enumerate(on):
        if v:
            for k in range(i + 1, min(len(on), i + 3)):
                out[k] = True
    return out

# the monitor is in the same place on every screen plate -- locked, not re-detected
SCREEN = {"x": 41, "y": 528, "w": 637, "h": 369}
TITLE_FRAMES = {8, 9, 12, 13, 16, 17, 18, 33, 36, 37}

_CAPS = json.load(open(os.path.join(ROOT, "src/ins_caps.json")))

def blank_monitor(n):
    """Mark ONLY on a screen with nothing else on it. Cleaning the plates made
    a card measure as blank, so the measurement alone is not enough: a frame
    that has a caption drawn INSIDE the screen is not a blank monitor."""
    if n in TITLE_FRAMES:
        return False
    for c in _CAPS.get("frame%d" % n, []):
        if SCREEN["y"] <= c["y"] <= SCREEN["y"] + SCREEN["h"]:
            return False
    """The mark goes ONLY on a genuinely blank screen. Measured, not listed:
    a title card has ink in the box and a shot with no monitor is not bright.
    Hardcoding a frame list is what leaked the mark into scenes without one."""
    from PIL import Image
    import numpy as np
    a = np.asarray(Image.open(os.path.join(ROOT, "public/ins/plates/frame%d.png" % n)).convert("L"))
    box = a[SCREEN["y"]:SCREEN["y"] + SCREEN["h"], SCREEN["x"]:SCREEN["x"] + SCREEN["w"]]
    return bool((box > 228).mean() > 0.985 and (box < 128).mean() < 0.008)

# frames, slice, hold, flap?, note, splits (local seconds where each frame starts)
SPLITS = {
  "frame9": [0.0, 2.99], "frame13": [0.0, 4.53],
  "frame33": [0.0, 3.69], "frame37": [0.0, 2.28, 6.30, 7.39],
}

LINES = [
    (["frame1","frame2"],   "sameer_line", 0.8, True,  "loop line, second half"),
    (["frame3"],            "aj_p02",      1.0, False, "bluff + slurp"),
    (["frame4"],            "aj_p03",      1.0, False, "signature"),
    (["frame5"],            "aj_p04",      0.8, False, "click"),
    (["frame6"],            "ai_p05",      0.8, False, "the mechanism"),
    (["frame7"],            "aj_p06",      0.8, False, "the want"),
    (["frame8"],            "ai_t_impressive", 0.5, False, "AI reads the title"),
    (["frame9","frame10"],  "ai_p08",      0.6, False, None),
    (["frame11"],           "aj_p09",      -0.07, False, "interrupted"),
    (["frame12"],           "ai_t_hindering",  0.5, False, "AI reads the title"),
    (["frame13","frame14"], "ai_p10",      0.6, False, None),
    (["frame15"],           "aj_p11",      -0.07, False, "interrupted"),
    (["frame16"],           "ai_t_wrong",      0.5, False, "AI reads the title"),
    (["frame17"],           "ai_wrong_mine",   0.5, False, "ON MY SIDE -- it indicts itself first"),
    (["frame11","frame10"], "aj_ha",           0.0, True,  "AJ vindicated, cut off"),
    (["frame18"],           "ai_wrong_yours",  0.6, False, "ON YOURS -- the turn"),
    (["frame19","frame20"], "aj_p13",      -0.07, True,  "interrupted"),
    (["frame21"],           [("ai_p14a", 0.0), ("aj_whatever", 0.85)], 2.4, False, "AI line, then AJ's own word"),
    (["frame22","frame23"], "aj_p15",      0.55, True,  "interrupted"),
    (["frame24"],           [("ai_p16", 0.0), ("ai_agents", 0.45)], 0.6, False, "names the file, shows the line"),
    (["frame25"],           None,          1.0, False, "beat"),
    (["frame26"],           "aj_p17",      0.4, False, None),
    (["frame27"],           "ai_p17",      0.6, False, None),
    (["frame28"],           None,          0.8, False, "click"),
    (["frame29"],           "ai_p18a",     -0.05, False, "explainer placeholder"),
    (["frame30"],           None,          0.5, False, "click"),
    (["frame31"],           "ai_p18b",     0.4, False, "explainer placeholder"),
    # CUT: click beat before "wait you can do that"
    # CUT (Mohit, 30 Sep): the loop suggestion before "wait you can do that"
    # (["frame33","frame34"], "ai_p20",      0.8, False, "on the horizon"),
    (["frame35"],           "aj_p21",      0.8, False, None),
    (["frame36"],           "ai_t_memorable",  0.5, False, "AI reads the title"),
    (["frame37","frame38","frame39","frame40"], "ai_p22", 0.0, False, "cut off"),
    (["frame41"],           "aj_p23a",     0.15, False, "pointing: capitals only"),
    (["frame42"],           [("aj_p23b", 0.0, 0.15), ("peter_p24", 0.55, 1.0)], 0.5, False, "AJ rants UNDER Peter"),
    (["frame43"],           "sameer_p24a", 0.4, False, None),
    (["frame44"],           None,          0.8, False, "beat"),
    (["frame45"],           "sameer_p24b", 0.4, False, None),
    (["frame46"],           "sameer_hey",  0.0, False, "HARD CUT to frame1"),
]
F41_VISIBLE = None   # frame41 holds the whole of aj_p23

panels, cues = [], []
t = 0.0
for frames, slice_, hold, flap, note in LINES:
    n = int(frames[0].replace("frame", ""))
    if slice_ is None:
        span, d = hold, 0.0
    else:
        seq = slice_ if isinstance(slice_, list) else [(slice_, 0.0)]
        d, at = 0.0, t
        for item in seq:
            if len(item) == 3:
                # (file, offset FROM PANEL START, gain) -- cues overlap on purpose
                name, off, g = item
                dd = dur(name)
                cues.append({"file": name + ".wav", "at": round(t + off, 3),
                             "dur": round(dd, 3), "gain": g})
                d = max(d, off + dd)
            else:
                name, gap = item
                at += gap
                dd = dur(name)
                cues.append({"file": name + ".wav", "at": round(at, 3), "dur": round(dd, 3),
                             "gain": GAINS.get(name, 1.0)})
                at += dd
                d = at - t
        span = d + hold

    if flap:
        # ONE panel, two real drawn plates, swapped on the voice. Never painted.
        f0 = int(round(t * FPS)); f1 = int(round((t + span) * FPS))
        panels.append({
            "frames": frames, "plates": frames, "flap": True,
            # a reused drawing carries its own line, not the one it had before
            "capKey": {"frame11": "ha"}.get(frames[0]),
            "explainer": None, "phase": None, "title": None, "expT0": 0.0,
            "start": round(t, 3), "startF": f0, "durF": f1 - f0,
            "track": flap_track(slice_[0][0] if isinstance(slice_, list) else slice_, f1 - f0),
            "mark": blank_monitor(n), "speaking": bool(slice_ and str(slice_).find("ai_") >= 0),
            "note": note,
        })
        t += span
    else:
        sp = SPLITS.get(frames[0])
        offs = sp if sp else [span * k / len(frames) for k in range(len(frames))]
        for k, f in enumerate(frames):
            each = (offs[k + 1] if k + 1 < len(offs) else span) - offs[k]
            fn = int(f.replace("frame", ""))
            f0 = int(round(t * FPS)); f1 = int(round((t + each) * FPS))
            panels.append({
                "frames": [f], "plates": [f], "flap": False,
                "_exp": None,
                "explainer": {"frame29": "hook", "frame31": "skill",
                              "frame24": "agents", "frame33": "horizon",
                              "frame13": "hinder",
                              "frame17": "wrong",  "frame18": "wrong"}.get(f),
                "phase": {"frame17": "mine", "frame18": "yours"}.get(f),
                "capKey": {"frame11": "ha"}.get(f) if flap else None,
                # where this frame sits inside a line it shares, so a visual
                # spanning two frames keeps one continuous clock
                "expT0": 0.0,
                "title": {"frame12": "WHAT\u2019S HINDERING YOU",
                          "frame16": "WHERE THINGS GO WRONG",
                          "frame33": "THE HORIZON"}.get(f),
                "start": round(t, 3), "startF": f0, "durF": f1 - f0,
                "track": None,
                "mark": blank_monitor(fn) or fn in (13, 17, 18, 33), "speaking": bool(slice_ and str(slice_).find("ai_") >= 0),
                "note": note,
            })
            t += each

total = t
# AJ's bickering under the Peter/Sameer wide. Cut dead at the loop join.
f42 = next(p for p in panels if p["frames"] == ["frame42"])
f46 = next(p for p in panels if p["frames"] == ["frame46"])
bick_at = round(f42["start"] + dur("aj_p23b") + 0.2, 3)   # never over AJ's own line
def at_of(frame_name):
    return next(p["start"] for p in panels if p["frames"][0] == frame_name)

sfx = []
# Sameer drinking while AJ bluffs. This is loop's OWN slurp --
# public/v10/audio/coffee sound.mp3 at 3.50-6.10, the same 2.6s take that runs
# across its frames 2-4. One long effect, not three short ones.
# Sameer sips WHILE AJ bluffs -- simultaneous, and low enough to sit under him
sfx.append({"file": "slurp.wav", "at": round(at_of("frame3") + 0.55, 3), "gain": 0.3})
# he TYPES his question -- keyboard, not a mouse click
sfx.append({"file": "typing.wav", "at": round(at_of("frame5") + 0.15, 3), "gain": 0.75})
# and he CLICKS Copy, once per suggestion
for f, off, g in (("frame24", 0.12, 1.0), ("frame28", 0.12, 1.0),
                  ("frame30", 0.02, 1.4)):
    sfx.append({"file": "click.wav", "at": round(at_of(f) + off, 3), "gain": g})
# the ding brings "used in 41 sessions" up, AFTER AJ's own "whatever"
wh = next(c for c in cues if c["file"] == "aj_whatever.wav")
ding_at = round(wh["at"] + wh["dur"] + 0.35, 3)
sfx.append({"file": "ding.wav", "at": ding_at, "gain": 0.6})

# office bed, ducked ~7dB under every voice (present is not audible)
nF = int(round(total * FPS))
duck = [1.0] * nF
for c in cues:
    a = int(c["at"] * FPS) - 3
    b = int((c["at"] + c["dur"]) * FPS) + 6
    for i in range(max(0, a), min(nF, b)):
        duck[i] = 0.5

# the laughing cat, playing ON the background monitor while AJ melts down.
# Screen rect measured off the plates; the hand masks put his arm back in front.
CAT = {"x": 494, "y": 155, "w": 137, "h": 92, "frames": 105,
       "on": ["frame42", "frame43", "frame44", "frame45"]}
cat = dict(CAT, at=round(at_of("frame42") + 0.6, 3),
           until=round(at_of("frame46"), 3), gain=0.12,
           # muted for now -- the cue and its level are kept so this is a
           # one-flag change if the laugh is wanted back
           muted=True)

cut = {
    "fps": FPS, "w": 720, "h": 1280,
    "durationF": int(round(total * FPS)), "durationS": round(total, 2),
    "screen": SCREEN, "panels": panels, "vo": cues,
    "cat": cat, "sfx": sfx, "ding_at": ding_at, "duck": duck,
    "amb": {"file": "ambience.wav", "gain": 1.0},
    "bicker": {"file": "bicker.wav", "at": bick_at,
               "until": round(f46["start"], 3), "gain": 0.095},
}
out = os.path.join(ROOT, "src/ins_cut.json")
json.dump(cut, open(out, "w"))
print("panels %d   plates %d   vo %d   total %.2fs = %d:%04.1f"
      % (len(panels), sum(len(p["plates"]) for p in panels), len(cues),
         total, int(total // 60), total % 60))
