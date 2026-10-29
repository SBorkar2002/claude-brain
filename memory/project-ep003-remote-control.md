---
name: project-ep003-remote-control
description: "EP003 \"remote control\" — full build state, decisions, file map and the traps that cost hours"
metadata: 
  node_type: memory
  type: project
  originSessionId: 71402597-d5cb-41f7-a481-6f5da322f80e
  modified: 2026-09-22T13:58:39.642Z
---

EP003 of *I Have No Idea What That Means* (AI FOMO), term = **remote control**.
Built 21–23 Sep 2026. ~61.8s, 9x16, 31 panels from 32 Figma frames.

**Story.** Peter (Dev 1, the lead) is on a date, remembers his changes are
uncommitted, and drives his office machine from his phone under the table while
she tells a story he isn't listening to. Her phone pings too — she's been doing
the same thing, better. Loops: his *"what did your sister do next?"* is answered
by *"oh, you want to know what she did next?"* → cuts to *"my sister just books
the whole thing."* The loop take (23 Sep, 17:37) is ONE recording cut THREE ways at 1.81 and
3.81, both mid-gap: "oh yeah, as i was saying.." closes the film, "my sister
just books the whole thing." opens it, "doesn't ask anyone." is panel 3. It has
to be one generation or her pitch steps across the join. The LAST panel is
scene1 again, so the last frame and the first frame are PIXEL-IDENTICAL and the
loop has no visual cut at all. "as i was saying" sits at the END on purpose:
at the start it would spend the scroll-stopping window on a phrase a cold
viewer cannot parse. **Format deliberately drops the IHNIWTM
signature** — no term drop, no polite blank face, no stamp, no bucket outro.

**Where it lives**
- Build: `~/Documents/Work/comics-video` — `src/RemoteControl.tsx` + `src/AIMark.tsx`,
  data in `src/rc_cut.json`, emitted by `/tmp/emit_rc.py`; audio built by
  `/tmp/build_final.py`. Studio: `remotion studio src/index.ts --port 3000`.
- Script + prompts: `product-brain/video/youtube/comics/scripts/remote-control.md`
- Figma page `remote control`, node **619:2**, file `UM66oBdfGGPHkENjoPpN1S`
  (scene1..scene28). Artifact: claude.ai/code/artifact/0c020fc3-6696-49c5-8a36-966acac661c9
- Plates in `public/rc/plates/` — `sceneN.png` raw, `cleanN.png` with the baked
  caption masked out, `cleanN_open/_shut` mouth variants, `clean11_{oo,os,so,ss}`
  for the two-shot where both mouths move.

**Locked decisions**
- Peter **1.10x**. Her VO is MIXED and this is a known defect: everything cut
  from `mono_fast.wav` / `tail_fast.wav` is at **~1.25x** (built when she asked
  for 1.25 and never rebuilt at 1.15), while every take spliced in since is at
  **1.15x** via `tseg`. Measured against the untouched sources (a.wav, c.wav):
  41 matching words run 17.60s raw vs 14.16s in mono_fast = 1.24x. To unify,
  atempo the two fast files by 1.15/1.25 and divide every cut point into them
  by the same number — the scaling is exact whatever the true tempo was.
- **scene4.5** (Figma node 647:551, saved as `scene45.png`) is the BRIDGE: he
  stops talking, looks down at the phone on the table, THEN we are in the
  office. Held 1.80s. Its drawn "..." is kept baked — it carries no VO and a
  live caption's 5px stroke turns three dots into three rings. `P04`/`onit`
  are derived from that beat, not typed. It carries **Peter's thought "wait. i
  can just remote control it."** — the episode's term, at 7.4s, on the man doing
  it. Before that line the term appeared ONCE, at 41s, in HER mouth, against
  three mentions of auto mode / approving. The frame splits into 45a (as drawn)
  and 45b (push-in 1.00->1.35) which starts inside the take's own 0.83s pause.
  Its baked "..." is now MASKED — it meant "he says nothing" and he no longer
  does. No flap: a thought does not move his mouth. The export is 1082px wide (the base
  rect starts at x=1) — crop to 1080 before saving.
