# Playbook: comic video production (*I Have No Idea What That Means*)

How to make the NEXT episode of Sejal's comic shorts, from term to delivered render.
Distilled from Aug to Oct 2026 (EP001 to EP005, prompt engineering, the channel intro).
Episode state lives in `../projects/comic-series.md`; the expensive mistakes live in
`../lessons/comics-traps.md`. Read both before touching a build.

Every rule below was learned on a real episode; the parenthetical says which one.

---

## 0. The format in one screen

| | |
|---|---|
| Channel | **AI FOMO** (handle AI FOMO Lab), employer-brand, **zero product content** |
| Series | *I Have No Idea What That Means*: someone drops an AI/eng term, a dev nods, then privately asks his AI. One term per episode. |
| Master | **9:16, 1080x1920, 30 fps.** Plates are authored at 720x1280 and the stage is scaled 1.5x. |
| Length | 1:00 to 2:00 target. Hard ceiling **3:00** (YouTube Shorts limit; EP005 needed a 2:59 cut). |
| Look | Greyscale comic + exactly one accent, teal `#03A6CF`. Colour allowed in explainer animation only. |
| Motion | Panels are still and HARD-CUT. Only things pulled out of the plate move: screens, explainers, captions, SFX words, mouths (by plate swap), the AI mark. |
| Audio | ElevenLabs VO per character, office/room bed, SFX. Every sound gets a word on screen. |
| Build | Remotion 4.0.239 in `~/Documents/Work/comics-video`, driven by a Python emitter that writes one JSON per episode. |

Sejal's standing style rules that apply to everything here: **no em dashes** in any on-screen
text, Figma text or layer names (check after every build); never overlap elements; never tilt
cards; never spend paid credits (Figma AI images, Higgsfield) unless she opts in.

---

## 1. Where things live

