---
name: project-comic-cast-lock
description: "Comic art direction — DECIDED 4 Sep 2026: neat comic register (crude/xkcd rejected), greyscale + teal accent, AI has one six-petal mark with an eye"
metadata: 
  node_type: memory
  type: project
  originSessionId: fc202d5b-3fae-47cb-b09e-0997eec6dbcf
  modified: 2026-09-04T09:14:43.810Z
---

Art direction for the comic series, **settled 4 Sep 2026** by Sejal. The register
test was never run; she decided directly.

**Register — neat comic, prompted with ChatGPT.** The crude / xkcd-family
alternative I recommended on 28 Aug is **rejected.** Nothing downstream should
be written to survive both looks any more — `characters/appearance.md` no longer
carries a swappable style block, and `register-test-prompts.md` is deleted.

What that gives up, so nobody re-litigates it: crude-as-Figma-components would
have been ~3× cheaper per episode and made consistency structural rather than
probabilistic. The cost is now real and paid per episode, and the polite blank
face — the series' thumbnail image — stays a generation that has to be checked
rather than a component instance that can't drift.

**Greyscale + exactly one accent** (`#03A6CF` teal) survived. Colour is confined
to the educational animation; the comic itself is greyscale. Value, not hue,
separates the four devs — the tone ladder in `appearance.md`.

**The AI screen signature question is answered by the mark, not by composition.**
The 28 Aug plan was to distinguish each AI by how full its screen is
(empty = burnt out, crowded = manic, diagram = over-documenting). Too weak on its
own once the teal glow went. Now: **all four AIs share ONE mark** — six petals
around a single eye, teal — and the register in the writing is what tells them
apart. Screen fullness is still texture, no longer the whole signal.

The mark is not a face and not a four-point sparkle (every AI product uses one).
Rejected shapes: a triangle-in-chevron, which read as a play button on a
monitor, and a droplet. Full geometry and the three expression parameters
(`gaze`, `squint`, `wide`) live in `comics/characters/appearance.md` under **The
AI mark**; the generator is `comics-video/v10/aimark.py`, which shares its
numbers with the animated `AIMark` component so the exported asset can't drift
from the video. Exported PNG + SVG are in Drive under `AI mark/` at the series
root — see [[project-comic-pipeline]].

**Two motion limits, learned expensively:** a symmetric mark cannot turn its
head, and an internal detail shifting inside a small body is invisible at 48px.
If the AI has to look somewhere, move the whole object.

**Four devs, four identifiers** stayed as recommended: Dev 1's messy hair, Dev
2's coffee and dark circles, Dev 3's glasses, Dev 4's backwards cap. Ties were
cut on CEO feedback.
