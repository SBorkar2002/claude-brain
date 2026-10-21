---
name: feedback-layout-meta-rules
description: "Meta rules for visual layout decisions — comparisons side-by-side, stat card orientation, TEAL emphasis on important words"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d34891d5-bf3d-45da-a44f-bd55ac4ba270
---

## Rule 1 — Comparisons must be side-by-side on the same screen

Whenever the VO or script compares two things (teams, states, before/after, good/bad, average/elite), show them simultaneously side-by-side on a single screen. Do not show them one after the other — that is repetitive and loses the contrast.

This applies to any visual form: bar graphs, tables, pie charts, stat cards, timelines, or any other comparison format.

**Why:** Sequential presentation of comparisons feels repetitive and buries the contrast. Side-by-side makes the difference immediately obvious.

**How to apply:** When building a scene that involves a comparison:
- Split the canvas into two panels (left = one state, right = the other)
- Animate left first, then right, so the contrast builds in frame
- Use consistent sizing and alignment between panels so the comparison reads cleanly
- Label each side clearly (e.g. "AVERAGE TEAM" / "ELITE TEAM")

---

## Rule 2 — Stat card orientation follows its position on screen

Stat card layout must adapt to where it sits:
- **Left or right side of screen** → use a **vertical card** (value stacked above label, centered)
- **Top or bottom of screen** → use a **horizontal card** (icon left, value + status right)

**Why:** A vertical card in a side column reads naturally top-to-bottom. A horizontal card at the bottom or top reads left-to-right, matching natural reading flow for that position.

**How to apply:** Before placing a stat card, determine its screen region:
- Side column (x < 200 or x > 1080) → vertical layout
- Top strip (y < 200) or bottom strip (y > 500) → horizontal layout
- Centered mid-screen → default to vertical unless content is long, then horizontal

---

## Rule 3 — Key words get TEAL (#03A6CF) emphasis

Any word or phrase that carries significant weight — a stat, a threshold, a key outcome, a contrast word — should render in TEAL (`#03A6CF`) to signal importance.

This applies in captions, subtitles, metric descriptions, and titles.

**Why:** TEAL is the brand/signal color. Emphasis words in TEAL guide the viewer's eye to what matters most and reinforce the Tetriz brand color in every scene.

**How to apply:** Use `RichWordReveal` (segments array) or split the text at the emphasis boundary:
- Identify the weight-carrying phrase: numbers, thresholds, outcome words ("under an hour", "5x faster", "under 5%", "multiple times a day")
- Render the lead-in in `#0d0d0d`, the emphasis phrase in `#03A6CF`
- Never color entire sentences — only the specific word(s) that carry the point

[[feedback-caption-meta-rules]]
[[feedback-typography-system]]
