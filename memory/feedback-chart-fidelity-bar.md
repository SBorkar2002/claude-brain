---
name: feedback-chart-fidelity-bar
description: "Manager reference (2026-07-06): chart/analytics/dashboard scenes in launch videos need real product-prototype polish, not wireframe sketches"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d07d3b1e-6e7e-4c8e-9ced-d2f1a0ea30ad
---

- **Any scene showing a chart, stat cards, or dashboard UI must be built at real product-prototype
  fidelity — not a rough wireframe/sketch — even though it's conceptual and doesn't need to match
  a real Tetriz screen pixel-for-pixel.**
  **Why:** Sejal's manager shared a reference mockup (a Claude-style analytics dashboard: icon-paired
  stat cards with delta arrows, smooth step/area charts with dashed gridlines, pill filter chips,
  staged as a light product window floating inside a bold saturated color canvas) as the bar to hit.
  Explicit: "even though conceptual, we are allowed to have conceptual screens... we do not need
  to match the design with the actual dashboard" — the point is polish level, not accuracy to the
  real product.
  **How to apply:** Full detail written into [[reference-product-brain-repo]]'s sibling skill file
  `tetriz-content/skills/launch-scene-prompt-generator.md` under "Fidelity Bar for
  Chart/Analytics/Dashboard Scenes" — real drop shadows (not flat borders), icons paired with
  labels/deltas, smooth multi-point chart curves with dashed gridlines and real area fills, pill-
  shaped filter chips, and consider staging the product UI as a light window inside a full-bleed
  TEAL canvas. Applies retroactively too — the rough first-pass Figma keyframes built for script
  v12.1 (Scene 1 curve, Scene 5 harness cards, Scene 7 ROI cards) were explicitly a rough pass and
  should be revisited against this bar before being treated as final.
