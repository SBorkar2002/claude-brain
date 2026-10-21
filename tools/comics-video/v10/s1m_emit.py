"""Emit the `system one model` cut. One source of truth: panels, VO, flap, SFX, bed.

Run order:  python3 v10/s1m_audio.py   (cuts the three ElevenLabs takes into lines)
            python3 v10/s1m_emit.py    (levels, timeline, flap, typing, bed -> src/s1m_cut.json)

Rules this file carries (comic-audio.md / comic-animation.md):
 - every panel starts on its first spoken word and holds ~1s after the voice ends
 - an interruption is a CUT: the AI's "But-" is sliced mid-flow and the panel ends on it
 - lip flap swaps two REAL drawn plates (Sejal's own open-mouth layer on / off, or two
   board frames that differ only at the mouth), driven by the take's own envelope
 - word ORDER from whisper, word EDGES from the signal (affine-mapped per clip)
 - night is silent; the bed is baked whole with the duck under every voice
"""
import json, os, wave, subprocess
import numpy as np

FPS = 30
ROOT = os.path.expanduser("~/Documents/comics-video")
RAW = os.path.join(ROOT, "public/s1m/vo")
VO = os.path.join(ROOT, "public/s1m/vo_n")
SFX = os.path.join(ROOT, "public/s1m/sfx")
WORDS = json.load(open(os.path.join(ROOT, "s1m/vo_src/clips_tx.json")))

def read(path):
    w = wave.open(path); sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768.0
    return x, sr

def env_db(x, sr, hop_s=0.01):
    hop = int(sr * hop_s)
    n = len(x) // hop
    seg = x[:n * hop].reshape(n, hop)
    return 20 * np.log10(np.sqrt((seg ** 2).mean(1)) + 1e-9)

# ---------------------------------------------------------------- levels
# active level target per line; the median of the raw takes was -15.8 dBFS
TARGET = -16.0
SPECIAL = {"aj_f06": -19.0,   # the thought: quieter than speech, never a whisper
           "aj_f42": -14.5,   # the shout keeps some of its size
           "aj_f16": -14.5,
           "ken_f61": -17.5}  # muttered, but it is the last line and must be heard

def normalise():
    os.makedirs(VO, exist_ok=True)
    report = {}
    for fn in sorted(os.listdir(RAW)):
        if not fn.endswith(".wav"): continue
        name = fn[:-4]
        x, sr = read(os.path.join(RAW, fn))
        db = env_db(x, sr)
        act = db[db > -45]
        lvl = 10 * np.log10(np.mean(10 ** (act / 10))) if len(act) else -60
        peak = 20 * np.log10(np.abs(x).max() + 1e-9)
        tgt = SPECIAL.get(name, TARGET)
        g_db = min(tgt - lvl, -1.0 - peak)          # never past -1 dBFS
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(RAW, fn),
                        "-af", f"volume={g_db:.2f}dB", "-c:a", "pcm_s16le",
                        os.path.join(VO, fn)], check=True)
        report[name] = (round(lvl, 1), round(g_db, 1))
    return report

def edges(name):
    """voiced start / end of a normalised clip, measured, not read off whisper"""
    x, sr = read(os.path.join(VO, name + ".wav"))
    db = env_db(x, sr)
    floor = np.percentile(db, 10)
    thr = max(-42.0, floor + 9.0)
    v = np.where(db > thr)[0]
    return (v[0] * 0.01, (v[-1] + 1) * 0.01, len(x) / sr) if len(v) else (0, len(x) / sr, len(x) / sr)

def words(name):
    """whisper's word order, stretched onto the measured voiced run"""
    W = WORDS.get(name + ".wav", {}).get("words", [])
    if not W: return []
    a, b, _ = edges(name)
    ws, we = W[0]["s"], W[-1]["e"]
    k = (b - a) / (we - ws) if we > ws else 1.0
    return [(w["w"].strip(".,?!").lower(), round(a + (w["s"] - ws) * k, 3)) for w in W]

def at(name, word, nth=0):
    """time of the nth occurrence of a word inside a clip"""
    hits = [t for w, t in words(name) if w.startswith(word)]
    return hits[min(nth, len(hits) - 1)] if hits else None

def runs_of(op, val):
    out, k = [], 0
    while k < len(op):
        if op[k] == val:
            j = k
            while j < len(op) and op[j] == val: j += 1
            out.append((k, j)); k = j
        else:
            k += 1
    return out

