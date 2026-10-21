#!/usr/bin/env python3
"""
E001 loop -- 9:16 cut, v10. Single source of truth.

Captions are NOT baked into the plates any more. `plates/pNN.png` are the
Figma frames with every dialogue text layer hidden; the caption is drawn back
on here, one word at a time, on the word's own VO timing. Geometry, font size
and colour below are read straight off the Figma text nodes so the words land
exactly where they sat when the caption was baked.

Non-dialogue text (*slurps*, *sigh*, the "click" labels, the LOOP -cleared-
stamp) is still baked into the plate -- it isn't spoken, so it has nothing to
sync to.
"""
import os

# ---- where the assets live ----------------------------------------------
# `public/v10` is the ONE copy of every plate and every audio file, because
# that is the directory Remotion serves from. There used to be a second copy
# under v10/ for the Python scripts to read; two copies of the same asset is a
# drift waiting to happen, so everything here reads out of public/ instead.
_PUB   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public", "v10")
PLATES = os.path.join(_PUB, "plates")
AUDIO  = os.path.join(_PUB, "audio")

# ---- audio sources -------------------------------------------------------
DEV1  = "dev1_peter.mp3"
AI    = "AI.mp3"
AICAP = "ai_cap.mp3"       # panel 16 re-voiced 9 Sep: "...that's the only
                           # thing stopping it, unless you give it a step-" --
                           # cut off by the dev. Its own take, so the AI.mp3
                           # slices after it (31/33/34) are untouched.
DEV2  = "dev2.mp3"
DEV2L = "dev2 last line.mp3"   # the loop line: ends on "long night"
DEV3  = "dev3_fast.mp3"        # 1.3x, pitch preserved
SURE  = "dev1 you sure.mp3"
CRED  = "dev1_ai creds.mp3"
NIGHT = "dev1_longnight.mp3"
COFF  = "coffee sound.mp3"
KEYS  = "keyboard.mp3"
SCREAM = "scream.mp3"        # the meme sting; 0.30s of lead-in before the yell
EXH   = "dev2_exhausted.mp3"   # the new ending, split across the loop point
AIPLAIN = "ai_plain.mp3"    # the plain answer, cut out of the 11:31 generation
AITECH = "ai_tech2.mp3"     # the technical block of the 7 Sep take, 0.00-13.55.
                            # Was ai_tech.mp3 (an older take with two silences
                            # spliced in by hand). Sejal recorded both answers in
                            # ONE generation, so both panels now come off the same
                            # take -- same voice settings, same room, no splices.
                            # The new delivery breaks the opening line into three
                            # measured chunks (0.09-0.68 / 0.97-1.64 / 1.92-2.75)
                            # where the old one ran it as a single 2.33s phrase,
                            # so every ring timing below was re-solved against it.
INTRO = "intro_long.mp3"       # EXH 2.85-4.18 as its own file: no mp3 seek, no drift
SIGH  = "sigh_vo.mp3"      # THE SIGH IN THE TAKE -- 14.94-15.50 of the 7 Sep
                           # generation, the breath the voice actually takes
                           # between the two answers.
                           # Was sigh.mp3: AI 10.62-11.34 pulled out of a
                           # DIFFERENT generation and lifted +18dB. Level was
                           # never the problem (rms -36.8 vs -39.0 here) -- an
                           # artificially boosted breath from another take is
                           # why Sejal heard it as pasted in. Same room, same
                           # breath, and it now belongs to the line it precedes.

# Dev 2's loop line is split across the loop point: the tail ("long night")
# opens the episode, so when the Short repeats, the sentence completes. Measured
# by envelope -- the gap at 2.74-2.86 is the natural break.
DEV2L_SPLIT = 2.80
# One take holds the outro answer AND the line that opens the episode. Onsets
# measured off the envelope -- there is no whisper json for it. Slice 0:5 is the
# answer, 5:7 is the intro, and the 0.38s pause between them is reconstructed
# across the loop point.
MANUAL_WORDS = {
  DEV2L: [("Long", 2.88, 3.20), ("night.", 3.20, 3.59)],
  EXH: [("Exhausted", 0.16, 0.75), ("because", 0.78, 1.46), ("it", 1.54, 1.62),
        ("was", 1.66, 1.78), ("a..", 1.80, 2.46)],
  # Aligned to the PERCEPTUAL onset, not the signal onset. "Long" is measurable
  # from 0.18 but only -26dB there; it isn't clearly audible until 0.26, and at
  # the very top of the video that 0.08s reads as the caption arriving first.
  INTRO: [("Long", 0.26, 0.72), ("night.", 0.98, 1.20)],
}
EXH_SPLIT = 2.85

VO_JSON = {                    # whisper word lists live here
    DEV1: "dev1_peter.mp3", AI: "AI.mp3", DEV2: "dev2.mp3",
    DEV3: "dev3.mp3", SURE: "dev1 you sure.mp3",
    CRED: "dev1_ai creds.mp3", NIGHT: "dev1_longnight.mp3",
    AICAP: "ai_cap.mp3",
}
TEMPO = {DEV3: 14.602/11.242}   # divide whisper times by this for sped-up files

