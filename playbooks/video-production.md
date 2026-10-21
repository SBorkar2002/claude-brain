# Video production: narrated motion-graphics explainers and product videos

How Sejal makes a narrated motion-graphics video from script to render: a product launch video, an SEO/educational explainer, a teaser. Built from four months of work (Jun to Oct 2026) on the Tetriz launch video (2:23, 16:9 plus a 9:16 re-composition), the DORA metrics explainer, and the 60s teaser. Every rule below came from a correction, a reviewer note, or a bug that cost hours.

Companions: `playbooks/tools-evaluated.md` (which tool for what), `lessons/video-traps.md` (symptom, cause, fix). Raw facts: `memory/feedback-caption-*`, `feedback-animation-prefs`, `feedback-vo-*`, `project-launch-storyboard`, `project-video-pipeline`.

Comic episodes are a different pipeline (hard cuts, plates, lip flap): see `playbooks/comics.md`. VO audio rules here apply to both.

---

## 0. Posture

- **Design stays human, automation does the repetitive parts.** Script refinement, scene prompts, VO, timing and the animation code are automatable. Frame design is Sejal's (or a designer's) call, reviewed in Figma.
- **Iterate in reviewable steps.** One scene or sequence at a time: build, render stills, show, then the next. Never generate the whole video in one pass.
- **Measure before you opine.** If a beat "doesn't land", diff the frames and time the screen before anyone rewrites the script (EP003: 8.74s where only a mouth moved; no rewrite fixes that).
- **Ask before editing a shared skill file.** Propose the rule list (new / changed / overridden / removed), get her go, then write it.
- **Keep a decision log** (`DECISIONS.md` at the project root, newest first): what changed and why, per session. Her manager mandated it and it is the only record of why each beat sits where it does.

---

## 1. The pipeline at a glance

```
raw script / brief
  -> 1. SPINE (beats + which real screen proves each feature)        [review gate: manager]
  -> 2. SCRIPT (VO words, on-screen intent, word count)              [review gate: CEO/PM/manager]
  -> 3. FIGMA BRIEF (Mode 1: static keyframes, no motion language)
  -> 4. FIGMA FRAMES 1920x1080, designer-edited                       [review gate: Sejal]
  -> 5. VO: ElevenLabs, whole script in one generation
  -> 6. WHISPER word timestamps + 20ms RMS silence map
  -> 7. ANIMATION in Remotion, scene by scene, locked to VO words
  -> 8. edit -> still -> Read -> adjust loop; full render
  -> 9. REVIEW round (manager / CEO / PM), log in DECISIONS.md, repeat
  -> 10. RENDER + deliver (Desktop mp4, local player, Slack message)
```

Never skip from script to animation. The Figma review step between brief and animation is required (her standing rule: "Always Figma first").

Production targets her manager set: storyboard for a 30s video in 1 day (first one took 4), 70% of a 30s video in 2 days with one feedback round in.

---

## 2. Tool choice (short version)

| Job | Use | Why |
|---|---|---|
| Animation, final composition, VO sync | **Remotion 4** (React, 1920x1080 @30fps) | Deterministic, frame-locked to word timestamps, data-driven panels are a `.map()`, shared-element transitions are trivial, re-timing to a new VO read is re-deriving numbers. 90 to 95% of After Effects polish. |
| Frames / storyboard | **Figma** (built via the Figma MCP or by hand) | Reviewable, editable by Sejal between sessions. |
| VO | **ElevenLabs** | Quality; full-script single generation keeps flow. |
| Word timing | **Whisper** (python `openai-whisper`, base model) | Word timestamps; verify cuts by transcribing. |
| Organic one-offs (branching tree growth) | Higgsfield, only if Sejal opts in (paid) | Did the job once when Claude Design could not. |
| Dashboard-heavy static screens | Figma Make (optional) | Code-backed charts render cleaner than hand-drawn vectors. |
| Short GSAP/HTML clips | Claude Design | Deck-style only. Not product animation. |

Do NOT use AI video generators (Veo, Sora, Runway, Kling) for UI motion graphics: they hallucinate interface text and cannot click precisely. Full verdicts in `tools-evaluated.md`.

---

## 3. Script and spine

### Spine before script
- When a script gets "surface level" feedback twice, stop polishing prose. Write a bones-only spine: one line per beat (problem -> enter product -> feature 1..n -> recap -> CTA -> close), and for each feature beat name the **specific real product screen** that carries the depth.
- Split what the VO **claims** (outcome) from what the visual **proves** (the real screen, real number, real button). Not everything needs to be spoken; visuals carry depth.
- Adversarially check every feature beat against product ground truth: the VO and the visual must describe the SAME real feature, and its ship status must be real (a "Future" capability shown as live is a lie on screen). Fabricated stats get cut.