- Frames play in Figma order 1→28, with 4.5 between 4 and 5. scene2 and scene9 are mouth variants, not
  panels. **Order matters**: 2/3 have the phone ON THE TABLE, 11 has it in his
  hand under the table.
- AI mark is asleep (closed lid, slow breathe) until 1.85s into his first
  request, then wakes with a pop. Locked position on all four split frames:
  monitor (527,431) size 185; phone (535,1366) size 140 rot **-8.0°**.
- `AT THE OFFICE` in Geist Mono above the monitor on every split frame.
- Her story carries NO caption while he or the AI speaks; elsewhere it starts
  and is cut short (~55%) to read as background.
- **She never goes silent.** The new take supplies only "my sister just books
  the whole thing / doesn't ask anyone"; from there the OLD take carries on
  ("doesn't say a word .. completely normal. and you know what she did next??")
  as ONE unbroken segment `M2c` = M 7.95->16.20. Peter and the AI talk over her
  and she ducks, but a duck overlapping the ramble is floored at 0.20 so she
  stays audible. Never replace her continuation with silence. `gb` is 3.10s —
  it grew to buy room for his remote-control beat, and it still falls ONLY
  while he is talking. Her rant runs
  UNBROKEN through the 1am confirmation (longest internal silence 0.28s); the
  one pause `gb` (2.35s) comes AFTER "like it's completely normal.", so "and
  you know what she did next??" lands isolated. A pause mid-anecdote is wrong.
- The two halves of the last line are butted with NO gap — peter_uh carries
  0.14s of tail and peter_p20 0.08s of head, which IS the take's hesitation.
  Any gap on top of that and the punchline sounds spliced.
- **Restaurant ambience** is a BED at -18dB on the source (-44 dBFS in the mix,
  22dB under dialogue). Built by `rc_emit.build_ambience`: it picks the calmest
  window of the 147s source, then folds the tail onto the head over 1s so the
  film's loop point is seamless. It runs unbroken across the split screens —
  the office is a place he is looking at, not a place he is in. It DUCKS ~7dB
  under every voice (hers included, 85% of the film) — restaurant babble is the
  worst masker there is for dialogue because it IS dialogue, same band, same
  rhythm. At -44 dBFS it needed no duck and was inaudible; at -36, where you
  can hear it, it has to move.
- **The dog clip's audio is not a dog.** 76% of its energy is 2-4 kHz with
  nothing under 1 kHz: camera hiss / a high whine, not a whimper. 2-4 kHz is
  where speech consonants live, so adding it fights the dialogue. Left out.
- Her line 4 is now "well.. it's on auto mode and only pings me when it's
  done." — "auto mode" sits NEXT TO the "which idiot" punchline on purpose, not
  in the "remote controlling" line, which is where the episode's term lands.
- **The shivering-dog meme** (keyed by `v10/rc_dog.py` to public/rc/dog/NNN.png)
  cuts in over Peter on the scene16 cut — the moment she crosses her arms — and
  out on the cut away from scene17. Scale 0.66 on purpose: his HAIR still shows
  around the dog's head, which is what makes it read as his head and not a
  sticker. Peter is pixel-identical on scenes 14-17, so one box holds. No
  entrance animation; it arrives on the same hard cut as the shot.
- **The ending resolves now** (Anandhi's diagnosis, 23 Sep: the payoff was
  missing because her scene-17 question "who are you talking to??" was never
  answered). Order: 25 her punchline on PETER → 26 HIS ping gives him away →
  the two-shot: **scene24.7** (665:607) is the same two-shot again with PETER's mouth OPEN —
  his nervous laugh — so 247/245 are a pair for HIM on that shot (ink 356 vs
  110) and the laugh flaps on its own three "ha" pulses. **scene24.5** (660:558) is her staring, mouth SHUT — a ~1.5s
  beat, no line — and **scene24.6** (663:583) is the same frame with the mouth
  open. They are a real open/shut PAIR (ink 110 vs 303), so the question
  flaps. "wait, have you been approving every step?" → 27 he cuts in.
  Her line is NOT cut short — it is the answer to the film's open question.
- **The "uh" plays TWICE** — once on the scene20 push-in, once at the head of
  "…what did your sister do next?", which is where the take originally had it.
  Panel 27 starts on the first one.