# ---- captions ------------------------------------------------------------
# frame: (text, x, y, box_w, align, hex, italic, vo_file, word_slice, shift)
#   x,y,box_w  : frame-relative, from the Figma text node's absoluteBoundingBox
#   word_slice : (first, last+1) into the flat whisper word list for vo_file
#   shift      : seconds added to every word time, to correct whisper drift
C = {
 1:  ("Long night.",                         38, 351, 155, "L", "000000", 0, INTRO,(0,2),   0.0),
 5:  ("left a loop\nrunning",                36, 316, 141, "C", "000000", 0, DEV2, (2,6),   0.0),
 7:  ("Riiiiight",                           54, 316, 104, "C", "000000", 0, DEV1, (0,1),   0.0),
 9:  ("A loop.",                             70, 320,  99, "C", "000000", 0, DEV1, (1,3),   0.42),
 11: ("I have no idea what that means",      42, 483, 178, "C", "848484", 1, DEV1, (3,10),  0.0),
 12: ("Hey..",                              314, 222, 370, "C", "000000", 0, DEV1, (10,11), 0.0),
 14: ("my colleague said he left a loop running last night.\n"
      "What does that mean?..",             403, 145, 276, "C", "000000", 0, DEV1, (11,25), 0.0),
 # 15 has NO caption. The explanation panel carries its own words -- DECOMPOSE,
 # RUN A STEP, EVALUATE, STEPS DONE n/3, CONDITION MET -- so the caption was
 # competing with labels that say the same thing, on a panel where the VO is
 # already naming them. It also freed the top third for the counter.
 # (Anandhi, 4 Sep: "maybe the captions can just be a part of the screen
 # itself?" -- in a flowchart they already are.)
 17: ("Right. Yes.",                        482, 218, 159, "C", "000000", 0, DEV1, (25,27), 0.0),
 # Same shot as 17, so the caption must not move between them -- see
 # CAPTION CONTINUITY below. Geometry copied from 17, not from Figma.
 18: ("…Say that again like I'm not an engineer.",
                                            482, 218, 159, "C", "000000", 0, DEV1, (27,35), 0.0),
 # 20 has NO caption, same reason as 15: the panel carries its own words --
 # numbered gates and FINISH -- and the VO names every beat. "Nobody in the
 # middle" is retired with it; the line ends "so you don't have to" now.
 21: ("...Oh",                              340, 341, 276, "C", "000000", 0, DEV1, (35,36), 0.0),
 22: ("WAIT.\nYOU CAN DO THAT??",           200, 212, 320, "C", "000000", 0, DEV1, (36,41), 0.0),
 24: ("You've had this the whole time.",    111, 299, 498, "C", "000000", 0, AI,   (46,52), 0.0),
 25: ("Okay. Fix every failing test in this file, stop when they pass.",
                                            370, 204, 243, "C", "000000", 0, DEV1, (41,53), 0.0),
 26: ("…You don't need me watching?",  222, 237, 276, "C", "000000", 0, DEV1, (53,58), 0.0),
 27: ("No.",                                111, 299, 498, "C", "000000", 0, AI,   (52,53), 0.0),
 28: ("You\nSureeeee?????",                 302, 259, 335, "C", "000000", 0, SURE, (0,2),   0.0),
 29: ("You gave it a finish line\nThat's the only thing stopping it\nunless you give it a ste—",
                                            111, 299, 498, "C", "000000", 0, AICAP, (0,18), 0.0),
 30: ("So I can go home?",                   77, 306, 335, "C", "000000", 0, DEV1, (58,63), 0.0),
 31: ("Yes. But before you g—",        360, 364, 335, "C", "000000", 0, AI,   (65,70), 0.0),
 32: ("Great. Night!",                      319, 251, 335, "C", "000000", 0, DEV1, (63,65), 0.0),
 # Figma reads "...the step and the budget cap...." but the VO has no second
 # "the" -- dropped so the reveal stays one word per spoken word.
 33: ("…the step and budget cap....",  198, 209, 276, "C", "000000", 0, AI,   (70,75), 0.0),
 34: ("..Peter?",                           222, 389, 276, "C", "ffffff", 0, AI,   (75,76), 0.0),
 45: ("…hey. What happened to my AI credits?",
                                             54,  79, 447, "C", "000000", 0, CRED, (0,7),   0.0),
 # LOOP CAPTION POSITION (meta): the last caption of a looping episode takes the
 # FIRST caption's geometry, not its own from Figma. The sentence completes
 # across the loop point, so the words must not jump position as it repeats --
 # geometry copied from frame 1 verbatim.
 46: ("Exhausted because it was a..",         38, 351, 155, "C", "000000", 0, EXH,  (0,5),   0.0),
}

# whisper heard "against determination condition" where the VO (and the
# caption) actually say "against a termination condition" -- split word 3.
WORD_SPLITS = {(AI, 3): [("a", 1.74, 1.84), ("termination", 1.84, 2.26)]}

FONT_R = "fonts/Lato-Regular.ttf"
LINE_H = 38          # Figma AUTO line height for Lato 32
SIZE   = 32

