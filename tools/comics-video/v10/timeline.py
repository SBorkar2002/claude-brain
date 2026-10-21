#!/usr/bin/env python3
"""
E001 loop -- 9:16 cut, v10. Frame + audio timeline.

Frame starts are set from MEASURED speech onsets (RMS envelope), not whisper's
word times -- whisper's absolute times drift by up to 0.4s in this material and
its segment ends undershoot, which is what clipped "means" down to "mean" and
leaked the "m" of "my" into "Hey".

Every slice below was checked against the measured runs: in-point sits just
before the first onset, out-point at least ~0.1s past the last decay, and no
slice reaches into the next utterance.

Captions are drawn per word by captions.py -- see spec.py.
"""
from spec import DEV1, AI, AITECH, AIPLAIN, DEV2, DEV2L, DEV3, SURE, CRED, NIGHT, COFF, KEYS, SIGH, SCREAM, EXH, INTRO, AICAP

# (frame, start, [(file, src_in, src_out, offset_from_frame_start)])
T = [
 # Opens on the TAIL of Dev 2's line -- the half that says "long night". The
 # first half sits at the far end of the loop, so the sentence completes when
 # the Short repeats. Offset 0.12 lands the voice at 0.20 exactly where the old
 # take did, so the slurp at 1.00 and everything after are untouched.
 ( 1,  0.00, [(INTRO, 0.00, 1.33, 0.0)]),
 ( 2,  1.45, [(COFF, 3.50, 6.10, 0.0)]),      # one long slurp spans frames 2-4
 ( 3,  2.50, []),
 ( 4,  3.50, []),
 ( 5,  4.05, [(DEV2, 4.10, 5.85, 0.0)]),
 ( 6,  5.95, []),
 ( 7,  6.45, [(DEV1, 0.00, 2.15, 0.0)]),
 ( 8,  8.60, []),
 ( 9,  9.10, [(DEV1, 2.42, 3.80, 0.0)]),      # was 2.50 -- clipped the "A" onset
 (10, 10.40, []),
 (11, 10.85, [(DEV1, 3.80, 6.18, 0.0)]),      # was 5.90 -- cut "means" to "mean"
 (12, 13.37, [(DEV1, 6.90, 7.43, 0.0)]),      # was 7.50 -- leaked the "m" of "my"
 (13, 13.95, []),                             # +0.13: "Hey.." was only up 0.27s
 (14, 14.57, [(DEV1, 7.42, 11.62, 0.0)]),     # was 7.46/11.45 -- clipped both ends
 # The definition screen now carries the WHOLE explanation in one slice, so the
 # monitor holds ~10s for the animation to live in, and the blank face lands
 # after it instead of covering it.
 ( 15, 18.90, [(AITECH, 0.00, 13.55, 0.0)]),
 ( 16, 34.45, []),                             # 1.50s of blank face. It is the joke; do not trim it again.
 (17, 35.95, [(DEV1, 12.75, 14.60, 0.0)]),    # was 14.85 -- touched "Say"
 (18, 38.05, [(DEV1, 14.78, 17.95, 0.0)]),
 (19, 41.25, [(SIGH, 0.00, 0.56, 0.0)]),      # its own file: no seek, no drift
 # Whisper marked "You" at 11.58, but that is the AI's second BREATH -- the word
 # itself starts at 12.08. Slicing from 11.50 played that breath as a second
 # sigh, and anchored every caption in this panel ~0.5s ahead of the voice.
 ( 20, 42.45, [(AIPLAIN, 0.00, 10.62, 0.0), (SCREAM, 0.00, 1.70, 10.28)]),
 (21, 54.45, [(DEV1, 17.70, 18.85, 0.0)]),
 # The "...Oh" panel holds after its caption clears, and the cut to this one
 # lands ON "wait" rather than 0.6s ahead of it.
 (22, 56.22, [(DEV1, 19.42, 21.30, 0.0)]),
 (23, 58.22, []),                             # +0.27: gives "YOU CAN DO THAT??" room
 (24, 58.95, [(AI, 20.00, 21.45, 0.0)]),
 (25, 60.72, [(DEV1, 21.70, 27.35, 0.0), (KEYS, 0.40, 5.60, 0.9)]),
 (26, 66.22, [(DEV1, 28.10, 30.20, 0.0)]),    # was 29.90 -- clipped "watching"
 (27, 68.43, [(AI, 22.30, 23.15, 0.0)]),      # "No."
 (28, 69.33, [(SURE, 0.00, 2.43, 0.0)]),      # was 1.45 -- chopped "Sureeeee" in half
 (29, 71.98, [(AICAP, 0.00, 4.77, 0.0)]),   # re-voiced+severed mid-"step"; dev crashes in on the cut
 (30, 76.50, [(DEV1, 31.05, 32.55, 0.0)]),
 (31, 78.83, [(AI, 27.70, 29.16, 0.0)]),      # severed mid-"get"
 (32, 80.20, [(DEV1, 33.00, 34.19, 0.0)]),    # "Great. Night!" crashes in
 (33, 81.81, [(AI, 29.34, 31.45, 0.85)]),     # 1.0s of silence, then he's gone
 # Dark room: 2.5s of nothing, then "Peter?" -- and the caption is drawn on the
 # word, so nothing is on screen before it.
 (34, 84.92, [(AI, 31.90, 32.85, 1.60)]),
 # The stamp holds 2.40s: the counter needs to reach 0 AND be seen sitting at 0.
 # Hitting zero is the point; watching it sit there is what lands it.
 (44, 88.19, []),
 # The ending is a real exchange now, on its own frames: Dev 1 asks, Dev 2
 # answers, and his answer runs out of the video into the top of it. "Exhausted"
 # is doing double duty -- the credits and the man.
 (45, 93.89, [(CRED, 0.00, 2.90, 0.30)]),
 (46, 97.60, [(EXH, 0.00, 2.68, 0.35)]),
]
END = 100.63

# ambience_clean.mp3 already has the printer cluster (38-46s) ducked 12dB.
# out_at lands in the gap after "Night!" so the room empties into real silence.
AMB = dict(gain=1.4, lead=0.15, out_at=85.04, out_dur=0.5, in_at=92.90, in_dur=1.2, tail=0.15)
