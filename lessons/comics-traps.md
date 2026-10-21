# Comics traps: what cost hours, and what worked

Companion to `../playbooks/comics.md`. Each trap is **symptom → cause → fix (episode)**.
Read the top ten before starting any comic build; they are the ones that recurred.

## The top ten (each one cost a day or more)

1. **VO renders silent except the first line of each voice** → `ffmpeg -i src -ss X ... -af afade`
   (output-side seek) keeps original timestamps, so the fade-out fires before the clip starts →
   always `-ss START -t DUR -i src`, verify with `volumedetect` (mean -91 dB = silent). (EP002)
2. **Remotion "doesn't work on this Mac"** (exit 137, no output; renders hang) → bundled
   chrome-headless-shell is unsigned and SIGKILLed; worker pool can't reach localhost →
   `Config.setBrowserExecutable("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")`
   and `Config.setConcurrency(1)` in `remotion.config.ts`. Cost two days of thinking the tool was
   unusable. (EP001)
3. **Painted mouths read as ink blots / a dash on the neck** → synthesising closed mouths with
   skin patches or dark ovals → flap ONLY between two real drawn plates; find pairs by diffing,
   decide open/shut by ink count; no pair = no flap. Sejal rejected this hard, three times.
   (EP002 v4/v5)
4. **Her line "still fades" after three fixes to the cut fade** → the duck system was ducking her
   under the interrupting cue (1.00 to 0.20 over 0.18s mid-word); the fade was never the problem →
   exclude the interrupting cue from ducking, sever at full level with a 4 ms fade. (EP003)
