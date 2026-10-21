---
name: feedback-ambience-bed
description: "An ambience bed loud enough to hear MUST duck under every voice; and presence is measurable, audibility is not"
metadata:
  type: feedback
---

**Room tone that you can hear has to get out of the way of dialogue.**

**Why:** on EP003 I set a restaurant bed by measurement at -44 dBFS (22dB under
dialogue), said my instinct was "maybe 2dB quiet", and Sejal could not hear it
at all. It was 8dB. I raised it to -36 and did not duck it — and her next note
was that a line sounded muted and eaten. Restaurant babble is the WORST masker
there is for speech, because it IS speech: same band, same rhythm.

**How to apply:**
- Below about -42 dBFS a bed needs no duck and nobody can hear it. Anywhere it
  is actually audible, duck it **~7dB under every voice in the film**, including
  the background character's, and let it come back up in the gaps. That is where
  it is doing its work anyway.
- **I can verify a bed is PRESENT. I cannot verify it is AUDIBLE.** State the
  measurement, then say plainly that the level needs her ears. Do not present a
  measured number as if it settles it.
- Make a loop-length bed seamless by crossfading its own tail onto its head, so
  the video's loop point has no dip and no click.

- **Level alone doesn't predict audibility; check the SPECTRUM and the voice COVERAGE too.** On EP005
  (9 Oct) the office bed sat at -33 dB, 16 dB under the VO, and she asked "where is the office
  ambience?". 90% of its energy was under 1 kHz (rumble small speakers don't play), and the VO
  covered 79% of the day, so it was ducked almost all the time. Fix that worked: high-pass at 140 Hz,
  a +4 dB shelf at 2 kHz, a 5 dB duck. The level then needed two tries: +6 dB overall (-26 dB in gaps, -30 under voice) was "too loud", so it came down to +2 dB (-30 in gaps, -34 under voice). Start a new bed near -30 in the gaps, with the EQ.
- **Raising a bed raises its transients.** Scan for knocks before boosting (peak 15 dB over the room's
  typical 50 ms peak) and patch them, or they clip.

Related: [[project-ep003-remote-control]] [[project-system-one-model-episode]]
- **EP005 final (9 Oct): quieter still, and no brightening.** At +2 dB with the shelf it was still "too loud". She also suspected the earlier "can't hear it" came from a Studio playback bug rather than the level. The landing level is -35 dB in gaps and -39 under voice, about 19 and 23 dB below the dialogue. That's close to where it started, so don't overcorrect from one "can't hear it" note.
- **The printer hides in short bursts too.** After the long run is cut, 0.3-0.5s whirrs at +6 to +13 dB (2.5-8 kHz over the room) remain, and a treble boost exposes them. Patch at +3 dB with multiple passes, taking each patch from a window that is itself clean.