def flap_track(name, cue_at, start, nframes):
    """per-video-frame mouth flags, measured off the take's own envelope.
    Open where the voice is up, shut where it is not -- and shut again at the dip
    between syllables, so a phrase reads as talking rather than a held-open mouth.

    Ken is CALMER (Sejal, 9 Oct: his mouth moved too much): a higher bar to open,
    only deep dips close it, no one-frame flicks either way, and longer open runs.
    He is the manager and he is tired; he should look like he is barely moving his mouth."""
    calm = name.startswith(("ken_", "aj_"))   # Ken (v2) and AJ (v3): both read calmer
    x, sr = read(os.path.join(VO, name + ".wav"))
    db = env_db(x, sr, 1.0 / FPS)
    peak = db.max()
    voiced = db > peak - 24            # relative to the line itself, so a noisy take still closes
    thr = np.percentile(db[voiced], 50 if calm else 35) if voiced.any() else peak - 12
    op = voiced & (db > thr)
    # syllable dips: a frame well under the louder of its neighbours closes the mouth
    dip = 5.0 if calm else 2.5
    for k in range(1, len(db) - 1):
        if op[k] and db[k] < max(db[k - 1], db[k + 1]) - dip and db[k] <= min(db[k - 1], db[k + 1]) + 0.5:
            op[k] = False
    if calm:
        # no flicks: a lone open frame stays shut, a gap of 1-2 shut frames inside a word stays open
        for a, b in runs_of(op, True):
            if b - a < 2: op[a:b] = False
        for a, b in runs_of(op, False):
            if a > 0 and b < len(op) and b - a <= 2: op[a:b] = True
    max_run = 9 if calm else 5
    # never hold open longer than max_run frames: shut at the quietest frame of a long run
    k = 0
    while k < len(op):
        if op[k]:
            j = k
            while j < len(op) and op[j]: j += 1
            run = list(range(k, j))
            while len(run) > max_run:
                seg = run[1:-1]
                m = min(seg, key=lambda q: db[q])
                op[m] = False
                idx = run.index(m)
                left, right = run[:idx], run[idx + 1:]
                run = left if len(left) > len(right) else right
            k = j
        else:
            k += 1
    out = []
    for i in range(nframes):
        q = int(round((start + i / FPS - cue_at) * FPS))
        out.append(bool(0 <= q < len(op) and op[q]))
    return out

# ---------------------------------------------------------------- typing
KB_SRC = os.path.join(SFX, "keyboard_full.wav")
def keystrokes():
    x, sr = read(KB_SRC)
    db = env_db(x, sr, 0.005)
    on = []
    for i in range(6, len(db)):
        if db[i] > -38 and db[i] - db[i - 6:i].min() > 9 and (not on or i * 0.005 - on[-1] > 0.06):
            on.append(i * 0.005)
    return on
KS = keystrokes()

def typing_cue(tag, t0, dur, src_off):
    """slice the shared keyboard bed to its own file, played from zero (never seek an mp3)"""
    out = os.path.join(SFX, f"type_{tag}.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{src_off:.3f}", "-t", f"{dur:.3f}",
                    "-i", KB_SRC, "-af", f"afade=t=in:d=0.03,afade=t=out:st={max(0, dur - 0.12):.3f}:d=0.12",
                    "-c:a", "pcm_s16le", out], check=True)
    hits = [round(t0 + (k - src_off), 3) for k in KS if src_off + 0.02 <= k <= src_off + dur - 0.1]
    return {"file": f"sfx/type_{tag}.wav", "at": round(t0, 3), "dur": round(dur, 3), "gain": 1.0, "hits": hits}

def ui(name, t, gain=1.0):
    """an interface sound on the frame its element arrives (times mirror S1mExplainers.tsx)"""
    sfx.append({"file": f"sfx/{name}.wav", "at": round(t, 3), "gain": gain, "hits": [], "tag": name})

# ---------------------------------------------------------------- timeline
LEVELS = normalise()
panels, cues, sfx = [], [], []
T = [0.0]

def cue(name, offset=0.0):
    a, b, d = edges(name)
    c = {"file": f"vo_n/{name}.wav", "name": name, "at": round(T[0] + offset, 3), "dur": round(d, 3), "end": round(T[0] + offset + b, 3)}
    cues.append(c)
    return c, b

