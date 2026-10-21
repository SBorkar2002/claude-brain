---
name: feedback-comic-hard-cuts
description: "Comic episode videos are cut-cut-cut — every panel hard-cuts, never a crossfade/fade, even on scene changes"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 33bb43b4-c232-415a-b741-3929b64ec3f5
  modified: 2026-09-11T08:33:48.071Z
---

When assembling a comic episode in Remotion (loop, graph, etc.), **every panel
HARD-CUTS to the next. No crossfades, no fade-in/out — ever, not even on a
scene or mood change.** Comics are cut-cut-cut. Sejal flagged a v1 of the graph
cut for having "smooth transitions that don't sit right."

**Why:** the format reads as a comic; fades make it feel like a slideshow and
soften the beats. This is already written in the skill (`comic-animation.md`:
"the panels themselves are hard cuts and don't animate") — the miss was in
execution, not the rule.

**How to apply:** in the Remotion comp, no opacity crossfade between panels;
each scene Sequence starts exactly where the previous ends. Only per-element
motion pulled out of the plate is allowed to animate, never the panel swap.
See [[feedback-continuation-scenes]] (that rule is the same principle for
matched-layout consecutive frames).
