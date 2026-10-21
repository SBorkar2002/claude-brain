---
name: project-aidlc-maturity-curve
description: AIDLC maturity curve slide graphic built in Figma for the Tetriz_EY deck
metadata: 
  node_type: memory
  type: project
  originSessionId: eab58231-862f-4a95-ad20-997d3fb4a971
  modified: 2026-08-06T07:23:02.928Z
---

Slide graphic **"AIDLC maturity curve"** — converts Sumit Gwalani's LinkedIn "Cherny adoption" curve into a Tetriz-brand slide visual, for the **Tetriz_EY [WIP]** Google Slides deck (id 1Fd06MF-tFh7sD3SHydlGBrCGZA7oVSkmiD-tUQr7460, slide 9 placeholder "to add: AIDLC maturity curve"; slide 8 frames it).

- **Figma:** file `xBuBbSkPmGaBZv0oJnYuTH`, frame node **4:2**, named `AIDLC maturity curve`, **1920×1080** (16:9 deck res). https://www.figma.com/design/xBuBbSkPmGaBZv0oJnYuTH/Untitled?node-id=4-2
- **Brand tokens (from core repo `packages/site-ui/src/tokens.css`):** teal `#0096BB`, bg white/`#F9F9F9`, fg `#262626` (+alpha ramp 88/56/40), borders `#EDEDED`/`#E8E8E8`; fonts **Mona Sans** (display) + **Geist Mono** (axis/kicker). No rainbow — value shown via teal→neutral opacity ramp.
- **Structure:** Y = AI-Native Value Index as 5 stacked *bands* with labels centered *between* gridlines (bottom→top: Piloting, Deploying, Integrating, Reinventing, Compounding); X = Cherny adoption 0·Gated→4·AI-native. Two curves from **same start at Deploying** (Piloting stays empty below): teal **ideal** curve with data-dots + sparkle endpoint at 2·Parallel (½ time), gray **trailing** curve to 4·AI-native (2× time). Shaded gap between = "the gap is the AI Tax".
- **Decisions:** title/heading intentionally OMITTED (added from Slides). Endpoint marker = layered 4-point **sparkle** with teal outer border + white inner border + teal center (3 concentric stars, nodes ~23:2-4). Iterated: flat sparkle → glow (rejected as white-border artifact) → ringed dot → this bordered star. NO drop-shadow glow anywhere. OPEN: whether to switch trailing curve to orange + colored level labels to match her top reference, vs keep brand-neutral (current). She edits labels directly in the file — don't revert her tweaks.
- Feedback rules that bit here: [[feedback-no-overlap]], [[feedback-caption-placement]]. Related: [[project-video-pipeline]], [[reference-product-brain-repo]].