def panel(plate, dur, caps=None, exp=None, header=None, mark=False, flap=None, ev=None, clicks=False, phase=None, morph=False):
    s = T[0]
    f0 = int(round(s * FPS)); f1 = int(round((s + dur) * FPS))
    p = {"plate": plate, "start": round(s, 3), "startF": f0, "durF": f1 - f0,
         "caps": caps, "exp": exp, "phase": phase, "header": header, "mark": mark,
         "ev": ev or {}, "clicks": clicks, "flap": None, "morph": morph}
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

# 1-3  the ask, the bluff
line("ken_f01", "frame1", 0.25, caps="frame1", flap=("frame1", "frame2"))
line("ken_f02", "frame2", 0.55, caps="frame2", flap=("frame1", "frame2"))
line("aj_f03", "frame3", 0.8, caps="frame3", flap=("frame3", "frame3_shut"))
# 4-5  Ken leaves mid-line; the line carries over the empty doorway
c, b = cue("ken_f04")
panel("frame4", 0.80, caps="frame4")
panel("frame5", (b - 0.80) + 0.9, caps="frame5")
# 6  the signature
line("aj_f06", "frame6", 0.9, caps="frame6")
# 7-8  he types his ask_ai script; the screen shows it
# held longer (Sejal, 9 Oct): the code types at a readable pace and the test result gets time to land
p7, c7 = line("aj_f07", "frame7", 1.0, caps="frame7", flap=("frame7", "frame7_shut"), clicks=True)
p8 = panel("frame8", 4.8, exp="code")
ui("ui_chime", p8["start"] + 3.1, 0.8)                                # 10 / 10 lands
sfx.append(dict(typing_cue("f07", p7["start"] + 0.12, (p8["start"] + 2.85) - (p7["start"] + 0.12), 0.40), tag="f07"))
# 9-10  ten for ten (open grin on the line, the closed smile holds after)
c, b = cue("aj_f09")
panel("frame9", b + 0.05, caps="frame9")
panel("frame10", 0.8, caps="frame10")
# 11-13  the plant, waved off, the AI cut short
line("ai_f11", "frame11", 0.6, caps="frame11", mark=True)
line("aj_f12", "frame12", 0.4, caps="frame12", flap=("frame12", "frame12_shut"))
c, b = cue("ai_f13")
panel("frame13", c["dur"], caps="frame13", mark=True)             # the cut IS the interruption
# 14-16  the coupon, the exit
# AJ talks OVER the cut (Sejal, 9 Oct: "still a small gap"): his take has 75 ms of air before the M,
# and the M ramps for another ~50 ms. Start it early so the M is already rising under the end of "a"
# and "Man" is at full level the instant the AI is cut. The picture cuts on the AI's last sample.
AJ_OVER = -0.105
c, b = cue("aj_f14", AJ_OVER)
panel("frame14", b + AJ_OVER + 0.12, caps="frame14")
line("aj_f15", "frame15", 0.6, caps="frame15")
line("aj_f16", "frame16", 0.7, caps="frame16")
# 17-21  the empty desk, the night, the limit, the morning
panel("frame17", 1.2)
night_at = T[0]
panel("frame18", 1.6)
panel("frame19", 2.2, exp="night", header="2:13 AM")
p20 = panel("frame20", 2.4, exp="limit_night", header="3:51 AM")
ui("ui_error", p20["start"] + 1.0, 0.9)                               # USAGE LIMIT REACHED
light_at = T[0]
panel("frame21", 1.6, exp="limit_day", header="9:20 AM")
panel("frame22", 1.3)
c, b = cue("aj_f23", 0.12)
panel("frame23", 0.12 + b + 0.75, exp="limit_day")                 # no caption over a visual
panel("frame24", 1.0)
# 25-26  Ken: arms crossed, then the facepalm on "I said a system one model"
c, b = cue("ken_f25")
split = at("ken_f25", "i") - 0.10
panel("frame25", split, caps="frame25", flap=("ken_f25", c, "frame25", "frame25_shut"))
panel("frame26", (b - split) + 0.7, caps="frame26")
panel("frame27", 0.8, caps="frame27")
line("aj_f28", "frame28", 0.6, caps="frame28", flap=("frame28", "frame27"))
line("ken_f29", "frame29", 0.15, caps="frame29", flap=("frame29", "frame29_shut"))
line("ken_f30", "frame30", 0.8, caps="frame30", flap=("frame30", "frame30_shut"))
# 31-32  he types the question (32 is the same drawing with the mouth shut)
p31, c31 = line("aj_f31", "frame31", 0.6, caps="frame31", flap=("frame31", "frame32"), clicks=True)
sfx.append(dict(typing_cue("f31", p31["start"] + 0.05, p31["durF"] / FPS - 0.25, 1.90), tag="f31"))
# 33-36  the AI explains, twice. On 33 its mark changes shape with the words (v3)
p33, c33 = line("ai_f33", "frame33", 1.0, caps="frame33", mark=True, morph=True, ev={
    "read": at("ai_f33", "read"), "reasoned": at("ai_f33", "reasoned"),
    "paid": at("ai_f33", "paid"), "thinking": at("ai_f33", "thinking"), "sorting": at("ai_f33", "sorting"),
    "choose": at("ai_f33", "choose")})