# Figma box heights (38px per line). With one-word-at-a-time captions the box
# is no longer laid out -- only its CENTRE matters, and that's (x+w/2, y+h/2).
H = {1:38, 5:76, 7:38, 9:38, 11:114, 12:38, 14:190, 15:190, 17:38, 18:38,
     20:190, 21:38, 22:76, 24:38, 25:152, 26:76, 27:38, 28:76, 29:76, 30:38,
     31:38, 32:38, 33:76, 34:38, 35:114, 37:38, 39:38, 40:114, 41:152,
     43:38, 45:76, 46:38}

# Captions that clear while their panel keeps holding. Frame 21 is the "...Oh"
# beat: the word goes, the face stays, and the cut lands on the next line.
# Value is seconds after the last word appears.
CLEAR_AFTER = {
  21: 0.55,   # the "...Oh" beat: word goes, face stays
}

# How a caption reveals. "flash" is what shipped: one word at a time, alone, at
# the centre of its Figma box -- see captions.render(). "build" reveals the same
# words on the same voice onsets but leaves them up, each in the laid-out
# position Figma gave it, so the sentence accumulates and stays.
#
# The reason to reconsider: the Figma boxes are sized for the WHOLE caption --
# f41's box is 4 lines tall, f14's is 5 -- and storyboard.py asserts the wrap
# matches that height. So the layout already assumes a full caption on screen,
# and "flash" shows one word in the middle of a box built for twelve. Rohan and
# Anandhi both read the result as hard to follow.
# How a caption reveals.
#   "flash" -- what shipped: one word at a time, alone, at the centre of its
#             Figma box. Two viewers found the longer lines hard to follow.
#   "build" -- same onsets, but each word stays in its Figma position so the
#             sentence accumulates.
#   "lines" -- Natural Habitat Shorts style: white fill with a heavy black
#             outline, a whole LINE at a time, in one fixed place. The outline
#             is what makes the fixed position possible -- the per-frame Figma
#             boxes existed to keep black text on clean paper, and an outlined
#             caption is legible over anything, so the whole placement system
#             stops being necessary.
CAPTION_MODE = "lines"

# The subtitle band. Wrapped at 48/560 because that is the measure that splits
# "Iterative execution against a termination condition." exactly where Sejal
# split it: "Iterative execution against" / "a termination condition."
#
# cx is 325, not 360: Shorts eats 110px off the right for its own buttons, so
# the usable width is 40..610 and its centre is 325. Centred on the frame
# instead, the widest line ("Okay. Fix every failing test", 558px) would run to
# 639 and sit under the rail.
SUB = dict(
  # Back to 32, the size these captions were always set at, and back to the
  # positions Figma placed them in -- those were chosen well and the outline
  # does not require the caption to sit on clean paper, it only makes that
  # optional. What the outline buys is the freedom to run WIDER than the box it
  # was placed in, which is what stops short sentences being split: at 32px
  # only two captions in the film are genuinely too long for one line.
  size=32, line=42,
  # A line may be up to the full safe width regardless of how narrow its box
  # was. 570 = the safe area 40..610, so any line this wide or less can be
  # placed somewhere inside it.
  maxw=570, safe_l=40, safe_r=610,
  # Shorts chrome, in 720x1280 terms: the back-arrow / search / kebab overlay
  # eats the top ~150-170px and the caption + CTA + progress bar the bottom
  # ~220. A guard of 90 was too shallow -- "…hey. What happened to my AI
  # credits?" was landing at y=96, directly under the top overlay.
  safe_t=170, safe_b=1060,
  fill="#FFFFFF", stroke="#000000", stroke_w=5, weight=800,
  stack=1,                       # one line at a time, each replacing the last
)

MIN_DWELL = 0.18   # a word under ~5 video frames reads as a flicker, not a word
LAST_HOLD = 0.30   # the final word has to survive long enough to be read


# ---------- LOOP CAPTION POSITION (meta rule) ----------
# When an episode ends by looping back to its opening, the LAST caption takes
# the FIRST caption's position. The closing line runs into the opening line, so
# if the two sit in different places the text jumps at the exact moment the
# viewer is meant to hear one continuous sentence. Copy frame 1's geometry to
# the final frame, whatever Figma says for that frame on its own.
# Applies to every script that loops, not just this one.


# ---------- CAPTION CONTINUITY ----------
# Consecutive panels on the SAME shot keep their caption in the SAME position.
# Figma lays each caption out for its own frame, so the boxes drift; on a cut
# that reads as the caption jumping. Copy the geometry from the first panel of
# the run rather than taking each one from Figma, unless a panel is deliberately
# reframed.


# ---------- SFX lettering, no longer baked into the plate ----------
# The two "click"s over the keyboard. Each one spikes on a REAL keystroke --
# onsets detected in keyboard.mp3 -- taking every 4th and alternating sides, so
# the lettering is in time with what you hear instead of on its own rhythm.
# The two "click"s over the keyboard. Figma gives the rotated node's AABB, so
# the centre is (x + aabb_w/2, y + aabb_h/2) and the node itself is 63x37.
# Figma rotation is counter-clockwise; CSS is clockwise, hence the negation.
# Offsets from frame 25's start, for the same reason as PLAIN above. A negative
# value is lead-in before the cut. emit.py resolves them against the frame.
SFX_FRAME = 25
SFX = [
  dict(text="click", cx=342.5, cy=1172.5, rot=-31.86, size=32, color="#ffffff",
       hits=[-0.3, 0.75, 1.6, 2.68, 3.72, 4.6]),
  dict(text="click", cx=669.5, cy=1053.0, rot=25.34,  size=32, color="#ffffff",
       hits=[0.17, 1.1, 2.06, 3.38, 4.14]),
]

