---
name: feedback-diff-before-rewrite
description: "When a beat 'doesn't land', diff the actual frames before anyone rewrites the script"
metadata:
  type: feedback
---

If a moment is not working, measure what is on screen before treating it as a
writing problem.

**Why:** on EP003 four people (Mohit, Prashasti, Anandhi, Sejal) spent a long
Slack thread on why the punchline did not land, and the thread moved toward
rewriting the whole story. I diffed the last three plates: **scene25 vs scene26
= 0 pixels different**, scene26 vs scene27 = 3,137 pixels, all inside one
105x42 box — his mouth. **8.74 seconds of film in which the only thing that
moves is a mouth opening.** No script change fixes that, and no reviewer had
the number.

**How to apply:**
- Diff consecutive plates and report the pixel count and the bounding box.
- Report screen time for the stretch that is failing.
- Put the measurement into the review thread. It converts opinion-vs-opinion
  into a decision, and it is usually the thing nobody has.
- The same check catches art that was supposed to change and did not: a new
  Figma frame came back pixel-identical to the one it was meant to differ from,
  twice, because a layer had not taken.

Related: [[feedback-push-back]], [[project-ep003-remote-control]]
