"""Emit the `prompt engineering` cut (Script A, "Wait, What?"). One source of truth.

Run order:  python3 v10/pe_audio.py   (cuts the four ElevenLabs takes into lines)
            python3 v10/pe_emit.py    (levels, timeline, flap, SFX, bed -> src/pe_cut.json)

Plates: Sejal's 36 frames off Figma page `Prompt engieering` (828:3), exported 720x1280 with
every dialogue / SFX / placeholder-screen text layer hidden. Kept baked: the phone notifications
(frame2) and the drawn "...", "..", "???".

Rules carried here (comic-animation.md / comic-audio.md):
 - hard cuts only; every panel holds ~1s after its voice ends
 - lip flap swaps two REAL drawn plates, calm flap for everyone (no fast chatter)
 - captions: whole line at once at the Figma box; never on a screen or explainer
 - every SFX gets its word on screen, popping on the sound
 - the card read uses the re-recorded ai_card take (ai_f32), not the long take
"""
import json, os, wave, subprocess
import numpy as np

FPS = 30
ROOT = os.path.expanduser("~/Documents/comics-video")
PE = os.path.join(ROOT, "public/pe")
RAW = os.path.join(PE, "vo")
VO = os.path.join(PE, "vo_n")
SFX = os.path.join(PE, "sfx")
WORDS = json.load(open(os.path.join(PE, "vo_src/clips_tx.json")))

def read(path):
    w = wave.open(path); sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768.0
    return x, sr

def env_db(x, sr, hop_s=0.01):
    hop = int(sr * hop_s); n = len(x) // hop
    return 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)

# ---------------------------------------------------------------- levels
TARGET = -16.0
SPECIAL = {"pe_f23": -19.0,   # the thought: quieter than speech, never a whisper
           "pe_f34": -15.0, "pe_f35": -15.0}   # flustered, keeps some size

def normalise():
    os.makedirs(VO, exist_ok=True)
    for fn in sorted(os.listdir(RAW)):
        if not fn.endswith(".wav"): continue
        name = fn[:-4]
        x, sr = read(os.path.join(RAW, fn))
        db = env_db(x, sr); act = db[db > -45]
        lvl = 10 * np.log10(np.mean(10 ** (act / 10))) if len(act) else -60
        peak = 20 * np.log10(np.abs(x).max() + 1e-9)
        g_db = min(SPECIAL.get(name, TARGET) - lvl, -1.0 - peak)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(RAW, fn), "-af", f"volume={g_db:.2f}dB",
                        "-c:a", "pcm_s16le", os.path.join(VO, fn)], check=True)

def edges(name):
    x, sr = read(os.path.join(VO, name + ".wav"))
    db = env_db(x, sr)
    thr = max(-42.0, np.percentile(db, 10) + 9.0)
    v = np.where(db > thr)[0]
    return (v[0] * 0.01, (v[-1] + 1) * 0.01, len(x) / sr)

def words(name):
    """whisper's word order, stretched onto the measured voiced run"""
    W = WORDS[name + ".wav"]["words"]
    a, b, _ = edges(name)
    ws, we = W[0]["s"], W[-1]["e"]
    k = (b - a) / (we - ws) if we > ws else 1.0
    return [(w["w"].strip(" .,?!:'‘’").lower(), round(a + (w["s"] - ws) * k, 3)) for w in W]

def at(name, word, nth=0):
    hits = [t for w, t in words(name) if w.startswith(word)]
    if not hits: raise SystemExit(f"word '{word}' missing from {name}")
    return hits[min(nth, len(hits) - 1)]

def runs_of(op, val):
    out, k = [], 0
    while k < len(op):
        if op[k] == val:
            j = k
            while j < len(op) and op[j] == val: j += 1
            out.append((k, j)); k = j
        else: k += 1
    return out