# ---------- captions that don't belong to their panel's own speaker ----------
# Frame 45 carries two lines: Dev 1's credits question, then Dev 2 answering.
# spec.C holds one caption per frame, so the second lives here. It sits at the
# SAME centre as Dev 1's -- they're sequential, not simultaneous, and moving it
# would break CAPTION CONTINUITY (and push it into the Shorts UI band).
#
# Word onsets measured off the envelope; there is no whisper json for this file.
# "a" is drawn out before the pause, which is what runs it into "long night".
EXTRA_CAPTIONS = [
  # The sigh was baked into p19, so it sat on screen for the whole panel while
  # the breath itself is much shorter. Two things were wrong: the clip started
  # 0.24s before anything was audible, and the sigh PEAKS at -51dB against a
  # room tone of -47 -- it was buried, so it read as "caption first, sound
  # later". Cropped to the audible swell and lifted above the room (CLIP_GAIN).
  dict(frame=19, src=SIGH, text="*sigh*",
       cx=360.0, cy=338.0, color="#000000", italic=True,
       onsets=[0.04], clear=0.72),   # its own file, so 0.04 IS the audible start
]


# ---------- the technical explanation (frame 15) ----------
# Four versions in. What finally worked was drawing the loop as a loop.
#
# A flowchart with a return edge, and then three lanes running left to right,
# both asked the viewer to INFER the repetition -- and both needed several
# elements changing at once to say it, which is what read as "too fast" and
# "abrupt". A dot going round a circle needs no inferring and only ever has one
# moving part.
#
# The panel runs in two stages with a motivated cut. Stage one is an ordinary
# AI-speaking shot -- the monitor, the mark centred on it, and the first line of
# the explanation held above it as a WHOLE SENTENCE -- through the jargon,
# "iterative execution against a termination condition", which nobody is meant
# to follow. Then on "It decomposes the task" the monitor is gone and the ring
# has the frame.
#
# What the viewer sees: RUN A STEP is a gate at the top, CHECK is a gate at the
# right, the count lives INSIDE the loop because it is the loop's state, and the
# way out hangs off the bottom SHUT until the count fills. One dot goes round.
# Three checks: pass, fail, pass. On the failure the gate goes red and the count
# does not move -- you watch a whole lap get spent, which is what "evaluates the
# result" means.
#
# No caption on this panel: the ring is made of words, so it survives muted. No
# mark either, once the monitor is gone -- which also keeps the panel out of the
# open question about whether the mark reads as a generic AI logo. If the dot
# should ever BE the mark it drops straight in and nothing else moves.

