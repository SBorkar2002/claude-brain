# Video traps: what cost hours, and what worked

Symptom -> cause -> fix, from the Tetriz launch video (Remotion, Jul to Aug 2026, dozens of review rounds), its 9:16 port, the DORA explainer (HyperFrames, Claude Design, Remotion), and comic-episode audio work. Read before touching any narrated video. The playbook is `playbooks/video-production.md`.

---

## 1. VO and audio

| Symptom | Cause | Fix |
|---|---|---|
| Last word of a line sounds chopped ("handled", "...the next.") | Window ended on the Whisper `end` timestamp, which marks the last phoneme, not the audible decay. Once a window closed 2 frames after the word. | Leave >= 0.4s (12 to 15f) after the last word. Then shift the next window's `startFrom` AND `from` by the same amount so downstream alignment holds. Verify by RMS on the render. |
| A syllable plays twice across a scene cut ("bec- because", "guess... ss") | Window B resumed at the same source frame window A ended on, or the cut sat inside a fricative; whisper start times are late so the next onset leaked. | End windows mid-silence, several frames clear of the next onset; never let two windows contain any part of one word. Add a 4f fade-out / 2f fade-in at the seam. |
| Four cut attempts in a row all leaked | Word boundary was read from the energy envelope. The loud burst assumed to be "because" was the "-ess" of "guess". | **Transcribe candidate cut points** (cut at 3 to 4 positions, transcribe each, pick the clean one). Never infer word boundaries from energy alone. |
| A breath could not be inserted cleanly no matter where | The read co-articulated the two words; no silent seam exists. | Stop after measuring: either re-generate with punctuation that forces a pause, borrow that phrase from an older read that has a real seam (only at a scene cut), or drop the pause (Sejal's eventual call). |
| Splicing one phrase from another read sounded abrupt | Voice changed mid-scene. | Change reads only at a scene cut, where a cut already exists. |
| Two VO lines played on top of each other for 67 frames | After a scene re-order, a window longer than its scene spilled into the next scene's audio. | After any re-order, list every window's `from + duration` against its scene end. Give each line its own window starting on the frame its text appears. |
| A new VO read desynced the back half of the video | Beats were shifted by a constant; the new read was progressively tighter (up to ~8s cumulative). | Re-derive every scene's beats from the new word timestamps with the one formula. |
| Whisper said gaps were fine; they sounded too long/short | Whisper back-dates segment-initial words; its gaps lie. | 20ms RMS silence map on a 16kHz mono wav of the render. |
| "Tetriz" transcribed as "Tetris", "org" as "awg", "hour" as "R" | No vocabulary hint. | `initial_prompt` with product nouns; spot-check odd words by listening. |
| 90% of sliced VO lines rendered silent | ffmpeg `-ss` placed after `-i`, so `afade` ran on original timestamps and faded everything to zero. | `ffmpeg -ss START -t DUR -i in.mp3 -af "afade=t=in:st=0:d=0.03,afade=t=out:st=DUR-0.08:d=0.08"`. Check `volumedetect` (-91 dB = silent). |
| One line "sounds like a different speed" though tempo was identical | ElevenLabs picks its own delivery rate per generation; `atempo` preserves the difference (4.15 vs 5.5 syllables/s). | Measure syllables/s per segment; per-take tempo override closing most of the gap (4.15 -> ~4.6). If timbre also differs, re-generate in one batch. |
| An interrupted line "still fades out" after three fixes | The fade was the ducking system ducking her under the interrupter's cue, not the cut. | Exclude the interrupting cue from ducking; sever at full level with a 4ms fade. |
| "I can't hear the ambience" then "it's eating the line" | Bed set by level only; babble masks speech; most energy under 1 kHz; VO covered ~80% of runtime. | High-pass ~140 Hz, duck ~5 to 7 dB under every voice. Start near -30 dB in gaps; the landing level was -35 in gaps / -39 under voice. Say you can verify presence, not audibility. |
| Wrong word in the read ("within the org" vs "within the hour") | Generation drift. | Patch that one sentence from the previous master at the same anchor frame with tails both sides, or re-record the line. |

## 2. Timing and sync

| Symptom | Cause | Fix |
|---|---|---|
| Reviewer: "the curve isn't bending AS she says it" | Draw-on was a single long inOut ease; nothing visible for the first seconds after the anchor word. | Two-phase draw: visible ease-out rise within frames of the anchor, inOut surge landing on the target word. Derive frames from the word JSON. |
| KPI cards appear before the VO mentions them | Beats placed on round seconds or scene starts. | Each mark pops on the word that names it; everything else in the panel arrives earlier. |
| Label "The gap is the AI Tax" named something not yet on screen | Hardcoded `fadeAt(471)` from an earlier layout. | Gate labels after the thing exists AND after the VO says it. |
| Panels vanish before anyone can read them | Scene ended on the last word. | ~1s hold after each line (silent gap between windows); keep ambient motion so it is not frozen. 1.5 to 2s holds felt too long. |
| The final state of a build existed for only ~12 frames | Build ran the whole VO line. | Build fast, rest long: final state should own most of the line. |
| Captions popped up too early / at odd times | Starts at arbitrary local frames. | Fixed lead: 0.3s (9f) before the first word, measured. Ends ~14f after the last word. |
| Last scene silently cut to 79 of 240 frames | New scene not added to `TOTAL_FRAMES`. Render "succeeded". | Every scene in `TOTAL_FRAMES`; check the last frame of the render. |
| Checked a fix at the wrong moment and concluded it failed | Beat constants are scene-local; `remotion still Full` takes a global frame. | `global = scene.start + local`. Print the scene table before checking. |

## 3. Remotion rendering

| Symptom | Cause | Fix |
|---|---|---|
| Draw-on looks right in Studio, wrong in the render | SVG `pathLength` misrenders in headless Chrome. | Measured polyline + real length in `strokeDasharray/offset`. |
| Stray dot at the start of an undrawn curve | Fully offset round-cap dash still renders a cap. | Render nothing until progress > 0.001. |
| Shield outline left a gap at the top | Hand-estimated dash length. | Measure (or normalise) the real length. |
| White focus wash "never visible" though coded | Overlay was `inset: 0` inside a transformed zero-size parent: rendered 0x0 px. | Explicit full-frame size (1920x1080) on overlays inside transforms. |
| Fonts wrong in some frames | CSS `@import` not loaded when a sequence mounts mid-render in a parallel tab. | `Fonts` component with `delayRender` + `document.fonts.load` per weight. |
| "12 active11 active" flashed side by side | Two spans crossfading in normal flow. | Absolutely stack the incoming span over the outgoing. |
| Curve sagged below its start dot after "making the chart bigger" | Bezier control points are hardcoded pixels; plot box was resized. | Never resize `PLOT_*`; move/scale the chart group with a transform. |
| Children past x=1080 squeezed to zero width (9:16) | No explicit containing block in the design-space wrapper. | Give Stage/Camera an explicit `width: SCENE_W`. |
| 9:16 port clipped the bottom of charts | 17 hardcoded `1920`/`1080` literals did not follow the constants. | Replace literals with `WIDTH`/`HEIGHT` first, confirm 16:9 is identical, then flip. |
| Camera follow looked jagged | Follow keys sampled every 5 frames. | Sample every frame with the draw's own easing; one shared progress function. |
| Camera reached the top of the curve before the pointer | Camera and pointer used different easing copies. | One progress function drives both. |
| Camera "jumps" when switching from keys to follow-cam | Boundary key eyeballed. | Compute the key at the boundary frame from the override's value. |
| `collect is not defined` after deleting a feature | Leftover reference in a gate. | `npx tsc --noEmit` after removals (not bare `tsc`). |
| `remotion still` takes ~40s each when checking many frames | It re-bundles per call. | Bundle once, render a list of frames (a `shots.mjs` script). |
| Shell heredoc scripts fail with FileNotFoundError | Shell cwd resets between calls. | Prefix every command with `cd <root> &&`. Composition id is `Full`, not `FullVideo`. |
| Transient "NetworkError" on a still | Flaky. | Retry once. |

## 4. Editing the code (Claude-side process)

| Symptom | Cause | Fix |
|---|---|---|
| A "fixed" alignment bug survived a whole review round | Python `s.replace()` missed on indentation (18 vs 16 spaces) and silently no-op'd; new constants were added but never referenced. | Every string surgery asserts `old in s` before and `old not in s` after. Then measure the result in pixels. |
| A patch "passed" but half the job was missed | Assert matched one panel; the sibling panel had a different value (21px vs 20px). | When a rule applies to a family of panels, grep all siblings. |
| New card layout appeared in one scene but the old one in the next | A private copy of shared card internals. | Export the body component, not just numbers; one definition. |
| A column title appeared that was never in the design | Invented while re-laying out. | Answer "was this in the original?" from the repo and frames, not memory. Never invent labels. |
| Same card wrong three rounds running (9:16) | Layout fixed by eye; sized for 5 data rows when the array had 6; `ROWS x PITCH` adds a phantom pitch after the last row. | Derive geometry from one arithmetic chain written into the source; count rows first. |
| Board columns drifted left of their headings | Hand-picked heading offsets differed from cell offsets; mixed left- and right-anchored offsets in one row. | One column grid (`COL_W` summing to the inner width); headings and cells from the same grid; list the gutters to verify. |
| "Centre alignment" read too literally: every avatar at a different x | Centred avatar+name groups of different widths. | Align like a table (see playbook section 9). |
| Built over Sejal's manual Figma edits | Rebuilt frames from my last version. | Re-screenshot the frame before animating; surgical edits only. |

## 5. Design and review

| Symptom | Cause | Fix |
|---|---|---|
| "Everything looks like a box" | No object language. | Icon carries identity, colour carries state; official vector icons. |
| "Focus is in five different places" | Several elements animating at once. | One thing moves at a time; de-emphasise the old. |
| "No visual difference between bad and good" | Same component, same colours. | Visible transition (red -> green, crossed out -> checked). |
| Accent words in the scene's identity colour flagged as a mistake | Lever colour used for emphasis. | Emphasis words are always brand TEAL. |
| "Don't tilt the cards" | Rotation used for organic feel. | Position, size, opacity only. |
| Ghost background panels "not visible at all" and "2 left 2 right doesn't make sense" | Opacity 0.14, mirrored placement. | Raise to ~0.3 to 0.4, uneven scatter. |
| Heart shape did not land for executives | Literal metaphor. | Abstract (a diamond echoing the icon layout). |
| A stat on screen ~1s then gone mid-zoom | Stale camera keys ran past the scene end. | Hero stats >= 2.5s at final framing, move completes early. |
| Zoom "not zooming onto anything" | Camera travelled sideways toward empty space. | Straight push about the subject's centre (x/y unchanged). |
| Abrupt scene ends flagged in three scenes in one round | Blocks with an entrance and no exit. | Audit the last 15 frames of every scene. |
| A continuation cut "feels like a lag" | Fade out/in between identical layouts. | Hard cut, matched positions, pixel-diff the boundary. |
| Navbar of the next state flashed for a beat | Persistent chrome snapped / lingered across a cut. | Mount it in the outgoing state and ramp; remove it inside the previous scene when the next has none. |
| Captions collided with zoomed panel text | Panel text drifted into the caption band on push-ins. | CaptionScrim tied to camera scale. |
| Caption and big emphasis said the same words | Two tiers carrying the same phrase. | CC carries setup, emphasis the punchline; drop the CC if needed. |
| Word-by-word CC pulled eyes away from visuals | Old rule (WordReveal everywhere). | CC full line at once; only emphasis reveals by word. |
| Avatars leaking outside their circle | No clip on the image. | Clip avatar images to the circle. |
| Jagged dark outlines on brand logos | PNG tiles background-stripped by pixel processing. | Official SVGs; ask for the file if none exists. |

## 6. Tools and access

| Symptom | Cause | Fix |
|---|---|---|
| Every Figma call `net::ERR_FAILED`, even after reconnecting | The session's connector bridge died; a stale session cannot reopen the transport. | New session, `whoami` first. Meanwhile the desktop Dev Mode MCP (`127.0.0.1:3845`) works read-only. |
| Sejal: "Why are you sending me an SVG?" | Write connector dead, I fell back to an SVG mock without saying why up front. | Say immediately that Figma write is down and what she needs to do; offer the fallback as a stopgap. |
| Desktop Figma MCP: "nothing selected", timeouts, "node not found" | It reads only the frontmost file and the live selection; a huge section times out; a view-only seat blocks metadata. | Frontmost window, select ONE frame, call immediately; check which team/seat owns the file. |
| `page.findChildren` missed frames, rebuild duplicated them | Frames were inside a Section. | `section.findChildren` / `page.findAll`. |
| `get_screenshot` of a Section looked huge | Render pads to canvas origin. | Ignore; screenshot frames instead. |
| HyperFrames output was bad (frames fighting) | Agent put `data-start`/`data-duration` on inner clip divs while a GSAP timeline also drove opacity; zoom applied to the scene wrapper. | One paused GSAP timeline owns all visibility; zoom the image, not the wrapper. Quality still judged poor overall. |
| Claude Design export: start of video blank | Animated elements had no CSS initial `opacity:0`; and a localStorage "resume playhead" restored a mid-animation position. | CSS initial states + `gsap.set()`, stage hidden until `fitStage()`, no localStorage resume. |
| Skill file pasted into Claude Design did nothing useful | Generation tools take a prompt, not a rules doc. | The skill runs in Claude Code and outputs a merged prompt you paste into the tool. |
| Claude Design kept breaking the branching tree | It cannot hold complex SVG paths while animating. | Code it (Remotion/HyperFrames path draw) or render it elsewhere (Higgsfield worked) and composite. |
| `npm install -g` EACCES; `sudo` impossible in agent shell | Global prefix in `/usr/local`. | `npm config set prefix ~/.npm-global` and add to PATH, or Sejal runs sudo herself. Never accept a password in chat. |
| Org monthly spend limit hit mid deep-research | Fan-out research workflows are expensive. | Keep research scoped; results arrive partial. |

---

## What worked (repeat these)

- **The master mp3 is never edited.** Playback windows + a silence map made pauses, re-orders (a whole narrative re-order with no re-record), and single-line splices cheap and reversible.
- **One formula for every beat** from word timestamps, and re-deriving (not shifting) when a new read lands.
- **edit -> still -> Read -> adjust**, and measuring (RMS, transcription of the render, pixel diffs, hue-isolated alignment) instead of eyeballing. Every real bug was found by measuring.
- **Frozen baseline PR before a rework**, branch per rework, `DECISIONS.md` every session, `HANDOFF.md` so a fresh session resumes in minutes.
- **Shared components as the house style:** `WordReveal`, `popReveal`, `Camera` + `CaptionScrim`, `PillarMap` with eased handoff. Rules that become components stop regressing.
- **Shared-element continuity:** the same chart object travelling across scene cuts; panels growing from and collapsing into their nav chip.
- **Design in Figma first, then animate**, with Sejal approving the frame.
- **Rules into the skill file the same day**, listed for her approval first (new / changed / overridden / removed).
- **9:16 as a git worktree** with a diff that proves timing untouched.
- **Spine before script** and checking every feature claim against product ground truth caught two real contradictions and a fabricated stat before render.
