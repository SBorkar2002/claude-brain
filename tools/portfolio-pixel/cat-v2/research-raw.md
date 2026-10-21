# Pixel cat craft: raw research (cat-v2)

Researched 17 Oct 2026 for a 24 to 48 px black cat mascot (target 32 px, round O eyes).
Every rule has its source next to it. Items marked **[derived]** are my own application of the sourced rules, not something a source says.
Items marked **[observed]** are what I saw when I zoomed into another artist's published preview image (studied for learning only, nothing copied).

Saint11 (Pedro Medeiros) tutorials are image posters. Their text was read off the GIF frames. The index page is https://saint11.art/blog/pixel-art-tutorials/ and each poster lives at https://saint11.art/img/pixel-tutorials/NAME.gif (cited below by NAME).

---

## 1. Line rules at small size

- A clean line is 1px thick and its steps touch **only diagonally**, with no extra pixels at the joins. Sketch rough, then zoom in and delete pixels until segments meet only at corners. (Sam Keddy, "Pixel Art Outlines", https://lospec.com/articles/pixel-art-outlines/)
- **Straight lines:** use "regular" lines where every step has the same number of pixels. (Saint11, Fundamentals2: https://saint11.art/img/pixel-tutorials/Fundamentals2.gif)
- **Perfect slopes** are the simple ratios 0:1, 1:2, 1:1, 2:1, 1:0; the eye follows them easily. In-between slopes (alternating 2 and 1) look much less appealing, use sparingly. (OpenGameArt lineart chapter 2: https://opengameart.org/content/chapter-2-lines-and-curves)
- **Irregular lines** are "non-ideal but useful": if you need one, repeat a pattern of adjacent numbers, e.g. 2,2,3,2,2,3. (Saint11, Fundamentals2)
- **Curves:** each step should be shorter than the previous one until you reach the "corner", then go backwards, increasing step size (so 3-2-1-1-2-3, never 3-1-2). (Saint11, Fundamentals2)
- **Curves and circles:** longest segments sit at the top, bottom, left and right; they shorten gradually toward the diagonals. Uneven ordering creates a lump. (Sam Keddy, Lospec, link above)
- Curve segment lengths should "vary in a progressive manner"; avoid right angles inside a curve, they make it look broken. (OpenGameArt chapter 2)
- **Jaggies** = a pixel or group out of place that breaks the flow of a line; usually one segment is too short or too long. Fix by making segment-length transitions uniform. (cure, "Pixel Art Tutorial", Pixel Joint: http://pixeljoint.com/forum/forum_posts.asp?TID=11299)
- Keep segment lengths on curves changing gradually; jaggies appear when segments grow or shrink unevenly. Reduce outlines to 1px and remove stray pixels in cleanup. Jaggies cannot be removed entirely on anything but simple shapes, only minimised. (Derek Yu, Pixel Art Tutorial: https://www.derekyu.com/makegames/pixelart.html; diagram saved as refs/derekyu-jaggies-curves.png)
- **Doubles / bad corners:** "line steps should always connect diagonally"; L-shaped corners create a thicker point in the line. (Saint11, Fundamentals2). Saint11's line clean-up order: start with a dirty line, clean up unwanted corners, fix 2px lines, change irregular patterns. (Saint11, Outlines: https://saint11.art/img/pixel-tutorials/Outlines.gif)
- Exception: unwanted corners can be useful to add detail or a sharp point in low-res images (ear tips, claws). (Saint11, Outlines). Break the 1px diagonal rule on corners to create a point. (Sam Keddy, Lospec)
- **Orphan pixels** = pixels not in a chunk; too many add noise. They are useful for strong deliberate details. (Saint11, Fundamentals: https://saint11.art/img/pixel-tutorials/Fundamentals.gif). Isolated pixels are justified for small essential details such as the eyes of a small sprite. (cure, Pixel Joint)
- Diagonal pixels do not connect very well; avoid many tiny clusters. When animating, keep track of clusters and avoid breaking them. (Saint11, Fundamentals)
- **Unintentional squares:** adjacent pixels tend to form big squares; place colours in a brick-like pattern and look for imaginary squares. (Saint11, Fundamentals2)
- **Banding** = neighbouring pixel runs ending on the same x or y, which exposes the grid. Variants: hugging the outline, fat pixels, skip-one, 45 degree banding. (cure, Pixel Joint). Many similar shades in a gradient also band; reduce colours. (Derek Yu). Compress colour bands so steps are harder to see. (Saint11, Shading: https://saint11.art/img/pixel-tutorials/Shading.gif)
- **Pillow shading** = concentric darkening around the centre of a shape, ignoring the light source; shade by light direction and form instead. (cure, Pixel Joint)
- **Outline or not:** outlines take a lot of space, so avoid them if possible in very low res. (Saint11, Outlines). Smaller sprites carry more responsibility per pixel; define shapes with colour rather than outlines that eat room. (Derek Yu)
- Outer border separates the shape from the background; an internal border separates shapes from each other, and the internal border can be lighter. (Saint11, Outlines)
- Selective outline (selout) = a lighter outline where light hits, removed where the sprite meets negative space; good only if built for a known background. (Derek Yu; cure, Pixel Joint)
- An outline must always increase contrast, never decrease it, and should be darker than both the object and the background. (Sam Keddy, "Outlines Part 2: Using Color": https://lospec.com/articles/pixel-art-outlines-part-2-using-color/)
- **[derived]** For a solid black cat on a light page, the black mass already is the outline. No separate outline is needed; the work is in the silhouette edge (clean 1px stair steps) and in any lighter interior lines.

## 2. Silhouette and readability at 1x

- "The silhouette is the prologue, the first thing the viewer will notice." Process: silhouette sketch, then add details, then animate. Sketching an animation in silhouette makes sure the action is easy to read. (Saint11, Character Design 1: https://saint11.art/img/pixel-tutorials/Silhouette.gif)
- Add strong recognisable elements to the silhouette (his examples: flat head, tank treads). (Saint11, Silhouette). **[derived]** For a cat these are the two ear points and the tail.
- Sharp, spiky, complicated shapes read as danger; rounded soft shapes read as friendly. (Saint11, Silhouette and Cuteness: https://saint11.art/img/pixel-tutorials/Cuteness.gif)
- Even at 8x8 a character must stay readable; show only necessary information and let the viewer imagine the rest. (Slynyrd, Pixelblog 47 Tiny Pixels: https://www.slynyrd.com/blog/2023/11/26/pixelblog-47-tiny-pixels)
- Leave at least one pixel of space between limb lines so poses stay readable. (Brandon James Greer, "How to make Chrono Trigger sprites", transcript: https://sozai.app/transcript/make-chrono-trigger-sprites-pixel-art/)
- Any two touching colours must be distinguishable at 1x; if they blend, change one or separate them. (Sam Keddy, Lospec Part 2)
- Add interior lines only where contrast between parts is low (head vs neck); a short partial line extended inward from the outline is enough to suggest separation. Omit the outline where an object touches another surface (paws on ground) or it will look like it floats. (Sam Keddy, Lospec)
- Use a dark colour instead of black for a softer outline; lighter internal borders separate overlapping parts. (Saint11, Outlines)
- **[observed]** Slynyrd's tiny sitting cat (about 13 x 11 px, inside https://www.slynyrd.com/blog/2018/8/19/pixelblog-8-intro-to-animation, image refs/slynyrd-idle-cycles-with-cat.gif) is one flat dark colour, no outline, no interior lines; it reads purely from silhouette: two 1px ear spikes, a stair-stepped back, a 2px thick tail, and two 1px yellow eyes.
- **[observed]** YukiCrimson's 32 px black cat (https://yukicrimson.itch.io/black-cat-sprite) separates overlapping legs and the tail with a near-black outline around a dark grey fill plus 1px lighter grey rim pixels on the back; legs are 1px columns with 1px gaps. Revouger's black cat (https://revouger.itch.io/black-cat) does the same with 3 to 4 greys and a near-black outline.
- **[derived]** For a pure single-colour black sprite, overlapping parts can only be separated by (a) a 1px gap of background between them, or (b) a 1px line of a slightly lighter dark (rim). Pose the cat so parts do not overlap where possible (side view, tail away from body).

## 3. Proportions consistency across frames

- Squash and stretch: "Mass... mass never changes." When you change the width, always change the height too, so mass stays constant. This is the most important rule of squash and stretch. (Saint11, Squash and Stretch: https://saint11.art/img/pixel-tutorials/Squash.gif)
- Idle: move down 1px then up 1px; the "character doesn't change mass". (Saint11, Character Idle: https://saint11.art/img/pixel-tutorials/characterIdle.gif)
- Quadruped walk: the distance travelled by front and back legs must match or the body looks like an accordion; make sure all details are consistent in every frame. (Slynyrd, Pixelblog 25 Motion Cycles: https://www.slynyrd.com/blog/2020/1/23/pixelblog-25-motion-cycles)
- Break the body into separate flat-colour shapes and animate one part at a time across all frames: legs first, then body, head, tail. (Slynyrd, Pixelblog 25)
- Block motion with a dummy sprite of solid-colour parts before detailing. (Slynyrd, Pixelblog 22: https://www.slynyrd.com/blog/2019/10/21/pixelblog-22-top-down-character-sprites)
- At small sizes the head usually takes a third to half of the sprite; realistic proportions at small size give a stick figure. (Slynyrd, Pixelblog 22)
- Cute proportions: big forehead, big eye sockets, big ears, wide head, short (under 4 heads), weight at the bottom "like a flour sack", rounded soft shapes. (Saint11, Cuteness)
- Keep track of clusters and avoid breaking them between frames. (Saint11, Fundamentals)
- In the fighting idle, "the initial pose is maintained" and everything is anchored to the steady motion of the torso. (Slynyrd, Pixelblog 52: https://www.slynyrd.com/blog/2024/9/26/pixelblog-52-idle-fighting-stance)
- **[derived]** At 32 px, 1px is about 3% of the body. Lock head width, ear height, eye ring size and eye spacing as fixed stamps that are moved, never redrawn. If a squash frame makes the body 1px shorter, make it 1px wider.

## 4. Drawing small eyes

- No reached source gives exact 5x5 to 8x8 eye templates. Lospec's tutorial tag pages for "eyes" and "circles" both list 0 tutorials (https://lospec.com/pixel-art-tutorials/tags/eyes, https://lospec.com/pixel-art-tutorials/tags/circles).
- Circle construction rule: longest segments at top, bottom, left, right, shortening toward the diagonals. (Sam Keddy, Lospec). Each step smaller until the corner, then larger. (Saint11, Fundamentals2)
- Odd diameter has one true centre pixel and is symmetric around it; even diameter has no centre pixel, the centre falls between pixels. (Donat Studios Pixel Circle Generator notes: https://donatstudios.com/PixelCircleGenerator)
- **[derived]** 1px ring ("O") eyes that follow those rules (`#` = eye colour, `.` = body):
  - 5x5: `.###.` / `#...#` x3 / `.###.` (segments 3, corner, 3; hole 3x3)
  - 6x6, 1px corner cut: `.####.` / `#....#` x4 / `.####.` (4, corner, 4; reads a bit square)
  - 6x6, 2px corner cut: `..##..` / `.#..#.` / `#....#` x2 / `.#..#.` / `..##..` (2-1-2; rounder but more diamond)
  - 7x7: `..###..` / `.#...#.` / `#.....#` x3 / `.#...#.` / `..###..` (3-1-3)
  - 8x8: `..####..` / `.#....#.` / `#......#` x4 / `.#....#.` / `..####..` (4-1-4)
  - Filled discs by the centre-in-circle rule: 5 = rows 3-5-5-5-3, 6 = 4-6-6-6-6-4, 7 = 3-5-7-7-7-5-3, 8 = 4-6-8-8-8-8-6-4.
- Shiny dark eyes give a very strong "puppy" effect. (Saint11, Cuteness)
- Move the contents of the face after the silhouette has moved; move the interior before or after the silhouette for subtle motion. (Saint11, Character Idle; Saint11, <1 Pixel Movement: https://saint11.art/img/pixel-tutorials/Subpixel.gif)
- **[derived]** Look-around: keep every ring pixel fixed and shift only the pupil 1px inside the hole. Odd rings (5, 7) suit a 1px or 3px centred pupil; even rings (6, 8) suit a 2x2 pupil. Keep 1px of gap between pupil and ring when possible or the ring reads as broken.
- Blink: shift the eye pixels down by about half the eye height (about 1px for tiny eyes); the fully closed frame is about 2px tall including both lids. (Fire Emblem Universe forum: https://feuniverse.us/t/tutorial-for-blinking-animations/2398)
- Blink drawings: open, closed, nearly open, open (order 1, 2, 3, 1); closed held 4 frames and nearly-open 2 frames at 24 fps (about 167 ms and 83 ms); eyes "close quickly for just an instant". (Clip Studio Tips: https://tips.clip-studio.com/en-us/articles/2643)
- A real blink lasts about 100 to 150 ms (UCL), or 100 to 400 ms (Harvard BioNumbers); adults blink about 17 times a minute, 4 to 5 when focused. (Wikipedia, Blinking: https://en.wikipedia.org/wiki/Blinking)
- One pixel tutorial blinks every 8 frames of 200 ms and says blinking every 4 frames looks too often and unnatural. (imonk, itch.io: https://itch.io/t/2489389/pixel-tutorial-hero-idle-animation)
- **[observed]** At 32 px, other artists draw much smaller eyes than an O ring: Slynyrd's mini cat 1x1 px yellow; Revouger 1x2 px (yellow over orange) about 3px apart; YukiCrimson 1 to 2 px yellow with a light pixel; Neko (oneko sheet, refs/oneko-neko-sprite-sheet-32px.gif) short 1px vertical dashes. Closed eyes in sleep frames are 1px dark lines (YukiCrimson) or short diagonal strokes (Neko).

## 5. Small-sprite walk cycles

- Quadruped walk = imagine 2 bipeds walking with a small time offset; make the head follow the front biped with a delay. (Saint11, Quadruped Walk/Trot: https://saint11.art/img/pixel-tutorials/4LegsWalk.gif, saved as refs/saint11-quadruped-walk-trot.gif)
- Leg contact order in his diagram: 1 back-right, 2 front-right, 3 back-left, 4 front-left ("can be mirrored"; "run uses a different order"). In his trot example a leg touches the ground every 2 frames; walking has a lower offset. (Saint11, 4LegsWalk)
- Each leg follows contact, drag, rise, forward. Back leg: thigh moves regularly, knee raises the foot, paw lags behind. Front leg: shoulder moves regularly, elbow moves fast on contact and release, paw snaps on release. (Saint11, 4LegsWalk)
- The back leg follows one step behind the front leg of the opposite side; animate one pair at a time. (Slynyrd, Pixelblog 25; its dog walk GIF is 8 frames at 100 ms each, measured from https://images.squarespace-cdn.com/content/v1/551a19f8e4b0e8322a93850a/1580347723121-2XCW5BLJQ9MUFKF6YY27/64-Dog_Walk_2.gif)
- Back pelvis and front shoulders move up and down with opposite but equal motion. (Slynyrd, Pixelblog 25)
- Real cats walk with a "pacing" gait, moving the two legs on one side together, and place each hind paw close to the track of the front paw; when trotting they switch to a diagonal gait. (Wikipedia, Cat: https://en.wikipedia.org/wiki/Cat). Adult cats use a four-beat gait. (Wikipedia, Cat anatomy: https://en.wikipedia.org/wiki/Cat_anatomy)
- Biped walk poses: contact, down, down+ (lowest), prepare passing, passing, up (highest). 12 frames = fluid (6 per leg); 6 frames = useful in low resolution (3 per leg). The leg on the ground always moves toward the back. (Saint11, Walk Cycle: https://saint11.art/img/pixel-tutorials/Walk.gif)
- Quadruped key poses: contact, up, down, passing; quadruped = two biped cycles offset in time. (Ulster University animation blog: https://blogs.ulster.ac.uk/daynke/?p=328)
- Small top-down sprites: walk 4 frames, run 8; the walk reuses run frames and plays slower. (Slynyrd, Pixelblog 22)
- Run cycles: contact and pass frames are the keyframes you never remove; 8 frames at 80 ms, 4 frames at 160 ms (slow playback down when you cut frames to keep the energy). (Slynyrd, Pixelblog 8: https://www.slynyrd.com/blog/2018/8/19/pixelblog-8-intro-to-animation)
- Body bob: stepping frames are 1px shorter than the standing frame. (Jason Perry, Walk Cycles Part 2: http://finalbossblues.com/walk-cycles-part-2/)
- At tiny scale every frame should move at least 1px; a full stride needs only a few frames. (Slynyrd, Pixelblog 47)
- **Neko's 2-frame cheat:** oneko.js uses 32x32 frames, 2 frames per direction for running, a frame update at most every 100 ms, and moves the cat 10 px per tick, so travel across the screen does most of the work. (oneko.js source: https://github.com/adryd325/oneko.js/blob/main/oneko.js). The X11 oneko default timer is 125000 microseconds (125 ms) and default speed 16 dots per move. (oneko man page: https://manpages.debian.org/wheezy/oneko/oneko.6.en.html)
- **[observed]** Neko's two run frames per direction are one stretched pose (legs reaching fore and aft) and one gathered pose (legs bunched under), a bound rather than a true walk. (refs/oneko-neko-sprite-sheet-32px.gif)
- Stardew Valley pets: 32x32 sprites, sheet of exactly 4 columns; rows are move down, right, up, left (4 frames each), then unique animations; frames 28 and 29 are the 2 sleep frames; every frame has its own millisecond Duration. (Stardew Valley Wiki, Modding:Pets: https://stardewvalleywiki.com/Modding:Pets)
- Commercial black-cat packs: Witchy Kitty idle 2 frames, walk 4 frames (https://nightspore.itch.io/witchy-kitty-platformer-sprite); YukiCrimson walk is 4 frames, its preview GIF runs at 100 ms per frame **[observed]**.

## 6. Idle breathing

- 2 frames: (1) move down 1px, bend knees; (2) move up 1px. 3 frames: the middle frame makes the fall slower and delays the face. 6 frames: add secondary motion (hair lag) and <1px tricks. (Saint11, Character Idle)
- Vertical movement alone is boring; have horizontal movement compensate the vertical. Move face contents after the silhouette moves. (Saint11, Character Idle)
- Use the idle to show personality: blink, yawn, look around, scratch. (Saint11, Character Idle)
- 2 frames: "not fancy but better than nothing, most suitable for small sprites". 4 frames: more life but "can become noisy if the sprite is too small". 8-frame cat example: "not all idle cycles need to be bouncy, any movement that adds life is fine". (Slynyrd, Idle Cycles poster in Pixelblog 8, saved as refs/slynyrd-idle-cycles-with-cat.gif)
- **[observed]** In that poster the dark cat's body never moves; only the tail sweeps from a raised curl down to flat on the ground and back over 8 frames; the GIF runs at 200 ms per frame.
- **[observed]** Revouger's sitting black cat idle (https://revouger.itch.io/black-cat) also keeps the body still and sweeps the tail; preview GIF frames are 150 and 200 ms.
- Reusing a 2-frame walk as the idle is a classic 8-bit memory saver. (Slynyrd, Pixelblog 8)
- <1px tricks: move part of the shape first; move light rather than shapes; the silhouette barely changes. (Saint11, Subpixel)
- Neko's idle is a single static frame; after more than 10 idle ticks there is a 1 in 200 chance per tick (about every 20 s by the code comment) of starting a sleep or scratch animation. (oneko.js source)
- Idle loop data from one tutorial: 2 keyframes plus 1 tween for a 4-frame base cycle, doubled to 8 frames so the blink lands every 8 frames; 200 ms per frame for turn-based games, 125 ms (16-frame cycle) for action games. (imonk, itch.io)
- Analysed Homestuck sprite idles: 3 to 6 frames at 80 to 200 ms. (https://homestuck.net/resources/art-studies/idle-animation-examination.html)
- Slynyrd's fighting idle: 8 frames, 100 ms for the 4 rising frames and 50 ms for the 4 falling frames; torso range 4px on a 48x92 sprite. (Slynyrd, Pixelblog 52)
- **[derived]** For a 32px cat: 1px back or chest rise, 2 to 4 frames, about 400 to 600 ms each, blink as a separate overlay every few seconds. No reached source states 400 to 600 ms for breathing; sourced idle frame times run 80 to 200 ms with frames held or doubled.

## 7. Squash and stretch, anticipation, hop

- Mass never changes: change width and height together. (Saint11, Squash)
- Anticipation: the preparation squashes the object in the opposite direction of the action. Stiff materials deform less. Stretching is a cheap way to smooth fast animations. His sequence: prepare (squash wide), jump (stretch along travel), brake, prepare, recover. (Saint11, Squash; poster GIF runs at 80 ms per frame)
- Jump phases: 1 anticipation (avoid on player-controlled characters), 2 going up (simple, does not loop), 3 invert (bridge frames when Y speed changes at the apex), 4 fall, 5 contact: "squash as much as you can on contact"; add dust. (Saint11, Jump: https://saint11.art/img/pixel-tutorials/Jump.gif; GIF at 80 ms per frame)
- Easing: nothing moves linearly; slow in/out; back in/out = anticipation and overshoot; sometimes skip the middle frame to make a movement stronger; spacing between drawings gives acceleration. (Saint11, Easing: https://saint11.art/img/pixel-tutorials/Easings.gif)
- Cute characters: extra bouncy, lots of squash and stretch, everything soft. (Saint11, Cuteness)
- Running cat: rear legs push off and pass through the front limbs; squash and stretch during the leap; front legs contact first on landing. (Ulster University animation blog)
- **[derived]** At 32 px a squash of 1 to 2 px is already strong; take 1px of height off and add 1px of width (or 2 and 2), keeping head and eyes as unchanged stamps that only shift.

## 8. How other artists draw cat parts

- **Whiskers [observed]:** Revouger: 1 to 2 px dark stubs poking just outside the head silhouette, about 2 per side (one at eye level, one at mouth level). Neko: 1px black lines. Slynyrd and YukiCrimson: no whiskers at all. A whisker of the same black as the body is invisible inside the silhouette; it only reads where it crosses background.
- **Tail [observed]:** Slynyrd mini cat 2px thick, a hook that curls up at the tip. YukiCrimson about 2px plus outline, drawn as a question-mark curl when standing and wrapped along the ground when sitting. Revouger 1 to 2 px tail that sweeps in the idle. **[derived]** Draw the curve with Saint11's step rule (shrinking then growing runs) so it does not read as a stick; a 2px core gives room for a rounded 1px-narrower tip.
- **Ears [observed]:** Slynyrd mini cat: 1px wide by 2px tall spikes with a notch between. YukiCrimson: 2px wide with a 1px pink inner pixel. Revouger: about 3px wide with lighter inner pixels. Most cats have straight triangular upright ears that move independently and lie back when frightened or playing. (Wikipedia, Cat anatomy). Pixels are square and sharp, use that for pointy edges. (Saint11, Outlines)
- **Sitting pose [observed]:** compact triangle: head at top front, back stepping down diagonally, tail wrapped along the ground or curled up (Slynyrd, YukiCrimson, Revouger).
- **Sleeping [observed]:** Neko sleeps curled into a rounded ball with ears visible and a "Z z" above; 2 frames. YukiCrimson's lying frame is a flat loaf with 1px closed-eye lines. Neko shows `tired` for 8 ticks, then swaps the 2 sleeping frames every 4 ticks (about 400 ms at 100 ms ticks), resetting after 192 ticks. (oneko.js source). Stardew uses 2 sleep frames (Modding:Pets). A cat loaf is the pose with paws and tail tucked under the body. (search summary of drawing pages, not a pixel source)
- **Yawn:** Saint11 lists yawn as a personality idle (Character Idle) but no reached source shows how to draw one at small size. Not found.
- **Peek behind an edge:** no reached source covers it. Not found.
- Cats usually sleep 12 to 16 hours a day. (Wikipedia, Cat)

## 9. Animation timing table (sourced numbers only)

| Animation | Frames | ms per frame | Source |
|---|---|---|---|
| Neko run (per direction) | 2 | update at most every 100 ms; 10 px travel per tick | oneko.js |
| Neko X11 timer default | n/a | 125 ms | oneko man page |
| Neko sleep | 2 | swap every 4 ticks (about 400 ms) after 8 ticks of `tired` | oneko.js |
| Neko scratch | 3 (self), 2 (wall) | runs 10 ticks | oneko.js |
| Neko random idle event | n/a | 1/200 chance per tick, about every 20 s | oneko.js |
| Quadruped trot poster | 16 GIF frames | 100 | Saint11 4LegsWalk (measured) |
| Dog walk | 8 | 100 | Slynyrd Pixelblog 25 GIF (measured) |
| Run cycle | 8 / 4 | 80 / 160 | Slynyrd Pixelblog 8 |
| Black cat walk preview | 4 | 100 | YukiCrimson GIF (measured) |
| Idle cycles poster incl. cat tail idle | 8 per idle | 200 | Slynyrd Pixelblog 8 GIF (measured) |
| Sitting cat tail idle | 29 GIF frames | 150 and 200 | Revouger GIF (measured) |
| Idle, turn-based / action | 8 / 16 | 200 / 125 | imonk, itch.io |
| Fighting idle | 8 | 100 rising, 50 falling | Slynyrd Pixelblog 52 |
| Sprite idles studied | 3 to 6 | 80 to 200 | homestuck.net study |
| Squash, jump posters | n/a | 80 | Saint11 Squash, Jump GIFs (measured) |
| Blink (real human) | n/a | 100 to 150 (up to 400) | Wikipedia, Blinking |
| Blink (2D animation) | open, closed, nearly open, open | closed about 167, nearly open about 83 | Clip Studio Tips (24 fps) |
| Blink frequency (pixel) | every 8 frames at 200 ms | about 1.6 s (author chose it) | imonk, itch.io |

Gaps: no reached source gives timing for a yawn or a react/startle. Neko's `alert` is a single frame shown for one tick (oneko.js).

---

## Sources

Reached and used:
- Saint11 tutorial index: https://saint11.art/blog/pixel-art-tutorials/ (posters 4LegsWalk, Walk, characterIdle, Squash, Jump, Silhouette, Outlines, Cuteness, Fundamentals, Fundamentals2, Subpixel, Easings, Shading, Portrait at https://saint11.art/img/pixel-tutorials/)
- Lospec tutorial index and tag pages: https://lospec.com/pixel-art-tutorials, /tags/lines, /tags/walkcycle, /tags/idle
- Sam Keddy, Pixel Art Outlines (Lospec): https://lospec.com/articles/pixel-art-outlines/
- Sam Keddy, Outlines Part 2 (Lospec): https://lospec.com/articles/pixel-art-outlines-part-2-using-color/
- cure, Pixel Art Tutorial (Pixel Joint): http://pixeljoint.com/forum/forum_posts.asp?TID=11299
- Derek Yu, Pixel Art Tutorial: https://www.derekyu.com/makegames/pixelart.html
- OpenGameArt lineart chapter 2: https://opengameart.org/content/chapter-2-lines-and-curves
- Slynyrd Pixelblog catalogue: https://www.slynyrd.com/pixelblog-catalogue
- Slynyrd Pixelblog 8, 22, 25, 47, 52 (URLs above)
- Jason Perry, Walk Cycles Part 2: http://finalbossblues.com/walk-cycles-part-2/
- oneko.js source: https://github.com/adryd325/oneko.js/blob/main/oneko.js
- oneko man page: https://manpages.debian.org/wheezy/oneko/oneko.6.en.html
- Wikipedia: Neko (software) https://en.wikipedia.org/wiki/Neko_(software), Cat, Cat anatomy, Blinking, Gait
- Stardew Valley Wiki, Modding:Pets: https://stardewvalleywiki.com/Modding:Pets
- itch.io black cat packs (preview images studied, not copied): https://yukicrimson.itch.io/black-cat-sprite, https://revouger.itch.io/black-cat, https://nightspore.itch.io/witchy-kitty-platformer-sprite, https://elthen.itch.io/2d-pixel-art-cat-sprites (32x32, no frame counts listed), https://delinear-te.itch.io/cat-animation-pack (32x32 grid, no frame counts listed)
- Brandon James Greer transcript: https://sozai.app/transcript/make-chrono-trigger-sprites-pixel-art/
- imonk idle tutorial: https://itch.io/t/2489389/pixel-tutorial-hero-idle-animation
- Homestuck idle study: https://homestuck.net/resources/art-studies/idle-animation-examination.html
- FE Universe blink thread: https://feuniverse.us/t/tutorial-for-blinking-animations/2398
- Clip Studio blink tips: https://tips.clip-studio.com/en-us/articles/2643
- Ulster animation blog: https://blogs.ulster.ac.uk/daynke/?p=328
- Donat Studios circle generator: https://donatstudios.com/PixelCircleGenerator

Could not be reached or gave no usable content:
- Saint11 Medium article "Working with Lines" (https://medium.com/pixel-grimoire/how-to-start-making-pixel-art-7-e504bfa4ddf2): HTTP 403.
- Saint11 "Cats", "Eyes" and Celeste-specific posts: no such posters found in the tutorial index.
- Derek Yu tumblr copy (makegames.tumblr.com): blocked by a browser check (the derekyu.com copy worked).
- Pixel Logic (Michael Azzi) product page https://michafrar.gumroad.com/l/pixel-logic: only the title loaded, no contents.
- MortMort "3 PixelArt Techniques/Common Mistakes (Doubles, Jaggies & Outline)" https://www.youtube.com/watch?v=gW1G_FLsuEs: title and channel confirmed, description is links only, no transcript.
- Brandon James Greer: only the Chrono Trigger transcript found; it has no animation or eye content.
- Slynyrd Pixelblog 20 (top-down sprites): the catalogue lists it as Pixelblog 22, which was used.
- Stardew cat art itself and Celeste sprite sizes: not checked in-game.

## Saved reference files (refs/)

| File | Shows | Source URL |
|---|---|---|
| saint11-quadruped-walk-trot.gif | Quadruped walk/trot, leg contact order, leg joint behaviour | https://saint11.art/img/pixel-tutorials/4LegsWalk.gif |
| saint11-line-fundamentals.gif | Regular vs irregular lines, curve step rule, bad corners, unintentional squares | https://saint11.art/img/pixel-tutorials/Fundamentals2.gif |
| saint11-character-idle.gif | 2, 3, 6 frame idles, face-after-silhouette, personality idles | https://saint11.art/img/pixel-tutorials/characterIdle.gif |
| slynyrd-idle-cycles-with-cat.gif | 2/4/6/8 frame idles incl. a tiny dark cat tail-only idle | https://images.squarespace-cdn.com/content/v1/551a19f8e4b0e8322a93850a/1536968690636-28JX8MYUIJRD5NZGAFKQ/13-Idle_Cycles.gif |
| oneko-neko-sprite-sheet-32px.gif | Classic Neko 32x32 sheet: 2-frame runs, sleep curl, scratch, alert | https://raw.githubusercontent.com/adryd325/oneko.js/main/oneko.gif |
| derekyu-jaggies-curves.png | Smooth curve vs a curve with one jaggy segment | https://www.derekyu.com/makegames/images/pixel/jaggy02.png |

All six checked with `file` (GIF 512x512 x3, GIF 768x768, GIF 256x128, PNG 576x224). `refs/sejal-reference-cat.png` was already in the folder and is not part of this download set.