RING = dict(
  # Geometry lifted from the Figma frame TECHNICAL EXPLAINER (429:1420) --
  # Sejal's design, replacing the hand-built version. Exact values, not eyeballed.
  #
  # What changed and why it is better: the old version said one thing with four
  # elements -- a dot, a separate 0/2, a pip row and a STEPS DONE label -- which
  # is very likely why Anandhi read the counter as a number of weeks. Here the
  # count sits INSIDE the ring and the ring is its gauge, so the fraction and the
  # arc are the same fact stated twice.
  #
  # The two gates also collapse into one place. RUN A STEP is the heading and
  # CHECK is a status chip at the top, so a lap IS a step and the chip reports
  # what the check found. They stay conceptually distinct -- which they must,
  # because the check is the termination condition and that is the term being
  # defined -- without needing two labelled positions on the ring.
  bg="#f5f5f2",
  cx=360, cy=605.5, r=142, w=16, track="#D5D5D0",
  dot_r=12.5, dot_collar=3,      # teal disc with a white collar, per the design
  run_deg=-90, check_deg=-90,    # a lap starts and is judged at the top

  header=dict(cy=355, size=32, text="RUN A STEP", color="#1e1e1c"),
  chip=dict(cx=357, cy=425, w=90, h=34, size=14, dot=8, text="CHECK",
            face="#ffffff", edge="#d5d5d0", color="#1e1e1c"),
  count=dict(num_cy=598, num_size=48, label_cy=638, label_size=12,
             label="STEPS DONE", label_color="#8a8a87", total=2),

  # The caps are not decoration: a loop stops when every step passes, OR it hits
  # the step cap, OR it runs out of budget. They are the other two termination
  # conditions, which is exactly what the panel is defining. Kept quiet and
  # unanimated so they never compete with the count -- and they pay off later,
  # when the AI says "fifty steps, five dollars" and the viewer has already seen
  # the numbers the dev talked over.
  caps=dict(label_cy=585, value_cy=610, label_size=16, value_size=20,
            label_color="#8a8a87", value_color="#1e1e1c",
            left_x=64, right_x=656,
            left=("STEP CAP", "50 max"), right=("BUDGET", "$5.00")),

  exit=dict(x=357, y=761, w=6, h=77, color="#cfcfcb", op=0.5),
  done=dict(x=212, y=841.5, w=296, h=80, r=64, size=27,
            label="CONDITION MET", color="#cfcfcb", edge_w=3),

  # ---- timings: offsets into AITECH, unchanged. They are solved from where the
  # words land in the take and do not depend on the geometry.
  #   0.09-2.75   "Iterative execution against a termination condition."
  #   4.77-5.68   "I decompose the task."        -> the ring divides into 2
  #   6.41-6.91   "Run a step."                  -> the dot sets off
  #   7.34-8.17   "Evaluate the result."         -> it comes back round to CHECK
  #   9.21-9.83   "If I fail,"                   -> the chip goes red, arc holds
  #  10.08-11.17  "I go round and run it again." -> lap 2, faster
  #  11.87-13.32  "I stop when every step has passed." -> lap 3, 2/2, fill
  #
  # RULE: never advance the count without a lap. And the ARC tracks the COUNT,
  # not the dot -- so a failed lap is a whole revolution where the arc does not
  # move, which is the most legible way to show a wasted iteration.
  # "I decompose the task" has to be an EVENT, not a nick in the line. The ring
  # is drawn as `total` separate arcs whose gap starts at zero -- so it is one
  # continuous ring until the split, then the gaps open (with a little
  # overshoot) and each segment pulses in turn, counting the steps out. After
  # that the ring is visibly two objects for the rest of the panel, and each one
  # fills as its own step passes, so the ring and the fraction cannot disagree.
  split_gap=13,                  # degrees, ~32px of arc at r=142
  # One at a time: arc A swells and returns to size, THEN arc B does. The
  # stagger must be >= the pulse or they overlap and it reads as both at once
  # rather than as counting.
  split_pulse=0.30,              # how long one arc takes to swell and settle
  split_stagger=0.34,            # gap between one arc and the next
  draw=dict(at=3.40, dur=0.60),
  split=dict(at=4.76, dur=0.70),
  # Each lap ends at -90, the top, because that is where the CHECK chip is.
  # These used to stop at 240 (upper-left), which was the old layout's separate
  # check gate -- the chip would fire while the dot sat somewhere else.
  arc=[[6.41, -90], [8.00, 270], [10.10, 270], [11.00, 630],
       [12.25, 630], [13.00, 990]],
  # each lap is judged at the top, where the CHECK chip is
  checks=[[9.50, False], [11.15, True], [13.10, True]],
  flash=0.5,
  fill=dict(at=13.22, dur=0.50),
  exit_at=dict(at=13.60, dur=0.30),
  done_at=dict(at=13.75),
  count_steps=[[11.15, 1], [13.10, 2]],
)

# Stage one holds the monitor; stage two drops it. `at` is the cut.
# mark_after is None: the mark belongs to the monitor, and once the monitor is
# gone the diagram is the subject and a badge in the corner is just clutter.
PUSH = dict(frame=15, at=3.25, bg="#f4f4f1", mark_after=None)  # offset into AITECH


# ---------- held captions ----------
# A caption that arrives as a WHOLE SENTENCE and holds, not one word at a time.
# Used for stage one of the explanation, above the monitor.
#
# The word-by-word reveal is wrong for a line like this. The jargon is meant to
# arrive as a wall, and a wall is easier to take in one piece than in
# twenty-three flickers -- across this film the median caption word is on screen
# for 299ms and 30% are under 200ms, which is below the time it takes to read
# one. Stage two carries no caption at all: the diagram is made of words.
HOLD_CAPTIONS = [
  dict(frame=15, text="Iterative execution against a termination condition.",
       x=111, y=228, w=498, align="C", size=32, line=40, hex="000000",
       at=0.05, until=3.15, fade=0.28),   # offsets from frame 15's start;
       # the opening line now ends at 2.75, so the card holds 0.4s past it
]


# ---------- per-clip gain ----------
# Kept for future clips. The sigh's boost is baked into its own file instead:
# seeking into an mp3 with startFrom is not frame-accurate, and the clip was
# landing ~0.2s late, which is what made the caption look early.
# The sting peaks at -4dB in the source; dialogue sits near -24. 0.28 put it at
# about -15dB in the mix, which was too hot. 40% of that puts it near -23 --
# level with the dialogue, so it punctuates instead of dominating.
# The scream sting fires with the disintegration. It briefly came out when the
# line changed -- a scream over a sleeping man made no sense -- and came back
# when Sejal put the dev himself on the track: he wakes up, tries to run it,
# gets X-ed out, screams, disintegrates.
CLIP_GAIN = {(20, SCREAM): 0.112}


