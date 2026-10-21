---
name: feedback-no-overlap
description: Never overlap UI elements unless user explicitly asks — layout must always have clear separation
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ba75a559-8b7c-419a-b618-44886115e95b
---

Never render overlapping UI elements unless the user explicitly requests it (e.g. layered effects, intentional overlays).

**Why:** Overlapping breaks readability and looks like a layout bug. User called this out explicitly on Row4 (elite badge overlapping counter, squares flying too close to title text).

**How to apply:** Before placing any absolutely-positioned element, check its bounding box against all other elements in the same layer. When using `position: absolute`, confirm top/right/left/bottom values leave clear separation from neighboring elements. If two elements share a corner/edge region, offset one of them.
