---
name: feedback-caption-meta-rules
description: Meta rules for ALL on-screen text in the DORA Remotion video — captions, subtitles, titles, anything VO-derived
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d34891d5-bf3d-45da-a44f-bd55ac4ba270
---

These are hard rules that apply to ALL captions in ALL rows of the DORA metrics video, always, without exception:

1. **Every piece of VO text must be animated word-by-word using WordReveal — regardless of where it appears.** This includes bottom captions, metric titles, scene subtitles, panel descriptions, and any other on-screen text that corresponds to or accompanies the VO. No static spans, no CaptionSlide, no fade-in of a full text block. Each word springs in individually using the WordReveal component (damping:22, stiffness:220, mass:0.5).

2. **WordDelay = 4 frames (~133ms) per word.** Current default: `wordDelay=4`. Captions feel snappy and land slightly ahead of the VO. Never go higher than 6. Scene headings/titles also use 4.

3. **Every caption first letter must be capitalized.** Even mid-sentence captions that were lowercase in design. E.g. "across 33,000" → "Across 33,000", "under an hour" → "Under an hour".

4. **Captions that are sequential must never appear simultaneously.** If caption A is replaced by caption B, A must fade out (or reach its end frame) before B starts, with a clean cut or short fade-out.

5. **Every scene's internal timing must be locked to the VO timestamps — never let scenes run ahead of the VO.** When building or editing a composition that has a voiceover: look up the exact VO timestamp for each phase/cue from `constants.ts` TIMESTAMPS, convert to local frames (subtract the sequence start frame), and anchor each phase's IN/PANELS_IN/CAPTION to those local frames. Captions should fire ~6 frames *before* their VO cue so the first word lands on time. Visual elements (panels, bars, stat cards) should complete animating before the caption fires — work backward from the caption frame to set bar/table draw frames. Never compress a scene shorter than its VO window; never let a scene hold blank for more than a few frames before the next VO cue.

**Why:** The user explicitly set these as "meta rules" to avoid repeating feedback. Scenes running ahead of the VO break the sync and make the video feel rushed or disconnected.

6. **Any text explicitly stated to come from the VO transcript must match the VO word-for-word.** Subtitles, metric descriptions, captions, titles — if the user says "it should be [exact phrase]" or "it's derived from the VO", use that exact phrasing. Never paraphrase, shorten, or reword VO-sourced text. If the VO wording isn't provided, ask before inventing it.

7. **Captions must EXIT gracefully — ease out the way they came in (added Jul 2026, Tetriz video).** A caption must never vanish abruptly at a scene cut or at its end frame. It exits with a short fade + drift (opacity 1→0, translateY 0→~10px, over ~12–14 frames) before the cut — mirroring how the words eased in. On full-scene fades the caption may fade with the scene; on continuation-scene hard cuts (noExit), give the caption its own exit interpolation ending ~2 frames before the cut.

8. **No word repetition between caption tiers (added Jul 2026, Tetriz launch).** The small closed caption and the big emphasis caption must never say the same phrase in the same beat — the CC keeps the setup, the emphasis owns the punchline (e.g. CC "One habit." → emph "Everyone's default."). If de-duping guts the CC, drop the CC for that beat and let big captions carry it alone (done in S7c). Also: emphasis lines need clear air below the card — EMPH_Y 824, not hugging the card bottom.

**How to apply:** When adding any new caption/subtitle/title to any row:
- Wrap it in `<WordReveal>` with `wordDelay={4}`
- Capitalize the first letter of the string
- Check it doesn't overlap with the previous caption
- Derive its `startFrame` from the relevant TIMESTAMPS entry minus the sequence offset, minus ~6 frames early lead
- If the text comes from the VO, use the exact VO wording — never paraphrase

[[feedback-working-style]]
[[feedback-animation-prefs]]