for key in ("read", "reasoned", "paid", "thinking", "sorting"):
    ui("ui_morph", p33["start"] + p33["ev"][key] - 0.15, 1.0)
p34, c34 = line("ai_f34", "frame34", 1.0, exp="dense", ev={
    "system": at("ai_f34", "system"), "outputs": at("ai_f34", "outputs"),
    "calibrated": at("ai_f34", "calibrated"), "every": at("ai_f34", "every"),
    "parallel": at("ai_f34", "parallel"), "nothing": at("ai_f34", "nothing"),
    "token": at("ai_f34", "token")})
# exp-34 v2 (9 Oct): the cards tick in, the one pass ripples, the pick chimes (times mirror DenseScreen)
e = p34["ev"]
for i in range(4): ui("ui_tick", p34["start"] + e["outputs"] - 0.05 + i * 0.12, 0.7)
ui("ui_ripple", p34["start"] + e["parallel"] - 0.05, 0.8)
ui("ui_chime", p34["start"] + e["token"] + 0.5, 0.6)
panel("frame35", 0.7, caps="frame35")
line("aj_f36", "frame36", 0.7, caps="frame36", flap=("frame36", "frame35"))
# 37-39  the plain rung: doctor, nurse, the four doors -- each line gets room to land (v3)
p37, _ = line("ai_f37", "exp37", 1.0, exp="doctor", ev={
    "doctor": at("ai_f37", "doctor"), "read": at("ai_f37", "read"), "page": at("ai_f37", "page"),
    "reason": at("ai_f37", "reason"), "pay": at("ai_f37", "pay"),
    "reading": at("ai_f37", "reading"), "reasoning": at("ai_f37", "reasoning"),
    "worth": at("ai_f37", "worth")})
ui("ui_pop", p37["start"] + p37["ev"]["reason"], 0.7)                 # the thinking bubble
ui("ui_whoosh", p37["start"] + p37["ev"]["pay"] - 0.3, 1.0)           # the bill slides up
p38, _ = line("ai_f38", "exp38", 1.0, exp="nurse", ev={
    "nurse": at("ai_f38", "nurse"), "built": at("ai_f38", "built"), "define": at("ai_f38", "define"),
    "doors": at("ai_f38", "doors"), "picks": at("ai_f38", "picks"), "sure": at("ai_f38", "sure"),
    "not": at("ai_f38", "not"), "says": at("ai_f38", "says")})
e = p38["ev"]
ui("ui_whoosh", p38["start"] + e["built"] - 0.35 + 0.3, 1.0)          # doors and bench rise
ui("ui_pop", p38["start"] + e["sure"] - 0.1, 1.0)                     # 97%
ui("ui_pop_low", p38["start"] + e["not"] + 0.2, 1.0)                  # ? 51%
# v8 (9 Oct): the line is back, re-recorded short: "Your doors are the four folders." It ties the
# nurse's doors to AJ's PDFs before "WAIT. YOU CAN DO THAT??". The labels already name the folders,
# so the voice doesn't list them: they land one by one from "folders" -- each ticks, the chip pops on the first.
fold = at("ai_f39", "folders")
LABELS = {f"d{i}": round(fold - 0.05 + i * 0.35, 3) for i in range(4)}
p39, _ = line("ai_f39", "exp39", 1.5, exp="doors", ev=dict(LABELS))
for key, tt in LABELS.items():
    ui("ui_pop" if key == "d0" else "ui_tick", p39["start"] + tt - (0.05 if key == "d0" else 0), 0.9)

