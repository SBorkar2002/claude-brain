---
name: feedback-motion-quality-bar
description: "STANDING 7 Oct 2026: web/UI motion must be After Effects motion-graphics quality, and visuals must come from the page's own system; generic fade-up/bounce/pop and dropped-in clip-art read as AI"
metadata:
  type: feedback
---

Sejal on the Instahyre landing page: the fade + bouncy pop-in animation "looks like what GPT or DeepSeek does"; she wants "after effects kind of quality". She also rejected a glossy vector gift illustration as "forced on the screen": it didn't match the page's flat, typographic system.

**Why:** generic entrance animations and stock-style illustrations are the tell of AI-made design; she's being judged as a designer.

**How to apply:** build motion from motion-design techniques: type rising from behind clip masks, line/strike draw-ons, mask wipes with inner parallax, cover wipes, playhead scrubs, choreographed staggers. Use custom expo-out / quart in-out curves; no bounce, no scale pops, no fade on its own. For any new graphic, derive it from motifs already on the page (tickets, tiles, rules, mono labels) instead of adding an illustration. In Figma there's no on-scroll trigger: use interactive component variants (Static → Idle → phases) with MOUSE_ENTER + ON_CLICK. Related: [[feedback-motion-easing]], [[feedback-pop-reveal-rule]], [[project-instahyre-assessment]].