def flap_track(name, cue_at, start, nframes):
    """per-frame mouth flags off the take's own envelope -- the CALM flap for everyone
    (Sejal: proper lip sync, not too fast). A high bar to open, only deep dips close,
    no 1-2 frame flicks, open runs capped at 9 frames."""
    x, sr = read(os.path.join(VO, name + ".wav"))
    db = env_db(x, sr, 1.0 / FPS)
    peak = db.max()
    voiced = db > peak - 24
    # the bar is LOCAL (the loudest frame within +-0.3s, minus 14 dB): a line that trails off
    # ("...the next hackathon") keeps moving instead of closing on its quieter half
    w = int(0.3 * FPS)
    local = np.array([db[max(0, i - w):i + w + 1].max() for i in range(len(db))])
    op = voiced & (db > np.maximum(peak - 30, local - 14))
    for k in range(1, len(db) - 1):
        if op[k] and db[k] < max(db[k - 1], db[k + 1]) - 5.0 and db[k] <= min(db[k - 1], db[k + 1]) + 0.5:
            op[k] = False
    for a, b in runs_of(op, True):
        if b - a < 2: op[a:b] = False
    for a, b in runs_of(op, False):
        if a > 0 and b < len(op) and b - a <= 2: op[a:b] = True
    # never hold open longer than 9 frames: close at the quietest frame of a long run, both halves
    # kept >= 3 frames, every piece re-checked (not just the longer one)
    stack = [list(range(a_, b_)) for a_, b_ in runs_of(op, True)]
    while stack:
        run = stack.pop()
        if len(run) <= 9: continue
        m = min(run[3:-3], key=lambda q: db[q])
        op[m] = False
        idx = run.index(m)
        stack += [run[:idx], run[idx + 1:]]
    # splitting can leave 1-2 frame slivers: a mouth must stay open >= 3 frames, or it reads as chatter
    for a_, b_ in runs_of(op, False):          # a one-frame close is a blink of the jaw: hold it two
        if b_ - a_ == 1 and 0 < a_ and b_ < len(op): op[b_] = False
    for a_, b_ in runs_of(op, True):
        if b_ - a_ < 3: op[a_:b_] = False
    out = []
    for i in range(nframes):
        q = int(round((start + i / FPS - cue_at) * FPS))
        out.append(bool(0 <= q < len(op) and op[q]))
    return out

# ---------------------------------------------------------------- sfx sources
KB_SRC = os.path.join(SFX, "keyboard_full.wav")
def keystrokes():
    x, sr = read(KB_SRC)
    db = env_db(x, sr, 0.005); on = []
    for i in range(6, len(db)):
        if db[i] > -38 and db[i] - db[i - 6:i].min() > 9 and (not on or i * 0.005 - on[-1] > 0.06):
            on.append(i * 0.005)
    return on
KS = keystrokes()

def typing_cue(tag, t0, dur, src_off, gain=0.8):
    out = os.path.join(SFX, f"type_{tag}.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{src_off:.3f}", "-t", f"{dur:.3f}", "-i", KB_SRC,
                    "-af", f"afade=t=in:d=0.03,afade=t=out:st={max(0, dur - 0.12):.3f}:d=0.12",
                    "-c:a", "pcm_s16le", out], check=True)
    hits = [round(t0 + (k - src_off), 3) for k in KS if src_off + 0.02 <= k <= src_off + dur - 0.1]
    sfx.append({"file": f"sfx/type_{tag}.wav", "at": round(t0, 3), "gain": gain, "hits": hits, "tag": "type"})

# the library ding peaks at -30 dBFS: lift it once to sit just under the dialogue
PING = os.path.join(SFX, "ping.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(SFX, "ding.wav"), "-af", "volume=15dB",
                "-c:a", "pcm_s16le", PING], check=True)

def ui(name, t, gain=1.0):
    sfx.append({"file": f"sfx/{name}.wav", "at": round(t, 3), "gain": gain, "hits": [], "tag": name})

# ---------------------------------------------------------------- timeline
normalise()
panels, cues, sfx = [], [], []
T = [0.0]

def cue(name, offset=0.0):
    a, b, d = edges(name)
    c = {"file": f"vo_n/{name}.wav", "name": name, "at": round(T[0] + offset, 3), "dur": round(d, 3),
         "v0": round(T[0] + offset + a, 3), "end": round(T[0] + offset + b, 3)}
    cues.append(c)
    return c, b