# ---------- the plain-english explanation (frame 20) ----------
# The opposite of the technical screen in every way: no monitor, no chrome, no
# colour beyond one accent. A dot, a line, and the space between them.
#
# "You give it a finish line."      HE plants it -- the only thing he does
# "It does one thing,"              the dot leaves him and hops
# "checks whether it's there yet,"  it pings the line and gets nothing back
# "does the next thing."            it hops again
# "Nobody in the middle."           HE FADES OUT and it carries on without him
#
# The first version had no human in it at all, so "nobody" had nothing to be the
# absence OF. You have to see somebody leave for the empty middle to mean
# anything -- and it quietly previews what he is about to do in the story.
# EVERY TIME IN HERE IS AN OFFSET FROM THE PANEL'S OWN START, not film time.
# They used to be absolute, and four retimes of the technical panel left the
# whole hopping sequence firing 5.7s before its own panel opened -- so the panel
# opened with the dot already arrived and the animation simply never played.
# emit.py adds the frame's start; nothing here moves when the timeline does.
PLAIN = dict(
  # THE FORK. Traced from Sejal's generated circuit (9 Sep 2026) and scaled to
  # 60% so it stops filling the frame. Thinned to a 1px centreline, and the
  # topology came back as exactly two junctions and zero endpoints -- a theta
  # graph, three distinct routes between the same two points. The fork is real
  # geometry, not an artefact of the drawing.
  #
  # It replaces a single path where "failure" was a lap on which a number did
  # not move. Here the failure is a DECISION you can see: the runner takes the
  # short chord, and the checkpoint it skipped is sitting on the road it did not
  # take. Same idea, visible cause.
  #
  # All three routes run A (u=0) -> B (u=1).
  #   main  1150px   the big lobe, and the lap's start/finish sits on it
  #   long   707px   carries checkpoint 2
  #   short  362px   bypasses checkpoint 2 entirely
  routes=dict(
   main=[
    [473.1,658.6], [478.3,650.5], [483.6,642.5], [488.8,634.6], [493.4,626.3], [497,617.4],
    [499.2,608], [500.4,598.1], [500.1,587.9], [498.6,578], [496,568.5], [492.3,559.4],
    [488,551], [483.1,543.1], [478,535.6], [472.8,528.4], [467.1,521.5], [461.2,514.8],
    [455.2,508.2], [448.9,502], [442.5,495.6], [435.9,489.2], [428.7,482.8], [421.3,476.2],
    [413.8,469.8], [406.1,463.6], [398.4,457.3], [390.7,451], [383,444.9], [375.8,438.7],
    [369,432.6], [362.5,426.3], [356.6,419.8], [351,412.6], [346,404.8], [341.6,396.3],
    [337.9,387.3], [335,377.8], [333,368.1], [332,357.9], [332,347.7], [333,337.6],
    [334.8,327.6], [337.5,318.2], [341,309.3], [345.3,301], [350.2,293.4], [355.7,286.4],
    [361.8,280.1], [368.6,274.3], [376.1,269.2], [384.3,264.6], [393.1,261], [402.4,258.2],
    [412,256.4], [422.2,255.4], [432.5,255.4], [442.8,256.4], [452.8,258.2], [462.5,261],
    [471.5,264.6], [479.9,269], [487.6,274.1], [494.5,279.3], [500.5,285], [506.2,290.9],
    [511.4,296.9], [516.7,303], [521.7,309.3], [526.6,315.8], [531.6,322.6], [536.6,330],
    [542,337.9], [547.4,346.5], [552.8,355.1], [558,364], [563,372.8], [567.8,381.7],
    [572.3,390.6], [576.6,399.6], [580.6,408.5], [584.3,417.2], [588,426.2], [591.4,435.2],
    [594.6,444.2], [597.6,453.5], [600.4,462.8], [603,472.2], [605.4,481.6], [607.7,491.3],
    [609.8,501.1], [611.7,511], [613.4,521.2], [614.8,531.4], [616,541.9], [617,552.4],
    [617.8,562.9], [618.5,573.5], [618.8,584], [619.1,594.6], [619.1,605.1], [619,615.7],
    [618.7,626.2], [618.2,636.7], [617.5,647.2], [616.5,657.6], [615.2,668], [613.7,678],
    [611.8,687.9], [609.7,697.6], [607.2,706.9], [604.5,716.2], [601.7,725.2], [598.6,734.1],
    [595.3,742.9], [591.7,751.4], [588,759.6], [584,767.8], [579.8,775.7], [575.4,783.6],
    [570.8,791.1], [566,798.4], [561,805.4], [555.7,812.3], [550.1,819.3], [544.1,826.5],
    [537.8,833.6], [531.2,840.7], [524.3,847.6], [517.2,854.2], [510,860.5], [502.8,866.4],
    [495.7,871.9], [488.6,877.2], [481.2,882], [473.5,886.7], [465.2,891.2], [456.7,895.8],
    [447.9,899.9], [439,903.7], [430,907.1], [420.7,910.1], [411,912.6], [401.1,914.6],
    [390.8,916], [380.5,916.8], [370,917.2], [359.4,917.2], [349,917], [338.7,916.2],
    [328.6,915.3],
   ],
   long=[
    [465.6,663.8], [455.5,662.8], [445.3,661.6], [435.2,660], [425.6,657.7], [416.3,654.8],
    [407.4,651.2], [398.6,647.2], [389.9,643], [380.9,639.2], [371.5,636], [361.8,633.3],
    [351.7,631.5], [341.2,630.2], [330.8,629.8], [320.3,630], [310,630.8], [299.8,632.5],
    [290,634.7], [280.8,637.6], [272,641.1], [263.6,645.1], [255.7,649.7], [248,654.7],
    [240.6,660.2], [233.3,666.5], [226.4,673.3], [220,680.4], [214.4,687.8], [209.4,695.3],
    [205,703.1], [200.9,711.4], [197.4,720.1], [194.3,729.2], [191.5,739], [189.4,749.1],
    [187.6,759.5], [186.1,769.8], [184.5,780.1], [182.7,790.1], [180.6,799.9], [178.1,809.5],
    [175.3,818.8], [172.1,828.1], [168.6,837], [164.8,845.9], [160.7,854.8], [156.4,863.6],
    [151.8,872.5], [146.9,881.5], [141.7,890.5], [136.6,899.5], [131.3,908.6], [126,917.6],
    [120.8,926.5], [115.6,935.5], [110.7,944.5], [106.6,953.6], [103.4,963], [101.8,972.8],
    [101.8,982.6], [103.6,992.1], [106.9,1000.8], [112,1008.5], [118.2,1014.7], [125.8,1019.6],
    [134.4,1023], [143.8,1024.6], [153.5,1024.6], [163,1023], [171.6,1019.7], [179,1015.4],
    [185.3,1009.7], [190.4,1003.2], [194.9,995.5], [198.9,987.2], [202.8,978.5], [206.7,969.7],
    [210.7,961], [215,952.7], [220,945], [225.8,937.9], [232.6,931.9], [240.4,926.8],
    [249,923], [258.5,920.4], [268.6,918.7], [278.9,918], [289.4,917.7], [299.8,917.6],
    [310.1,917.6], [320.3,917.6],
   ],
   short=[
    [473.9,666.9], [484.1,668.6], [493.6,671], [502.4,674.4], [509.8,679.4], [515.6,686.2],
    [519.6,694.3], [522,703.5], [522.6,713.3], [521.3,723], [518.2,732], [513.3,739.6],
    [506.4,745.5], [498,749.7], [488.5,752.1], [478.3,753.3], [467.9,753.9], [457.3,754.1],
    [446.8,754.2], [436.2,754.2], [425.7,754.2], [415.2,754.2], [404.6,754.2], [394.1,754.2],
    [383.5,754.3], [373,754.8], [362.7,755.7], [352.7,757.2], [343.1,759.7], [334.3,763.4],
    [326.3,768], [319,773.7], [312.8,780.3], [307.4,787.7], [303.1,795.9], [299.8,804.8],
    [297.5,814.3], [296.1,824.4], [295.8,834.5], [296.4,844.7], [298.1,854.5], [300.5,863.9],
    [303.6,872.8], [307.4,881.1], [311.5,888.7], [315.5,896.1], [319.2,903.2], [322.6,910.1],
   ],
  ),
  w=22, order=("main", "long", "short"),
  start_u=0.236,                     # start/finish, on main, beside the dev

  gate_w=16, gate_h=62, num_d=44, size=64,
  flag_w=110, flag_h=26, flag_sq=13, label_d=96,

  # Checkpoint 2 is the whole point: it is only reachable via the long leg.
  cps=[dict(n=1, route="main",  u=0.110),
       dict(n=2, route="long",  u=0.500),
       dict(n=3, route="main",  u=0.660)],

  # ---- the itinerary, as offsets into ai_plain.mp3 -------------------------
  #   0.13-1.23   "You give me a finish line."       -> the finish draws
  #   1.81-3.55   "I make sure I hit every checkpoint." -> track, then gates
  #   4.30-4.78   "Miss one,"                        -> 2 goes red, un-visited
  #   5.26-6.62   "I go back until I get it right."  -> reverses out, takes long
  #   7.96-8.79   "I race for you,"                  -> the run home
  #   9.58-10.53  "so you don't have to."            -> he tries it himself
  legs=[
    dict(at=2.95, until=3.90, route="main",  u0=0.236,   u1=0.0),
    dict(at=3.90, until=4.50, route="short", u0=0.0,   u1=1.0),
    dict(at=5.26, until=5.85, route="short", u0=1.0,   u1=0.0),
    dict(at=5.85, until=6.58, route="long",  u0=0.0,   u1=1.0),
    dict(at=6.58, until=9.20, route="main",  u0=1.0,   u1=0.236),
  ],
  # DERIVED from the itinerary -- a checkpoint lights the frame the runner
  # reaches it, never a beat later. Hand-set times drifted up to 0.56s late.
  checks=[[3.45, 1, True], [4.55, 2, False], [6.21, 2, True], [7.79, 3, True]],
  flash=0.55,
  flag_at=0.45, flag_dur=0.60,
  track_at=1.81, track_dur=0.80,
  gates_at=2.75, gates_dur=0.42, gates_stagger=0.30,
  cross_at=9.20,

  head=dict(
    cx=202, cy=268, h=190,   # solved clear of track, band, every label and the counter
    awake="face.png",        awake_ar=0.7923,  awake_dx=+0.0073, awake_dy=+0.0269,
    asleep="face-sleep.png", asleep_ar=0.9445, asleep_scale=1.0922,
                             asleep_dx=+0.1185, asleep_dy=-0.0099,
    sleep_at=2.95, wake_at=7.96,
    step=[8.25, 8.75], run=[8.75, 9.70], run_u=0.06, run_h=135,
    x_at=9.75, x_dur=0.22, x_size=104, x_w=12,
  ),
  # A running tally, bottom-right, clear of the track and every label. Small on
  # purpose: it confirms the count without competing with the road, where the
  # actual teaching happens.
  counter=dict(cx=560, cy=1032, w=96, h=54, r=12, size=30,
               face="#ffffff", edge="#dcdcd6"),
  gone_at=10.35, emoji_hold=0.0, emoji_fps=20, emoji_n=27, emoji_size=220,
)


