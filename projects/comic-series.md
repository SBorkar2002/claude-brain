# Project: the comic series (*I Have No Idea What That Means*, channel AI FOMO)

State of every episode as of 22 Oct 2026, when the work account was being shut down.
How to build one: `../playbooks/comics.md`. What went wrong before: `../lessons/comics-traps.md`.

## Context

- Employer-brand channel **AI FOMO** (handle AI FOMO Lab) for Epifi/Workloom, run by Sejal
  (script, art direction, build) with **Prashasti** (PM: topic ideation, distribution, uploading),
  **Anandhi** (manager, creative review), **Mohit** (technical accuracy and script revisions),
  **Sumit** (CEO, occasional notes), **Harshit/Hrishabh** (viewer feedback). Zero product content.
- Reach by late Sep 2026: 4 videos out; the "intern video" (AJ, believed to be EP002 graph
  engineering) passed **30k Instagram views**, others 200 to 1,500; YouTube 500+. Sejal's rule:
  quote only the 30k publicly, never the weak numbers.
- Build repo: `~/Documents/Work/comics-video` (Remotion, local git, no remote; last commit 9 Sep,
  everything from EP002 on is uncommitted, 57 changed/untracked paths on 22 Oct). Scripts and skills: `~/Documents/Work/product-brain/video/youtube/comics/`.
- Figma file `comic` holds every board, one page per episode (work account).
- The three-bucket system (speed/cost/quality, each with a fixed outro question) shaped EP001 and
  EP002. **Retired from endings on 5 Oct** (no stamp, no outro); buckets are only a tracker label now.

## Cast in use

Peter (Dev 1, lead, messy hair) · Sameer (Dev 2, coffee) · Ken (Dev 3, glasses, `.env` tee,
AJ's manager from EP005) · AJ (Dev 4, intern, backwards cap) · the AI (one teal six-petal mark
for every AI) · the date (EP003 only). Voices and looks: playbook section 2.

---

## Episode table

All paths relative to `~/Documents/Work/comics-video/`. "Final" = the last render Sejal accepted.

| Ep | Term | Final file | Length | Composition | Built |
|---|---|---|---|---|---|
| EP001 | loop | `out/loop_v10_final.mp4` | 100.7s | `LoopV10` | 2 to 9 Sep |
| bumper | channel intro | `out/intro_v1.mp4` | 31.6s | `IntroV1` | 10 Sep |
| EP002 | graph engineering | `out/EP002 graph engineering*98s*.mp4` (name has a special dash; use the glob) | 97.8s | `GraphV1` | 10 to 18 Sep |
| EP003 | remote control | `out/EP003 remote control - v20 - 9x16 - 61.8s.mp4` | 61.9s | `RemoteControl` | 21 to 24 Sep |
| EP004 | /insights | `out/EP004 insights - v8 - 9x16 - 121.5s.mp4` (720x1280, the only non-1080 master) | 121.6s | `Insights` | 30 Sep |
| EP005 | system one model | `out/EP005 system one model - v8 - 9x16 - 193.6s.mp4`; Shorts cut `... - v9 shorts - 9x16 - 179.2s.mp4` | 193.6s / 179.2s | `SystemOne` | 8 to 12 Oct |
| (EP006?) | prompt engineering | `out/prompt_engineering_v3.mp4` | 134.4s | `PromptEng` | 20 Oct |
| short | make it better | not built | ~11s planned | none | script 14 Oct |

Episode numbering past EP005 is unclear from history.

---

## EP001 `loop`

- **Story:** Dev 2 (later named Sameer): "Long night. Left a loop running." Dev 1 (Peter) nods ("Riiiight. A loop."), thinks
  *I have no idea what that means*, privately asks his burnt-out AI. Technical answer (dense ring
  diagram), held blank face, plain answer (2D race map with checkpoints, Peter's sleeping-mask
  head at the start line, the AI mark racing, a fork where the short route misses a checkpoint and
  goes back). Peter cuts the AI off twice ("unless you give it a ste-"). Ends on a credits meter
  draining to 0 and loops into the opening line, one take split.