- Pings follow the lettering she drew: one on scene11, two on scene14, one on
  scene15, one on scene18, her phone during the push-in on scene20.
- Only ONE push-in: scene20 (he sweats, says "uh"), 1.00→1.19, snapping back on
  the ping. NOT on "it's kind of complicated".
- The "uh" was hiding at the head of the `…what did your sister do next?` take —
  split out and moved to after "try me."

**Traps that cost real time — do not repeat**
1. **Never resample to analyse.** Loading her VO at 16 kHz and writing back at
   44.1 destroyed all consonant detail. Analyse at any rate; APPLY at native.
2. **Never index her lines by position in the detected run list.** Removing a
   breath re-splits the envelope and silently shifts every caption and cue.
   Address lines by STRUCTURE (last line of group 0, first of group 1, …).
2a. **Scenes 5/6/12/13 are one shot** (the split screen) and share ONE caption
   position, `SPLIT=(540,862)`. Its only clear area is y 722..947, between the
   desk line and the divider — Figma's own box for scene6 puts "On it." on the
   monitor stand. rc_emit now fails loudly if any caption lands on ink.
3. **A caption must never outlive its panel** — clamp it, or it bleeds into the
   next scene.
4. **Duck windows closer than 0.55s must merge**, or her level pops back to full
   between two of his lines and reads as a spike.
5. **A panel only flaps if a real open/shut pair exists on disk.** Without the
   guard the plate 404s and the frame renders blank (this ate the "try me" frame).
6. **Derive tail cuts from measured line ends.** A hardcoded cut plus a line that
   moved = her talking over the silent beat frame.
7. `date_main` must be wrapped in a `<Sequence>`; unwrapped it plays from frame 0.
8. Mouth patch boxes must cover the WHOLE open-mouth shape or the boundary clips
   it and leaves a black blob.
9. Screen detection finds the wrong region when a finger occludes the screen —
   lock the mark position, don't re-detect per frame.
10. **Never infer which drawn frame is mouth-open — MEASURE the ink.** An open
    mouth is a filled oval, a closed one a thin line, so the dark-pixel count
    settles it. Her two-shot pair was built backwards for days on an assumption.
9a. **The same tempo multiplier does NOT equalise pace.** ElevenLabs picks its
    own delivery speed per generation, so a take at the right atempo can still
    sound 30% slower than the take beside it. Measure SYLLABLES/SEC across her
    whole track, not the multiplier. `tseg(..., tempo=)` overrides one take —
    T3p needed 1.28x where everything else is 1.15x.
10a. **A word seed can fall OUTSIDE its own voiced run.** Whisper undershoots
    the start of a word after a long silence, so the midpoint lands in the gap.
    rc_emit snaps an unowned seed to the nearest unclaimed run — do not "fix"
    this by moving the cut point.
11. **Never address her lines by index into the detected run list, or by group
    structure.** Removing a breath re-splits the envelope; a replaced take
    changes the group count. Seed on a WORD, take the phrase edges from the
    envelope, and let the build STOP by name when a word goes missing.
12a. **Any long stretch of her rambling needs its OWN word seed** (`normal` ->
    RAMBLE). Without it the growth loop finds no closer owner and hands those
    runs to NEXT, so "and you know what she did next??" starts six seconds early.
13. **SFX lettering is pulled out in Figma, not inpainted.** Hide the text
    nodes, re-export, restore. Painting them out of a plate smears any line the
    glyphs crossed — the strokes sit on top of the art, so there is nothing
    underneath to recover.

**Build scripts (in the repo, re-runnable in this order)**
- `v10/rc_audio.py`   her VO: splices, tempo, structural gaps
- `v10/rc_plates.py`  every plate: caption masks, mouth variants (ink-decided)
- `v10/rc_emit.py`    the cut: cues, panels, ducks, flap, captions, SFX words
Then `remotion render src/index.ts RemoteControl out/….mp4`.

**Still open**
- Peter's voice changes at "Run the tests" / "it's kind of complicated" — that
  take is **Eric, 155 Hz**, against ~120 Hz for the rest of him. Either re-record
  those two with his real ID or redo the rest with Eric.
- scene19 ("try me") has no mouth pair, so it can't flap.
- Captions are rendered live from the VO; the plates' own text is masked out.
