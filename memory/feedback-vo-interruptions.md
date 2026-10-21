---
name: feedback-vo-interruptions
description: "An interruption is a CUT, not a duck — and the cut point is found by transcribing candidates, not by reading the envelope"
metadata:
  type: feedback
---

When one character talks over another, the interrupted line is **cut**, at full
volume, mid-word.

**Why:** on EP003 Sejal told me three times that her line still faded out. It
was not the cut — it was the DUCK. The build ducked her under every one of
Peter's cues including the one interrupting her, so her gain ramped 1.00 -> 0.20
over 0.18s while she was still mid-word. I kept shortening the fade on the cut,
which was never the thing making the sound.

**How to apply:**
- **Exclude the interrupting cue from the ducking system entirely.** The
  interrupted speaker plays at FULL level and stops dead.
- Fade the cut at **4ms** — enough to stop a click, nothing more. See the
  exception now recorded in [[feedback-vo-cut-tails]].
- **Find the cut point by TRANSCRIBING candidate cuts, not by reading the
  envelope.** I read the envelope, decided "every" ended at 1.78 and the /s/ of
  "step" started, and cut at 1.82 — which severed the "-y". Cutting the file at
  1.82 / 1.88 / 1.92 and transcribing each settled it in one pass. For a word
  that is meant to survive intact, the envelope is not enough; for a word that
  is meant to be severed, neither is whisper.
- Decide whether the line should COMPLETE or be severed by what the line does.
  If it is the line that resolves the film's open question, let it complete and
  have the other voice land 0.1s later — burying it wastes it.

Related: [[project-ep003-remote-control]], [[feedback-vo-cut-tails]]