# ---------- the AI's mark ----------
# It had no body: a screen sometimes, an abstract dot other times. One mark on
# every blank monitor AND as the thing travelling in the plain explanation means
# the diagram stops being a diagram -- it isn't "a dot", it's him.
#
# Deliberately NOT a face (the AIs never have faces) and NOT a four-point
# sparkle (every AI product on the market uses one). A rounded body with a
# forward chevron: abstract, unmistakably facing somewhere, nobody's logo.
#
# Facing matters -- a symmetric mark can't show a head-turn, and the check in
# panel 20 is a look BACK at where it came from.
# Frame 15 carries the mark for STAGE ONE ONLY -- centred on the monitor, as on
# every other frame the AI speaks. PUSH["mark_after"] is None, so it goes when
# the monitor goes. (The mark was queried on review as reading like a generic AI
# logo; kept here on Sejal's call because a blank monitor with a caption above it
# needs something in it, and this is the one place it is doing that job.)
AI_MARK_FRAMES = [15, 19, 23, 24, 27, 29, 34, 42, 43]
# Frame 15 is not here: it starts centred on the monitor like every other AI
# shot, then PUSH["mark_after"] drops it to a corner byline once the diagram
# takes the frame -- a byline saying who is talking, not the subject.
AI_MARK_OVERRIDE = {
  34: dict(cx=360.0, cy=637.0, size=66),   # the lit screen in the dark room
}
AI_MARK = dict(screen_cx=359.5, screen_cy=713.0, screen_size=132, travel_size=82)
# The check has to be a PHYSICAL move, not just a core shifting inside the body.
# At 48px the internal gaze was invisible; the mark now slides back toward the
# start, holds, and returns -- legible at any size.
CHECK_BACK = 44          # plate units it retreats on a check