def panel(plate, dur, caps=None, exp=None, header=None, mark=False, flap=None, ev=None, sfxw=None):
    s = T[0]
    f0 = int(round(s * FPS)); f1 = int(round((s + dur) * FPS))
    p = {"plate": plate, "start": round(s, 3), "startF": f0, "durF": f1 - f0, "caps": caps, "exp": exp,
         "header": header, "mark": mark, "ev": {k: round(v, 3) for k, v in (ev or {}).items()},
         "sfxw": sfxw or [], "flap": None}
    if flap:
        name, c, open_, shut = flap
        p["flap"] = {"open": open_, "shut": shut, "track": flap_track(name, c["at"], s, f1 - f0)}
    panels.append(p)
    T[0] = s + dur
    return p

def line(name, plate, hold=1.0, **kw):
    c, b = cue(name)
    fl = kw.pop("flap", None)
    if fl: kw["flap"] = (name, c, fl[0], fl[1])
    return panel(plate, b + hold, **kw), c

def rel(name, word, nth=0):
    """a word's time inside the panel that starts with its cue"""
    return at(name, word, nth)

# 1-3  AJ's phone pings; the post; "bet."
p = panel("frame1", 1.25, sfxw=[{"w": "ping", "x": 580, "y": 400, "rot": 9, "at": 0.30}])
ui("ping", p["start"] + 0.30, 1.0)
line("aj_f02", "frame2", 0.55, caps="frame2")
line("aj_f03", "frame3", 0.7, caps="frame3")
# 4-6  Peter's phone; his time to shine; the wish prompt, typed
p = panel("frame4", 1.35, header="2:00 PM", sfxw=[{"w": "ping", "x": 454, "y": 720, "rot": 9, "at": 0.22}])
ui("ping", p["start"] + 0.22, 1.0)
line("pe_f05", "frame5", 0.55, caps="frame5")
p6, c6 = line("pe_f06", "frame6", 0.8, caps="frame6", sfxw=[
    {"w": "click", "x": 306, "y": 1140, "rot": 32, "type": True}, {"w": "click", "x": 633, "y": 1023, "rot": -25, "type": True}])
typing_cue("f06", p6["start"] + 0.10, p6["durF"] / FPS - 0.25, 0.40)
# 7-9  AJ: okay okay, the four lines, one shot
p7, c7 = line("aj_f07", "frame7", 0.45, caps="frame7", sfxw=[
    {"w": "click", "x": 504, "y": 723, "rot": 9, "type": True}, {"w": "click", "x": 504, "y": 961, "rot": 25, "type": True}])
typing_cue("f07", p7["start"] + 0.05, p7["durF"] / FPS - 0.1, 6.0)
c, b = cue("aj_f08")
n = "aj_f08"
panel("frame8", b + 0.9, exp="ajprompt", ev={
    "g": rel(n, "goal"), "gv": rel(n, "any"), "c": rel(n, "constraints"), "cv": rel(n, "no"),
    "o": rel(n, "output"), "ov": rel(n, "one"), "f": rel(n, "failure"), "fv": rel(n, "not"), "end": b})
line("aj_f09", "frame9", 0.6, caps="frame9")
# 10-13  the AI asks first; new here; the app works; one link
c, b = cue("ai_f10")
p = panel("frame10", b + 0.5, exp="question", header="2:01 PM", mark=True, ev={
    "q": edges("ai_f10")[0], "new": rel("ai_f10", "new"), "five": rel("ai_f10", "five")})
ui("ui_pop", p["start"] + edges("ai_f10")[0], 0.9)
line("aj_f11", "frame11", 0.6, caps="frame11")
p = panel("frame12", 3.0, exp="app", header="2:04 PM", ev={"in": 0.25, "out": 1.75})
ui("ui_tick", p["start"] + 1.75, 0.9)
c, b = cue("ai_f13")
p = panel("frame13", b + 0.85, caps="frame13", exp="app_link", mark=True, ev={"link": rel("ai_f13", "link")})
ui("ui_pop", p["start"] + rel("ai_f13", "link"), 0.9)
# 14-16  4:58; Peter's 212 features; "now that's a platform"
panel("frame14", 1.3, header="4:58 PM")
c, b = cue("ai_f15")
p = panel("frame15", b + 0.85, caps="frame15", exp="features", mark=True, ev={
    "done": rel("ai_f15", "done"), "two": rel("ai_f15", "two"), "feat": rel("ai_f15", "features")})
