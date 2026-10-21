---
name: feedback-animation-prefs
description: Animation preferences and rules for the DORA video project (Page 2 only)
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9bc1ae27-797c-40a4-873a-9bf29c451411
---

Animate Page 2 only. Page 1 is a rough draft — ignore completely.

**Why:** Page 2 is the final production frames. Page 1 is exploratory/reference only.

**How to apply:** Never reference page 1 frames when planning or building animations.

---

## Global animation rules

- **Tool**: Remotion (preferred) or Claude design. Animate row by row (1→2→3→4→5→6), stitch at end.
- **All transitions**: Smooth, no quick swaps. Everything eases into existence.
- **Baked-PNG ghosts — cover, then redraw (meta rule, Jul 2026)**: When animating over exported Figma PNGs, every animated element already exists baked in the PNG. Cover the baked content region with a solid div in the frame's EXACT bg color (pixel-sample it — bgs vary per frame), then reveal only via animated PngClip windows or fresh draws. One-instance rule: an element appears either via its revealed baked pixels OR as a fresh animated copy, never both (double-tooltip bug). Rounded elements get rounded clips + their own boxShadow (square clips slice corners/shadows sharp). Baked navbar must be masked/pinned so it never appears as a second navbar during motion. Positions from Figma node geometry, not eyeballing.
- **Lines are DRAWN, never eased/faded in (meta rule, Jul 2026)**: Any connector/line between two or more elements must animate as if drawn from its start point to its end point (SVG length interpolation, strokeDashoffset, or a directional clip reveal along the line). NEVER fade a line in, and never let a line ride inside an element's pop/translate animation — a horizontal line easing in vertically looks broken. Corollary: when popping PNG-clip elements, the clip region must exclude baked line pixels (clip icon+label only), and the drawn SVG line is the only line on screen.
- **Theme-bridge fade (meta rule, Jul 2026)**: Whenever a transition crosses light↔dark themes (e.g. light UI frames → the dark constellation logo animation), NEVER hard-cut — always bridge with a fade. Implementation: the outgoing scene dips to the incoming theme's exact base color (a full-frame overlay fading in over ~20–25 frames, covering the navbar too — this overrides the navbar-never-fades rule for theme changes), then the incoming scene starts on that same color so the cut is invisible. Constellation bg is #060608.
- **Navbar NEVER fades (meta rule, reaffirmed Jul 2026)**: The navbar stays pinned at full opacity through every scene transition — render it OUTSIDE the fading scene container (component NavBar overlay in row 1; pinned top-strip PNG clip in CoachScene rows). The ONLY exception is pillar title screens (THE COACH / THE PLAYBOOK / THE MEMORY), where the whole frame including navbar fades by design (`pinNavbar={false}`). If a scene wrapper fades its full frame, that's the bug to fix. See [[feedback-continuation-scenes]].
- **Title cards** (1E, 6A, 4A, 5A etc.): Standalone full-opacity appear — no sub-animations, single statement.
- **Subtexts / captions**: Always ease in AFTER the main title is shown. Delay ~200ms.
- **Terminals** (ALL frames with terminals): Typewriter effect, line by line, quick pace. Applicable to every terminal scene in the project.
- **Scatter plot dots**: Pop in RANDOMLY (not left-to-right or ordered). Quick stagger ~40ms. Applicable to all scatter plots designed in the future.
- **Arrows + annotation text** (e.g. "Are you here?", "ELITE THRESHOLD"): Arrow reveals first, then text pops in after (scale 0.8→1 + opacity 0→1, ~250ms).
- **Word-by-word VO sync (meta rule)**: Every text block — titles, subtitles, captions — must reveal word by word timed to the VO speaker. Use `WordReveal` with `wordDelay` calibrated to speech pace: titles 5–6 frames/word, conversational subtitles 6–8 frames/word, deliberately spoken subtitles 7–9 frames/word. Never reveal all text at once.
- **List / table row stagger (meta rule)**: All list items animate in one by one with consistent stagger, for BOTH the failure and success states. Never fade an entire list in at once. Use the same `STAGGER` offset for all states so rhythm is identical.
- **No label/badge buttons** unless the Figma design explicitly shows them (e.g. remove "ELITE · MULTIPLE PER DAY" pills if not in final design).
- **D·O·R·A reveal**: One letter at a time, staggered ~120ms each.
- **Calendar event popups**: Card pops up (scale 0.92→1 + opacity 0→1, ~280ms). Calendar pre-set to correct date before card appears.
- **Element stagger default**: 120ms between sequential reveals.
- **Easing**: ease-out cubic (0.0, 0.0, 0.2, 1.0).
- **Title in-duration**: ~400ms.
- **Pop-up duration**: ~250ms.

- **Nothing appears, changes color, or glows abruptly (meta rule, Jul 2026)**: every element eases IN (fade + slight scale/translate, ~15–20f) and OUT the same way; every color change and glow is an eased CROSSFADE over a window (use `interpolateColors` + `Easing.inOut`), never a binary switch on one frame. A hard pop/instant recolor reads as a bug. This is common-sense default for ALL elements — icons, labels, cards, state/color changes, glows.

- **Camera language (meta rule, Jul 2026 — launch video)**: Sejal wants virtual-camera moves on top of element animation — zoom in on the exact spot where a number counts / a bar fills / a click happens; follow-cam on text as it types; then ease back wide. ALL camera moves are smooth eased transitions ("should not be abrupt… not a cut"). **The WHOLE screen zooms together — the pillar map / any persistent header goes INSIDE the camera and slides off-frame naturally (never pinned, never faded out). Only captions/emphasis stay outside, fixed.** Hold the camera STEADY while elements fly in (don't chase each item — their motion carries the shot). Go TIGHT on hero moments: clicks ~2.1+, typed text ~2.5 ("zoom in as much as you can"). Implementation: `components/Camera.tsx` in tetriz-launch-video-v4.2 — keyframes {f, x, y, s}, inOut-cubic per segment, hold by repeating a key. Reuse for future videos.