# the cats' own audio (v4): kept, never stripped, one flag mutes all three (CAT_AUDIO_MUTED).
# Each slice is baked to its exact window and stops dead on the cut to frame 42.
CAT_AUDIO_MUTED = False
CATS = os.path.join(ROOT, "public/s1m/cats")
def cat_audio(src, out, start_abs, end_abs, gain_db, src_from=0.0):
    L = end_abs - start_abs
    x, sr = read(os.path.join(CATS, src))
    x = x[int(src_from * sr):]
    reps = int(np.ceil(L * sr / len(x))) + 1
    y = np.tile(x, reps)[: int(L * sr)] * 10 ** (gain_db / 20)
    fi, fo = int(0.02 * sr), int(0.05 * sr)
    y[:fi] *= np.linspace(0, 1, fi); y[-fo:] *= np.linspace(1, 0, fo)
    (np.clip(y, -1, 1) * 32767).astype(np.int16).tofile("/tmp/cat.raw")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(sr), "-ac", "1", "-i", "/tmp/cat.raw",
                    "-c:a", "pcm_s16le", os.path.join(SFX, out)], check=True)
    sfx.append({"file": f"sfx/{out}", "at": round(start_abs, 3), "gain": 1.0, "hits": [], "tag": out, "cat": True})
e38 = p38["ev"]
enter_abs = p38["start"] + (e38["built"] - 0.35) + 0.9
p39_end = p39["start"] + p39["durF"] / FPS
cat_audio("banana_walk.wav", "cat_walk.wav", enter_abs, enter_abs + 2.45, 0.0)
# happy-happy cat's song removed (v5, Sejal). The keyed clip stays; only its audio is out.
# the crying stops when the AI starts naming the doors (v6): the cry ends on the cut into exp39
cat_audio("banana_cry.wav", "cat_cry.wav", p38["start"] + e38["not"], p39["start"] + 0.05, -5.0)

# 42 moved up (v3): AJ's "WAIT. YOU CAN DO THAT??" answers the nurse -- a model that picks the
# team and says how sure it is -- not "sorting the mail". Then the penny drops (40, 41).
line("aj_f42", "frame42", 0.7, caps="frame42")
line("aj_f40", "frame40", 0.6, caps="frame40")
line("ai_f41", "frame41", 0.7, caps="frame41", mark=True)
# 43  setting up the nurse, three takes, one card that grows in place
pa, _ = line("ai_f43a", "exp43", 1.0, exp="setup", phase="a", ev={
    "set": at("ai_f43a", "set"), "step1": at("ai_f43a", "step", 0), "question": at("ai_f43a", "question"),
    "step2": at("ai_f43a", "step", 1), "doors": at("ai_f43a", "doors"), "what": at("ai_f43a", "what")})
e = pa["ev"]
ui("ui_whoosh", pa["start"] + 0.1, 1.0)
ui("ui_tick", pa["start"] + e["step1"] + 0.1, 0.9)
for i in range(4): ui("ui_tick", pa["start"] + e["doors"] - 0.1 + i * 0.12, 0.8)
pb, _ = line("ai_f43b", "exp43", 1.0, exp="setup", phase="b", ev={
    "step3": at("ai_f43b", "step"), "isnt": at("ai_f43b", "isn"), "dark": at("ai_f43b", "isn") + 0.55,
    # the example resolves on "which DOOR"
    "request": at("ai_f43b", "door", 1), "tell": at("ai_f43b", "tell"), "fifty": at("ai_f43b", "50")})
e = pb["ev"]
ui("ui_pop_low", pb["start"] + e["isnt"] - 0.05, 0.9)                 # NOT FOR
ui("ui_whoosh", pb["start"] + e["dark"] - 0.35, 1.0)                  # the dark-mode ticket
ui("ui_pop", pb["start"] + e["request"] - 0.2, 0.9)                   # AFTER: 94%
pc, _ = line("ai_f43c", "exp43", 1.0, exp="setup", phase="c", ev={
    "step4": at("ai_f43c", "step"), "show": at("ai_f43c", "show"),
    "last": at("ai_f43c", "last"), "sorted": at("ai_f43c", "sorted")})
