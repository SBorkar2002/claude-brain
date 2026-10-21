---
name: feedback-sfx-text-pops
description: "Every SFX word on screen (click, swipe, ding, AH, scream) must pop/animate on its sound — never baked flat into the plate"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 33bb43b4-c232-415a-b741-3929b64ec3f5
  modified: 2026-09-12T09:54:44.659Z
---

**The rule runs both ways.** Every sound-effect word rendered on screen gets the
same pop treatment — not just "click" — **and every sound that plays gets a word
on screen.** Adding an SFX without its lettering breaks the comic's language;
the audience has been taught that sounds are spelled out (flagged on graph v34
when a door thud shipped with no `*thud*` beside it).

click, swipe, *ding*, -AH, AHHHHHH-, *thud*, and any future SFX lettering snap
in exactly on their sound, overshoot in scale, settle, and clear. None of them
may sit baked-flat in the exported plate. If you add a cue, you owe it a word.

**Why:** Sejal built the click-pop behaviour in the loop video and expects it as
the house language for SFX lettering; a static SFX word next to an animated one
reads as an oversight (flagged on graph v6, 11 Sep 2026).

**How to apply:** hide the SFX text nodes in Figma before exporting frames, read
their geometry first (x/y/width/rotation/fontSize — swipe is rotated, so carry
the rotation through as CSS `rotate(-figmaRotation)` with `transform-origin:0 0`),
then render them in Remotion with a shared component: snap-in ~0.05s, scale
overshoot decaying over 0.26s (the click's constant), hold, then clear.
Timed to the actual SFX audio, not to the panel start. See
[[feedback-lip-sync-real-frames]] and [[feedback-comic-hard-cuts]].

**DONE:** folded into the assembly contract in
`video/youtube/comics/skills/comic-animation.md` (17 Sep 2026), both directions.
