---
name: feedback-vo-cut-tails
description: STANDING RULE — never cut a VO segment mid-word; leave a decay tail after the last word (EXCEPT an interruption, which is the opposite)
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e4ad1864-43e4-46d4-9663-c67079767e5c
  modified: 2026-08-14T06:21:14.145Z
---

When splitting the master VO into playback segments (`<Sequence>` windows over vo.mp3), NEVER let a cut clip the end of a word. Words must be completely spoken — an abrupt cut to match a scene beat is always wrong; move the scene beat instead.

**Why:** Sejal (2026-08-14) caught "Everything else, handled." with "handled" cut abruptly — the segment ended exactly on the Whisper end-timestamp, which undershoots the audible decay of the word.

**How to apply:** Whisper `end` times mark the last phoneme, not the audible tail — add ≥0.4s (12–15f) after the last word before ending a segment. Then make the NEXT segment skip past that tail: shift its `startFrom` forward by the same amount AND its `from` equally, so master-time alignment (and every VO-locked beat downstream) is unchanged. Whisper START times are late too: a window ending just before the next word's timestamp can leak its onset burst ("bec- because"). End the window mid-silence, several frames clear of the next onset, and never let two windows both contain any part of the same word. Check every split point, not just the flagged one. See [[feedback-panel-screen-time]].

**EXCEPTION — an interruption (added 2026-09-23, EP003).** This rule governs
SEGMENT SPLITS, where the speaker finishes and the edit moves on. It is the
opposite of what an interruption needs. When another character cuts a line off,
the word MUST be severed and the fade must be as short as it can be without
clicking — **4ms**, not 0.4s. A 0.4s decay tail on an interrupted line sounds
like the speaker finished and the other one waited politely. See
[[feedback-vo-interruptions]].
