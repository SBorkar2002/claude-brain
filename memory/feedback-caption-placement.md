---
name: feedback-caption-placement
description: "Meta rule — captions must stay fully within their designated background area, never overlapping UI elements"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ba75a559-8b7c-419a-b618-44886115e95b
---

Caption text must be fully contained within the clean/white area of the scene it belongs to — never overlapping buttons, cards, notification panels, or other UI elements.

**Why:** Readability. If a caption bleeds into a busy UI element the text becomes illegible and looks unpolished.

**How to apply:**
- Before placing any caption, calculate the safe bounding box for that scene: identify where UI elements start (e.g. notification panel left edge at ~505px in the 2.1× zoomed calendar view) and constrain `width` to stay clear of that boundary.
- If the text is long and wrapping is needed, reduce width and let it grow taller vertically — that's always preferred over horizontal overflow into UI elements.
- Keep `textAlign: center` within the constrained width for readability.
- This applies to all rows/scenes in the DORA video, not just Row 1.
