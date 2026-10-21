---
name: feedback-pop-reveal-rule
description: META RULE — any grid of small repeated marks (cells, dots) reveals with the same staggered spring pop-in, and lands on the VO words it illustrates
metadata:
  type: feedback
---

**META RULE (Sejal, Aug 17 2026):** any panel that reveals a set of small
repeated marks — grid cells, dot clusters, tick marks — uses ONE shared
animation: each mark **pops in on a spring**, scaling up from 0.7 while it fades
in, staggered **left → right** across the group rather than appearing all at once.
Direction matters: the reveal must run the same way the content reads (W1 → W4 →
W8, and left → right within each cluster). Established by
the Memory "every week starts smarter" grid; now factored into
`src/components/popReveal.ts` so every panel shares it.

Two rules travel with it:
1. **The marks land on the words they illustrate**, not before. The coaching-impact
   dots ARE the picture of "week after week", so they pop exactly on that phrase.
2. **Everything else in the panel arrives EARLY.** When the illustrated line lands,
   those marks must be the only thing still moving — the viewer should already
   have had time to read every other metric on the panel.

**Why:** motion that arrives before its words reads as decoration; motion that
lands on its words reads as meaning. And if several things animate at once, the
one that matters is lost among them.

**How to apply:** put the beat at the measured word frame (whisper timestamps),
front-load every other reveal in the panel, and keep the stagger tight enough
that the last mark still lands inside the spoken line.

Related: [[feedback-panel-screen-time]], [[feedback-animation-prefs]],
[[feedback-continuation-scenes]]
