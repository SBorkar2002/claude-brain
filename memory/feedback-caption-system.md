---
name: feedback-caption-system
description: "Two-tier caption system — closed captions (small, bottom-center, full VO, always) vs baked-in emphasis captions (large/weighted, anywhere, always above the CC zone)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5149539b-f928-45b2-bda9-ef87f6710745
---

Sejal, Jul 2026 — Tetriz videos move to a two-tier caption system (replaces the
old "every caption is a baked WordReveal" approach):

1. **Closed captions (default, always on):** carry the FULL VO script. Small font,
   bottom-center, present in every scene. This is where the transcript lives now —
   NOT baked into the frame. Keeps the screen uncluttered / muted-watchable.

2. **Baked-in captions (emphasis only):** used only when a specific line carries
   real value and deserves weight. Larger font + heavier weight, can be placed
   ANYWHERE on the screen (it holds value, so it's a design element). **HARD RULE:
   a baked-in caption must ALWAYS sit ABOVE the closed-caption band — never overlap
   the CC zone at the bottom-center.**

Reserve a bottom-center CC band (e.g. ~y 940–1015 in a 1920×1024 frame). Baked-in
emphasis text lives above that band, anywhere the composition wants it.

Some scenes are VO-only with NO captions at all (e.g. the "Three upgrades" offer /
logo+cards moment) — neither CC nor baked, by explicit direction.

Related: [[feedback-caption-placement]] [[feedback-caption-meta-rules]] [[feedback-object-identity]]