e = pc["ev"]
for i in range(4): ui("ui_tick", pc["start"] + e["show"] + 0.3 + i * 0.35, 0.8)
ui("ui_pop", pc["start"] + e["last"] - 0.05, 0.9)
# 44-46
line("aj_f44", "frame45", 0.5, caps="frame44", flap=("frame45", "frame44"))
line("ai_f46", "frame46", 0.8, caps="frame46", mark=True)
# 47  he reaches for run-all
p47 = panel("frame47", 1.1, caps="frame47", clicks=True)
sfx.append(dict(typing_cue("f47", p47["start"] + 0.05, 1.0, 4.80), tag="f47"))
# Shorts cut (Sejal, 12 Oct): step five, "skip the test" and the test result are out (-10.7s) so the
# episode fits YouTube Shorts' 3:00. He reaches for run-all (47) and the diff of his script follows.
# 52-53  same script, the nurse sorts
p52, _ = line("ai_f52", "frame52", 1.0, exp="diff", ev={
    "only": at("ai_f52", "only"), "changes": at("ai_f52", "changes"), "me": at("ai_f52", "me"),
    "nurse": at("ai_f52", "nurse")})
for key in ("only", "changes", "me"): ui("ui_tick", p52["start"] + p52["ev"][key], 0.9)
p53, _ = line("ai_f53", "frame53", 1.3, exp="piles", ev={
    "comes": at("ai_f53", "comes"), "you": at("ai_f53", "you")})
ui("ui_ripple", p53["start"] + 0.05, 1.0)
ui("ui_pop", p53["start"] + p53["ev"]["comes"], 0.9)                 # the pile for AJ
# 54-61  the payoff and the turn
line("aj_f54", "frame54", 0.8, caps="frame54", flap=("frame54", "frame54_shut"), header="9:51 AM")
p55 = panel("frame55", 3.2, exp="payoff", header="10:00 AM")
ui("ui_whoosh", p55["start"] + 0.1, 1.0); ui("ui_whoosh", p55["start"] + 1.0, 1.0); ui("ui_chime", p55["start"] + 2.2, 0.7)
line("ken_f56", "frame56", 0.5, caps="frame56", flap=("frame56", "frame56_shut"))
line("aj_f57", "frame57", 0.6, caps="frame57")
panel("frame58", 0.8, caps="frame58")
line("ken_f59", "frame59", 0.6, caps="frame59", flap=("frame59", "frame58"))
line("aj_f60", "frame60", 0.8, caps="frame60")
# the end card (v6, Sejal 9 Oct), placed where GE puts its own: right after the term is said, with the
# last reaction kept for after it, the way GE plays "couldn't care less" after its slate. No meter.
pe = panel("exp_end", 3.8, exp="endcard")
ui("ui_tick", pe["start"] + 2.55, 0.6)                                # the bookmark fills
line("ken_f61", "frame61", 1.4, caps="frame61", flap=("frame61", "frame61_shut"))

# ---------------------------------------------------------------- long captions, in parts (v5, Sejal)
# A caption over ~55 characters is too much to read at once. It shows in parts, in the SAME box,
# each part arriving on the first word of its own sentence (measured, not guessed).
CAP_SPLITS = {
    "frame1":  ("ken_f01", [("80,000 customer PDFs in the backlog.", None), ("sorted by standup.", ("sorted", 0))]),
    "frame3":  ("aj_f03",  [("ohh system one? yeah yeah obviously.", None), ("i use it all the time", ("i", 0))]),
    "frame25": ("ken_f25", [("that was the team's AI budget.", None), ("for the whole month.", ("for", 0))]),
    "frame31": ("aj_f31",  [("\u2026yo what's a system one model.", None), ("and why did you eat 250 dollars", ("and", 0))]),
    "frame33": ("ai_f33",  [("Because I read every line and reasoned it through.", None),
                            ("You paid for the reading and the thinking.", ("you", 0)),
                            ("For sorting, you want something built to choose.", ("for", 1))]),
    "frame57": ("aj_f57",  [("done. twelve bucks.", None), ("the doctor reads everything, the nurse just picks the door.", ("the", 0))]),
}
_CAPS = json.load(open(os.path.join(ROOT, "src/s1m_caps.json")))
for p in panels:
    key = p["caps"]
    if key not in CAP_SPLITS: continue
    clip, parts = CAP_SPLITS[key]
    c = next(c for c in cues if c["name"] == clip)
    off = c["at"] - p["start"]                       # where the line starts inside this panel
    geo = _CAPS[key][0]
    starts = [0.0] + [off + at(clip, w, n) - 0.05 for _, (w, n) in parts[1:]]
    chunks = []
    for i, (text, _) in enumerate(parts):
        chunks.append({"t": text, "x": geo["x"], "y": geo["y"], "w": geo["w"], "italic": geo.get("italic", False),
                       "from": round(starts[i], 3), "until": round(starts[i + 1], 3) if i + 1 < len(parts) else None})
    p["capChunks"] = chunks

