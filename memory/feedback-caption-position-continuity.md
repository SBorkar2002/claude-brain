---
name: feedback-caption-position-continuity
description: "Captions on consecutive panels of the same shot must stay in ONE position — don't inherit Figma's per-frame layout"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 59ed5d6c-1be0-488a-9d9f-1d2b26aa2046
  modified: 2026-09-03T07:43:27.897Z
---

Consecutive panels on the **same shot** keep their caption in the **same
position**. Do not take the geometry from Figma frame by frame — copy it from
the first panel of the run.

**Why:** Figma lays each caption out for its own frame in isolation, so the
boxes drift between frames that are visually identical. On a hard cut that
reads as the caption jumping across the screen, which breaks continuity even
though each frame looks fine on its own. Caught on E001 `loop`: "Right. Yes."
sat at (562, 237) and "…Say that again…" at (158, 179) — same shot, same
character, caption leaping from upper-right to upper-left.

**How to apply:** when building the caption spec, check whether a panel shares
its artwork with the one before. If it does, reuse that panel's centre point
rather than the Figma node's. Since captions render one word at a time, only
the centre matters — box width and height just set it. Break the rule only when
a panel is deliberately reframed, or when Sejal asks for a specific position.

Lives in `comics-video/v10/spec.py` under CAPTION CONTINUITY. Related:
[[feedback-caption-placement]], [[feedback-caption-system]],
[[feedback-caption-meta-rules]].