ui("ui_chime", p["start"] + rel("ai_f15", "done") - 0.05, 0.7)
ui("ui_ripple", p["start"] + rel("ai_f15", "two"), 0.8)
line("pe_f16", "frame16", 0.7, caps="frame16", flap=("frame16", "frame14"))
# 17-19  5:00, the leaderboard; ???; ..
# both avatars land, then a second later Peter's turns into the crying dog (silent; Sejal, 20 Oct)
DOG_AT = 2.3
# the dog's own sniffing, from the same 2.0s point in the clip as its frames, at 40% (Sejal, 20 Oct).
# Its loudest sniffs sit 0.75s and 1.75s in: "sniff" pops under the dog on each (every sound gets its word).
p = panel("frame17", 5.0, exp="leaderboard", header="5:00 PM", ev={"aj": 0.35, "pe": 1.15, "dog": DOG_AT},
          sfxw=[{"w": "sniff", "x": 82, "y": 834, "rot": 0, "hits": [DOG_AT + 0.75, DOG_AT + 1.75]}])
ui("ui_chime", p["start"] + 0.35, 0.8)
ui("ui_pop_low", p["start"] + 1.15, 0.8)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "2.0", "-t", f"{5.0 - DOG_AT:.2f}", "-i",
                os.path.join(PE, "dog_src/dog.mp4"), "-vn", "-ac", "1", "-ar", "44100",
                "-af", f"afade=t=in:d=0.02,afade=t=out:st={5.0 - DOG_AT - 0.25:.2f}:d=0.25",
                "-c:a", "pcm_s16le", os.path.join(SFX, "dog_sniff.wav")], check=True)
ui("dog_sniff", p["start"] + DOG_AT, 0.4)
panel("frame18", 1.1)
panel("frame19", 1.0)
# 20-23  nice work; ty, prompt engineered it; right, obviously; the blank face
line("pe_f20", "frame20", 0.3, caps="frame20", flap=("frame20", "frame20_ss"))
line("aj_f21", "frame21", 0.8, caps="frame21", flap=("frame21", "frame20_ss"))
line("pe_f22", "frame22", 0.45, caps="frame22", flap=("frame22", "frame23"))
line("pe_f23", "frame23", 1.1, caps="frame23")
# 24-26  he types, opens AJ's app, becomes user #41; the app answers
p24 = panel("frame24", 1.6, sfxw=[
    {"w": "click", "x": 306, "y": 1140, "rot": 32, "type": True}, {"w": "click", "x": 633, "y": 1023, "rot": -25, "type": True}])
typing_cue("f24", p24["start"] + 0.12, 1.35, 11.0)
p = panel("frame25", 3.1, exp="app41", ev={"paste": 0.45, "tick": 1.55})
ui("ui_tick", p["start"] + 0.45, 0.9)
ui("ui_pop", p["start"] + 1.55, 1.0)
c, b = cue("ai_f26")
panel("frame26", b + 0.9, exp="app_answer", mark=True, ev={"start": edges("ai_f26")[0], "end": b})
panels[-1]["ev"]["words"] = [t for _, t in words("ai_f26")]   # the answer reveals word by word with the voice
# 27-28  why?; the wish words go
line("pe_f27", "frame27", 0.6, caps="frame27")
c, b = cue("ai_f28")
n = "ai_f28"
p = panel("frame28", b + 0.9, exp="teach", mark=True, ev={
    "amazing": rel(n, "amazing"), "mistakes": rel(n, "no"), "check": rel(n, "check"),
    "take": rel(n, "take"), "build": rel(n, "build")})
ui("ui_tick", p["start"] + rel(n, "amazing"), 0.7)
ui("ui_tick", p["start"] + rel(n, "no"), 0.7)
ui("ui_whoosh", p["start"] + rel(n, "take") + 0.1, 1.0)
# 29-30  the prompt contract, box by box (white explainer: no captions, no mark)
c, b = cue("ai_f29")
n = "ai_f29"
p29 = panel("frame29", b + 0.6, exp="contract", ev={
    "boxes": rel(n, "boxes"), "none": rel(n, "none"), "goal": rel(n, "goal"), "done": rel(n, "done"),
    "stopped": rel(n, "stopped"), "never": rel(n, "never")})
