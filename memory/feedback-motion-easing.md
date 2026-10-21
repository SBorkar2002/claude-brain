---
name: feedback-motion-easing
description: "A pulse/oscillation must ease out, never stop dead at the end of its window; fade by opacity, never by scaling geometry"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 33bb43b4-c232-415a-b741-3929b64ec3f5
  modified: 2026-09-17T08:56:16.769Z
---

**Any oscillating emphasis — a throb, a breathe, a sweep — must be enveloped in
AND out.** Cutting the oscillation at the end of its window snaps the element
back to size and reads as a glitch. Envelope it:
`abs(sin(e·hz)) · min(1, e/0.28) · min(1, (len-e)/0.45)`.

The sibling rule: **never fade something by scaling its geometry.** Draw-in and
fade-out are separate parameters. Scaling a bracket's height to fade it made it
look like it was snapping in half (graph v20).

**Why:** Sejal reads any abrupt stop or size-snap as a render bug, not a style
choice. This is the same instinct behind [[feedback-comic-hard-cuts]] — cuts
between panels are deliberate and hard, but motion *within* a panel always
settles.

**How to apply:** before shipping any looping animation, evaluate it at the last
few frames of its window and confirm it approaches zero. Recorded in the
assembly contract in `video/youtube/comics/skills/comic-animation.md` under
**Motion hygiene**.
