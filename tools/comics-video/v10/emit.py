#!/usr/bin/env python3
"""Emit the whole cut as data for Remotion.

Reads the same spec.py / timeline.py the ffmpeg build reads, so the two paths
cannot drift on timing. Run this after any change to either.
"""
import json, sys, os, pathlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spec, timeline, frames, captions

FPS = 30
T, END = timeline.T, timeline.END

# Resolved once, because it is needed in two places. Everything on a panel is
# authored as an offset into that panel's own clip; turning those into film
# times in more than one place is how the AI mark ended up parked in the middle
# of the diagram for the entire technical explanation.
PUSH_AT = round(spec.PUSH["at"]
                + next(r[1] for r in T if r[0] == spec.PUSH["frame"]), 2)
out = {"fps": FPS, "width": 1080, "height": 1920, "scale": 1.5,
       "durationInFrames": round(END * FPS),
       "panels": [], "audio": [], "captions": []}

def _sub_lines(text, times, frame=None, box=None, cx=360.0, cy=640.0):
    """The caption as LINES, each taking its first word's voice onset.

    Line breaking is captions.clean_lines(), which chooses the fewest lines that
    keep the block off the artwork -- see there for why. Wrapped in Python, not
    the browser, so the measure is the same font at the same size storyboard.py
    uses.
    """
    if spec.CAPTION_MODE != "lines":
        return [], cx
    if frame is not None and box is not None:
        lines, sx, sy = captions.clean_lines(text, frame, box, spec.SUB)
    else:
        f = captions.font(spec.SUB["size"])
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        lw = max(f.getlength(l) for l in lines) if lines else 0
        h = len(lines) * spec.SUB["line"]
        lo, hi = spec.SUB["safe_l"] + lw / 2, spec.SUB["safe_r"] - lw / 2
        sx = (spec.SUB["safe_l"] + spec.SUB["safe_r"]) / 2 if lo > hi else min(max(cx, lo), hi)
        tlo, thi = spec.SUB["safe_t"] + h / 2, spec.SUB["safe_b"] - h / 2
        sy = (spec.SUB["safe_t"] + spec.SUB["safe_b"]) / 2 if tlo > thi else min(max(cy, tlo), thi)
    out, k = [], 0
    for ln in lines:
        if k < len(times):
            out.append({"t": times[k], "text": ln})
        k += len(ln.split(" "))
    return out, round(sx, 1), round(sy, 1)