- **Final:** `loop_v10_final.mp4` (9 Sep). Caption system = white fill + black stroke, whole line,
  Figma positions. Mid-film entry card (series title centred, then rises; term, definition, AI
  credits instrument panel), not an end card. Uploaded to Drive `04 Cuts`; artifact pointed at it.
- **Built from:** `v10/spec.py` + `v10/timeline.py` (the only files to edit) then `v10/emit.py`
  writes `src/cut.json`. `captions.py`, `frames.py` (imported by emit), `storyboard.py`,
  `aimark.py`, `sleephead.py`, `keying.py`, `ambience.py`, `env.py`. Assets in `public/v10`.
- **VO:** Alec (AI), Ezra (Dev 1), Arlo (Dev 2), Dylan (Dev 3) per Sejal 2 Sep; explainer lines
  re-recorded with David. SFX: coffee slurp, keyboard, emoji-disintegration scream (~60%), sigh
  taken from the AI's own take.
- **Open (from Anandhi, never closed):** does the mark read as Claude-adjacent; does `STEPS DONE 0/2`
  read (she read it as weeks); is the look too close to the Singapore finance-creator reference;
  static-ness between frames. The repo `loop.md` table predates the shipped ending in places.

## Channel intro bumper

- Peter to camera ("you too? ... we made a whole channel for this"), Sameer spewing jargon behind
  him, ducked to barely audible. Open/closed plate pairs for both, flap off the RMS envelope
  (`src/intro_mouth.json`). End card in the loop card's style (dark bookend, white text, one teal
  rule). Figma frames under node 499-1483. Built 31.6s (script said ~12s).
- Also made then: YouTube profile picture (AI mark on dark, 1024px, eye right of centre) and banner
  (2560x1440, two devs at the corners, "AI FOMO" centred), both in `~/Documents/Work/comic folder`.
- Whether it was published: unclear from history.

## EP002 `graph engineering`

