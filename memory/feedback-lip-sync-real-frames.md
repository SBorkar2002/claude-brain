---
name: feedback-lip-sync-real-frames
description: Lip sync = swap between REAL storyboard frames only; never paint/patch mouths onto art; check for identical-framing frame pairs first (diff the images)
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 33bb43b4-c232-415a-b741-3929b64ec3f5
  modified: 2026-09-11T09:40:13.651Z
---

For comic lip sync, Sejal draws the mouth states as separate storyboard frames
with identical framing (e.g. graph's typing shots: s8 == s10 exactly, s9 = same
drawing with mouth closed). **The flap is a swap between those real frames on
the VO envelope — nothing is ever painted, patched, or composited onto a
frame.** Synthesized mouths (dark ovals) read as "ink blots"; skin-patches leave
visible dashes (one landed on the character's neck). Both were rejected hard
(v4/v5 of graph, 11 Sep 2026).

**Why:** the artist already encodes who speaks and mouth state per frame; the
board is authoritative. Frames that look like duplicates are usually a
deliberate open/closed pair.

**How to apply:** before building lip sync, mean-abs-diff the same-pose frames
to find pairs (0.0 = identical plate, tiny diff = the mouth pair). Flap only the
scenes the script calls for (character dictating to their AI); thoughts,
listening, and off-screen VO keep the drawn mouth. Same principle as
[[feedback-comic-hard-cuts]]: use what's drawn, don't invent. Also in the
assembly contract in comic-animation.md.