for i, (fr, st, clips) in enumerate(T):
    end = T[i + 1][1] if i + 1 < len(T) else END
    panel = {"plate": f"p{fr:02d}.png", "at": st, "until": end}
    if fr == spec.PUSH["frame"]:
        # the push-in: the monitor holds through the jargon, then the screen
        # becomes the frame for the diagram
        panel["push_at"] = PUSH_AT
        panel["bg"] = spec.PUSH["bg"]
    out["panels"].append(panel)
    for (src, a, b, off) in clips:
        g = getattr(spec, "CLIP_GAIN", {}).get((fr, src))
        out["audio"].append({"src": src, "startFrom": a, "endAt": b, "at": st + off,
                             **({"gain": g} if g else {})})

    if fr in spec.C:
        text, x, y, bw, al, hexc, ital, vo, sl, sh = spec.C[fr]
        onsets = [t for t in frames.reveal_times(fr, clips, st) if st - 1e-6 <= t < end]
        words = text.replace("\n", " ").split()
        times = frames.schedule(onsets, end)
        # Where each word sits once laid out. Comes from Python because the wrap
        # has to be Figma's wrap -- storyboard.py asserts the line count against
        # the node's box height, and re-wrapping in the browser with different
        # font metrics would break that agreement by a word.
        laid = captions.word_positions(text, bw, al, x)
        sub_lines, sub_x, sub_y = _sub_lines(text, times, fr, (x, y, bw, al))
        clear = spec.CLEAR_AFTER.get(fr)
        out["captions"].append({
            "at": st, "until": end,
            "cx": x + bw / 2.0, "cy": y + spec.H[fr] / 2.0,
            "color": "#" + hexc, "italic": bool(ital),
            "clearAt": (times[-1] + clear) if clear is not None else None,
            "words": [
                {"t": t, "w": w,
                 **({"x": lx, "cy": y + li * spec.LINE_H + spec.LINE_H / 2.0 + captions.DY}
                    if i < len(laid) else {})}
                for i, (t, w, (_lw, lx, li)) in enumerate(
                    zip(times, words, laid + [(None, 0, 0)] * len(words)))
            ],
            "mode": spec.CAPTION_MODE,
            "lines": sub_lines,
            "sx": sub_x,
            "sy": sub_y,
        })

    for ec in getattr(spec, "EXTRA_CAPTIONS", []):
        if ec["frame"] != fr:
            continue
        clip = next(c for c in clips if c[0] == ec["src"])
        _, cin, _, coff = clip
        base = st + coff - cin
        words = ec["text"].split()
        assert len(words) == len(ec["onsets"]), f"frame {fr}: {len(words)} words, {len(ec['onsets'])} onsets"
        out["captions"].append({
            "at": st, "until": end, "cx": ec["cx"], "cy": ec["cy"],
            "color": ec["color"], "italic": ec["italic"],
            "clearAt": (base + ec["onsets"][-1] + ec["clear"]) if ec.get("clear") else None,
            "words": [{"t": base + o, "w": w} for o, w in zip(ec["onsets"], words)],
            # the extra captions are subtitles too -- same band, same styling
            "mode": spec.CAPTION_MODE,
            **dict(zip(("lines", "sx", "sy"),
                       _sub_lines(ec["text"], [base + o for o in ec["onsets"]],
                                  cx=ec["cx"], cy=ec["cy"]))),
        })

amb = timeline.AMB
out["ambience"] = {"src": "ambience_bed.mp3",
                   **{k: amb[k] for k in ("lead", "out_at", "out_dur", "in_at", "in_dur", "tail")},
                   "end": END}
# same rule as PLAIN and SFX: offsets from the frame, resolved here
out["holdCaptions"] = []
for h in getattr(spec, "HOLD_CAPTIONS", []):
    base = next(r[1] for r in T if r[0] == h["frame"])
    out["holdCaptions"].append({**h, "at": round(h["at"] + base, 2),
                                "until": round(h["until"] + base, 2)})

# RING is authored as offsets into AITECH, not as film times -- absolute times
# here desynced silently twice when a frame upstream moved. Resolved once, here.
_p15 = next(r[1] for r in T if r[0] == 15)
_ring = dict(spec.RING)
for k in ("draw", "split", "fill", "exit_at", "done_at"):
    _ring[k] = {**_ring[k], "at": round(_ring[k]["at"] + _p15, 2)}
_ring["arc"] = [[round(a + _p15, 2), g] for a, g in _ring["arc"]]
_ring["checks"] = [[round(a + _p15, 2), ok] for a, ok in _ring["checks"]]
_ring["count_steps"] = [[round(a + _p15, 2), n] for a, n in _ring["count_steps"]]
out["sub"] = spec.SUB
out["screen"] = {"at": _p15,
                 "until": next(T[i + 1][1] for i, r in enumerate(T) if r[0] == 15),
                 "ring": _ring}
_sfx_base = next(r[1] for r in T if r[0] == spec.SFX_FRAME)
out["sfx"] = [{**g, "hits": [round(h + _sfx_base, 2) for h in g["hits"]]}
              for g in spec.SFX]
_c44 = next((i, st) for i, (fr, st, _c) in enumerate(T) if fr == 44)
out["credits"] = {**spec.CREDITS, "at": _c44[1],
                  "until": T[_c44[0] + 1][1] if _c44[0] + 1 < len(T) else END}