ui("ui_whoosh", p29["start"] + 0.05, 0.9)
ui("ui_ripple", p29["start"] + rel(n, "boxes"), 0.6)
ui("ui_pop", p29["start"] + rel(n, "goal"), 0.9)
ui("ui_ripple", p29["start"] + rel(n, "never"), 0.7)
c, b = cue("ai_f30")
n = "ai_f30"
p30 = panel("frame30", b + 0.8, exp="contract2", ev={
    "skip": rel(n, "skip"), "back": rel(n, "back"), "link": rel(n, "link"), "karaoke": rel(n, "karaoke")})
ui("ui_pop", p30["start"] + rel(n, "skip"), 0.9)
ui("ui_pop", p30["start"] + rel(n, "back"), 0.9)
ui("ui_whoosh", p30["start"] + rel(n, "karaoke") - 0.25, 0.9)
# 31  failure: ask vs guess, the cost (no VO in the take for this panel -- held silent)
p = panel("frame31", 3.4, exp="cost", ev={"fail": 0.25, "aj": 1.0, "pe": 1.9})
ui("ui_pop", p["start"] + 0.25, 0.9)
ui("ui_tick", p["start"] + 1.0, 0.9)
ui("ui_pop_low", p["start"] + 1.9, 0.9)
# 32-33  the card (screenshot frame), from the re-recorded take
c, b = cue("ai_f32")
n = "ai_f32"
p = panel("frame32", b + 0.5, exp="card", mark=True, ev={
    "g": rel(n, "goal"), "c": rel(n, "constraints"), "o": rel(n, "output"), "f": rel(n, "failure")})
for key in ("goal", "constraints", "output", "failure"):
    ui("ui_tick", p["start"] + rel(n, key), 0.8)
line("ai_f33", "frame33", 1.2, caps="frame33", exp="card_full", mark=True)
# 34-35  "I was going to say that!"  "You know what? I'm winning the next hackathon."
# frame34 == frame36 (open) and frame35 (shut) are one shot: the pair flaps across both lines
line("pe_f34", "frame34", 0.25, caps="frame34", flap=("frame34", "frame35"))
line("pe_f35", "frame35", 0.9, caps="frame35", flap=("frame34", "frame35"))

total = T[0]
nF = int(round(total * FPS))

# ---------------------------------------------------------------- bed
# EP005's office track is already printer-free; its daylight runs from 43.5s to 179s.
AMB = os.path.join(SFX, "amb_track.mp3")
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", "44.0", "-t", f"{total + 0.5:.2f}", "-i", AMB,
                      "-ac", "1", "-ar", "44100", "-af", "highpass=f=140:p=2,volume=-3dB", "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
bed = np.frombuffer(raw, dtype=np.float32).astype(np.float64)[: int(total * 44100)].copy()
# the loop: fade the last 1.2s into the opening's level so the replay does not step
g = np.ones(len(bed))
for cc in cues:
    a = int((cc["at"] - 0.10) * 44100); b2 = int((cc["at"] + cc["dur"] + 0.15) * 44100)
    g[max(0, a):min(len(g), b2)] = 0.56
kern = np.ones(int(0.30 * 44100)) / int(0.30 * 44100)
g = np.convolve(g, kern, mode="same")
bed *= g
f_in = int(0.4 * 44100); bed[:f_in] *= np.linspace(0, 1, f_in)
f_out = int(0.4 * 44100); bed[-f_out:] *= np.linspace(1, 0, f_out)
bed_path = os.path.join(SFX, "amb_pe.wav")
(np.clip(bed, -1, 1) * 32767).astype(np.int16).tofile("/tmp/pe_bed.raw")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", "44100", "-ac", "1", "-i", "/tmp/pe_bed.raw",
                "-c:a", "pcm_s16le", bed_path], check=True)

