"""EP003 `remote control` -- writes src/rc_cut.json from the built audio.

Nothing here is a hand-typed timing. Every cue, panel boundary and caption is
DERIVED from the voice track, because hardcoded numbers silently rot the moment
a take is replaced. Her lines are addressed by the WORDS in them -- position in
the run list breaks when a breath is removed, and group structure breaks when a
take is swapped, but a word does not move.
"""
import json, subprocess, numpy as np
FPS, OFF = 30, 1.78
D = json.load(open("/tmp/rc_durs.json"))

def env(path, win=0.025, hop=0.010):
    raw = subprocess.run(["ffmpeg","-v","quiet","-i",path,"-ac","1","-ar","16000",
                          "-f","f32le","-"], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32); h, w = int(hop*16000), int(win*16000)
    return np.array([20*np.log10(np.sqrt(np.mean(x[i*h:i*h+w]**2)+1e-12)+1e-12)
                     for i in range(max(1,(len(x)-w)//h))])

def runs(path, mg=0.15, thr=-42):
    db = env(path); on = db > thr; out=[]; s=None
    for i,v in enumerate(on):
        if v and s is None: s=i
        elif not v and s is not None: out.append([s*.01,i*.01]); s=None
    if s is not None: out.append([s*.01,len(db)*.01])
    m=[]
    for a,b in out:
        if m and a-m[-1][1]<mg: m[-1][1]=b
        else: m.append([a,b])
    return [r for r in m if r[1]-r[0] > 0.12]

L = [(a+OFF, b+OFF) for a,b in runs("public/rc/date_main.wav")]

# ---------------------------------------------------------------- her lines
import whisper as _w
_r = _w.load_model("small").transcribe("public/rc/date_main.wav",
        word_timestamps=True, language="en")
_words = [(w["word"].strip().lower().strip(".,!?"), w["start"]+OFF, w["end"]+OFF)
          for sg in _r["segments"] for w in sg.get("words", [])]
def _seed(key):
    for t,a,b in _words:
        if key in t: return (a+b)/2
    raise SystemExit("word %r is not in her VO -- check the take" % key)
# The punchline is seeded on "single", not on the insult: the line is moving
# from "idiot" to "noob" and whisper will render that as noob / newb / nube.
# "every single step" is the part of the sentence that is not changing.
SEEDS = [("normal","RAMBLE"),("next","NEXT"),("guessed","GUESS"),("nine","PAID"),("talking","WHO"),
         ("try","TRY"),("hold","HOLD"),("raising","PR"),("appetiz","REMOTE"),
         ("pings","PINGS"),("single","IDIOT"),("wait","CATCH")]
_st = [(_seed(k), n) for k,n in SEEDS]
own = {}
for a,b in L:
    hit = sorted([(t,n) for t,n in _st if a-0.05 <= t <= b+0.05])
    if len(hit) == 1:
        own.setdefault(hit[0][1], []).append((a,b))
    elif len(hit) > 1:
        # two lines ran together in one voiced run -- split it between them
        edges=[a]+[ (hit[i][0]+hit[i+1][0])/2 for i in range(len(hit)-1) ]+[b]
        for i,(_,n) in enumerate(hit):
            own.setdefault(n, []).append((round(edges[i],2), round(edges[i+1],2)))
free = [r for r in L if not any(r in v for v in own.values())]
for _t, _n in _st:
    # whisper undershoots the start of a word that follows a long silence, so a
    # seed can land in the gap just before its own run. Snap it to the nearest
    # unclaimed run rather than failing -- the WORD is still the address.
    if _n in own: continue
    _c = min(free, key=lambda r: 0 if r[0] <= _t <= r[1] else min(abs(r[0]-_t), abs(r[1]-_t)))
    own[_n] = [_c]; free.remove(_c)
changed = True
while changed:                      # grow each phrase outward from its seed
    changed = False
    for r in list(free):
        best = None
        for n, rs in own.items():
            lo, hi = min(x[0] for x in rs), max(x[1] for x in rs)
            d = lo-r[1] if r[1] <= lo else (r[0]-hi if r[0] >= hi else 0.0)
            if d < 0.30 and (best is None or d < best[0]): best = (d, n)
        if best: own[best[1]].append(r); free.remove(r); changed = True
def span(n):
    rs = own.get(n)
    if not rs: raise SystemExit("no audio found for her line %s" % n)
    return [round(min(r[0] for r in rs), 2), round(max(r[1] for r in rs), 2)]
RAMBLE, NEXT, GUESS, PAID, WHO, TRY, HOLD, PR, REMOTE, PINGS, IDIOT, CATCH = (span(n) for _,n in SEEDS)
print("her lines, measured:")
for nm, v in zip([n for _,n in SEEDS], [RAMBLE,NEXT,GUESS,PAID,WHO,TRY,HOLD,PR,REMOTE,PINGS,IDIOT,CATCH]):
    print("   %-7s %6.2f -> %6.2f" % (nm, v[0], v[1]))

# ---------------------------------------------------------------- cues
d = lambda f: D[f + ".wav"]
# scene4.5 is the bridge: he stops talking, looks down at the phone on the
# table, and only THEN are we in the office. It is a held beat, so the panel
# length is declared here and the office lines move behind it.
P02  = 3.10
S45  = P02 + d("peter_p02") + 0.25      # he finishes, we stay on him a moment
P03  = S45 + 0.12                       # "wait. i can just remote control it."
ZOOM = P03 + 1.05                       # the push-in starts INSIDE the take's
                                        # own pause, so the move is already
                                        # running when he names the thing
P04  = P03 + d("peter_p03") + 0.30
cues = [("loop_open","rc/loop_open.wav", 0.05),
        ("date_main","rc/date_main.wav", OFF),
        ("p02","rc/peter_p02.wav", P02),
        ("p03","rc/peter_p03.wav", P03),
        ("p04","rc/peter_p04.wav", P04),
        ("onit","rc/ai_onit.wav",  P04+d("peter_p04")+0.30),
        ("p06","rc/peter_p06.wav", NEXT[1]+0.50),
        ("ping1","rc/ping.wav",    GUESS[1]+0.18),
        ("p08","rc/peter_p08.wav", GUESS[1]+0.40),
        ("ai09","rc/ai_p09.wav",   PAID[0]+1.10),
        ("p11","rc/peter_p11.wav", PAID[0]+3.32)]
P11 = PAID[0]+3.32
cues += [("ping2","rc/ping.wav", PAID[1]+0.02),
         ("ping3","rc/ping.wav", PAID[1]+0.38),
         ("ping4","rc/ping.wav", PAID[1]+0.92),
         ("p14","rc/peter_p14.wav", WHO[1]+0.42),
         ("ping5","rc/ping.wav",    WHO[1]+1.95),
         ("uh","rc/peter_uh.wav",   TRY[1]+0.87),
         ("pingH","rc/ping_her.wav",TRY[1]+1.87)]
# The comedic beat after the punchline. It was 1.80 when the line began with
# "what" -- the "uh" now carries 0.9s of that hang itself, so the silence is
# shorter and the total wait is unchanged.
# His ping, the one that gives him away, into the beat after her joke.
PING6 = IDIOT[1]+0.75
# He TALKS OVER her. One take, played WHOLE -- "Your sister! [laugh] What did
# your sister do next?" The three parts get three frames, but the audio is
# never cut: the pause before the question is the take's own.
# He lands ON the cut: his take carries 0.09s of lead-in, so his voice starts
# the instant her word is severed.
P20 = round(CATCH[1]-0.10, 2)
LAUGH, BACK = 0.66, 1.97          # part boundaries, measured off the built file
# THE LOOP CLOSE. She answers his question by going back to the beginning --
# over the SAME plate the film opens on, so the join has no visual cut at all
# and her voice carries straight across it.
LOOPC = round(P20 + d("peter_p20") + 0.30, 2)
cues += [("ping6","rc/ping.wav", PING6), ("p20","rc/peter_p20.wav", P20),
         ("loop_close","rc/loop_close.wav", LOOPC)]
# the film ends as her line does: any tail here becomes a hole at the loop
DUR = round(LOOPC + d("loop_close") + 0.03, 2)

# ------------------------------------------------- restaurant ambience
# A bed, not a layer: ~14dB under dialogue, so it is felt in the silences
# (the 2.5s beat, the pauses in her rant) and never competes with a voice.
# It runs UNBROKEN across the split screens on purpose -- the office is a
# place he is looking at, not a place he is in, and the room he is actually
# sitting in never stops.
AMB_SRC = "/Users/sejal/Downloads/dobcommunications-busy-restaurant-dining-room-ambience-128466 (1).mp3"
AMB_GAIN_DB = -10.0          # source is -26.1 dBFS; dialogue sits at -22.1, so
                             # this lands ~14dB under it. -18 put the bed at
                             # -44 dBFS, which measured fine and was inaudible
                             # on a phone. Set this by EAR, not by the number.
def build_ambience(dst, dur, xf=1.0):
    """Cut a calm stretch of room tone to length and make it loop into itself.

    The film loops, so the bed's last second is crossfaded onto its first:
    played back to back the join is continuous, with no dip and no click.
    """
    raw = subprocess.run(["ffmpeg","-v","quiet","-i",AMB_SRC,"-ac","2","-ar","44100",
                          "-f","f32le","-"], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).reshape(-1,2).copy()
    need = int(round((dur+xf)*44100))
    # pick the most even window -- no clatter, no laugh spiking through the mix
    H = 4410
    lvl = 20*np.log10(np.sqrt((x[:len(x)//H*H].reshape(-1,H,2)**2).mean(axis=(1,2)))+1e-12)
    best, bs = None, 0
    for st in range(0, (len(x)-need)//H, 10):
        w = lvl[st:st+need//H]
        sc = (w.max()-np.median(w)) + w.std()
        if best is None or sc < best: best, bs = sc, st*H
    seg = x[bs:bs+need]
    # fold the tail back onto the head so the loop point is seamless
    n = int(round(xf*44100))
    f = np.linspace(0,1,n,dtype=np.float32)[:,None]
    out = seg[:int(round(dur*44100))].copy()
    out[:n] = out[:n]*f + seg[-n:]*(1-f)
    out *= 10**(AMB_GAIN_DB/20)
    subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar","44100","-ac","2",
                    "-i","-","-c:a","pcm_s16le",dst], input=out.tobytes(), check=True)
    return bs/44100.0
_ambat = build_ambience("public/rc/ambience.wav", DUR)
print("ambience: %.0fs of room tone from %.0fs in, %+.0f dB, loop-matched"
      % (DUR, _ambat, AMB_GAIN_DB))
cues += [("amb","rc/ambience.wav", 0.0)]
cues = sorted([dict(id=i, src=s, t=round(t,2), frame=round(t*FPS)) for i,s,t in cues],
              key=lambda k: k["t"])
C = {x["id"]: x["t"] for x in cues}

# ------------------------------------------------- her level under his lines
DEEP = {"ai09","p04","onit","p11"}; MID = {"p08"}
ducks = [[round(x["t"]-0.18,2), round(x["t"]+d(x["src"].split("/")[-1][:-4])+0.22,2),
          0.13 if x["id"] in DEEP else (0.22 if x["id"] in MID else 0.20)]
         # p20 is an INTERRUPTION, not an overlap. Ducking her under it ramps
         # her down over 0.18s while she is still mid-word, which reads as a
         # fade-out instead of a cut. She plays at full and stops dead.
         for x in cues if x["id"] not in ("date_main","loop_open","amb","p20")
         and not x["id"].startswith("ping")]
ducks.append([round(PAID[0]-0.10,2), round(PAID[1]+0.10,2), 0.42])
ducks.sort(); merged=[]
for a,b,v in ducks:                 # gaps under 0.55s make her level pop back up
    if merged and a-merged[-1][1] < 0.55:
        merged[-1][1]=max(merged[-1][1],b); merged[-1][2]=min(merged[-1][2],v)
    else: merged.append([a,b,v])
for m in merged:                    # under the rambling she must stay AUDIBLE
    if m[0] < RAMBLE[1] and m[1] > RAMBLE[0]: m[2] = max(m[2], 0.20)

# ------------------------------------------------- the bed gets out of the way
# Restaurant babble is the WORST masker for dialogue, because it IS dialogue --
# same band, same rhythm. At -44 dBFS it needed no duck; at -36, where it is
# actually audible, it has to move. It ducks under every voice in the film,
# hers included, so it lives in the gaps and nowhere else.
SPEECH = [x for x in cues if x["id"] not in ("date_main","loop_open","amb")
          and not x["id"].startswith("ping")]
aw = [[round(x["t"]-0.12,2), round(x["t"]+d(x["src"].split("/")[-1][:-4])+0.20,2)] for x in SPEECH]
aw += [[round(a-0.12,2), round(b+0.20,2)] for a,b in L]
aw += [[round(C["loop_open"]-0.12,2), round(C["loop_open"]+d("loop_open")+0.20,2)]]
aw.sort(); ambd=[]
for a,b in aw:
    if ambd and a-ambd[-1][1] < 0.35: ambd[-1][1] = max(ambd[-1][1], b)
    else: ambd.append([a,b])
ambd = [[a,b,0.45] for a,b in ambd]
print("ambience ducked over %d windows, %.0f%% of the film"
      % (len(ambd), 100*sum(b-a for a,b,_ in ambd)/DUR))

# ---------------------------------------------------------------- panels
PH=[535,1366,140,-8.0]; MON=[527,431,185]
SCR={s:dict(mon=MON,ph=PH) for s in ("5","6","12","13")}
R=lambda t: round(t,2)
_p14s=C["ping2"]-0.45; _p17s=WHO[0]-0.10; _third=(_p17s-_p14s)/3.0
PANELS=[(0.00,"1","her",None), (R(OFF),"3","her",None),
        (R(C["p02"]-0.50),"4",None,None),
        (R(S45),"45a",None,None), (R(ZOOM),"45b",None,[1.00,1.35]),
        (R(C["p04"]-0.25),"5",None,None),
        (R(C["onit"]-0.22),"6",None,None), (R(max(NEXT[0]-0.42, C["onit"]+d("ai_onit")+0.45)),"7","her",None),
        (R(C["p06"]-0.16),"8","him",None), (R(GUESS[0]-0.18),"10","her",None),
        (R(C["ping1"]-0.20),"11","both",None), (R(C["ai09"]-0.30),"12",None,None),
        (R(C["p11"]-0.32),"13",None,None), (R(_p14s),"14","her",None),
        (R(_p14s+_third),"15","her",None), (R(_p14s+2*_third),"16","her",None),
        (R(_p17s),"17","her",None), (R(C["p14"]-0.20),"18",None,None),
        (R(TRY[0]-0.38),"19","her",None), (R(C["uh"]-0.16),"20","him",[1.00,1.19]),
        (R(C["pingH"]-0.06),"21",None,None), (R(HOLD[0]-0.22),"22","her",None),
        (R(REMOTE[0]-0.20),"23","her",None), (R(PINGS[0]-0.18),"24","her",None),
        (R(IDIOT[0]-0.20),"25",None,None), (R(IDIOT[1]+0.30),"26",None,None),
        (R(C["ping6"]+0.50),"246","her",None),
        (R(P20-0.06),"20a","him",None), (R(P20+LAUGH),"247","him",None),
        (R(P20+BACK),"20b","him",None), (R(LOOPC-0.25),"1b","her",None)]
PLATE={"20a":"20","20b":"20","45a":"45","45b":"45","1b":"1"}   # panels sharing one drawing
panels=[dict(n=i+1, scene=sc, plate=PLATE.get(sc,sc), t=t, tEnd=(PANELS[i+1][0] if i+1<len(PANELS) else DUR),
             from_=round(t*FPS), to=round((PANELS[i+1][0] if i+1<len(PANELS) else DUR)*FPS),
             flap=fl, zoom=zm, screens=SCR.get(sc))
        for i,(t,sc,fl,zm) in enumerate(PANELS)]
import os
for p in panels:                    # a panel can only flap if the plates exist
    need = ["_oo","_os","_so","_ss"] if p["flap"]=="both" else ["_open","_shut"]
    if p["flap"] and not all(os.path.exists("public/rc/plates/clean%s%s.png"%(p["plate"],x)) for x in need):
        print("   scene%s has no mouth pair -- flap dropped" % p["scene"]); p["flap"]=None

# ---------------------------------------------------------------- lip flap
def flap(ids):
    """Open near each syllable peak, shut in the dip between, shut on silence.
    The reference is LOCAL (+/-0.35s) -- a global threshold either holds the
    mouth open through a loud line or never opens it on a quiet one."""
    N=round(DUR*FPS)+2; HOP=0.010
    lvl=np.full(int(DUR/HOP)+40, -99.0)
    for cid in ids:
        if cid not in C: continue
        e=env("public/"+[x for x in cues if x["id"]==cid][0]["src"], 0.025, HOP)
        base=int(round(C[cid]/HOP))
        for i,db in enumerate(e):
            k=base+i
            if 0<=k<len(lvl): lvl[k]=max(lvl[k],db)
    sp=lvl[lvl>-45]
    if not len(sp): return [False]*N
    FLOOR=np.median(sp)-24; Rw=int(0.35/HOP); st=False
    oh=np.zeros(len(lvl),bool)
    for i,v in enumerate(lvl):
        if v<FLOOR: st=False
        else:
            peak=lvl[max(0,i-Rw):min(len(lvl),i+Rw+1)].max()
            if not st and v>peak-7.0: st=True
            elif st and v<peak-13.0: st=False
        oh[i]=st
    out=np.zeros(N,bool)
    for f in range(N):
        k=int(round(f/FPS/HOP))
        out[f]=oh[k] if 0<=k<len(oh) else False
    i=0
    while i<N:                       # no state shorter than 2 frames
        j=i
        while j<N and out[j]==out[i]: j+=1
        if j-i<2 and i>0 and j<N: out[i:j]=out[i-1]
        i=j
    return [bool(v) for v in out]
fh=flap(["date_main","loop_open","loop_close"]); fm=flap(["p02","p03","p04","p06","p08","p11","p14","uh","p20"])
def hold(a, x, y):
    for f in range(int(round(x*FPS)), int(round(y*FPS))):
        if 0<=f<len(a): a[f]=True
    return a
fm=hold(fm, C["uh"], C["pingH"])     # he holds the "uh" until the ping
s14=[q for q in panels if q["scene"]=="14"][0]
fh=hold(fh, s14["t"], C["ping3"])    # open on the first ping, shut on the second
for f in range(int(round(C["ping3"]*FPS)), s14["to"]): fh[f]=False

# ------------------------------------------------------- SFX lettering
# comic-animation.md: every sound that plays gets a word, and every word on
# screen animates on its sound. Positions are the Figma text frames x1.5, so
# the live word lands exactly where she drew it. White on his dark trousers,
# near-black on the pale close-ups -- lettering inverts like the captions do.
W="#FFFFFF"; K="#141414"
SFX=[dict(id="ping1", t=C["ping1"], x=708, y=1299, col=W),
     dict(id="ping2", t=C["ping2"], x=705, y=1329, col=W),
     dict(id="ping3", t=C["ping3"], x=802, y=1350, col=W),
     dict(id="ping4", t=C["ping4"], x=726, y=1294, col=W),
     dict(id="ping5", t=C["ping5"], x=118, y=1286, col=K),
     dict(id="pingH", t=C["pingH"], x=42,  y=1554, col=K),
     dict(id="ping6", t=C["ping6"], x=860, y=1180, col=K)]

# ------------------------------------------------- the shivering dog
# A meme cut-in over Peter, in on the last ping of the burst and out on the
# cut away from her stare. Peter's head is pixel-identical on scenes 14-17
# (verified by diff), so one box holds for the whole stretch. The dog is sized
# to leave his hair showing around it -- that is what makes it read as HIS
# head and not as a sticker over the shot.
_s16 = [q for q in panels if q["scene"] == "16"][0]
_s17 = [q for q in panels if q["scene"] == "17"][0]
_n, _w, _h = (int(x) for x in open("public/rc/dog/meta.txt").read().split())
DOGSC = 0.66
# addressed in FRAMES, not seconds: the panel cuts on a frame boundary and a
# seconds comparison leaves the dog hanging over the next shot for one frame.
# It lands on the cut to her crossed arms -- the moment she stops gesturing
# and just looks at him -- and holds until we cut away from her stare.
DOG = dict(dir="rc/dog", n=_n, t=_s16["t"], tEnd=_s17["tEnd"],
           from_=_s16["from_"], to=_s17["to"],
           w=round(_w*DOGSC), h=round(_h*DOGSC), cx=815, bottom=930)
# Its own audio, kept low. The clip's track is 76% 2-4kHz -- camera hiss, not a
# whimper -- and that is exactly the band her consonants live in, so it gets the
# same duck the room tone gets and sits ~16dB under dialogue on top of that.
DOG_SRC = "/Users/sejal/Downloads/Dog Shivering Green Screen - Green Screens by CreatorSet (608p).mp4"
_dd = DOG["tEnd"] - DOG["t"]
subprocess.run(["ffmpeg","-v","error","-y","-t","%.3f"%_dd,"-i",DOG_SRC,"-vn","-ac","1","-ar","44100",
                "-af","volume=-8.6dB,afade=t=in:st=0:d=0.08,afade=t=out:st=%.3f:d=0.12"%(_dd-0.12),
                "public/rc/dogaud.wav"], check=True)
DOG["aud"] = "rc/dogaud.wav"
print("dog: %.2f -> %.2f  (%.2fs, %d frames at %dx%d) + audio at -8.6dB"
      % (DOG["t"], DOG["tEnd"], DOG["tEnd"]-DOG["t"], DOG["n"], DOG["w"], DOG["h"]))

# ---------------------------------------------------------------- captions
# scenes 5/6/12/13 are ONE shot -- the split screen. Its only clear area is the
# band between the desk line and the divider (measured: y 722..947), so all four
# captions share one position there. Figma's per-frame boxes put "On it." on the
# monitor stand, and a caption never sits on drawn furniture.
SPLIT=(540,862)
BOX={"1":(540,415),"1b":(540,415),"3":(540,415),"4":(539,415),"45a":(540,400),"45b":(540,400),"5":SPLIT,"6":SPLIT,
     "7":(540,415),"8":(540,415),"10":(539,415),"11":(540,415),"12":SPLIT,
     "13":SPLIT,"17":(540,415),"18":(540,414),"19":(538,416),"22":(539,454),
     "23":(539,454),"24":(538,452),"246":(539,454),"25":(541,401),"27":(540,373),"20a":(540,400),"20b":(540,400),"247":(539,454)}
PAN={p["scene"]:(p["t"],p["tEnd"]) for p in panels}
FG=[]; BG=[]
def add(lst,text,a,b,sc,half=False):
    x,y=BOX[sc]
    lst.append(dict(text=text,t=a,tEnd=b,x=x,y=y,scene=sc,half=half,
                    align="center"))
cue=lambda i: (C[i], C[i]+d([x for x in cues if x["id"]==i][0]["src"].split("/")[-1][:-4]))
for cid,txt,sc in [("p02","oh shit. my changes are uncommitted.","4"),
                   ("p04","Open the PR for the API fix.","5"),("onit","On it.","6"),
                   ("p06","uh huh. was it something crazy?","8"),("p08","right.","11"),
                   ("ai09","Permission to push?","12"),("p11","Run the tests.","13"),
                   ("p14","um, it's kind of complicated.","18"),
                   ]:
    a,b=cue(cid); add(FG,txt,a,b+0.24,sc)
# the remote-control beat, captioned in the two halves its two panels cut on
add(FG,"wait.",                        P03+0.10, ZOOM-0.05, "45a")
add(FG,"i can just remote control it.", P03+1.25, P03+d("peter_p03")+0.16, "45b")
# his last line, captioned in the three pieces its three frames cut on
add(FG,"your sister!",              P20+0.06, P20+LAUGH-0.03, "20a")
add(FG,"ahaha-",                    P20+LAUGH+0.02, P20+BACK-0.05, "247")
add(FG,"what did your sister do next??", P20+BACK+0.02, P20+d("peter_p20")+0.14, "20b")
for txt,v,sc in [("seriously.. who are you talking to??",WHO,"17"),("try me.",TRY,"19"),
                 ("wait, have you been approving every-",CATCH,"246"),
                 ("oh, hold on.",HOLD,"22"),("my AI just finished raising my PR.",PR,"22"),
                 ("been remote controlling it since the appetisers.",REMOTE,"23"),
                 ("well.. it's on auto mode and only pings me when it's done.",PINGS,"24"),
                 ("i mean, only a noob sits there approving every single step.",IDIOT,"25")]:
    add(FG,txt,v[0],v[1]+0.18,sc)
a,b=cue("loop_open"); add(BG,"my sister just books the whole thing.",a,b+0.12,"1")
a,b=cue("loop_close"); add(FG,"oh yeah, as i was saying..",a,b+0.10,"1b")
add(BG,"and you know what she did next??",NEXT[0],NEXT[1]+0.18,"7")
add(BG,"OH MY GOD you guessed it right!",GUESS[0],GUESS[1]+0.18,"10")
add(BG,"she just paid for all nine of us, upfront, non-refundable.",PAID[0],PAID[1]+0.16,"11",True)
def clamp(k):
    a,b=PAN[k["scene"]]; k["t"]=max(k["t"],a+0.02); k["tEnd"]=min(k["tEnd"],b-0.05); return k
FG=[clamp(k) for k in FG]; BG=[clamp(k) for k in BG]
for k in BG:                         # hers never shares the screen with his
    for f in FG:
        if k["t"]<f["tEnd"] and k["tEnd"]>f["t"]:
            if k["t"]<f["t"]: k["tEnd"]=min(k["tEnd"],f["t"]-0.06)
            else: k["t"]=max(k["t"],f["tEnd"]+0.06)
    if k["half"]: k["tEnd"]=min(k["tEnd"], k["t"]+(k["tEnd"]-k["t"])*0.55)
caps=sorted([k for k in FG+BG if k["tEnd"]-k["t"]>0.32], key=lambda k:k["t"])
for i in range(len(caps)-1):
    if caps[i]["tEnd"] > caps[i+1]["t"]-0.03: caps[i]["tEnd"]=round(caps[i+1]["t"]-0.05,2)

# a caption must land on clean paper -- never on drawn furniture or a face.
# (feedback-caption-placement: fully inside the scene's clear area.)
from PIL import Image as _I
_bad=[]
for k in caps:
    _pl = {q["scene"]: q["plate"] for q in panels}.get(k["scene"], k["scene"])
    a=np.asarray(_I.open("public/rc/plates/clean%s.png"%_pl).convert("L"))
    lines=max(1, -(-len(k["text"])//38))      # ~38 chars fit 960px at Lato 800/48
    top=int(k["y"]-34*1.5); box=a[max(0,top):top+63*lines, 60:1020]
    ink=int((box<170).sum())
    if ink: _bad.append((k["scene"], k["text"][:34], ink))
print("captions sitting on ink:", _bad or "none")

json.dump(dict(fps=FPS,width=1080,height=1920,durationInFrames=round(DUR*FPS),
    cues=cues, ducks=merged, ambDucks=ambd, panels=panels, flapHer=fh, flapHim=fm, dog=DOG,
    aiWake=round(C["p04"]+1.85,2), sfx=SFX,
    captions=[dict(k,t=round(k["t"],2),tEnd=round(k["tEnd"],2),
                   from_=round(k["t"]*FPS),to=round(k["tEnd"]*FPS)) for k in caps]),
    open("src/rc_cut.json","w"), indent=1)
print("\n%d panels   %d captions   %.2fs" % (len(panels), len(caps), DUR))
for p in panels:
    print("  %2d scene%-3s %6.2f -> %6.2f (%4.2f) %s" % (p["n"],p["scene"],p["t"],p["tEnd"],
          p["tEnd"]-p["t"], p["flap"] or ""))