# the card owns that panel outright: same window, and the plate underneath is
# replaced by its background so the old white stamp does not show through
out["outro"] = {**spec.OUTRO, "at": out["credits"]["at"], "until": out["credits"]["until"]}
for _p in out["panels"]:
    if _p["at"] == out["outro"]["at"]:
        _p["bg"] = spec.OUTRO["bg"]
_marks = [{"frame": fr, "at": st, "until": (T[i+1][1] if i+1 < len(T) else END),
           **spec.AI_MARK_OVERRIDE.get(fr, {})}
          for i, (fr, st, _c) in enumerate(T) if fr in spec.AI_MARK_FRAMES]

# The push-in panel carries the mark twice -- centred while the monitor is up,
# then small in the corner once the diagram has the frame. Split before the
# merge below, because the two are in different places and must not merge.
_split = []
for m in _marks:
    P = spec.PUSH
    # PUSH_AT, not P["at"] -- P["at"] is an offset into the clip, and comparing
    # it against film times silently made this branch unreachable, so the mark
    # sat in the middle of the diagram for the whole explanation.
    if m["frame"] == P["frame"] and m["at"] < PUSH_AT < m["until"]:
        _split.append({**m, "until": PUSH_AT})
        if P["mark_after"]:
            _split.append({**m, "at": PUSH_AT, **P["mark_after"]})
    else:
        _split.append(m)
_marks = _split

# Adjacent panels that both carry the mark get ONE sequence, not two. Every
# sequence fades the mark in over 0.3s, so a cut between two mark panels made it
# blink out and back -- a white flash landing exactly on the cut. Merging keeps
# it continuous, which is what "hard cut, no interruption" has to mean for
# anything drawn on top of the plates rather than baked into them.
merged = []
for m in _marks:
    prev = merged[-1] if merged else None
    same_place = prev is not None and all(prev.get(k) == m.get(k) for k in ("cx", "cy", "size"))
    if prev is not None and same_place and abs(prev["until"] - m["at"]) < 1e-6:
        prev["until"] = m["until"]
        prev["spans"] = prev.get("spans", [prev["frame"]]) + [m["frame"]]
    else:
        merged.append(dict(m))

out["aiMark"] = {**spec.AI_MARK, "check_back": spec.CHECK_BACK, "frames": merged}
# PLAIN and SFX carry offsets from their own panel's start, so a retime of any
# earlier panel can never desync them. Resolve them here, once.
_p20 = next(r[1] for r in T if r[0] == 20)
_plain = dict(spec.PLAIN)
for k in ("track_at", "gates_at", "flag_at", "cross_at", "gone_at"):
    _plain[k] = round(_plain[k] + _p20, 2)
_plain["legs"] = [{**l, "at": round(l["at"] + _p20, 2),
                   "until": round(l["until"] + _p20, 2)} for l in _plain["legs"]]
_plain["checks"] = [[round(t + _p20, 2), n, ok] for t, n, ok in _plain["checks"]]
_h = dict(_plain["head"])
for k in ("sleep_at", "wake_at", "x_at"):
    _h[k] = round(_h[k] + _p20, 2)
for k in ("step", "run"):
    _h[k] = [round(v + _p20, 2) for v in _h[k]]
if not os.path.exists(os.path.join(spec.PLATES, _h["asleep"])):
    print(f'  ! {_h["asleep"]} missing -- the mask beat falls back to face.png')
    _h["asleep"] = None
_plain["head"] = _h
out["plain"] = {**_plain, "at": _p20,
                "until": next(T[i + 1][1] for i, r in enumerate(T) if r[0] == 20)}

pathlib.Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "cut.json")
             ).write_text(json.dumps(out, indent=1))
print(f"panels {len(out['panels'])} | audio {len(out['audio'])} | captions {len(out['captions'])}"
      f" | words {sum(len(c['words']) for c in out['captions'])} | {out['durationInFrames']} frames")
