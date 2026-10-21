---
name: project-comic-generated-art-keying
description: "Generated comic art arrives on a SOLID background, not transparent — key it and measure the head before compositing, via comics-video/v10/keying.py + sleephead.py"
metadata: 
  node_type: memory
  type: project
  originSessionId: f900f3e7-0bda-492c-b6fc-bca16d65dbc9
  modified: 2026-09-07T12:20:19.209Z
---

Every asset ChatGPT hands back for this series is a **solid-background raster**,
never transparent. Heads come on light grey `(246,243,244)`; the emoji frames
came on pure white with `alpha=255` everywhere. Dropping either straight into a
Remotion scene paints an opaque rectangle over whatever is behind it — the
screaming-emoji disintegration cut a white hole through the race track for 1.5s
before Sejal caught it on 7 Sep 2026.

**Always key generated art before compositing.** `comics-video/v10/keying.py`
does it: reads the background colour off the four corners, takes it to alpha
with a **tight** feather (`lo=5, hi=12`). The band has to be tight because Dev
1's face fill is `(227,225,225)` — only 19 levels off his own background — so a
generous ramp turns his cheeks half-transparent.

**A second pose is not a drop-in replacement for the first.** The sleeping head's
ZZZ marks extend up and to the right of the face, so its bounding box is wider,
taller and off-centre relative to `face.png`. Naively swapping the file gives
three separate wrong results: share one aspect ratio and the head squashes,
share one height and the face renders smaller, share one anchor and the face
sits low and left. The swap then reads as the head jumping rather than as an
expression change.

`v10/sleephead.py` solves all four numbers (`ar`, `scale`, `dx`, `dy`) by
finding the head as the widest unbroken run of opaque pixels per row — the head
is the one wide blob, floating ZZZ are narrow — and anchoring on the **face
centre, not the image box**. Run it on any new expression:

    python3 v10/sleephead.py ~/Downloads/<file>.png [outname.png]

It prints the lines to paste into `spec.PLAIN["head"]`. `emit.py` warns and
falls back to the awake pose if the file is missing, so a missing expression
can't ship silently.

Related: [[project-comic-cast-lock]] (the register that makes these generations
necessary per episode), [[project-comic-pipeline]].
