---
name: feedback-continuation-scenes
description: "META RULE — when consecutive video frames are continuations (same layout, elements added), NO fade in/out between them; hard cut with matched element positions"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5950e443-6989-48fb-bd07-f2d84bf6c504
---

META RULE (Sejal, July 2026, Tetriz coaching row): when two consecutive storyboard
frames are *continuations* — the next frame is the same layout with one or more
elements added or moved — there must be NO fade-out/fade-in between their scenes.
A fade reads as a cut and breaks the illusion of one continuous shot.

**Why:** Frame 08 → 09 in the coaching row: 09 is 08's card sliding left to make
room for a new card. Fading between them made it "feel like there's a cut."

**How to apply:**
- Outgoing scene: disable exit fade (`noExit` on CoachScene / equivalent).
- Incoming scene: disable entrance fade (`fadeIn={0}`), and start its shared
  elements at EXACTLY the outgoing scene's final positions (e.g. Frame09's card
  starts at translateX matching Frame07's x=347, then slides).
- Only per-element animations bridge the cut (slides, pops of the new elements).
- Captions may hand off with a quick fade of the outgoing caption in the last
  ~10 frames, since the caption text legitimately changes.
- Fades remain correct for genuinely different scenes (e.g. pillar title cards
  like frame 06, which fades in and out by design).

Related: [[feedback-animation-prefs]], [[feedback-anandhi-storyboard-review]]