# ---------------------------------------------------------------- captions (Figma boxes, 720 space)
CAPS = {
    "frame2": [("Huh? A hackathon???", 193, 1155, 498)],
    "frame3": [("bet.", -103, 170, 498)],
    "frame5": [("My time to shine.", 222, 403, 498)],
    "frame7": [("okay okay", 29, 192, 370)],
    "frame9": [("one shot. not typing this twice.", 51, 226, 370)],
    "frame11": [("new here.", 51, 248, 370)],
    "frame13": [("Done. One link.", 92, 250, 536)],
    "frame15": [("Done. Two hundred and twelve features.", 76, 243, 569)],
    "frame16": [("Now that's a platform.", 266, 325, 310)],
    "frame20": [("Nice work, AJ.", 88, 323, 200, "left")],
    "frame21": [("ty. just prompt engineered it lol", 236, 621, 438, "left")],
    "frame22": [("Right. Obviously.", 497, 938, 157)],
    "frame23": [("I have no idea what that means.", 497, 882, 157, "center", True)],
    "frame27": [("Okay. His worked. Mine didn't. Why?", 403, 217, 276)],
    "frame33": [("Fill these four before you hit enter.", 75, 333, 570)],
    "frame34": [("I was going to say that!", 131, 241, 458)],
    "frame35": [("You know what? I'm winning the next hackathon.", 131, 212, 458)],
}
# a caption over ~55 characters shows in parts, in the same box, each from its own first word
SPLITS = {"frame6": ("pe_f06", (271, 204, 342), [("Build an app the whole office will love.", None),
                                               ("Make it amazing.", ("make", 0)), ("Make no mistakes.", ("make", 1))])}
for p in panels:
    key = p["caps"]
    if not key: continue
    clip = next(c for c in cues if abs(c["at"] - p["start"]) < 1e-6)
    v0 = clip["v0"] - p["start"]          # the caption arrives with the voice, whole line at once
    if key in SPLITS:
        name, (x, y, w), parts = SPLITS[key]
        starts = [v0] + [clip["at"] - p["start"] + at(name, wd, nth) - 0.05 for _, (wd, nth) in parts[1:]]
        p["capList"] = [{"t": t, "x": x, "y": y, "w": w, "align": "center", "italic": False,
                         "from": round(starts[i], 3), "until": round(starts[i + 1], 3) if i + 1 < len(parts) else None}
                        for i, (t, _) in enumerate(parts)]
    else:
        p["capList"] = [{"t": c[0], "x": c[1], "y": c[2], "w": c[3], "align": c[4] if len(c) > 4 else "center",
                         "italic": c[5] if len(c) > 5 else False, "from": round(max(0, v0 - 0.03), 3), "until": None}
                        for c in CAPS[key]]

# ---------------------------------------------------------------- checks
assert all(p["durF"] > 0 for p in panels)
for i in range(1, len(panels)):
    assert panels[i]["startF"] == panels[i - 1]["startF"] + panels[i - 1]["durF"], panels[i]["plate"]
for c in cues:
    assert os.path.exists(os.path.join(PE, c["file"])), c["file"]
# no voice may run into the next panel's voice, or past the film
for a, b in zip(cues, cues[1:]):
    assert a["end"] <= b["v0"], (a["name"], b["name"])
assert max(c["end"] for c in cues) <= total
for p in panels:
    if p["flap"]:
        for m in (p["flap"]["open"], p["flap"]["shut"]):
            assert os.path.exists(os.path.join(PE, "plates", m + ".png")), m
    else:
        assert os.path.exists(os.path.join(PE, "plates", p["plate"] + ".png")), p["plate"]

cut = {"fps": FPS, "w": 1080, "h": 1920, "S": 1.5, "durationF": nF, "durationS": round(total, 2),
       "screen": {"x": 41, "y": 528, "w": 638, "h": 371},
       "panels": panels, "vo": cues, "sfx": sfx, "bed": {"file": "sfx/amb_pe.wav", "gain": 1.0}}
json.dump(cut, open(os.path.join(ROOT, "src/pe_cut.json"), "w"))
print("panels %d  vo %d  sfx %d  total %.2fs (%d:%04.1f)"
      % (len(panels), len(cues), len(sfx), total, int(total // 60), total % 60))
for p in panels:
    fl = p["flap"]
    print(f"  {p['plate']:10s} {p['start']:6.2f} {p['durF'] / FPS:5.2f}s"
          + (f"  flap {sum(fl['track'])}/{len(fl['track'])} open" if fl else "") + (f"  {p['exp']}" if p["exp"] else ""))