### Two video types, two rule sets (never mix)

| | SEO / educational | Launch / product |
|---|---|---|
| Goal | Rank on search, get cited by LLMs, educate | Sell, book a demo |
| Brand | No product name or logo (product UI may appear unbranded only in advanced topics) | Product name + logo |
| Hook | Real-world pain the viewer recognises in 5s | Problem first, then product; logo intro allowed |
| Tone | Peer engineer, friendly but firm. Never "did you know" / "have you ever wondered" | Confident, punchy, sales-pitch, not explainer-verbose |
| Length | Under 60s for Shorts/Reels; 60 to 90s max | 60s teaser, up to ~2:30 for the full launch cut |
| Close | Non-obvious insight, no CTA | CTA ("Book a demo") |
| Motion | Slow accumulation, fast clarity | Snappy, virtual camera |
| Mute | Must read on mute | Closed captions carry it |

SEO script template: problem in first ~5s -> explain the concept -> "why use this". Keyword spoken within the first 15s. Every key term spoken must appear on screen at the same moment. Numbers always animate from 0.

### Script mechanics
- Words: ~148 to 166 wpm. 166 words is about 60s; hard ceiling 180 for a 60s piece.
- Pauses are real beats: write them in ("one beat after X").
- Launch audience (CTO / VP Eng, time-poor, hype-resistant): sell 3 to 4 big ideas clearly; each feature uses the SAME template ("for the individual it does X, for the org it does Y"), shown visually too.
- Invented coined terms throw viewers ("Agent Playbook" was killed). Use words the audience already knows.
- Raw scripts often carry generic AI-prompted on-screen ideas: mostly ignore them, think out-of-the-box, keep only real engineering environments (terminal, GitHub PR list, CI run, Slack alert, calendar) or visuals that show tension the VO cannot.
- On-screen text that comes from the VO is **verbatim**. Never paraphrase. If wording is not given, ask.
- Script deliverable for review: a single artifact per project, version-labelled, with a changes table, outline, script with word counts, timing table, production rules, open flags, prior versions appended.

---

## 4. Storyboard in Figma

### Two output modes (keep them separate)
- **Mode 1, Figma brief:** static keyframe descriptions only. What is on screen, where, in what state. Banned words: slides, fades, eases, bounces, durations. A designer builds and edits from this.
- **Mode 2, animation prompt:** only after frames are approved; references frames by name; specifies timing from VO words, motion, easing, camera keys (frame from VO word, target x/y, scale, hold).

### Frame rules
- 1920x1080 (the DORA/SEO set used 1280x720). Name frames by scene and beat (S3a, S3b; or Hook-A1, Context-B2) so Figma names and animation code match.
- Split dense scenes into sub-frames (one engineer -> the team -> the org) and distribute the script's caption lines one per sub-frame. Do not invent captions.
- **Re-screenshot the Figma frame before animating it.** Sejal edits frames between sessions; never trust your last-built version. Prefer surgical edits over rebuilds (rebuilds clobber her manual edits).
- New scene design goes to Figma FIRST so she can see the thinking, not straight into the video ("start designing the frame in the figma link instead of directly making edits on the video").
- Dashboards: distill real screenshots (strip tables and clutter) to the one metric that proves the beat. Replicate real screens faithfully when they exist; mark mocks as mocks.
- Chart / dashboard scenes need product-prototype fidelity: real drop shadows (not flat borders), icons paired with labels and deltas, smooth multi-point curves with dashed gridlines and real area fills, pill filter chips. Conceptual screens are allowed; wireframe polish is not.

### Figma MCP mechanics
- Load the `figma-use` skill before every `use_figma` call. `use_figma` runs Plugin API JS, supports top-level `return`, and an error rolls back the whole call. Build one frame per call. `createNodeFromSvg` is good for curves and arrows.
- Frames inside a Section are not direct page children: use `section.findChildren` or `page.findAll`, or delete-before-rebuild silently duplicates.
- If the claude.ai Figma connector dies mid-session (every call `net::ERR_FAILED`), reconnecting does not revive that session: start a new session and `whoami` first. The desktop Dev Mode MCP at `http://127.0.0.1:3845/mcp` is read-only and only sees the frontmost file with a single frame selected.

---