5. **Printer still audible in every cut for weeks** → a stored "spike map" listed 19 clicks; the
   printer is a sustained ~10s run plus short bursts → re-derive the noise map from the audio
   (2.5 to 8 kHz energy vs the room's low end), cut whole runs, verify spectrally. (EP001/EP002/EP005)
6. **Captions shipped twice (baked + live)** → a single-frame re-export hid only the label being
   fixed; dialogue came back baked → every export is a full hide-ALL-text pass with an asserted
   empty restore list. (EP004)
7. **Wrong word in a "better" take** → ElevenLabs said "ran them at the same time" instead of "one
   at a time", inverting the episode → transcribe every delivered take before use; salvage by
   splicing the bad 0.74s from an older take at a true silence, re-transcribe the join. (EP002)
8. **Bed ended six seconds early / loop landed on a hard seam** → the ambience is pre-rendered
   to one length and the cut grew past it → rebuild the bed on every timing change
   (`v10/ambience.py <total> <night_at> <light_at> [out]`, it prints its own proof). (EP002)
9. **Mixed tempo on one character (8.7% mismatch)** → two baked files stayed at 1.25x after she
   switched to 1.15x; only new splices got 1.15 → when a global tempo changes, rebuild every
   derived file and rescale every cut point by the same ratio; audit syllables/sec. (EP003)
10. **Sejal saw an old cut after "it's fixed"** → two renders shared one filename, her player
    showed the cached first → every render gets a new `vN` in the filename. (EP003)

---

## Audio

| Symptom | Cause | Fix |
|---|---|---|
| "means" heard as "mean"; "mm" of "my" leaking into "Hey" | Cutting on whisper times (up to 0.42s early, ends undershoot) | Word ORDER from whisper, EDGES from a 10 ms RMS envelope; end >= 0.4s past last voiced frame, start >= 0.08s before next onset (EP001) |
| Caption 0.5s ahead of voice for 7 seconds; a sigh played twice | Whisper put a word marker on a breath | Count voiced segments before trusting first/last markers; pitch check (speech 90 to 200 Hz, breath none) (EP001) |
| Interrupted line sounds like a polite handover | 0.4s decay tail applied to an interruption | Tail rule is for segment splits only; interruptions get 4 ms (EP003) |
| Severed "every" sounds unresolved | Cut point read off the envelope (1.82 severed the "-y") | Cut 3 candidates (1.82/1.88/1.92), transcribe each, pick (EP003) |
| A short clip lands ~0.2s late | `startFrom` seek into an mp3 is not frame-accurate | Cut each short clip to its own file, play from 0 (EP001, twice) |
| One line "sounds like a different speed" | Same atempo, but ElevenLabs delivered 4.15 vs 5.4 to 5.6 syl/s | Per-take tempo override toward the neighbours, not all the way (EP003) |
| One line sounds like a different person | Takes from separate sessions drift in timbre (Peter's "Eric" take at 155 Hz vs ~120 Hz) | Re-generate in one batch; F0 autocorrelation identifies whose take is whose (EP003, EP001) |
| Reviewer "can't hear" a line | Asset genuinely 7.7 dB under the median | Audit every line vs the median in one pass; level-match new takes before cutting (EP002) |
| Every SFX inaudible at sensible gains | Office bed source sat at -63 dBFS | `volumedetect` every source before choosing a gain (EP004) |
| Bed "too loud" then whole mix inaudible | Measured in a window where someone was still speaking | Find a proven-silent gap from the VO envelope first, then measure (EP004) |
| Bed set by numbers, she can't hear it; raised, it eats a line | Babble masks speech; level alone doesn't predict audibility | Audible bed ducks under every voice; state the measurement and say audibility needs her ears (EP003) |
| "Where is the office ambience?" at -33 dB | 90% of energy under 1 kHz (phones don't play it) and VO covered 79% of the time | High-pass 140 Hz, duck ~5 dB; landed at -35 gaps / -39 under voice. Don't overcorrect from one "can't hear it" (it may be a Studio playback bug) (EP005) |
| Raised bed clips on knocks | Raising a bed raises its transients | Scan for knocks (15 dB over the room's 50 ms peak) and patch before boosting (EP005) |
| Night dip re-fires mid-film; keyboard runs under the whole episode | Looped `<Audio>` volume callback gets loop-relative frames; `endAt` doesn't stop looped audio | Bake every envelope into one full-length file with ffmpeg/numpy; play one plain Audio (EP001/EP002) |
| Multi-point fade silences everything | Chained `afade` filters each span the whole timeline | One `volume=eval=frame` expression (EP001) |
| Loop seam steps in volume | Levelled after the crossfade | Level the whole stream BEFORE the tail-onto-head crossfade; match end loudness (EP002) |
| Bed sounds like a 35s loop | One clean window looped three times | Use all printer-free windows in order, level-matched, macro-levelled on 6s (EP002) |
| Door thud inaudible though "present" | Landed under a male voice in the same band; 82% energy < 80 Hz | Move it into a VO gap; body 160 to 320 Hz + 3 ms bright crack; verify band energy in the RENDER (EP002) |
| Resampled VO lost consonants | Loaded at 16 kHz, wrote back at 44.1 | Analyse at any rate, APPLY at native rate (EP003) |
| Meme "audio" was hiss | The dog clip was 76% energy at 2 to 4 kHz (camera whine) | Check a clip's spectrum before using its sound; speech consonants live there (EP003) |
| Accent flips (Indian to Russian) on a single regenerated line | ElevenLabs v3 decides accent per generation; short text has no context | Render full script and cut; Multilingual v2 or v3 "Robust"; API `previous_text`/`next_text`; or pad and trim (22 Oct) |

## Captions and text

| Symptom | Cause | Fix |
|---|---|---|
| Captions jump across the screen on a hard cut | Each Figma box laid out for its own frame | Same shot = copy the first panel's box (EP001, EP003 scenes 5/6/12/13) |
| Loop seam text jumps | Last caption at its own Figma spot | Last caption takes the first caption's position (EP001) |
| Captions ran across faces | Short sentences widened to one long line | Figma boxes sit on 0% busy pixels by design; keep their width, split into timed parts (EP001) |
| Words flashed for 7 ms; first words missing | Word-by-word reveal + `start < t` boundary test | Word-by-word was dropped (8 Sep) for whole lines; if ever word-timed: min dwell 0.18s, `start <= t`, assert rendered words == script words (EP001) |
| Two captions overlapped into mush | Two speakers in one panel at one centre | Assert no two captions share a point at once (EP001) |
| Caption bled into the next scene | No clamp | Clamp every caption to its panel (EP003) |
| "On it." sat on the monitor stand | Took Figma's box blindly on a split screen | Measure ink under every caption box; fail the build if on art (EP003) |
| Machine output read as narration (`used in 41 sessions` in caption style) | Text style chosen by eye | Box inside measured screen rect = screen text (Geist Mono, no stroke) (EP004) |
| SFX lettering looked like the keyboard talking | Given caption style | SFX = Arial regular `#3a3a3a`, no stroke (EP004) |
| Flat, unanimated SFX words | Left baked in the plate | Every SFX word pops on its sound; and every sound gets a word (`*thud*` per door) (EP002) |
| Caption style "wrong" on a new episode | Built a new style instead of copying loop's | Copy the exact spec: Lato 800, 32/720, 5px/720 black stroke, paint-order stroke (EP002) |
| Three-dot "..." turned into rings | Live caption's 5px stroke on dots | Keep a drawn "..." baked if it carries no VO (EP003) |
| Explainer cluttered | Subtitles + AI mark on top of the explainer | Explainers have no captions and no mark (EP001, EP002) |

## Lip sync and plates

| Symptom | Cause | Fix |
|---|---|---|
| Character talks "in negative" | Assumed which of a pair was open | Count dark pixels in the mouth box (open = filled oval = more ink) (EP003, days lost) |
| Frame renders blank on "try me" | Flap requested a plate variant that didn't exist | Guard: flap only if a real pair exists (EP003) |
| Black blob at the mouth edge | Mouth patch box smaller than the open mouth | Cover the whole open shape (EP003; then patches were banned anyway) |
| Two-shot "breathes" | bbox-based registration shifted one frame +3px; best fit was 0 | Register by minimum residual diff; for one moving mouth, swap only that mouth region onto one fixed body (intro) |
| Mouth chatters | Flap followed every envelope wiggle | Calm flap: local threshold, >= 5 dB dips close, runs 3 to 9 frames (EP005, PE) |
| Thought line moved the mouth | Flap applied to a thought | Thoughts, listening, off-screen VO never flap (EP002, EP003) |
| Head swap "jumps" | Sleeping pose has ZZZ, different bbox | `sleephead.py` anchors on the face's widest opaque run (EP001) |
| White rectangle cut through the track | ChatGPT art is on solid bg, not transparent | Key everything (`keying.py`, lo=5 hi=12) (EP001) |
| Mark on wrong screen after a finger occludes it | Re-detecting the screen per frame | Lock the mark position per shot (EP003) |
| Mark on title cards / shots with no monitor | Hand-typed frame list | Earn the mark by measurement: rect >98.5% near-white, <0.8% ink, no caption inside; explicit exclusion set for title cards (EP004) |
| A "changed" Figma frame came back identical (twice) | A layer hadn't taken | Diff every re-export against the frame it should differ from (EP003) |
| Pink lines at frame edges | Frame 714 tall instead of 720; scene4.5 1082 wide | Assert exact plate size on export, crop (EP001, EP003) |
| Ghost frames at the wrong time of day | Assumed both sleeping plates were night | Measure plate brightness (183 vs 93) before assigning headers (EP002) |
| Lettering smeared when painted out | Glyphs sit on top of the art | Hide SFX text in Figma and re-export; never inpaint (EP003) |
| Fringe/eaten linework on dark plates | Frame bg fill exports with the node | Temporarily set frame fill white, export, restore (panel generator rule) |

## Motion and explainers

| Symptom | Cause | Fix |
|---|---|---|
| Arrow/dot flicker only in the export | Animated real width/height, edges snap per frame | Transform only (scale/translate); confirm with `--sequence` lossless frames: alternating diffs = snapping (EP002) |
| Pulse "stops dead" | Oscillation cut at window end | Envelope in and out (0.28s / 0.45s) (EP002) |
| Bracket "snapped in half" | Faded by scaling height | Separate draw-in and opacity (EP002) |
| Loop icon jumps at the end | Motion computed only inside its window | One eased curve landing on whole turns (EP001) |
| Arcs clipped "by a box" | Tight SVG viewBox | Pad viewBox, scale container to compensate (EP001) |
| Strobing | 5.5 rad/s pulse | ~3.4 rad/s (EP002) |
| Clock prop wandered between shots | No wall holds a prop across setups; fixed size reads as a sticker | Time = mono header that follows the light (EP002) |
| Beat card killed a joke | Card landed between laugh and sleep frame | No time cards; header instead (EP002) |
| Explainer read as "parallelism" not "dependency" | Doors show permission, not waiting; biggest motion on the result | Name the relation (`WAITING ON API`); give the arrow the weight (EP002) |
| Explainer too fast | Visuals outran the VO | Insert 1.2 to 1.5s pauses at sentence gaps (6 ms fades), never slow playback (EP002, EP005) |
| "I didn't get the story at all" from 3 icons | Icons read as a toolbar | Nine passes on EP001; landed on two opposite shapes (ring for technical, race map for plain). Mock options in Figma first (EP001) |
| Title on top of its own visuals | Not cleared first | Title holds ~1s alone, then clears (EP004) |
| Reveals outlived a shortened line | Visuals don't shorten with the VO | Re-check every reveal after any VO re-cut (EP004) |
| Queue looked like sliding blocks | Parallel tracks, `abs(sin)` bob | Single file from one point, smootherstep, 0.13s stagger, signed-sine bob (EP002) |
| White flash on every cut in Studio | Image decode | Preload plates ~12 frames early at opacity 0 (EP001) |
| Overlay blinks on a cut | Each Sequence fades its children | Shared overlays in one Sequence (EP001) |

## Tooling, delivery, process

| Symptom | Cause | Fix |
|---|---|---|
| Studio won't open from preview tools | macOS TCC blocks reading ~/Documents | Run Studio in Sejal's terminal panel, fresh port (3334/3335) (EP005) |
| "i literally asked you to make it on remotion" | Built the first cut in plain ffmpeg | Remotion is the only assembly path (EP001) |
| Duration off by one frame | `round((b-a)*30)` on floats | Difference of already-rounded frame numbers (EP001) |
| Timings rotted when a take changed | Hand-typed cue times / index-addressed lines | Derive every cue from the audio; address lines by a word seed; stop by name if a word is missing (EP003) |
| `emit.py` broke after cleanup | `v10/frames.py` looked dead but emit imports it | Keep it (4 Sep cleanup) |
| Drive upload of media impossible via MCP | `create_file` is inline content | Chrome file-input + synthetic drop technique (playbook section 10) (EP001) |
| Second drop raised replace-or-keep dialog | Re-dropped to "check" | Drop once; verify by screenshot/search (EP004) |
| `file_upload` rejected files | Staged with hard links | `cp` copies (EP004) |
| 16.7 MB cut wouldn't upload | 10 MB per call cap | `split -b 8500000`, rebuild Blob, SHA-256 check, drop once (EP005) |
| Uploads landed inside a subfolder | Drop point was a folder row | Check `elementFromPoint` before dropping (EP005) |
| Docs PR merged an old draft | Squash-merged before the rewrite was pushed | Check what a squash merge captured; use fresh branches (product-brain PR) |
| Merged two of her frames unasked | "Improving" the board | Ask before changing what a frame is (EP004) |
| Production notes bloated the review artifact | Wrote build history onto the page | Artifact = panels + one short note; history in the repo (EP001, twice) |
| Agreed with each reviewer in turn | Endorsing whoever spoke last | Form a view, push back on her and reviewers, then follow her call (EP003) |
| Thread spiralled toward a full rewrite | Opinion without data | Diff the plates: scene25 vs 26 = 0 px; 8.74s where only a mouth moved (EP003) |

---

## What worked (repeat these)

- **Data-driven cut.** One emitter per episode writes one JSON; the TSX only renders. Retiming is
  a number in one file. Every episode after EP001 built faster because of it.
- **Seamless loops via one sentence across the cut.** Last panel is frame 1's own plate,
  pixel-identical; one take split mid-sentence at its own pause; bed tail folded onto its head.
  EP002 ("...but-" / "you took all night for this??"), EP003 ("oh yeah, as i was saying.." /
  "my sister just books the whole thing").
- **The held blank face** between the technical and plain explanations: the single most praised
  beat (EP001).
- **Hard cuts plus abrupt audio** for comedy: "AH" cut in half, wake-up ding landing a few ms
  before the reaction, the interruption at full level (EP002, EP003).
- **Meme inserts with no entrance animation**: shivering dog over Peter (EP003), sleepy cat in the
  queue (EP002), banana/happy cats as patients (EP005), crying dog avatar swap (PE). Keyed off
  green, low or no audio.
- **A metaphor born from the VO's own words** (doors from "they sat in line four hours for
  nothing", EP002) and icon resolvers over text (EP005 doors, 50/50 to 94% card).
- **The intern (AJ) and the graph episode**: the "intern video" reached 30k+ Instagram views,
  ~20x the others. AJ is the proven character; the shorts experiment reuses him on purpose.
- **Silent beats**: a panel up with no caption before the first word (dark-room "..Peter?",
  EP003's 2.5s gap, scene4.5 bridge held 1.8s).
- **Measuring instead of arguing**: ink counts for mouths, pixel diffs for "it doesn't land",
  syllables/sec for "wrong speed", busy-pixel % for caption placement. Each settled a dispute in
  one message.
- **Figma frames before animation** for every explainer redesign; Sejal approves the static
  state, then it gets animated.
- **Per-line VO generation** with pauses written into the take, and a re-recorded short line to
  replace one mispronounced word (PE "constraints").