total = T[0]
nF = int(round(total * FPS))

# ---------------------------------------------------------------- bed
AMB_MP3 = os.path.join(ROOT, "public/s1m/sfx/amb_track.mp3")
subprocess.run(["python3", "v10/ambience.py", f"{total + 0.5:.2f}", f"{night_at:.2f}", f"{light_at:.2f}", AMB_MP3],
               cwd=ROOT, check=True)
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", AMB_MP3, "-ac", "1", "-ar", "44100", "-f", "f32le", "-"],
                     capture_output=True).stdout
bed = np.frombuffer(raw, dtype=np.float32).astype(np.float64)[: int(total * 44100)]
# the printer must not survive into the film: find any sustained high-frequency run
# the builder's own check still sees, and lay clean room from 6s earlier over it
import importlib.util
_spec = importlib.util.spec_from_file_location("amb", os.path.join(ROOT, "v10/ambience.py"))
_src = open(os.path.join(ROOT, "v10/ambience.py")).read().replace("\nmain()\n", "\n")
_amb = {}; exec(compile(_src, "ambience", "exec"), _amb)
def _day(runs):   # the night is digital silence; the ratio test is meaningless there
    return [r for r in runs if r[1] < night_at - 0.5 or r[0] > light_at + 1.5]
# v8 (Sejal, 9 Oct: "remove the printing sound"): the long printer run was already gone, but 15 short
# whirrs (0.3-0.5s, +6 to +13 dB of 2.5-8 kHz over the room) were left -- the 2 kHz shelf made them worse.
# Detect at 3 dB, lay clean room over each from a window that is itself clean, repeat until none are left.
PRINTER_OVER = 3.0
dur_bed = len(bed) / 44100
n_patched = 0
for _pass in range(5):
    runs = _day(_amb["hf_runs"](bed, over=PRINTER_OVER))
    if not runs: break
    for a, b2, over in runs:
        a0, b0 = max(0, a - 0.35), min(dur_bed, b2 + 0.35)
        L = b0 - a0
        def _clean(s0):
            return (s0 >= 0 and s0 + L <= dur_bed and not (s0 < light_at + 1.5 and s0 + L > night_at - 0.5)
                    and not any(r[0] < s0 + L + 0.1 and r[1] > s0 - 0.1 for r in runs))
        s0 = next((a0 + off for off in (-6, 6, -9, 9, -12, 12, -15, 15, -4, 4, -20, 20) if _clean(a0 + off)), None)
        if s0 is None: continue
        i0, i1 = int(a0 * 44100), int(a0 * 44100) + int(L * 44100)
        src = int(s0 * 44100)
        patch = bed[src:src + (i1 - i0)].copy()
        xf = int(0.08 * 44100); r = np.linspace(0, 1, xf)
        patch[:xf] = bed[i0:i0 + xf] * (1 - r) + patch[:xf] * r
        patch[-xf:] = patch[-xf:] * (1 - r) + bed[i1 - xf:i1] * r
        bed[i0:i1] = patch
        n_patched += 1
