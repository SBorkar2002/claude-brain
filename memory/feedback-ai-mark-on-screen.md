---
name: feedback-ai-mark-on-screen
description: "When compositing a comic video, the teal six-petal AI mark must be drawn on every AI monitor — plates ship with blank screens on purpose"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 33bb43b4-c232-415a-b741-3929b64ec3f5
  modified: 2026-09-11T08:33:58.039Z
---

The comic plates are generated with **empty monitors on purpose** — the AI's
six-petal teal mark (eye offset to the RIGHT of centre) is composited **live on
top** of the blank screen during the Remotion build, on every scene where the AI
"speaks" through a screen. Sejal flagged a graph cut for shipping blank monitors
with no AI logo.

**Why:** the AI is never a face/body — the mark on the screen IS its on-screen
identity (`cast.md`, and `comic-panel-generator.md`: "generate every monitor
EMPTY … the AI mark is drawn live on top"). A blank monitor reads as a bug.

**How to apply:** overlay the mark centred on the monitor screen for monitor
scenes; a small mark for full-screen AI text cards. Asset: `ai-mark.svg` in the
Drive "AI mark" folder (six teal ellipses + white/teal eye at cx=59). The rule
is in the skill; the miss was execution. See [[feedback-object-identity]].