# ---------- the card (frame 44) ----------
# The stamp moved up in Figma to make room. Underneath it, the thing that
# actually happened while he slept: the credits draining to nothing. It is the
# cost bucket's on-screen number from the series doc, made to run down.
CREDITS = dict(
  label_cy=705, num_cy=792, cx=360,
  start=4812,            # an unremarkable balance, so zero lands harder
  appear=3.100,           # seconds after the card
  run=1.15,              # how long it takes to drain
)

# ---------------------------------------------------------------------------
# The card, on frame 44 -- REPLACING the white "LOOP -cleared-" plate and the
# bare credits counter that used to float over it.
#
# It was briefly at the very end of the film, which was wrong: the episode's
# last line runs into its own opening line so the video loops seamlessly, and a
# card after that breaks the loop. This slot is the right one -- it is where the
# stamp already was, mid-film, and it still names the term.
#
# Written as a phrasebook entry because that is what the channel is: a public
# reference, one entry per video. The definition does the teach a last time in
# the plainest words available. Dark, against the light plates either side.
#
# The credits are a small instrument panel now, not digits in open space -- a
# meter with a label, a draining bar and a readout, which is what "cost" looks
# like when it is a thing being spent rather than a number going down.
OUTRO = dict(
  bg="#141416",
  # The series title is the HERO now, centred and set large -- this is the brand
  # slate. It used to be a 21px masthead at 3.64:1, which was the weakest thing
  # on a card where everything else was deliberate. Under it sits the phrasebook
  # entry it belongs to: the term, its pronunciation, its definition, and what
  # the night cost. Title first, then what the title is about.
  # The title arrives ALONE, centred, and holds -- for one second the frame is
  # nothing but the series name, which is what a slate is. Then it rises into a
  # header and the entry appears underneath it. A title that is a header from
  # frame one is never a title; it has to be the whole frame first.
  title=["I HAVE NO IDEA", "WHAT THAT MEANS"],
  title_cy=286,                  # where it settles, as a header
  title_cy_start=600,            # where it lands, centred and alone
  title_scale_start=1.16,        # slightly larger while it is the whole frame
  title_hold=1.35,               # how long it stays centred before it moves
  title_rise=0.55,
  title_size=54, title_line=64, title_color="#F2F2EF",
  rule_cy=392, rule_w=180,

  term="loop", term_cy=470, term_size=86,
  pron="/lu\u02d0p/  noun", pron_cy=534, pron_size=22,
  defn=["Stepwise work that checks itself", "and stops when it is done."],
  defn_cy=606, defn_size=34, defn_line=46,
  step=0.11,

  meter_at=2.65, meter_fade=0.45,

  # All three dy are the element's CENTRE. One 22px pad on all four sides and
  # 22px between elements.
  #   pad 22 | label 16 | 22 | bar 20 | 22 | number 52 | pad 22  = 176
  # num_dy is 2.7px above where the ink centres, because the comma hangs below.
  meter=dict(cx=360, cy=848, w=392, h=176, r=16,
             face="#23232B", edge="#40404B",
             label="AI CREDITS", label_dy=-58, label_size=20,
             bar_dy=-18, bar_w=348, bar_h=20, track="#34343E",
             num_dy=37, num_size=58),
)