left = _day(_amb["hf_runs"](bed, over=PRINTER_OVER))
print(f"  printer patched   {n_patched} runs; left at +{PRINTER_OVER} dB:", [(round(x, 1), round(y, 1)) for x, y, _ in left] if left else "clean")
# v5 (Sejal, 9 Oct: "where is the office ambience?"): it was there at -33 dB but 90% of it sat under
# 1 kHz, room rumble that laptop and phone speakers don't play, and the VO covers 79% of the day.
# Cut the rumble, lift the office texture (2 kHz shelf), and bring the whole bed up 6 dB.
BED_GAIN_DB = -3.0  # v8 (Sejal, 9 Oct): still too loud at +2; no brightening any more either
# knocks: a desk knock in the source (53.85s, and again at each repeat) peaked at -6 dBFS and clips once
# the bed comes up. Any 50 ms window peaking 15 dB over the room's own typical peak gets clean room laid over it.
_h = int(0.05 * 44100); _n = len(bed) // _h
_pk = 20 * np.log10(np.abs(bed[:_n * _h]).reshape(_n, _h).max(1) + 1e-9)
_room = np.median(_pk[_pk > -100])
for i in np.where(_pk > _room + 15)[0]:
    i0, i1 = int((i * 0.05 - 0.15) * 44100), int((i * 0.05 + 0.35) * 44100)
    src = i0 - int(1.0 * 44100)
    patch = bed[src:src + (i1 - i0)].copy()
    xf = int(0.04 * 44100); r = np.linspace(0, 1, xf)
    patch[:xf] = bed[i0:i0 + xf] * (1 - r) + patch[:xf] * r
    patch[-xf:] = patch[-xf:] * (1 - r) + bed[i1 - xf:i1] * r
    bed[i0:i1] = patch
    print(f"  knock patched    {i * 0.05:.2f}s (+{_pk[i] - _room:.1f} dB over the room)")
(bed.astype(np.float32)).tofile("/tmp/s1m_bed_eq_in.f32")
bed = np.frombuffer(subprocess.run(
    ["ffmpeg", "-v", "error", "-f", "f32le", "-ar", "44100", "-ac", "1", "-i", "/tmp/s1m_bed_eq_in.f32",
     "-af", f"highpass=f=140:p=2,volume={BED_GAIN_DB}dB", "-f", "f32le", "-"],
    capture_output=True, check=True).stdout, dtype=np.float32).astype(np.float64)[: len(bed)]
night_i = slice(int(night_at * 44100), int(light_at * 44100))
bed[night_i] = 0.0   # the night stays digital silence (the filters ring a few samples into it)
# duck ~7 dB under every voice, with 150 ms ramps (present is not audible: it has to move)
g = np.ones(len(bed))
for c in cues:
    a = int((c["at"] - 0.10) * 44100); b2 = int((c["at"] + c["dur"] + 0.15) * 44100)
    g[max(0, a):min(len(g), b2)] = 0.56   # about -5 dB: under the voice, never gone (v3: it vanished in the dense ending)
k = int(0.30 * 44100)
kern = np.ones(k) / k
g = np.convolve(g, kern, mode="same")
bed *= g
bed_path = os.path.join(ROOT, "public/s1m/sfx/amb_s1m.wav")
(np.clip(bed, -1, 1) * 32767).astype(np.int16).tofile("/tmp/s1m_bed.raw")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", "44100", "-ac", "1", "-i", "/tmp/s1m_bed.raw",
                "-c:a", "pcm_s16le", bed_path], check=True)

# ---------------------------------------------------------------- checks
assert all(p["durF"] > 0 for p in panels), "a panel has no frames"
for i in range(1, len(panels)):
    assert panels[i]["startF"] == panels[i - 1]["startF"] + panels[i - 1]["durF"], "gap or overlap at " + panels[i]["plate"]
for c in cues:
    assert os.path.exists(os.path.join(ROOT, "public/s1m", c["file"])), c["file"]
# no voice may run past the end of the film
assert max(c["at"] + c["dur"] for c in cues) <= total + 0.3

cut = {"fps": FPS, "w": 1080, "h": 1920, "S": 1.5, "durationF": nF, "durationS": round(total, 2),
       "screen": {"x": 41, "y": 528, "w": 638, "h": 371},
       "panels": panels, "vo": cues, "sfx": sfx,
       "bed": {"file": "sfx/amb_s1m.wav", "gain": 1.0}, "catAudioMuted": CAT_AUDIO_MUTED,
       "night_at": round(night_at, 3), "light_at": round(light_at, 3)}
json.dump(cut, open(os.path.join(ROOT, "src/s1m_cut.json"), "w"))
print("panels %d  vo %d  sfx %d  total %.2fs (%d:%04.1f)  night %.2f  light %.2f"
      % (len(panels), len(cues), len(sfx), total, int(total // 60), total % 60, night_at, light_at))