## 5. Voice-over

### Generation
- Generate the **whole script in one ElevenLabs generation** to keep flow and timbre. Takes generated in separate sessions drift in timbre; re-generate in one batch if a line sounds like a different person.
- Voices used: "Monika Sogam - Deep and Natural" (launch), "Mark - Natural Conversations" (DORA explainer). Filenames carried tokens like `sp95_s46_sb68_v3`; they appear to be speed / stability / similarity settings plus model version (inferred from naming, not confirmed in history).
- Keep a `VO-SCRIPT.txt` in the project: the exact text to paste into ElevenLabs, with pronunciation spelled out ("Book a demo at tetriz dot A-I"; "auth" as "awth"; "PR" as "P R").
- If a pause is needed (e.g. "...can only guess. / Because..."), write it into the generation (punctuation, line break). A read where two words are co-articulated cannot be split cleanly; after several failed cuts Sejal chose to drop the pause rather than keep fighting it.
- A single re-recorded line can be spliced in (one line, own file) as long as the seam sits in real silence. Splicing a different read mid-scene sounds abrupt: change voices only at a scene cut.

### The master file is never edited
- Import to `public/`. All pacing comes from **playback windows**: `<Sequence from durationInFrames><Audio src startFrom /></Sequence>`, one window per line, cut only inside measured silence. Adding a breath = gap between windows. Re-ordering sentences = playing windows out of source order (done for a whole narrative re-order without a re-record).
- `FullVideo.tsx` holds the audio map (one Sequence per VO line) and the `<Series>` scene order.

### Timestamps and silence map
```python
import whisper                       # python package; no CLI binary needed
m = whisper.load_model("base")
r = m.transcribe("public/vo.mp3", word_timestamps=True, language="en",
                 initial_prompt="<product nouns: Tetriz, AI-native, org, prompts, harness>")
# then a 20ms RMS pass over a 16kHz mono wav to list every true silence
```
- `initial_prompt` with the product nouns, or "Tetriz" becomes "Tetris" and "org" becomes "awg".
- Whisper `end` times undershoot the audible decay; `start` times are late; it back-dates segment-initial words, so its gaps lie. Use the RMS silence map for cut points and gap lengths.
- Save words to `out/vo_words.json`: the source of truth for all timing.

### Cut rules
- **Never cut mid-word.** Leave >= 0.4s (12 to 15f) of decay after the last word of a window. End windows mid-silence, several frames clear of the next onset; no two windows may contain any part of the same word.
- When you extend a window's tail, shift the NEXT window's `startFrom` AND `from` by the same amount so master-time alignment downstream is unchanged.
- Find a cut point by **transcribing candidate cuts**, not by reading the energy envelope (the loud burst you think is "because" can be the "-ess" of "guess").
- 4-frame volume fade on a window's tail and 2-frame fade-in on the next so edges cannot click.
- Exception, interruptions (dialogue): the interrupted word is severed at full level with a 4ms fade, and the interrupting cue is excluded from any ducking.
- ffmpeg slicing with fades: `-ss`/`-t` BEFORE `-i`, or `afade` runs on original timestamps and silences the clip. Verify with `volumedetect` (-91 dB mean = silent).
- Pace: the same `atempo` does not equalise delivery. Measure syllables per second of voiced time per segment; fix outliers with a per-take override, closing most (not all) of the gap.
- Ambience beds: below about -42 dBFS nobody hears them; if audible, duck ~7 dB under every voice. Level alone does not predict audibility (check spectrum and VO coverage). You can verify presence, not audibility: state the number and ask for her ears.

---

## 6. Remotion project setup

