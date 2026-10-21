---
name: feedback-tempo-vs-pace
description: "The same atempo multiplier does NOT equalise delivery — measure syllables/sec across the track, not the setting"
metadata:
  type: feedback
---

Two takes at the same tempo setting can still sound like different people.
ElevenLabs picks its own delivery rate per generation; `atempo` scales whatever
it gave you and preserves the difference.

**Why:** Sejal asked whether one line was at the wrong speed because "the voice
suddenly changes". It was at 1.15x, exactly like its neighbours. Measured in
syllables per second it ran **4.15** against **5.42** and **5.62** either side —
30% slower, same multiplier.

**How to apply:**
- Audit her whole track in **syllables/sec of voiced time**, per segment. The
  multiplier tells you nothing.
- Correct the outlier with a PER-TAKE tempo override, not a global change.
- Do not fully match the neighbours — closing most of the gap is right, closing
  all of it sounds rushed. 4.15 -> ~4.6 against neighbours at 5.5.
- Some of it cannot be fixed by tempo: takes generated in separate sessions
  drift in timbre. If it still sounds like a different person after the pace is
  matched, it needs re-generating in one batch.

Related: [[project-ep003-remote-control]]
