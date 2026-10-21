---
name: feedback-object-identity
description: "Object-identity visual system for Tetriz videos — icon carries identity, color carries state; reusable across scripts"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5149539b-f928-45b2-bda9-ef87f6710745
---

Anandhi + Sumit (Jul 2026): "everything looks like a box" — viewer can't tell a
skill from a dashboard from a screenshot. Sejal wants a reusable system so any
future script gets instant object recognition (reduced cognitive load).

**META RULE: icons carry object IDENTITY; color carries STATE. Never repurpose a
state color decoratively.**

Object types → marker:
- Skill = ⚡ + a `skill.md` file chip (Sejal's own example)
- Plugin = 🧩 jigsaw
- Harness rule/config = `.md` doc / ⚙
- Dashboard (live) = browser chrome (traffic lights + URL + filters), interactive
- Screenshot (static) = image frame + shadow, NO chrome (reads as picture)
- Terminal = mac traffic lights, ink #0d1117 mono

State colors (reserved): teal #03A6CF good/resolved/Tetriz · amber #F5A623 AI Tax/
leaking/cost/before · red #FF6B6B problem/risky/denied · green #22c55e confirmed.

Three levers = icon-led with per-lever identity colors (Sejal, Jul 2026 —
supersedes the earlier all-teal note): Coach = ORANGE #F4652F (hotter/red-leaning,
distinct from AI-Tax amber #E58A0F), Playbook = PURPLE #7C6BF5, Memory = TEAL
#03A6CF. GREEN #22B268 is reserved exclusively for success/"it worked"/the
Results label — never a lever identity. Pillar chips persist top-center from the
Offer scene on; active pillar glows in its color + ~10% larger, others grey.

Theme: dark bookends (hook/result/close #08090d), light middle. Also saved to the
launch skill md. Related: [[feedback-typography-system]] [[feedback-anandhi-storyboard-review]] [[feedback-continuation-scenes]]


**META RULE — brand/tool icons (2026-07-21, Sejal after jagged-outline bug):** third-party tool icons (Claude, Slack, GitHub, Copilot, etc.) must be OFFICIAL vector assets (SVG — simpleicons CDN `cdn.simpleicons.org/<slug>`, Wikimedia, or Sejal-provided). NEVER pixel-process PNGs to strip backgrounds — the anti-aliased tile edges survive as jagged dark outlines on light canvases. If no clean vector exists, ask Sejal for the SVG before shipping. Current SVG set lives in `tetriz-launch-video-v4.2/public/assets/*.svg`.