| What | Where | Survives the account shutdown? |
|---|---|---|
| Remotion build, all plates, all audio, all emit scripts | `~/Documents/Work/comics-video` (local git repo, no remote) | Yes, if the Mac does. Not pushed anywhere. |
| Raw downloads, character sheets, YT banner/profile PNGs | `~/Documents/Work/comic folder` (`CHARACTERS.png`, `peter.png`, `AJ.png`, `Ken.png`, `Sameer.png`, `blank face.png`, `sleep.png`, per-episode subfolders) | Local only |
| Skill files, cast, appearance prompts, per-episode scripts, PIPELINE, LINKS, DESIGN-SPEC | `~/Documents/Work/product-brain/video/youtube/comics/` (clone of the work org's `product-brain` repo) | Local clone yes; the GitHub remote is the work org's, assume no access |
| Storyboards, VO takes, cuts, shared SFX, AI mark, character assets | Work Google Drive, series root `I Have No Idea What That Means` (inside `YouTube`) | **No.** Work account. |
| Panel boards | Figma file `comic` (one page per episode: `loop`, `graph`, `remote control`, `/insights`, `system one model`, `Prompt engieering` [sic]) | Work Figma, assume gone |
| Script review pages | claude.ai Artifacts | Gone with the account |

If a new Drive is set up, mirror this folder shape (decided 28 Aug, refined 4 Sep):

```
<series root>/
  01 Scripts/                 archival export of each approved script
  02 Storyboards/EPxxx - TERM/
      Frames - no captions/   clean plates
      Frames - with captions/ plates with the full caption laid in (v10/storyboard.py)
  03 Audio/EPxxx - TERM/
      VO/                     the takes as played in the cut
      Source takes/           the raw ElevenLabs downloads
  04 Cuts/                    finished videos (old versions in 04 Cuts/old)
  SFX/                        SHARED library, series root, never per episode
  AI mark/                    transparent PNG + SVG
  Characters/  Characters/Expressions/
```

Episode folder names look like `EP001 - LOOPS`. The tracker sheet is the published log (no
separate log folder). Every external link goes into the repo's `LINKS.md` so no session has to
ask Sejal for a URL.

**Three copies of every script, on purpose:** repo `.md` = frozen record, artifact = review
surface, Drive `01 Scripts` = archive. The repo copy is the one production reads from.

---

## 2. Cast lock and art direction (decided, do not relitigate)

### The four devs (personalities locked 31 Aug, look locked 2 Sep, names from Sep)

| Name | Dev | Identifier | Garment value (tone ladder) | Voice (ElevenLabs) | His AI's register |
|---|---|---|---|---|---|
| **Peter** | Dev 1, the lead, late 30s | messy spiky dark hair | light-mid grey collared shirt, sleeves up | **Eric** "Uninterested and Fast" (EP001 used Ezra) | burnt out: flat, minimal, brutal |
| **Sameer** | Dev 2, never sleeps | coffee cup, dark-circle lines | mid-dark crew sweatshirt, NO hood | Arlo on EP001; later takes unclear | manic: does six things when asked for one |
| **Ken** | Dev 3, careful senior / AJ's manager | round glasses; since EP005 a `.env` tee | white / very light | **Thomas** "Fast and Raspy" (sp84 s40 sb71) | over-documents, gets interrupted |
| **AJ** | Dev 4, the intern | backwards cap | near-black hoodie | **Jet** (`JOUWtlfdRuffI74LLmML`) since EP005; **Kai** on EP002 | plain, dry, blameless (see below) |
| The AI (all four) | screen only | the six-petal mark | teal | **David** "Polished and Full" (`rWV5HleMkWb5oluMwkA7`, sp100 s32 sb51) | per owner |
| The date (EP003 only) | guest | dress darker than Peter's shirt, no lipstick/nails | | **Vanessa** "Beach Girl" | n/a |

Lightest to darkest garment: Ken/Dev 3, Peter, Sameer, AJ. Value, not hue, separates them at
thumbnail size. Per-character reference sheets (10 Sep) are in `~/Documents/Work/comic folder`.
Casting is free: use whoever the joke needs. Voices in the original Character Sheet are the
source of truth when reachable; the table above is what the shipped takes actually used.

**AJ's AI voice (STANDING, 6 Oct):** the graph-engineering register. Short plain sentences,
"On it.", asks the one question that matters, dry understatement ("Though you could've been home
by eight."), never gloats; its punchline is the user's own words thrown back flat. Never "sir",
"Certainly", "instantiate", "dispatched". `cast.md` still says "absurdly formal, calls him sir":
that is stale.

**Runners are optional:** Peter's AI "Go to sleep." and AJ's AI `bruh` are flavour, not required.

### The look

- **Neat comic register** (Woke Salaryman family), generated with **ChatGPT (GPT Image)**. The
  crude/xkcd register was rejected 4 Sep; don't re-propose it. One generator only, because style
  drifts between models. (Higgsfield was used for non-character art such as the race track; that
  is the only carve-out.)
- Flat greyscale, thick uniform black outline, flat grey fills, no gradients/texture/shading.
- Faces: two small solid dot eyes set wide and just below the head's midline, NO NOSE (the big
  empty face is the signature), one short low mouth line, small ears. **Eyebrows only on a strong
  beat**, none at rest (EP003 change; older sheets still draw them).
- Speaking character's mouth is slightly open; everyone else a line.
- Backgrounds recede: palest grey in the frame AND drawn in thin pale lines, never the heavy
  outline. Sparse: only objects the character touches. Blank by default.
- Never: ties, blazers, lanyards, colour, text/lettering/speech bubbles in generations.
- **Every monitor and phone screen is generated EMPTY.** The AI mark and all screen content are
  composited live.
- The polite blank face (eyebrows raised, unfocused eyes, small closed smile, slight tilt) is the
  series' signature image and thumbnail.

### The AI mark (the AI's only body)

- Six petals: ellipses `cx 50 cy 25 rx 14.5 ry 25`, each rotated `i x 60deg` about (50,50).
  White eye ring r17, teal pupil r11. viewBox padded to `-6 -6 112 112` (tight box clips petals).
- **Eye rests RIGHT of centre: centre x = 50 + gaze x 9 = 59 (gaze=1).** A centred eye is wrong;
  it was exported wrong twice (EP001 PNG, the YouTube profile PNG).
- Expression params: `gaze` (-1 looks back), `squint` (pupil ry x (1 - squint x 0.62)), `wide`
  (pupil x (1 + wide x 0.25)).
- A symmetric mark cannot turn its head and an eye shift is invisible at 48px: to "look", move the
  whole mark.
- Pulse on every screen it occupies: `scale = 1 + sin(t x 2.1) x 0.035`. Bigger/faster reads as
  alarm (EP002). Asleep variant: closed lid, slower shallower breathe, wakes with a pop (EP003).
- Never on title cards, never during an explainer. Centred on blank monitors, small in a corner
  when a screen is busy.
- Code: `src/AIMark.tsx`; export: `python3 v10/aimark.py` (writes `v10/assets/ai-mark.png/.svg`,
  gaze=1).
- Anandhi has twice raised that the mark may read as Claude-adjacent. Unresolved risk.

### Colour in explainers

Explainers may use colour and absurdity ("keep it absurd while educating", Sejal 3 Sep). Keep
it narrow: one hue for working, one for passed, one for failed (appearing once). ID-badge blue
and orange worked next to teal (EP002). Brand fonts in explainers only: **Mona Sans** (display),
**Plus Jakarta Sans** (chrome), **Geist Mono** (values/screen text). Captions stay Lato.

---

## 3. Writing the script (rules that keep getting broken)

Source of the full method: `skills/comic-script-writer.md` in the comics folder. The live rules:

1. **Premise:** someone uses a word, the hero nods to save face, then asks the machine privately.
   Signature line *"I have no idea what that means."* fires once, as a thought caption, near the
   top. (EP003 deliberately dropped the signature; that was a one-off format test.)
2. **The comedy is a bracket, the middle teaches straight.**
3. **Somebody wants something, said early, as a request.** EP002 only worked once AJ asked for a
   deadline himself ("can you do all that by ten tonight?"). A nodded-at deadline is not a want.
4. **Check information flow:** every character must have a stated reason to know or not know
   what they know; every number must be unambiguous about which way the joke runs (EP002 "ten"
   vs "eight" vs 9 AM saga).
5. **The AI describes, it never names.** Jargon only on the deliberately dense rung.
6. **Two explanations that look opposite:** a technical one that is slightly too fast, a blank
   face, then a plain one (metaphor, four elements max). Introduce the abstract term as a
   *renaming* of a picture already understood.
7. **The teach must be accurate.** Spot-check every technical claim against the real docs
   (EP001's step-cap/budget claim was wrong; EP005's facts were checked against the vendor docs).
8. **Endings:** structural loop (only when earned), accumulation, self-demonstration, inversion,
   callback. A loop needs one sentence that spans the cut, recorded as ONE take and split.
9. **No end cards (STANDING 5 Oct):** no `TERM · CLEARED` stamp, no bucket outro question, no bucket
   in the script header. A definition slate mid-film or just before the final reaction is fine
   (EP002, EP005); nothing after the last line, or the loop dies.
10. Up to 2 "I"s in one VO line, not more. No em dashes on screen.
11. Keep the review artifact LEAN: panels plus at most one short note per script. Production
    history goes in the repo, never on the page.

---

## 4. The pipeline, step by step

### Step 1. Term and script
- Topic comes from Prashasti's backlog / topic filter (`topic-filter.md`).
- Write the panel script (`PANEL n / Direction / SPEAKER "line"`), mark reused framings.
- Publish as an artifact for review (Sejal, Anandhi, Mohit, Prashasti, sometimes Sumit). Script
  gate is blocking. Expect several rounds of reviewer notes; form your own view and push back
  (Sejal's explicit ask), then follow her lead.
- Freeze the approved text into the repo `scripts/<term>.md` with `Status: approved <date>`.

### Step 2. Rough voice pass (kill gate)
A scratch read of the whole script before any art. These gags live on delivery.

### Step 3. Generation prompts
- Base prompt + per-scene prompts from `skills/comic-panel-generator.md`, attach the approved cast
  sheet (or a crop of an already-approved face, which drifts less than the 4-up sheet).
- **Native 9:16, FULL BLEED.** Say "empty of OBJECTS, not empty of ARTWORK" or the model
  letterboxes. Fallback: generate 2:3 (1024x1536) with slack left/right and crop.
- Safe area at 720x1280: bottom 220px (title/channel), right 110px (like/share rail), top 90px.
  Compose subjects right-of-centre so caption space falls on the left. Top third = caption zone.
- **Shot economy:** panels are not generations. Generate each base framing once (wide, close on
  asker, at-desk, screen), make every reaction an edit of that source ("same framing, but he
  leaned back, mildly betrayed"). Loop: 20 panels from 6 generations + 6 edits. EP003: 5 bases.
- A held image can carry 3 to 4 frames while only the caption changes. Not more.

### Step 4. Art cleanup (Sejal does the boarding)
- Sejal generates in ChatGPT, fixes pixels in Affinity, boards in Figma, one frame per panel at
  720x1280, with caption/SFX text layers placed where she wants them. **Her board is
  authoritative: never merge, reorder, redraw or restructure frames without asking** (EP004:
  "I did not ask you to combine these frames").
- Generated art arrives on a SOLID background (heads on (246,243,244), emoji on white). Key it
  before compositing: `v10/keying.py` (corner-sampled bg, tight feather lo=5 hi=12, because
  Dev 1's face fill is only 19 levels off the bg).
- Swapping a head pose (awake to sleeping): `python3 v10/sleephead.py ~/Downloads/<file>.png
  <outname>.png` prints `ar/scale/dx/dy` that anchor on the FACE, not the image box.
- Green-screen memes (dog, cats): alpha from `g - max(r, b)` plus despill (`s1m_cats.py`,
  `pe_avatars.py`); `g - mean(r,b)` eats yellow (banana cat). One crop box per clip.

### Step 5. Final VO (ElevenLabs)
- Generate **per line, grouped by character, one sitting per character** (a full multi-speaker
  pass is ~1,000 credits per retry; a line is 30 to 50).
- Cast for register, not quality (presenter voices sound upbeat under any tag). Stability:
  Natural for flat/deadpan, Creative for range. Max two tags per line, dominant first.
- Write pauses INTO the recording ("Long night." [3.4s] "left a loop running").
- Loop line = one take, split later. Repeated lines reuse the original audio unmodified.
- Thoughts: quiet but NOT whispered (whispers have no measurable edges).
- Sejal's downloads are named like `ElevenLabs_<ts>_<Voice>_pvc_sp100_s50_sb75_v3.mp3`
  (sp = speed x100, s = stability, sb = similarity boost, v3 model).
- If a single re-generated line drifts accent (Indian to Russian on 22 Oct): render the full
  script and cut it; or use Multilingual v2 / v3 "Robust" stability; or the API's
  `previous_text`/`next_text` request stitching; or pad with 2 to 3 preceding sentences and trim.
- **Transcribe every delivered take before using it** (EP002: a take said "at the same time"
  instead of "one at a time", inverting the episode).

### Step 6. Export plates from Figma
- Hide **EVERY** text node on the page (not just dialogue), export, restore, and assert the
  restore list is empty (`stillHidden: []`). A re-export of one frame is still a full hide-all
  pass (EP004 shipped captions twice because a re-export hid only one label).
- Read the geometry of every caption and SFX text node first (x, y, w, fontSize, rotation; Figma
  rotation is CCW-positive, CSS is CW, so negate).
- `download_assets` at scale 1.5 for a 1080 master, or the 720 frame at scale 1 then upscale in
  Remotion. Figma caps a single export at 4096px on the long edge: clone frames into temporary
  4x3 grid sheets (2880x3840, magenta bg), export, crop locally, delete the sheets.
- Figma MCP: responses fail around 19.5 to 20k chars; U+2028 in text breaks the transport.
- Some frames export 1px off (scene4.5 came back 1082 wide, scene frame at 714 tall): check every
  plate is exactly 720x1280 (or 1080x1920) and crop.
- Put the `Shorts safe area` component over every frame before calling the board done.

### Step 7. Cut the audio (Python, per episode: `v10/<ep>_audio.py`)
- Seek on the INPUT side: `ffmpeg -ss START -t DUR -i src -af "afade=t=in:st=0:d=0.03,afade=t=out:st=DUR-0.06:d=0.06" out.wav`.
  `-ss` after `-i` silences every clip past ~1.7s.
- Word ORDER from whisper (`openai-whisper`, small/medium, `word_timestamps=True`), word EDGES
  from a 10 ms RMS envelope (`v10/env.py`, threshold ~ -45 dBFS). Whisper runs up to 0.42s early,
  undershoots ends, and puts words on breaths.
- Segment splits: end >= 0.4s after the last voiced frame, start >= 0.08s before the next onset.
- Interruptions: sever mid-word with a **4 ms** fade, interrupted line at FULL level, find the cut
  by transcribing candidate cut points.
- Short clips get their own file; never `startFrom`-seek into an mp3 (lands ~0.2s late).
- Normalise each line: active-speech level to ~-16 dB (thoughts ~-19), peak <= -1 dBFS
  (`pe_emit.normalise`). Audit every line against the folder median.
- Verify every clip: `ffmpeg -i clip.wav -af volumedetect -f null -` (mean -91 dB = silent).

### Step 8. Emit the cut (`v10/<ep>_emit.py` writes `src/<ep>_cut.json`)
One source of truth. Nothing is typed into the TSX. The emitter computes:
- **Panels:** each starts on its first spoken word and holds **~1.0s after the voice ends**
  (1.5 to 2s reads as dead air). Use frame numbers, never float differences (`(46.05-38.40)*30`
  rounds down and drops a frame).
- **Captions:** per line, whole line at once, at the Figma box (see section 6).
- **Lip flap** tracks (section 6), **SFX cues** with their lettering, **AI mark** windows,
  **ducks**, **push-ins**, **headers**.
- **The bed**, baked to one full-length file (section 5).
- Address lines by a WORD seed, never by index into the run list (removing a breath re-splits
  it). Fail loudly by name when a word goes missing. Fail loudly if a caption lands on ink.

### Step 9. Remotion composition (`src/<Ep>.tsx` + `src/Root.tsx`)
- One composition per episode (`LoopV10`, `IntroV1`, `GraphV1`, `RemoteControl`, `Insights`,
  `SystemOne`, `PromptEng`). Copy the newest one (`PromptEng.tsx` + `PeScreens.tsx`,
  `pe_emit.py`, `pe_audio.py`) as the template; it carries every current rule.
- Assets under `public/<ep>/` (plates, vo, vo_n, sfx, fonts). `public/` is the only copy.
- Studio: run in Sejal's **terminal panel** (macOS TCC stops preview tools reading ~/Documents):
  `cd ~/Documents/Work/comics-video && ./node_modules/.bin/remotion studio src/index.ts --port 3335`
  then give her `http://localhost:3335/<CompId>`. Use a fresh port if one is stuck.
- `remotion.config.ts` must keep `setBrowserExecutable(<Google Chrome>)` and `setConcurrency(1)`
  (bundled headless shell is SIGKILLed; worker pool cannot reach localhost).

### Step 10. Render and QC
```
./node_modules/.bin/remotion render src/index.ts <CompId> "out/EP00N <term> - vN - 9x16 - <secs>s.mp4"
./node_modules/.bin/remotion render src/index.ts <CompId> out/check.mp4 --scale=0.5     # quick look
./node_modules/.bin/remotion render src/index.ts <CompId> out/seq --sequence --frames=A-B  # lossless frames for flicker hunts
```
**Every render gets a new version number in the filename.** Reusing a name let Sejal's player
show a cached old cut (EP003). Then run the QC list in section 8 before telling her.

### Step 11. Deliver
- Drive: cut into `04 Cuts` (previous to `04 Cuts/old`), clean plates (+ captioned set via
  `python3 v10/storyboard.py`) into `02 Storyboards/EPxxx`, VO as played + source takes into
  `03 Audio/EPxxx`, any new SFX into the SHARED `SFX`. Upload them yourself; Sejal does not want
  to do it by hand.
- Update the repo script to what SHIPPED (reconstruct from the cut JSON if the artifact is
  stale), `LINKS.md`, the tracker. Then tell Sejal in one short message what changed.
- Skill files hold global rules only. **Show her the proposed skill-file diff before editing.**

---

## 5. Audio rules (settled numbers)

| Thing | Rule |
|---|---|
| Segment split tail | >= 0.4s past last voiced frame; next window starts mid-silence |
| Interruption | hard cut, 4 ms fade, full level, excluded from ducking |
| Ordinary cut fades | 10 to 30 ms in, 60 ms out (20 ms when a line is cut by an event, e.g. a ping) |
| Other speaker under dialogue | duck, floor 0.20 so she stays audible; duck windows < 0.55s apart MERGE |
| Background chatter (intro) | ducked to "barely heard" under the main speaker |
| Tempo | `atempo` per take; audit **syllables/sec**, not the multiplier; close most of a gap, not all (4.15 to ~4.6 vs 5.5) |
| Loop seam | two halves butted with NO gap; the take's own hesitation is the gap |
| Bed level (office) | landed at **-35 dB in gaps, -39 dB under voice** (about 19 to 23 dB under dialogue); EQ high-pass 140 Hz; duck ~4 to 7 dB under every voice with ~0.3s ramp |
| Bed level (restaurant babble) | must duck ~7 dB under every voice; babble masks speech worst |
| Bed construction | pre-rendered whole, rebuilt on EVERY timing change: `python3 v10/ambience.py <total_s> <night_at> <light_at> [out]` (prints length, seam, night floor, printer runs) |
| Printer in office bed | detect by HF (2.5 to 8 kHz) energy vs the room's low end; it is a ~10s run plus short 0.3 to 0.5s bursts; cut it, repeat clean room inside the night silence |
| Night | silent: bed fades out ~0.5s at lights-off, returns ~1.2s into daylight; a snore loop carries the night |
| Loop ending | bed tail folded onto its head (render long, crossfade overrun over the start); level the whole stream BEFORE the crossfade |
| Meme stings | source peaks near -4 dB vs dialogue -24; pull 15 dB+; scream at ~60%; dog sniff at 40% |
| Ken-level fix | when a reviewer can't hear a line, check the asset first (graph Ken line was 7.7 dB under median) |

**Synthesised SFX recipes** (the shared Drive SFX has only ambience, keyboard, coffee slurp,
scream, sigh; everything else was built with ffmpeg or `v10/s1m_sfx.py`):
- door thud: body at 160 to 320 Hz with a bright crack leading ~3 ms (40% of first 12 ms above
  1.2 kHz); a sub-80 Hz thud is inaudible on phones. Place it in a VO gap, not under a voice.
- notification ding: sines 1320 Hz (short) + 1760 Hz (longer, +120 ms), fade 0.35s. A second
  phone's ping must be pitched clearly apart (EP003).
- phone tick: two filtered taps 2200 Hz and 1800 Hz, 220 ms apart (a whoosh reads as motion).
- snore: brown noise lowpass 350 + ~24 Hz tremolo inhale, detuned 180 Hz sine exhale, looped;
  Sejal wanted it louder than subtle.
- UI set (`s1m_sfx.py`): pop, pop_low, tick, chime, error, whoosh, ripple, morph. Soft, under voice.
- Keyboard clicks only while someone is actually typing on screen.

---

## 6. Assembly contract (Remotion), all settled

### Three kinds of text, never mixed
| Kind | Style | Notes |
|---|---|---|
| **Caption** (a mouth moved) | Lato **800**, **32px in 720-space** (48 at 1080), line-height 42/32, white fill, **5px black stroke (720-space)**, `paint-order: stroke` | Whole line at once ("Natural Habitat Shorts" style, chosen 8 Sep over word-by-word). At the Figma text box x/y/w. |
| **SFX lettering** (a sound happened) | plain sans (Arial) regular, `#3a3a3a`, NO stroke | Pops on its sound: snap in ~0.05s, scale overshoot decaying over 0.26s, hold, clear. Keyboard: opacity 0.3 to 1 + scale +10% on every 3rd detected keystroke, alternating the drawn labels. |
| **Screen text** (a machine shows it) | Geist Mono, dark ink, NO stroke, inside the measured screen rect | Decide by measurement: if the caption box falls inside the plate's screen rect, it is screen text. |

### Caption rules
- Never on faces, never on screens, never during an explainer (explainers carry themselves with
  VO and visuals; at most one setup line above the monitor before it starts).
- Figma boxes are narrow because they sit on clean paper (measured 0% busy pixels). Don't widen
  them; short lines stay on one line, long ones split into timed parts in the same box.
- Same shot across consecutive panels = same caption position (copy the first panel's box).
- Looping episode: the LAST caption takes the FIRST caption's position.
- A caption never outlives its panel (clamp); a caption may clear early while the panel holds.
- Two captions never share a point at the same time (assert it).
- A cut-off line ends with a hyphen: `unless you give it a ste-`.
- No caption before the first word (silent beats work only because of this).
- Top area, not bottom (YouTube UI). Build-time check: measure ink under every caption box.
- Thought captions: same style; whisper/think `* *` markers removed.

### Lip flap (only ever a swap between REAL drawn plates)
- Find pairs by diffing plates (mean-abs-diff: 0 = identical, tiny localised diff = mouth pair).
- Decide which is open by **counting dark pixels in the mouth box** (more ink = open). Never
  assume. Never paint, patch or composite a mouth (ink blots, dashes on necks: EP002 v4/v5).
- No pair on disk = no flap (guard it, or the plate 404s and renders blank).
- Flap only where the board calls for speech; thoughts, listening and off-screen VO keep the drawn
  mouth.
- **Calm flap** (Sejal: "proper lip sync, not too fast"), from `pe_emit.flap_track`: open when
  voiced (> peak - 24 dB) AND above `max(peak - 30, local_max(+-0.3s) - 14)`; close on dips of
  >= 5 dB; open runs 3 to 9 frames (split long runs at their quietest frame); closes >= 2 frames.
  About 2 toggles/s.
- Two-shot where both mouths move: composite `_oo/_os/_so/_ss` variants from the real frames;
  register by best-fit diff, not bounding box (a bbox shift put a frame 3px off).

### Panels and camera
- **Hard cuts only**, every panel, every scene change. No crossfade, no fade in/out.
- Overlays shared by adjacent panels live in ONE Sequence (or they blink on the cut).
- Preload each plate ~12 frames early at opacity 0 (Studio white flash).
- Push-ins: slow, toward the FACE, zoom in only; e.g. 1.00 to 1.19 (EP003), 1.00 to 1.35 (EP003
  bridge), 1.00 to 1.26 (EP002). Hard cut back to wide. One push-in per beat, not everywhere.
- Props composited into the room scale with the camera (measure ink line weight per plate).
- Time of day: a Geist Mono header over the character that changes with the LIGHT, never with a
  sound (`10:00 PM` dark, `8:50 AM` daylight). Wall clocks and beat cards were both tried and cut.
- Memes cut in on the shot's hard cut, no entrance animation; scale so the character still shows
  around them (dog at 0.66 so Peter's hair shows).

### Motion hygiene
- Anything that ends decelerates to rest (one eased curve over the whole window).
- Pulses envelope in AND out: `abs(sin(e*hz)) * min(1, e/0.28) * min(1, (len-e)/0.45)`;
  ~3.4 rad/s (one a second), 5.5 rad/s strobes.
- Move with `transform` (scale/translate), never animate width/height/top/border (pixel-snap
  flicker that only shows in the export).
- States wipe in over ~0.3s; never fade by scaling geometry; pad SVG viewBoxes for motion.
- Derive positions from neighbours; give figures real gaps; one shared baseline.
- Queues form from one point, single file, smootherstep, 0.13s stagger.
- Pop reveals land on the VO word they illustrate; everything else arrives earlier.

### Explainers
- A metaphor, not a diagram; the metaphor must have the same shape as the idea (doors are about
  permission, dependency needs "WAITING ON API").
- Animate the point, not the result. Give a blockage a reason (a scanner, "PLEASE WAIT").
- Icons over sentences ("much better if you use icons more than text", EP004). Labels short
  ("NEED TO WAIT", not a sentence).
- Title holds alone ~1s and clears before visuals arrive.
- No subtitles, no AI mark during an explainer.
- Pace with pauses, never with playback speed: cut VO at sentence gaps, insert 1.2 to 1.5s of
  silence (6 ms fades), retime every beat.
- After any VO re-cut, check every reveal still lands and clears inside its panel.
- Turn one picture into the other in place (dots where the heads were).
- A meme gets its beat: hold intact ~0.2s before it crumbles.

---

## 7. Episode cadence of a typical build (what to expect)

A build is ~20 to 45 render rounds. Sejal watches each render (or Studio) and sends numbered
batches of notes. Typical arc: v1 assembly, then captions/flap/SFX fixes, then explainer redesign
in Figma frames first (she approves the static frames before animation), then audio polish (bed,
ducks, tails), then reviewer notes from Anandhi/Mohit/Prashasti, then delivery. Explainer
redesigns are the most expensive part: mock options in Figma before animating anything.

---

## 8. QC before showing Sejal (run all of it, report numbers not vibes)

1. Duration and `ffprobe` dims (1080x1920, 30 fps). File name versioned.
2. One still per panel at 70% (`v10/s1m_verify.py <mp4>` builds a contact sheet).
3. Every VO clip non-silent (`volumedetect`); every line within a few dB of the median.
4. Transcribe the rendered audio once; every line says what the script says.
5. No caption on ink/faces/screens; same-shot caption positions identical; last = first on loops.
6. Caption word count rendered == script word count (off-by-one drops first words: use `start <= t`).
7. Every SFX has a word on screen and every SFX word has a sound, on the same frame.
8. AI mark on every blank AI screen, never on title cards or explainers, eye right of centre.
9. Flap only on real pairs; no frame renders blank.
10. Bed present the whole film, loop seam level-matched (tail vs head dB), no printer runs, rebuilt
    for this length. Say plainly that audibility needs her ears.
11. Nothing outlives its panel; no crossfades anywhere.
12. No em dashes in any on-screen text or Figma names you touched.
13. Diff consecutive plates if a beat "doesn't land": report pixel count + bbox + screen time.

---

## 9. Working with Sejal on comics

- She wants an **advisor, not an assistant**: give a verdict with evidence, disagree with her and
  with reviewers when warranted, then follow her call. Never flip to whoever spoke last.
- She sends voice-typed notes in numbered batches; implement all, then list what changed.
- She often says "automate it, I am AFK": do the whole build, upload, and report.
- Ask before changing her board, before skill-file edits, before anything not requested.
- Handoffs and Slack drafts go in the reply as text, not into files or the artifact.
- "Is this exported?" means: rendered to `out/` with a new version AND (usually) uploaded to Drive.
- Keep reviewers' notes as input, not orders; the measurement usually settles disagreements.

---

## 10. Drive upload technique (if the new Drive has the same tool limits)

The Drive MCP `create_file` sends content inline (fine for text, useless for media). What worked:
inject an `<input type=file>` into the Drive web page, fill it with the Chrome extension's
`file_upload` (<= 10 MB per call, reads from disk), build a `DataTransfer` from `input.files`,
dispatch `dragenter` on document/window, wait ~800 ms, then fire ONE `dragenter`/`dragover`/`drop`
on `document.elementFromPoint()`. Patch `DataTransferItem.prototype.webkitGetAsEntry` to wrap the
File. Rules: drop ONCE per batch (a second drop raises replace-or-keep); `file_upload` rejects
hard-linked files (stage with `cp`, not `ln`); each upload replaces `input.files`; files > 10 MB:
`split -b 8500000`, stash each part as a Blob, rebuild one `File`, verify SHA-256 against
`shasum`, drop once; make sure `elementFromPoint` is not a subfolder row; verify via
`search_files` or the "N uploads complete" toast (the list lazy-loads past ~50 rows).
