#!/usr/bin/env python3
"""Caption reveal timing. `emit.py` depends on reveal_times() and schedule().

Also renders each frame as a run of sub-frames, one per revealed word -- that
half is left over from the ffmpeg build and nothing calls it now, but the
timing functions below are what put every word on its own voice.

A caption word appears the moment it starts being spoken and stays. Before the
first word the frame shows with no caption at all -- which is what makes the
dark-room beat work: the panel is up, silent and empty, and "..Peter?" only
arrives on the word.

Word times come from whisper but are AFFINE-ANCHORED onto the measured speech
run inside each slice: whisper drifts up to 0.4s here and its ends undershoot,
so raw times would drift the reveal off the voice by a word near the end of the
longer lines.
"""
import json, os, re, sys, bisect
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spec, captions
from env import env

BASE = os.path.dirname(os.path.abspath(__file__))
VO   = os.path.join(BASE, "..", "vo2")

_runs = {}
def runs(path, thr=-46, mingap=0.12):
    """Measured speech runs for a file, cached."""
    if path in _runs: return _runs[path]
    import subprocess
    d = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                              "-of","csv=p=0", os.path.join(spec.AUDIO,path)],
                             capture_output=True,text=True).stdout)
    out=[]; cur=None
    for t,lvl in env(os.path.join(spec.AUDIO,path), 0, d, 0.01):
        if lvl>thr:
            if cur is None: cur=[t,t]
            else: cur[1]=t
        else:
            if cur and t-cur[1]>mingap: out.append(tuple(cur)); cur=None
    if cur: out.append(tuple(cur))
    _runs[path]=out
    return out

_words = {}
def words(vofile):
    """Flat whisper word list for a VO file, in the timebase of the file we play."""
    if vofile in _words: return _words[vofile]
    if vofile in getattr(spec, "MANUAL_WORDS", {}):
        _words[vofile] = list(spec.MANUAL_WORDS[vofile])
        return _words[vofile]
    src = spec.VO_JSON[vofile]
    d = json.load(open(os.path.join(VO, src + ".json")))
    ws = [(w["word"].strip(), w["start"], w["end"])
          for s in d["segments"] for w in s.get("words", [])]
    tempo = spec.TEMPO.get(vofile, 1.0)
    if tempo != 1.0:
        ws = [(w, a/tempo, b/tempo) for w, a, b in ws]
    _words[vofile] = ws
    return ws

def reveal_times(frame, clips, fstart):
    """Timeline times at which word 1..N of this frame's caption appear."""
    if frame not in spec.C: return []
    text, x, y, bw, al, col, ital, vofile, (i0, i1), shift = spec.C[frame]
    clip = next((c for c in clips if c[0] == vofile), None)
    if clip is None: return []
    _, a, b, off = clip
    ws = list(words(vofile)[i0:i1])
    # splits are applied LOCALLY: inserting into the flat list would shift every
    # later index in spec.C by one.
    for (f, gi), parts in sorted(spec.WORD_SPLITS.items(), key=lambda kv: -kv[0][1]):
        if f == vofile and i0 <= gi < i1:
            tp = spec.TEMPO.get(vofile, 1.0)
            ws[gi-i0:gi-i0+1] = [(w, a/tp, b/tp) for w, a, b in parts]
    w0, wN = ws[0][1] + shift, ws[-1][2] + shift
    # anchor onto the measured run(s) inside the slice
    manual = vofile in getattr(spec, "MANUAL_WORDS", {})
    rs = [] if manual else [(s, e) for s, e in runs(vofile) if e > a + 0.01 and s < b - 0.01]
    if rs and wN > w0:
        o1, o2 = max(rs[0][0], a), min(rs[-1][1], b)
        k = (o2 - o1) / (wN - w0)
        if 0.6 < k < 1.7:                       # sanity: reject wild anchors
            m = lambda t: o1 + (t - w0) * k
        else:
            m = lambda t: t + (o1 - w0)
    else:
        m = lambda t: t
    return [fstart + off + (m(s + shift) - a) for _, s, _ in ws]

def schedule(onsets, end):
    """When each word appears, given the VO onsets and when the panel cuts.

    Words are shown one at a time, so a word whose slot is 2-3 video frames long
    reads as a flicker rather than a word -- one line was leaving its last word
    up for 7ms. Push each word forward to hold MIN_DWELL; only if that runs past
    the cut does the line get redistributed evenly, because redistributing walks
    the words off the voice.
    """
    n = len(onsets)
    if n == 0: return []
    lo, hi = onsets[0], end - spec.MIN_DWELL
    t = [lo]
    for o in onsets[1:]:
        t.append(max(o, t[-1] + spec.MIN_DWELL))
    if n > 1 and t[-1] > hi:
        span = max(hi - lo, 0.0) or (end - lo)
        t = [lo + i * span / (n - 1) for i in range(n)]
    return t


def build():
    import timeline
    T, END = timeline.T, timeline.END
    captions.DY = -1
    subs = []                                   # (png_path, start, end)
    os.makedirs(os.path.join(BASE, "render"), exist_ok=True)
    for i, (fr, st, clips) in enumerate(T):
        end = T[i+1][1] if i+1 < len(T) else END
        onsets = [t for t in reveal_times(fr, clips, st) if st - 1e-6 <= t < end]
        cuts = [st] + schedule(onsets, end)
        clear = getattr(spec, "CLEAR_AFTER", {}).get(fr)
        if clear is not None and len(cuts) > 1:
            cuts.append(cuts[-1] + clear)   # an extra state with nothing drawn
        plate = None
        for k, c in enumerate(cuts):
            nxt = cuts[k+1] if k+1 < len(cuts) else end
            if nxt - c < 0.005: continue
            clear = getattr(spec, "CLEAR_AFTER", {}).get(fr)
            blank = clear is not None and k == len(cuts) - 1
            p = os.path.join(BASE, "render", f"f{fr:02d}_{'x' if blank else f'{k:02d}'}.png")
            if not os.path.exists(p):
                captions.render(fr, 0 if blank else k).save(p)
            subs.append((p, c, nxt))
    return subs, END

if __name__ == "__main__":
    subs, END = build()
    print(f"{len(subs)} sub-frames, {END:.2f}s")

def phrase(times, words, maxw=4):
    """Collapse a word-by-word reveal into phrase chunks.

    One word at a time is right for a short line and wrong for a long one. The
    problem is not the pace of the words, it is that the reveal eats the panel:
    a caption clears the frame it is completed, so a 15-word line spent 4.64s
    building and left the COMPLETE sentence readable for 0.34s. Measured across
    the cut, the median complete line was up for 0.49s and 16 of 24 multi-word
    captions got under 0.7s. That is what Rohan and Anandhi were reading as
    "hard to follow" -- not the words being too fast, the sentence never being
    on screen as a sentence.

    Chunking buys the read time out of the build time, for nothing: the median
    goes 0.49s -> 0.97s with no extra film. Every chunk still lands on its own
    first word's voice onset, so it stays in sync -- it just stops asking the
    eye to track a cursor.

    Breaks at punctuation first, then every maxw words. A one-word caption is
    untouched: those already hold (median 1.1s) and the single word arriving on
    its own beat is the joke in several panels.
    """
    if len(words) < 2: return list(times)
    out, chunk = [], []
    for t, w in zip(times, words):
        chunk.append(t)
        if re.search(r"[.,!?;:\u2014]$|\u2026$", w) or len(chunk) >= maxw:
            out += [chunk[0]] * len(chunk)
            chunk = []
    if chunk: out += [chunk[0]] * len(chunk)
    return out
