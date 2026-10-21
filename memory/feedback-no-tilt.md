---
name: feedback-no-tilt
description: STANDING RULE — never tilt/rotate cards or any elements; everything stays axis-aligned
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a01a81b7-21a0-4bba-b3d4-81aa78b4a19e
  modified: 2026-08-14T06:03:14.062Z
---

No tilting cards or ANY elements — no rotation on panels, ghost cards, chips, images, anything. Everything sits axis-aligned (0°), in videos, Figma frames, and mocks alike.

**Why:** Sejal (2026-08-14), on the ghost panels behind the Personalised Coaching card: "they're tilted and all, I know you wanted to make them seem like that but don't do it." Organic/scattered ≠ rotated.

**How to apply:** Asymmetry and depth come from position, size, and opacity variance only — never from rotation. Strip any `rotate(...)`/`rot` props when reusing older layouts. See [[feedback-no-overlap]], [[feedback-object-identity]].