- **Story:** Ken scolds AJ ("you took all night for this??"), tells him to "just graph it next
  time", AJ thinks the signature line, asks his AI to do API/tests/docs/changelog "by ten
  tonight", waves off its dependency question ("whatever"), sleeps (snore), wakes at 8:50 AM to the
  ding. The AI: he could have been home by eight. Doors explainer: four people with ID badges
  queue at one ALL ENTRY door behind API being scanned (PLEASE WAIT); docs and changelog had their
  own coloured doors; sleepy-cat meme while they wait; doors close with `*thud*` and NO ENTRY
  stamps; then dots and arrows rename the picture ("dots for tasks, arrows for what depends on
  what"). Ends: "but what time is it?" then Ken "it's 9 am.. you said you'd be done by 10 pm
  yesterday but-" loops into frame 1.
- **Final:** the 98s render of 18 Sep ("Ken loop, printer-free bed"), roughly v45 of the internal
  numbering. Sejal asked for the old renders to be deleted and this one uploaded to Drive with a
  proper name. The repo `graph.md` header still says "cut v17 (87s)": stale.
- **Voices:** Ken = Thomas, AJ = Kai (`kai_re` for the shouts and "you're done??"), AI = David.
  Data is inline in `src/GraphV1.tsx` + `GraphExplainers.tsx`, mouths in `src/graph_mouth.json`,
  assets in `public/v10/graph`. Bed via `v10/ambience.py`. Snore is synthesised.
- **Open:** Mohit's sign-off on panels 10 and 25 (AJ parroting "graph it or something") was
  pending; hidden dependencies deferred to a separate quality episode.

## EP003 `remote control`

- **Story/format test:** Peter on a date drives his office machine from his phone under the table
  while she tells a story he isn't hearing; her phone pings too ("which noob sits there approving
  every step"). Drops the IHNIWTM signature, no term drop, no end card. Loop: one take of hers cut
  three ways ("oh yeah, as i was saying.." closes, "my sister just books the whole thing." opens).
  Last frame pixel-identical to the first.
- **Final:** v20 (24 Sep), 61.9s. Restaurant bed at -44 dBFS ducked ~7 dB under every voice;
  shivering-dog meme over Peter (scale 0.66); one push-in (scene20, 1.00 to 1.19) plus the
  scene4.5 bridge push-in (1.00 to 1.35) on "wait. i can just remote control it" (Mohit's note:
  the term needed emphasis over "auto mode").
- **Build:** `v10/rc_audio.py` then `v10/rc_plates.py` then `v10/rc_emit.py` writes
  `src/rc_cut.json`; dog keyed by `v10/rc_dog.py`. Figma page `remote control` (scene1..scene28,
  plus 4.5, 24.5, 24.6, 24.7). Voices: Peter = Eric, the date = Vanessa, AI = David.
- **Open (known defects):** her VO is mixed tempo (files cut from `mono_fast`/`tail_fast` at
  ~1.25x, later splices at 1.15x; unify by atempo 1.15/1.25 and rescale cut points); Peter's "Run
  the tests" / "it's kind of complicated" take is a different-sounding Eric (155 Hz vs ~120 Hz);
  scene19 ("try me") has no mouth pair. Staged Drive tree in `out/DRIVE UPLOAD/EP003 - REMOTE CONTROL`;
  whether the cut reached `04 Cuts` is unclear.
- Lesson that came out of the review thread: diff the plates before rewriting (25 vs 26 = 0 px).

## EP004 `/insights`

- **Story:** Sameer asks AJ if his AI was less brutal than his with /insights; AJ bluffs, asks his
  AI, gets actionable suggestions (file is `agents.md`, the AI indicts itself first in a
  two-column "wrong approach" beat). Peter is the bystander. Structural loop back to Sameer's line.
  Revised by Mohit.
- **Final:** v8 (30 Sep), 121.6s at **720x1280**; delivered to Drive (46 plates, 42 VO takes, cut).
  Captions are BAKED into these plates (older approach). Built by `v10/ins_emit.py` into
  `src/ins_cut.json` + `ins_texts.json` + `ins_keystrokes.json`. Repo `insights.md` is the frozen
  record of what shipped.
- **Open:** 121.5s vs 2:00 target (dropping MEMORABLE MOMENT, panels 31 to 35, gets ~1:51; held
  for Mohit); the "horizon" beat (frames 32 to 34) cut for runtime; `frame3` has no mouth pair so
  AJ doesn't flap replying to Sameer; `frame35` carries a stale hidden text layer in Figma.
- Several skill rules were born here: three text styles, screen text by measurement, mark
  placement by measurement, full hide-all exports, ask before merging frames.

## EP005 `system one model`

- **Version produced:** Prashasti's script (80,000 support tickets, later customer PDFs; budget
  runs out; doctor/nurse triage explainer; playground how-to; definition slate) on Sejal's 61-frame
  board (Figma page `system one model`). Sejal's own v3 (inversion engine) and Mohit's v2 (blame
  turn) were not produced. Ken is AJ's manager; AJ = Jet, AI = David, Ken = Thomas.
- **Final:** v8 (9 Oct, 193.6s) is in Drive `04 Cuts` (v6 moved to `old`). v9 Shorts cut (12 Oct,
  179.2s) fits the 3:00 Shorts cap by cutting exp50/aj_f49/f48 and trimming holds; whether v9 was
  uploaded is unclear.
- **Build:** `v10/s1m_audio.py` (cuts + `PDF_SPLICES`) then `v10/s1m_emit.py` writes
  `src/s1m_cut.json` + `s1m_caps.json`; `v10/s1m_cats.py` keys banana/happy cats;
  `v10/s1m_sfx.py` synthesises UI sounds; `v10/s1m_verify.py <mp4>` contact sheet. Code
  `src/SystemOne.tsx` + `src/S1mExplainers.tsx` (720-space, stage x1.5). 77 plates.
- **Open:** runtime far over budget even as the Shorts cut; Drive still holds v6-era office bed
  mp3, `ai_f13.wav` and the f34 still; board flags (f48 order, f42 stray text, captions in top
  90px on f14 to f16/f25 to f26, right-rail captions on f03/f57/f60); Sumit's 8 Oct note that the
  ending's last examples get mixed up; definition check on what "system one" means.