### Structure (the launch project; reuse it)
```
src/constants.ts      FPS/WIDTH/HEIGHT, springs, WORD_DELAY, colour + type tokens,
                      CC_Y / EMPH_Y, every scene length SEQ_* (frames @30fps)
src/FullVideo.tsx     AUDIO MAP + <Series> order + TOTAL_FRAMES (must list every scene)
src/Root.tsx          composition "Full" plus one composition per scene for isolated work
src/scenes/*.tsx      one file per scene; beat constants at the TOP, in scene-local frames
src/components/
  Camera.tsx          keyframed virtual camera {f,x,y,s}, inOut-cubic, + CaptionScrim
  WordReveal.tsx      per-word spring reveal with tints
  popReveal.ts        the one pop-in for grids of small marks
  Fonts.tsx           delayRender until fonts are actually loaded
  PillarMap.tsx       persistent nav chips with eased handoff
public/               vo.mp3, re-recorded line files, official SVG brand icons
out/                  renders, stills, whisper json (gitignored)
DECISIONS.md          the decision log
HANDOFF.md            context doc so a fresh session can resume with zero briefing
```
- `package.json`: `remotion`, `@remotion/cli` ^4, `react` ^18.3. Scripts: `dev` = `remotion studio`, `render`, `still`.
- `remotion.config.ts`: `setVideoImageFormat("jpeg")`, `setOverwriteOutput(true)`.
- Fonts: CSS `@import` from Google Fonts is not enough mid-render in parallel tabs. A `Fonts` component calls `delayRender`, awaits `document.fonts.load(...)` per weight, then `continueRender` (10s safety timeout).
- Reuse `node_modules` across sibling projects by symlink instead of reinstalling.
- Git from the start: `out/` and `node_modules/` ignored, code only. Freeze a baseline PR before any big rework (revert point). Never merge to master. Branch per rework.
- Shared geometry gets ONE exported definition (a card body used by two scenes): private copies drift silently.
- A 9:16 version: copy as a git worktree on its own branch so `git diff <16:9 branch> -- src/FullVideo.tsx` proves timing is untouched.

### The core constants (launch video values)
```
FPS 30 · 1920x1080
SPRING     = { damping: 22, stiffness: 220, mass: 0.5 }   // word reveal, general
POP_SPRING = { damping: 14, stiffness: 200, mass: 0.7 }   // placed-from-top overshoot
WORD_DELAY = 4                                            // frames per word (emphasis tier)
CC_Y = 928 · EMPH_Y = 908                                 // caption line (16:9)
```

### Viewing without a full render
```bash
npx remotion still src/index.ts Full out/check.png --frame=<GLOBAL frame>
```
Then Read the PNG. **edit -> still -> Read -> adjust** is the whole loop. Scene beats are scene-local; `Full` takes a global frame: `global = scene.start + local`. For many frames, bundle once and render a list (the 9:16 branch had `scripts/shots.mjs`; each `remotion still` re-bundles, ~40s). Studio for scrubbing: `npx remotion studio src/index.ts --port 3334`.

---

## 7. Timing system

### The one formula
```
scene-local frame = (window.from - scene.start) + (srcFrame - window.startFrom)
```
`srcFrame` from the whisper JSON. When a new read arrives, **re-derive every scene's beats from the new word times**; never shift by a constant (a newer read was up to ~8s tighter cumulatively).

### Values that held up
| Thing | Value |
|---|---|
| Closed caption opens | **0.3s (9f) before its first word** (0.5s felt early; Stack-type continuations can take 0.4s) |
| Closed caption ends | ~14f past its final word; its fade runs [end-12, end-2]. If the next line is too tight, the no-overlap rule wins and it drops early |
| Panel hold after its VO line | **~1s** (0.8 to 1s). 1.5 to 2s felt "weird watching them just pause" |
| Gap between scenes (true silence) | 1.3 to 2.5s; within a scene 0.4 to 0.8s |
| Hero stat on screen at final framing | >= 2.5s, camera move finished early |
| Completed panel rest before exit | ~0.5s at focused framing + a wide beat if the camera moved |
| Total length | 2:00 cap was lifted to 2:30 for the full launch cut; the shipped cut was 2:23.6 |

### Placement rules
- **Motion lands on the word it illustrates.** Derive the beat from the measured word frame (a curve bends ON "bends the curve upward"; KPI cards pop ON "runs", "costs", "outcomes"; dotted lines draw ON "measure"; a label naming a gap appears only after the gap exists).
- **Everything else in that panel arrives EARLY.** When the illustrated line lands, those marks are the only thing still moving.
- Visuals do not have to finish before the caption finishes, but nothing may keep building after the scene's VO ends while the scene is about to exit (build fast, rest long).
- During any hold, keep subtle ambient motion (glow breathing, status dot pulse, cursor blink) so the frame never looks frozen.
- When audio windows move, re-list every window's `from + duration` against its scene end: a window longer than its scene spills two VO lines on top of each other after a re-order.
- `TOTAL_FRAMES` must include every scene, or the render silently truncates the last one.
- Silent scenes (logo intro, outro tail) can be re-timed internally without touching the audio map. A tagline needs its own read time: check its fade-out against its reveal, not against the scene length.

---

## 8. Caption system (final state, Aug 2026)

Two tiers.

