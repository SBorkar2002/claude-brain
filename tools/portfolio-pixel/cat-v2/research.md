# Cat v2 · research

17 Oct 2026. The rules that matter for a small black mascot cat, where each one came from, and what it changed in v2. The full notes (every source, quotes, timing table, what could not be reached) are in `research-raw.md`. Reference images are in `refs/`, for study only: nothing in v2 is traced or copied.

## 1. Canvas size: why v2 is 48 px

- Size the canvas to the smallest detail you must show. Small sprites put more responsibility on every pixel, so cut detail, don't cram it in (Derek Yu, https://www.derekyu.com/makegames/pixelart.html; Slynyrd Pixelblog 47, https://www.slynyrd.com/blog/2023/11/26/pixelblog-47-tiny-pixels).
- Other 32 px black cats get away with 1 to 2 px eyes (Neko, Slynyrd's mini cat, itch.io packs; see research-raw.md section 4). Sejal's brief asks for something they don't have: an O ring with a black fill that moves without breaking the ring. Here is the smallest version that works:
  - 6 px ring (v1): the fill is a 4x4 square with nowhere to go. Looking means shrinking it into a corner, which is the "distorted" read.
  - 8 px ring (v2): the fill is a round 6x6 at rest. To look, it narrows to 5 px on the axis it moves along and slides 1 px. The ring stays a clean 1 px O in every frame.
- An 8 px eye at her reference's proportions (eye width is about 1/2.9 of head width) gives a 22 px head, and a side-on cat of about 35 x 34 px. That fits in 48 px with room for the hop, the heart and the Z. **One size for every frame: 48 x 48**, shown at 3 px per pixel in Figma (144 px), which puts it the same height on screen as v1 at 4 px.

## 2. Line and shape rules applied

| Rule | Source | In v2 |
|---|---|---|
| Lines are 1 px and touch only on the diagonal. No L corners ("doubles") | Saint11 Fundamentals2, https://saint11.art/img/pixel-tutorials/Fundamentals2.gif ; Sam Keddy, https://lospec.com/articles/pixel-art-outlines/ | Ring, closed eyes, arcs, whiskers and the Z are all 1 px, diagonal-only |
| Curves: steps get shorter toward the corner, then longer (3-2-1-1-2-3, never 3-1-2). Uneven steps make jaggies | Saint11 Fundamentals2; cure, http://pixeljoint.com/forum/forum_posts.asp?TID=11299 ; Derek Yu (refs/derekyu-jaggies-curves.png) | Ear inner edge 1,1,1,2. Cheeks 1,1. Sitting body sides 1,1,2,2,2,2. Tails redrawn by hand until the steps run in order |
| Straight slants use regular steps. Avoid alternating 2-1 | OpenGameArt ch. 2, https://opengameart.org/content/chapter-2-lines-and-curves | Leg slants split rows into equal runs, longest in the middle (3,4,3 or 2,3,3,2), from 10-row legs. v1's 2,3,2 runs were the jagged legs |
| Corners can break the rule to make a point (ear tips, claws) | Saint11 Outlines, https://saint11.art/img/pixel-tutorials/Outlines.gif | Ear tips are single corner pixels on purpose |
| Orphan pixels add noise. Keep them only for essential detail (a small sprite's eyes) | Saint11 Fundamentals; cure | The only lone pixel is the eye shine, placed one pixel in from the ring so it never notches the O. v1's sleep tail hole and spur are gone |
| Very low res: avoid outlines. The black mass is the outline | Saint11 Outlines; Derek Yu | No outline. All the work is in the silhouette edge |

## 3. Silhouette and separation (one colour, so the shape does all the work)

- Silhouette first: if the pose doesn't read as a black shape, no detail will save it (Saint11 Silhouette, https://saint11.art/img/pixel-tutorials/Silhouette.gif).
- On a single-colour sprite, overlapping parts only separate through a 1 px background gap (or a lighter rim, which v2 does not use). Pose the cat so parts don't overlap (research-raw.md section 2, derived from Keddy and Saint11). Leave at least 1 px between limbs (Brandon James Greer, https://sozai.app/transcript/make-chrono-trigger-sprites-pixel-art/).
- A whisker the same colour as the body disappears inside the silhouette. It only reads against the background (seen in itch.io packs, research-raw.md section 8).
- Rounded, soft shapes read as friendly. A big head, wide face and weight at the bottom read as cute (Saint11 Cuteness, https://saint11.art/img/pixel-tutorials/Cuteness.gif).

What it changed: legs in a pair are either fully overlapped or at least 1 px apart, never touching (fixes v1's fat-leg flicker). Far-side whiskers sit inside the body and vanish, so the back never grows whisker ledges. The sitting body is a pear (narrow chest under the cheeks, wide haunches), so head and body separate through shape. The sitting tail sits on the rear side with a gap that varies along its length, so it reads as a "?" and not a mug handle. Peek paws sit outside the head silhouette (a version with 1 px gaps carved into the chin read as teeth).

## 4. Consistency and squash / stretch

- Mass never changes: if a shape gets shorter, it gets wider (Saint11 Squash, https://saint11.art/img/pixel-tutorials/Squash.gif).
- Keep clusters intact between frames, and animate one part at a time (Saint11 Fundamentals; Slynyrd Pixelblog 25, https://www.slynyrd.com/blog/2020/1/23/pixelblog-25-motion-cycles).
- Jump: anticipation squash, stretch going up, an apex, then squash hard on contact (Saint11 Jump, https://saint11.art/img/pixel-tutorials/Jump.gif).

What it changed: the head, eyes, ears and whiskers are fixed stamps that move but are never redrawn. Breathing only adds rows (1 px of back or chest), never width. React is now 4 frames: 2 px shorter and 2 px wider, then 2 px taller and 2 px narrower going up, then the apex with the heart, then a 1 px landing squash. The yawn stretch adds chest rows instead of growing the head (v1 grew a chin).

## 5. Eyes

- Pixel circles: the longest runs sit at the top, bottom and sides. The 8 px ring is 4-1-4 (Keddy; Saint11 Fundamentals2; research-raw.md section 4).
- Shiny dark eyes are the strongest "cute" cue (Saint11 Cuteness). Move the face contents after the silhouette moves (Saint11 Character Idle, https://saint11.art/img/pixel-tutorials/characterIdle.gif).
- Blink: open, closed, nearly open, open. Closed for about 100 to 170 ms, nearly open for about 80 ms (Clip Studio, https://tips.clip-studio.com/en-us/articles/2643 ; Wikipedia Blinking, https://en.wikipedia.org/wiki/Blinking).

What it changed: 8 px ring, round 6x6 fill, 1 px shine. Look frames narrow the fill (5x6, 6x5 or 5x5), the way a real eyeball foreshortens when it turns. Sit and Idle blinks now run closed (0.15 s) and then nearly open (0.08 s). Closed and sleep eyes are parts of the same ring: a flat line for a blink, the lower arc for sleep, the upper arc for happy, and a lid line with the fill below it for half-closed.

## 6. Walk

- A quadruped walk is two bipeds a little out of step. Contact order: back-right, front-right, back-left, front-left (Saint11 4LegsWalk, refs/saint11-quadruped-walk-trot.gif).
- Hips and shoulders move up and down in opposite directions by the same amount (Slynyrd Pixelblog 25).
- Small sprites walk in 4 frames at about 100 to 160 ms. Neko gets by with 2 frames while it slides across the screen (Slynyrd Pixelblog 8 and 22; YukiCrimson preview; oneko.js, https://github.com/adryd325/oneko.js/blob/main/oneko.js).

What it changed: 4 frames at 0.14 s. Each leg goes +3 contact, 0 support, -2 push, then swings back hidden behind the support leg. Near and far legs are half a cycle apart, and the hind pair leads the fore pair by a quarter, so every frame has one pair spread with a 1 px gap and the other overlapped. In the spread pair the far foot sits 1 px up, so frames 1 and 3 differ (push-off and reach). The head rises 1 px while the tail drops 1 px on the frames where the front legs pass. The tail tip sways on frames 3 and 4.

## 7. Idle, sleep, timing

- Idles for small sprites: 2 to 4 frames, or keep the body still and move only the tail (Slynyrd's dark cat idle, refs/slynyrd-idle-cycles-with-cat.gif; Saint11 Character Idle). Use the idle for personality: blink, yawn, look around (Saint11).
- Neko sleeps in 2 frames swapped about every 400 ms (oneko.js).

What it changed: Idle is 5 frames (base, a 1 px breath, a glance with a tail flick, closed, nearly open). Sleep is a front-facing loaf with the head lowered onto it and a 1 px breath. One 5 px Z appears and drifts up 4 px, then it's gone (v1's two Zs flickered). Timings live in `sprites.py` (TIMINGS) and drive the Figma After-delays.

## 8. Things no source covered, so they were tested instead

The research found nothing on drawing a yawn or a peek at small size. Both were decided by rendering variants side by side at 1x and 3x:

- **Yawn eyes:** I tested > <, flat lines, ∩ and ∪ against four mouths. "> o <" reads as straining or shouting, ∩ with a mouth reads as laughing, and ∪ reads as singing. Flat closed lines with a tall, narrow mouth read as a yawn. Final: half-closed (sleepy), then shut with a small mouth and a 1 px stretch, then shut lines pushed up clear of the whiskers with the tall mouth, 2 px stretch and ears back, then the small mouth, then content ∪ eyes.
- **Small mouth:** a 4x4 rounded mouth reads as a pink flower or nose, which is v1's problem. A 2x3 lip, opening and lip reads as a mouth starting to open.
- **Peek:** paws drawn over the chin with 1 px gaps read as teeth. Paws either side of the face read as hands on a ledge.

## 9. Fuller, squishier body (Sejal's direction, 17 Oct)

Her words: "a bit on the fuller, fluffier cat, not the skinny cat... not a fat cat, a normal looking, kinda squishy cat." The face, eyes, whiskers, canvas and states are unchanged. What changed, and the rule behind each change:

- **Round shapes read soft and friendly.** Cute means weight at the bottom, like a flour sack (Saint11 Cuteness). The sitting body is now 26 px wide at the haunches (it was 24) with convex shoulders. The side steps go 2, 1, 1, then one step every 2 rows, then vertical, so they curve out like the top of a circle instead of running as a straight 1:2 slope. Every paw has its outer bottom corner rounded off.
- **Side view:** the back, tail and rump are one hand-drawn shape. The rump bulges 2 px behind the tail base, the back rises softly to the shoulders, and the belly sags 1 px between the legs. Legs are 5 px (they were 4) with the heel corner cut, so they read as paws, not sticks.
- **Plumper tail:** a 5 px shaft with a 6 px round tip, tapering in one clean step with no notch (an earlier version with a notch under the tip read as a bone).
- **Squishy motion that keeps its mass:** the React squash is now 2 rows shorter and 2 px wider on each side, so it feels squishy without gaining volume (Saint11 Squash). Sleep is a rounder dome (steps 3, 2, 1, 1, 0, 1) with the plump tail curled at the front.
- **Walk still follows the no-touch rule:** with 5 px legs, a spread pair now steps +3 and -3 around the hip. That keeps a 1 px gap between the feet, with even runs (2, 3, 3, 2) over 10 rows.
- **Not fat:** the head stays 22 px and the body stays narrower than 1.2 heads. The cat stands about the same height as before.

## 10. Round 3: Sejal's motion review (17 Oct)

She watched every state animated and asked for these changes. What was done:

- **Yawn looked vulgar.** The tall pink oval with a tongue read as something else. I tested five mouths side by side. Wide pink shapes read as lips and tall ones as a tongue. A small V of mouth-inner colour with two white fangs at the top corners reads as a cat's open mouth, so the big yawn is now a 6x4 V and the small one a 4x2 V.
- **Sitting kept its limbs apart.** The 1 px gaps between the haunches and the front paws made the cat look like it was holding itself apart. The base is now one solid, soft shape with rounded outer corners. This carries into Look, Yawn, React and Land.
- **Inspect points instead of pouncing.** It is now a side view facing the artwork. The cat notices it, sinks into a crouch (chin down on folded forearms, rump 5 px higher than the head, tail straight back and low), does a butt wiggle (rump up 1 px, tail tip flicks) twice, then rises. 8 frames.
- **Walk legs met at one point (a downward V).** The two legs of a pair shared a hip. Now each leg joins the body at its own spot (hips at x 6, 16, 24 and 34, the same as the Idle stance) and slants 2 px each way. A script checks that no two legs come within 1 px of each other in any frame. The body moves 2 px a frame, so a planted paw stays put.
- **New Fall state (page load).** The cat falls in the mid-air landing pose: body upright, four legs stretched out about 30 degrees (1:2 steps, which is 26.6 degrees), tail straight and raised. It spins a full turn around its vertical axis in 8 frames (front, three-quarter, profile, three-quarter back, back, then mirrored). These are separate drawings, never an in-plane rotation. The profile has its own head with one narrower O eye and forward whiskers. The back view has no face. The eyes look down at where it will land.
- **New Land state.** The paws reach for the divider, then a squashy plop (2 px wider each side, eyes squeezed by the impact), a small bounce, then Sit. Land chains into Sit in Figma.
- **React uses the same mid-air pose.** Squash, then a hop with four legs out and the tail up, then one heart at the top, the paws reaching on the way down, a soft landing, and back to Sit.
- **Unchanged, as she approved them:** Look (eyes) and Sleep.

## 11. Round 4: second motion review (17 Oct)

She approved Fall (the spin), Yawn and the Peek pose. Changes:

- **Land felt like a random plop.** It is now 7 frames with a beat in the middle: paws reach (0.08 s), a squashed impact with the eyes squeezed (0.16 s), a stunned hold with the eyes open and looking down (0.5 s), a blink (0.12 s), it stands up on four straight legs (0.35 s), lowers (0.14 s), then sits. On the page the whole landing takes about 1.5 s instead of 0.3 s.
- **Inspect, researched.** The sources agree on a low, coiled body, front paws reaching forward, back legs gathered to push off, and a twitching tail. One describes a cat that "lowers their body", whose "back legs prepare" and whose "tail may twitch" ([Raw Paws, cat hunting sequence](https://www.rawpawspetfood.com/blogs/raw-paws-blog/cat-hunting-sequence-stalk-chase-pounce-catch)). An animator's breakdown starts with a coiled crouch before the launch ([BGSU animation blog](https://blogs.bgsu.edu/artc413andjack/2008/09/22/draft/); search results summarised in the session). No source gives a frame-by-frame breakdown. Her notes on top of that: the tail is up, the front paws sit ahead of the face, and the back legs move. So the crouch has the chin low, the forearms flat with the paws stretched out 6 px past the face, and the back legs gathered under the belly as two paws. In the wiggle those paws tread (one lifts 1 px, then the other) while the rump bobs 1 px and the tail tip twitches the opposite way. The back now slopes down to meet the neck below the ear tips, so the head keeps its own silhouette.
- **Walk felt unsettling.** It is now a diagonal-pair gait: front-near with back-far, then front-far with back-near, the "opposite limbs together" pattern most people read as a walk (strictly a trot). Each leg keeps its own hip. The body rises 1 px on the passing frames, when the legs are under it, and drops on contact.
- **Peek bounce.** Ears hold for 1 s, then it pops up fast (0.06 s), overshoots 2 px (0.08 s), dips 1 px (0.08 s), settles (0.5 s), then looks left and right slowly (1 s each).
- **React's back legs splayed.** The hop now uses its own front pose with all four legs straight down under the body (front legs inside, back legs just outside and 3 px higher) and the tail straight up. The splayed pose stays only in the Fall spin, which she approved.

## 12. Round 5: the walk, studied from her two reference GIFs (17 Oct)

She sent two walking-cat GIFs. Frame by frame:

- **Orange cat** (19 frames at 40 ms, a 0.76 s cycle): short, rounded, capsule-shaped legs swing from fixed hips, and the body and head bob. The far-side legs are a darker shade than the near ones, which is the only reason you can see the opposite legs moving together.
- **Pixel black cat** (4 frames at 100 ms): the rump flows straight down into a thick back leg, the front legs are thinner, the feet are short under a long body, and the tail sways.

Why ours read wrong: with one flat colour, near and far legs are identical, so the diagonal pairs read as all legs out, then all legs in (jumping jacks). And the back legs were 5 px sticks with a notch where the rounded rump met them.

Fix: the back legs now have an 8 px thigh that grows out of the rump (the near one sits at the very back, so the rump flows into it with no notch) and tapers to a 5 px shin. The front legs are 5 px tapering to 4 px. The far legs are drawn first, behind the body, in a new colour variable `cat/body-far` (Light #423B54, Dark #BEB7D2), with their paws 1 px higher. The gait is diagonal pairs (near-front with far-back), stepping +3, 0, -3, then lifted, with a 1 px body bob, travelling 3 px a frame.

Land: she did not want it to sit twice. After the impact the cat now stays bent down on all fours (head low, front paws splayed under the chin, haunches bulging either side). It recovers with its eyes shut, then open and looking down, then looks up, then rises into one normal sit.

Load timing: it felt like time stopped just before the landing. The page used to rise with ease-out, slowing to a stop at the cat's paws. It now rises with ease-in, speeding up like a fall, so the touchdown hits hard. The spin is timed to finish on the front view 0.3 s before touchdown, and the paws reach in the last 0.1 s, so the cat no longer keeps turning right up to the ground.

## 13. Round 6: her refined reference (19 Oct)

Reference: `inventory/refs/cat-reference.webp`. It shows a white cat with lilac shading, yellow ring eyes with black pupils, distinct head and body, clean edges, and no nose, mouth or whiskers. Changes:

- Whiskers removed from every frame.
- Distinct head and body: every body pixel touching the head's sides or underside becomes the lilac shade ('f', the same colour as the far legs), so the head reads as its own shape (and as a darker grey-lilac line on the black light-mode cat).
- The yawn keeps its approved small V mouth and adds yellow marks beside the head, as in the reference. React's heart is replaced by the same yellow surprise marks. Sleep shows a small z, then a z and a big Z, never more than two.
- Landing rebuilt, because it "looks off". The paws reach straight down, the same standing front body compresses on impact (body down 5 px, legs shorter and splayed 1 px, belly 1 px wider, eyes squeezed), it stays low with its eyes shut, then open and looking down, then it rises and sits once. The old wide crouch read as a different shape.
- Export: the site reads `cat-v2/preview/frames.json` through `scripts/export-cat-frames.mjs`. The legend is unchanged.

## 14. Round 7: her direct notes on the refined reference (19 Oct)

- Keep the whiskers (restored), and no neck line (the lilac head separation is removed everywhere).
- Standing pose measured from her reference (sampled to a grid at about 9.3 px): the head sits on the front-top of a box body with its bottom at mid-body, and juts 8 px forward past the chest, leaving a gap under the chin. The tail is a tall straight 6 px column with a round top. The legs are 8 rows: a thick white near back leg at the very back, a lilac far back leg just ahead of it, a white near front leg under the back half of the head and a lilac far front leg under the chest.
- Walk: a stride like her reference. Near front and far back legs reach together, then the other pair, and the white near legs pass over the lilac far legs.
- Look around: now the standing pose with the eyes sweeping, as in her reference (it was the sitting pose).
- Inspect: the reference's low stalking crouch (head forward and highest, back sloping down to the rump, tail straight up, legs folded short), replacing the pounce crouch. Butt wiggle kept.
- Unchanged at her request: Yawn, Sleep, Peek (apart from the whiskers coming back).

## 15. Self-critique log

- **Pass 1 (first full render), three worst:** (1) sitting front paws carved into five bars, which read as a comb; (2) peek paws outlined inside the chin, which read as teeth; (3) yawn "> o <", which read as a scream. Also the tail and legs were too thin next to her reference (checked by setting the reference beside Idle 1). Fixed: fewer, shorter paw gaps; paws beside the face; flat-eyed yawn; 4 px tail and legs.
- **Pass 2, three worst:** (1) the Inspect raised paw read as a stick, so it got a round paw on a 1:1 arm; (2) the side-on torso read as a box, so it got a fillet where the tail rises and a 1 px belly tuck between the legs; (3) the small yawn mouth read as a nose, so it is now the 2x3 version. Then the research pass added mass-preserving squash, the open, closed, nearly open blink, and the opposite hip and shoulder bob.
- **Still open, for Sejal's eye:** the 1 px ring is thinner than v1's 2 px ring, which matches her reference but is quieter at 1x. Sit and Look carry the shine on the black cat. If she wants bolder eyes, a 2 px ring is a one-line change (`RING`) at the cost of a smaller fill.