## Prompt engineering (Script A, "Wait, What?")

- **Story:** office hackathon; Peter vs AJ on the same task (Sumit's ask: the intern wins because
  he prompts better). AJ's prompt contract card (GOAL / CONSTRAINTS / OUTPUT / FAILURE), Peter's
  212-feature OfficeOS, leaderboard where Peter's avatar hard-swaps to the crying-dog meme.
- **Final:** `out/prompt_engineering_v3.mp4` (20 Oct), 2:14, with leaderboard avatars, the dog
  swap and the dog's sniffing at 40% (with a "sniff" word). Figma page `Prompt engieering`
  (frame1..frame36).
- **Build:** `v10/pe_audio.py` (Peter = Eric, AJ = Jet, AI = David; `ai_card.mp3` replaces
  37.3 to 46.7s of the long take because "constraints" was mispronounced) then `v10/pe_emit.py`
  writes `src/pe_cut.json`; `v10/pe_avatars.py`; code `src/PromptEng.tsx` + `src/PeScreens.tsx`.
  Studio on port 3335. This is the most current template for a new episode.
- **Open:** f31 (cost screen) plays silent 3.4s because no AI line exists for script panel 18; AJ
  says "Thank you" but the caption reads "ty." (Figma text kept); no loop panel / "NEXT HACKATHON"
  ending, the film ends on f35/36; not uploaded to Drive as far as history shows; the repo
  `prompt-engineering.md` is an OLDER draft (free lunch, Peter vs AJ, 23 panels), not what was built.

## Shorts experiment: `make it better`

- Started 14 Oct: do 7 to 15s looping Reels/Shorts work? AJ says "better" until the AI's button is
  back to version one, he calls it perfect, asks again. Built entirely from existing graph plates
  (`s12, s32, s18, s23, s19, s21`) plus code-drawn screens; one "Done." take used four times.
  Holds 0.3 to 0.5s (not the ~1s episode rule). Script: `scripts/short-make-it-better.md`.
- **Not built.** Open decision: may panel 6 break the greyscale+teal palette with full colour?
- Backup idea `standup` (~8s, Ken asks AJ what he did yesterday; needs a new Ken plate).

---

## Backlog and ideas discussed

| Idea | State |
|---|---|
| `subagent` (AJ/Dev 4 + his AI, accumulation ending) | script only; its AI lines use the retired "sir/Certainly" register, rewrite per the AJ AI rule |
| `context window` (Ken presents, Sameer drops the term, Peter asks; loop on "context window blew up") | draft v2, 6 Oct |
| `skill` (Peter uses Ken's skill file, then becomes the author) | script only; still has the old stamp/outro ending |
| Sejal's own `system one model` v3 (inversion: AI reads AJ his fastest answers) | script only |
| Hidden dependencies (a step silently uses stale input) | deferred from EP002 as a quality episode |
| Harness / "~5% reveal" | left out of prompt engineering on purpose; its own episode |
| `vibe coding` | mentioned as sharing PE's skeleton (senior vs AJ on one task); script existence unclear |
| AIs that share a room across split screens ("don't listen to him") | unused cast device |
| Peter's AI degrading over the series (answers in three words by ep 15) | unused arc |
| Community replies in the AI's sassy voice | Sejal asked for this on 17 Oct for real comments |

**Unresolved series-level questions:** square vs 16:9 vs native 9:16 master (9:16 won in
practice); Reels vs ~2-min YouTube (Sumit prefers YouTube); product mentions (channel says zero);
who owns the nine-post distribution cascade; Anandhi's "know the next 4 to 10 ideas" never formalised.

**Note for a future session:** after the account shutdown the Drive, Figma, Slack threads and
artifacts are likely unreachable. Everything needed to rebuild or extend an episode locally is in
`~/Documents/Work/comics-video` (plates, VO, SFX, emitters) and the product-brain comics folder clone.
