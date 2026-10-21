---
name: feedback-graph-annotations
description: In-graph text labels must never overlap the plotted curve/line and must never leave the plot area
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a193b5e4-220e-4263-a294-24e2bdb5d464
  modified: 2026-08-06T13:07:44.997Z
---

Any annotation/label placed INSIDE a chart or graph (SVG curves, etc.) must satisfy BOTH: (1) it never overlaps the plotted curve/line, and (2) it never extends outside the graph/plot area (stay within the plot's x/y bounds, not just the SVG viewBox).

**Why:** On the Why Tetriz AI-Native maturity curve, Sejal repeatedly flagged the "The trailing curve" caption — first seeping past the right plot edge, then overlapping the grey trailing line. Placing text near a curve without measuring against the curve's actual height causes overlap; the plot edge (e.g. x≤1140) is tighter than the SVG viewBox (x≤1180).

**How to apply:** after positioning any in-plot label, programmatically verify before presenting — use `getBBox()` for the text and `getPointAtLength()` to sample the curve's y across the label's x-range; require a clear gap (~20px+) between the text bbox and the curve, and confirm the bbox stays inside the plot bounds (not the viewBox). Prefer the large open region below/away from the curve. See [[feedback-no-overlap]] and [[feedback-caption-placement]].