1. **Closed captions (CC):** carry the full VO, small, bottom-centre, every scene. Land as a **full line in one go** (wordDelay 0): word-by-word CCs pulled eyes off the visuals. Sequential, never two on screen at once.
2. **Emphasis captions:** big, heavier, only when a line carries real value. Word-by-word reveal (`WordReveal`, wordDelay 4, never above 6). Key words tinted **TEAL #03A6CF** (brand accent, never the scene's identity colour; one deliberate exception was an orange "guess" on a hook frame).

Placement history and current rule:
- Originally the emphasis tier sat anywhere ABOVE a reserved CC band (~y 940 to 1015) and must never overlap it.
- From Aug 14 Sejal put both tiers on ONE line (`EMPH_Y 908`, `CC_Y 928`): the CC fades out (a `ccHide` gate) before the emphasis lands. The CC keeps the setup, the emphasis owns the punchline.
- Some scenes are VO-only with no caption at all, by direction.

Hard rules:
- **No repetition between tiers** in the same beat. If de-duping guts the CC, drop the CC for that beat.
- First letter capitalised. **No em dashes** in caption copy (commas, colons, parentheses). Words stay verbatim to the VO.
- Captions **exit the way they came in**: opacity 1->0 + translateY 0->~10px over 12 to 14f, ending ~2f before a cut. Never vanish abruptly.
- Captions live OUTSIDE the camera (never scale or drift with zoom) and stay inside the clean area: constrain width, wrap taller, never overlap UI.
- **CaptionScrim:** on push-ins, panel text drifts into the caption band. A bright white bottom gradient (320px tall, 0.98 -> 0 up the screen) sits above the zoomed visuals and below the captions; its opacity tracks camera scale (0 at <=1.04x, full by 1.32x), max 0.9 (0.75 on the intro curve). Invisible on wide shots.
- Consecutive panels of the same shot keep the caption in the same position (copy from the first panel of the run; do not inherit Figma's per-frame boxes).
- Metrics and numbers always render ABOVE the caption band (9:16 rule, applies everywhere).

---

## 9. Visual system

### Colour tokens (Sejal's system, launch video v4.2 onwards)
| Token | Hex | Use |
|---|---|---|
| BG | `#F0F2F5` | Canvas. Not pure white, not dark |
| INK | `#0D0D0D` | Titles, stats (weight 800) |
| SEC | `#3A4B54` / `#6B7280` | Secondary text |
| MUTED | `#8A97A0` / `#9CA3AF` | Timestamps, axis, lowest contrast |
| LINE | `#E5E7EB` | All borders and dividers |
| TEAL (brand) | `#03A6CF` | Brand, emphasis words, good/resolved state. Legacy `#00BCD4` deprecated |
| TEAL_DK | `#02718D` | Dark teal |
| GREEN | `#22B268` | Success / "it worked" only, never an identity colour |
| AMBER | `#E58A0F` (`#F5A623` in DORA) | Cost, leaking, before, waiting |
| RED / CORAL | `#E14840` / `#FF6B6B` | Problem, risky, blocked, below threshold |
| Identity colours (one per concept) | magenta `#EC4899`, purple `#7C6BF5`, blue `#3B82F6`, teal `#03A6CF`, orange `#F4652F` | One per product pillar/lever, locked once chosen; tints `#FCE7F3 / #ECEAFD / #E7EFFE / #E3F4F9` |
| Dark canvas (outro constellation) | `#060608` / `#08090D` | Only with a theme-bridge fade |

No gradients (not in the brand). Flat colours. Marketing-site palette for SEO pieces: off-white `#F9F9F9`, cards `#FFFFFF`, text `#262626`, teal `#0096BB`.

### Type scale (from her DORA Figma file; reused for launch)
| Element | Family | Size / weight | Colour |
|---|---|---|---|
| Scene title | Mona Sans | 36px ExtraBold, lh 44, tracking -0.88 | `#0d0d0d` |
| KPI big number | Mona Sans | 76px ExtraBold, lh 72, tracking -1.44 | `#0d0d0d` |
| KPI unit | Plus Jakarta Sans | 20px Medium, tracking -0.88 | `#6b7280` |
| Subtitle | Plus Jakarta Sans | 22px Medium | `#888` |
| Category eyebrow | Geist SemiBold | 12px, uppercase, tracking 0.55 | `#666` |
| Table header | Geist Bold | 10px uppercase, tracking 0.45 | `#666` |
| Table row title | Geist | 16px Medium | `#0d0d0d` |
| PR number / duration / badge | Geist Mono | 14 / 14 / 12px Medium | coral for slow PRs |
| Chart axis | JetBrains Mono | 11px Regular | `#666` |
| Chart annotation | Plus Jakarta Sans | 14px Medium | `#666` |
| STATUS label | Plus Jakarta Sans | 12px Bold uppercase | TEAL |
| Terminal | Geist Mono | 15px, lh 1.8 | on `#1c1c1e` / `#0d1117` |

Mona Sans was often not installed in Figma: Plus Jakarta Sans ExtraBold stands in for display, Geist Mono for code. Remotion loaded Plus Jakarta Sans 400 to 800 + Geist Mono 400 to 700 from Google Fonts.

### Components
- Stat card: bg `#f9f9f9` or white, radius 24, shadow `0 11px 22.45px rgba(110,110,128,0.26)`, padding 50 / 20 to 30. Feature card radius 16, padding 20.
- Table: header 44px, rows 64px, gap 16, border-bottom `1px #e5e7eb`. Badge pill radius 100, padding 6/12. Content margins 79px on a 1280 canvas.
- Teal glow only behind the ONE hero card of a scene: radial, blur ~70 to 80px, ~40% opacity, fades in as the card settles.

### Object identity (reduces cognitive load)
- **Icons carry identity; colour carries state.** Never repurpose a state colour decoratively.
- Skill = lightning + `skill.md` chip; plugin = jigsaw; rule/config = `.md` doc or gear; live dashboard = browser chrome (traffic lights, URL, filters); static screenshot = image frame + shadow, no chrome; terminal = mac traffic lights, mono ink.
- Brand / tool icons: **official vectors only** (simpleicons CDN `cdn.simpleicons.org/<slug>`, Wikimedia, or ask Sejal). Never pixel-process PNG tiles (jagged dark outlines).
- Named people get distinct flat illustrated portraits (flat fills, no outlines), never grey placeholders; same component at every size.
- A persistent map of the 3 to 4 pillars (chips top-centre) tells the viewer where they are: active chip glows in its colour, ~10% larger, others grey; handoff ramps over ~13f, never snaps. Introduce a concept only in its own scene (no wrapper before it is explained).

### Layout rules
- **Attention hierarchy:** one place to look per frame. When something new arrives, de-emphasise the old.
- **No overlapping elements** unless asked; check every absolutely positioned bbox. Keep ~100px clear around CTAs and headlines for decorative icons/dots.
- **No tilting** anything. Asymmetry via position, size, opacity only. Organic scatter is uneven, never mirrored 2-left/2-right.
- **Comparisons side by side** on one screen, left animates first. Before/after must look visibly different (red -> green, fuzzy crossed out -> sharp checked).
- Stat card orientation follows position: side column = vertical, top/bottom strip = horizontal.
- **Tables align like tables:** avatars share one x, names left-aligned, middle text columns left, icons/tags/buttons centred, numeric last column right; every heading takes its column's alignment; one 52px flex row per baseline; equal gutters. Derive from one column grid (`COL_W` summing to inner width), not hand-picked offsets.
- **Equal padding** on all four sides of a card; the container grows with content. Count the data rows before sizing (a card sized for 5 rows when the array had 6 cost three rounds).
- In-chart labels never overlap the curve and never leave the plot area (check `getBBox` vs `getPointAtLength` samples, ~20px gap, plot bounds not viewBox).
- No label/badge/pill that is not in the approved frame. Structure must encode something true.
- A chart is fine only if what it shows is instantly clear; do not spend 10s growing a chart to say "improving".
- Designed curves are pixel-sampled from the Figma render, not hand-drawn beziers. Bezier control points are hardcoded pixels: move/scale the whole chart by transform, never resize the plot box.

---

## 10. Motion rules

### Bar
After Effects motion-graphics quality: mask reveals, draw-ons, wipes, cover wipes, choreographed staggers, expo-out / quart in-out. Generic fade-up plus bouncy pop reads as AI. Graphics come from the video's own system (tickets, tiles, rules, chips), not dropped-in clip-art.

### Defaults
| Thing | Value |
|---|---|
| Default ease | ease-out cubic `(0, 0, 0.2, 1)`; camera inOut cubic |
| Element stagger | 120ms (4f) between sequential non-text reveals |
| Pop-up / card | ~250ms; scale 0.92->1 + opacity; never from scale 0 |
| Title in | ~400ms; subtext 200ms+ after the title's last word |
| Card / panel entrance (launch) | slide up from below, power3.out, 0.3 to 0.5s |
| Counters | count from 0, ~0.8s, teal while counting |
| Charts | draw left to right, 1 to 1.5s, fill follows the line |
| Typewriter terminals | line by line, quick |
| Arrow + annotation | arrow draws first, then text (scale 0.8->1, ~250ms) |
| Grids of small marks | `popReveal`: spring from scale 0.7 + fade, staggered left->right in reading order, landing on the VO words they illustrate |
| Scatter plots | dots pop randomly, ~40ms stagger |
| Lists / table rows | one by one, same stagger for every state |

### Hard rules
- **Nothing appears, recolours or glows abruptly.** Every colour/glow change is an eased crossfade (`interpolateColors` + `Easing.inOut`) over a window.
- **Lines are drawn, never faded**, and never ride inside another element's pop. Use a measured polyline + `strokeDasharray/offset` with the real length. **Do not use SVG `pathLength`** (misrenders in headless Chrome). Gate the path until progress > 0.001 (a fully offset round-cap dash leaves a stray dot). Dashed lines reveal via a growing clip rect so the dash pattern stays real.
- Fills between animated curves clip to the LAGGING curve tip.
- Long VO-anchored draw-ons need a visible start: two-phase profile (quick ease-out rise on the anchor word, then an inOut surge landing on its word). The drawn element and its follow-cam share ONE progress function.
- Value swaps ("12 active" -> "11 active") crossfade with the new span absolutely STACKED over the old.
- Pulses and breathing must envelope in AND out: `abs(sin(e*hz)) * min(1, e/0.28) * min(1, (len-e)/0.45)`. Fade by opacity, never by scaling geometry.
- Show actions, not states: a cursor moves in and clicks Install -> button crossfades to "Installed". A pruned row flags amber on the word, then disappears entirely and the row below slides up (no strikethrough).

### Scene transitions
- **Continuation scenes** (same layout, elements added): NO fade. Hard cut with shared elements at exactly matched positions (both axes); only per-element motion bridges. Verify by pixel-diffing the frames either side. Shared objects may travel across the cut (a chart sliding centre -> left as one object).
- Genuinely different scenes: all elements exit together (fade + drift), or pack toward the nav chip they belong to and the next panel grows from its chip (spatial through-line instead of crossfade).
- **Every block needs an explicit exit.** Audit the last 15 frames of every scene before rendering; a missing exit is the most repeated abrupt-cut bug.
- Zoom back to s=1 before a cut so the next scene does not arrive out of a close-up (or, by direction, hold the zoom and pure-fade).
- Light <-> dark theme change: never hard cut. Dip to the incoming base colour over ~20 to 25f, start the next scene on it.
- Vary entrance patterns; reviewers flag monotony (everything one-after-another the same way). E.g. rules fly into a list from all directions; a "detected gap" scan-sweep for recommendations.

### Virtual camera
- `Camera` keyframes `{f, x, y, s}`, inOut cubic between keys, hold by repeating a key. The whole composition (including the pillar nav) goes inside the camera; only captions stay outside.
- Push in **on the word** that names the thing. Zoom needs a target: the subject sits at the centre of frame. A push straight in (x/y unchanged) beats a drift toward nothing.
- Go tight on hero moments: clicks ~2.1x+, typed text ~2.5x. Hold steady while elements fly in.
- Follow-cam for curves: keys sampled EVERY frame along the path with the draw's own easing (step-5 sampling looked jagged). Keyed <-> override boundaries must match exactly.
- One camera idea per beat. One move, not two half-moves (exception only if the middle position has a purpose).
- Do not zoom where something is already moving on its own, or on a scene with nothing to inspect.
- A completed chart earns a full-wide hold to the end of the scene.
- Dim everything except the hero with a white wash (~0.78 opacity, explicit full-frame size) when the camera rides a curve.
- Motion blur is the main gap vs AE: `@remotion/motion-blur` exists (multiplies render time), not adopted.

---

## 11. Review loop

### Verify by measuring
| To check | How |
|---|---|
| A frame is right | `remotion still` -> Read the PNG |
| A VO line sits in its scene | transcribe the **render**, not the source |
| A gap feels long | 20ms RMS on the render |
| A word is clipped | RMS the tail; >= 0.4s decay inside the window |
| Alignment | pixel-measure (isolate elements by fill/tint hue) |
| A continuation cut is seamless | pixel-diff the frames either side |
| A string patch landed | assert old text present before, absent after |

### What reviewers repeatedly flagged (pre-empt these)
- Script surface-level / features do not land -> spine with real screens (section 3).
- Focus in five places at once -> attention hierarchy.
- Before/after look the same -> visible state change.
- Panels leave before they can be read -> ~1s holds, more total duration.
- Transitions too fast / lose context between sections -> bridges (chip pack/grow, carry-over element).
- A key visual does not happen ON its VO word -> anchor to the measured word.
- Caption and emphasis clash -> one line, CC hides before emphasis; no repeated words.
- Everything animates the same way -> vary entrances.
- Placeholder avatars feel inhuman -> illustrated portraits.
- Literal metaphors (a heart) may not land for executives -> abstract shapes (diamond).
- Video starts abruptly -> a short logo-first intro (3s), then content; titles and visuals appear together as the VO names each.

### Process
- Show stills or a hosted preview after each change; she reviews in a local browser player.
- Voice-note feedback arrives as numbered lists, sometimes with transcription slips: restate ambiguous items before building.
- After a review round: list changes made (short, grouped), log in `DECISIONS.md`, commit, push.
- When rules change: list new / changed / overridden / removed rules, ask, then update the skill file(s) and memory in the same turn. Contradictions between old and new rules: the latest instruction wins; remove the stale one.

---

## 12. Render and delivery

```bash
npx remotion render src/index.ts Full out/<name>-v5.mp4     # ~4 to 5 min for ~4300 frames, ~22 MB
cp out/<name>-v5.mp4 ~/launch-video-preview/               # local player at http://localhost:4173
cp out/<name>-v5.mp4 ~/Desktop/<Name>-v5.mp4                # the copy she attaches to Slack
```
- Local player: a plain `index.html` with `<video controls autoplay>` whose `src` gets `?t=Date.now()` so every load fetches the latest render. Serve the folder on a fixed port.
- An Artifact page caps at 16 MB; a 22 MB video needs real hosting (ask before uploading anywhere).
- Name exports by version (v4.2, v4.3-loop, v5); keep the frozen baseline export.
- Slack update messages: typed in chat, short bullets, grouped (how it was built, effort, still working on, what we learned), in her first person. Never sent by Claude.

### 9:16 vertical version (re-composition, not resize)
- Scaling 1920-wide layouts into 1080 gives ~11px text. Timing (VO, window map, every `SEQ_*`, every beat) transfers unchanged and must be proven unchanged by diff; geometry is redone.
- Step 0: replace every hardcoded `1920`/`1080` literal with `WIDTH`/`HEIGHT` (`grep -rn 'height={1080}\|width={1920}' src/`), confirm the 16:9 render is identical, THEN flip the constants.
- Two coordinate spaces: design space 1920x1080 (scenes still authored here) mapped by `<Stage>`/`<Camera>` onto the 1080x1920 frame; only captions use frame space. Mixing them fails silently (clipped SVGs, captions off-frame).
- YouTube Shorts safe areas: top ~180px, bottom ~300 to 400px, right action rail ~120px. Clean area y 180 to 1620 must be FULL of visuals. Caption band `CC_Y 1500`, emphasis 1480, column 940px.
- Panels flip to vertical (rails -> columns, dashboards -> 2x2, side-by-side -> stacked) and get BIGGER (container and type), equal padding. Text buttons become icons (Install -> download icon -> done icon).
- Camera scales do not port: a tall frame needs MORE zoom (floor ~1.6x); visible design width = 1080 / s. Bigger panels and big zooms spend the same budget: pick one deliberately.
- Charts stay horizontal: scale as one unit, start zoomed on the y-axis labels, follow the curve, show the whole chart once.
- Decoration (outro) runs edge to edge; the logo lockup sits dead centre with nothing else in the centre.
- Effort record: initial port in one session, then 6 review rounds over 3 days (21 files, ~750 lines). Most rounds were alignment and padding.

---

## 13. Pre-render checklist

- [ ] Every scene listed in `TOTAL_FRAMES`; every audio window ends inside its scene with >= 0.4s tail.
- [ ] Render transcribed: every line in its own scene, no repeated or clipped syllable.
- [ ] Every caption opens 0.3s before its first word, exits with fade + drift, never overlaps the next; CC and emphasis never say the same words.
- [ ] Every block has an exit; continuation cuts pixel-diff clean.
- [ ] Every camera push has a centred target and lands on its word; returns wide (or holds by direction) before the cut.
- [ ] No overlaps, no tilts, no em dashes (`grep` the source for the character), official SVG icons.
- [ ] Panels hold ~1s after their line; hero stats >= 2.5s.
- [ ] `DECISIONS.md` appended; commit; push; never merge to master.
