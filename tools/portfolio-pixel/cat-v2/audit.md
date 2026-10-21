# Cat v1 audit (the cat now in Figma, component set 8:159)

17 Oct 2026. Source: `cat/sprites.py` (32x32, 35 frames). Checked frame by frame at 1x and 6x in both colourways, against Sejal's reference (`refs/sejal-reference-cat.png`). The Figma sprite sheets (12:246, 12:558) match the source exactly, so every finding below is in Figma too.

Her verdict was "cute at some places, distorted at some places". Both halves are true, and they come from different causes.

## What is cute (keep it)

- Big round eyes with a black fill and a highlight, sitting low in a big head. This is the whole charm and it holds up at 1x.
- A front-facing head on a side-on body, the way her reference does it.
- The ear notches and the flat top of the head. Her reference head is boxy too.
- Blink timing (0.15 s) and the hold lengths on the sitting frames.

## Where it is distorted, and why

Root cause first: **the canvas is too small for the eye she asked for.** A ring and a fill that can move around inside it needs at least a 7 to 8 px eye. At 32 px the eye is 6 px, so the fill is a 4x4 square that has nowhere to go. Most of the distortions follow from that, or from shapes drawn with rules instead of placed by hand.

### Everywhere

| # | Where | What you see | Why it happens |
|---|---|---|---|
| G1 | Look 1 to 6, Inspect 1, 2, 4, Idle 3, Peek 4, 5 | The eye goes lopsided, like a D: yellow 2 px thick on one side, 1 px on the other, with a small square in the corner | 6 px eye, so the 4x4 fill can only move by shrinking to 3x3 and pushing into a corner. The fill stops being round and the ring changes thickness |
| G2 | Look 3 (up), Look 4 (down) | Reads as a half-shut squint, not a look | The fill becomes 4 wide x 3 tall with a flat top or bottom |
| G3 | All open eyes | The "O" looks like a rounded square | Inside a 6 px pixel circle, the fill is a 4x4 square. The ring has four flat sides 4 px long and only one pixel cut at each corner |
| G4 | All open eyes | The top-left of the ring looks like it has a bright notch | The 1 px white highlight sits in the fill's corner, touching the ring on two sides |
| G5 | Idle 1 to 4, Walk 1 to 4 | Whiskers fuse into the back | The lower left whisker sits on the same row as the top of the back (row 15). The upper one floats 2 px above |

### Standing and walking (Idle, Walk)

| # | Frame | What you see | Why |
|---|---|---|---|
| S1 | Idle 1 to 4, Walk 1 to 4 | The head looks glued onto the front corner, and the cat looks like it would tip forward | Head spans cols 13 to 28, body cols 3 to 19. 9 of the 16 head columns hang past the chest with nothing under them, and both front legs (cols 14 to 15, 18 to 19) sit under the back half of the head. In her reference the front legs stand under the head |
| S2 | same | A stair-step "jaw" under the face | Rows 16 to 17 run out to col 28 under the head as a 2 px shelf, then the chest steps back to col 19 |
| S3 | same | The tail is a flagpole with a spear tip | A straight 3 px column (rows 7 to 15) topped by 1 px then 3 px, so the tip is pointed. Her reference tail is thick, bends slightly back, and has a round club tip |
| S4 | Walk 2, Walk 4 | The cat flickers between 4 thin legs and 2 fat ones | Legs at cols 5 to 6 and 7 to 8 (and 15 to 16, 17 to 18) touch, so each pair merges into one 4 px pillar. At 8 fps this is the strongest "distorted" read in the set |
| S5 | Walk 1, Walk 3 | Jagged leg diagonals, and the legs do the splits | Leg slants come from rounding a straight line, so the steps are uneven (runs of 2, 3, 2). Both outer legs splay out at once, so it reads as a scissor or jumping jack, not a gait |
| S6 | Walk 2, Walk 4 | A kink in the tail | The tail sway moves only its top 4 rows, so the tail breaks at row 9 |
| S7 | Idle 2 | A hump grows on the back, joined to a whisker | The breath adds an 8 px bump at row 15, on the same row as the whisker |

### Sitting (Sit, Look, Inspect, Yawn, React 1 and 3)

| # | Frame | What you see | Why |
|---|---|---|---|
| T1 | all sitting frames | A tombstone or bottle with eyes | Head and body are both 16 px wide with a 1 px neck notch, so the pose is one straight-sided slab. A sitting cat is a pear: a narrow chest under the cheeks, wider haunches, front legs between them |
| T2 | same | The tail is a mug handle | A 2 px stick parallel to a straight body side with an even 1 px gap, and a spear tip again |
| T3 | Sit 2 | The cat puffs up rather than breathing | The breath widens the body by 1 px each side (16 to 18 px, +12 %) and drops the head into it |
| T4 | Inspect 1 to 4 | Looks exactly like Look | Same pose and same eyes. No lean, no paw, nothing that says "studying something" |

### Yawn (the frame she called weird)

| # | Frame | What you see | Why |
|---|---|---|---|
| Y1 | Yawn 2, 4 | A pink nose appears | The "small mouth" is a 2x2 pink square at the centre of the face |
| Y2 | Yawn 3 | The squeezed eyes are scribbles | The > and < are 2 px dashes stepped 2 px apart, so the line breaks. At 1x they read as "= <" |
| Y3 | Yawn 3 | A muzzle or snout, and the head changes shape | The 6x4 pink block sits exactly between the two whisker rows, so the whiskers frame it like a snout. Two extra chin rows turn the head into a shield |
| Y4 | Yawn 1 to 4 | Nothing yawns except the face | A real yawn stretches the whole body: it rises, the ears go back, the eyes squeeze. Here only the face changes, plus a 1 px head lift |
| Y5 | Yawn 1 | Sunglasses | The half-shut eye is a 6 px bar, 1 px sides and a 4 px bottom: a rectangle |

### Sleep

| # | Frame | What you see | Why |
|---|---|---|---|
| L1 | Sleep 1, 2 | A slipper with a smile | The head merges into the right end of the loaf with no contour between them, and the closed eyes sit on the bottom edge |
| L2 | Sleep 1, 2 | Noise at the tail | The wrapped tail leaves a 1 px hole (row 27, col 3) and a 1 px spur |
| L3 | Sleep 1, 2 | A jagged comb on the right edge | Whiskers on rows 25 and 27 fuse with the body edge |
| L4 | Sleep 1 to 2 | Two Zs flicker | The Z jumps 7 px and changes size (5 to 6 px) every frame |

### React

| # | Frame | What you see | Why |
|---|---|---|---|
| R1 | React 1 | Shelves across the body | The whiskers fuse into the widened body on rows 15 and 17 |
| R2 | React 2 | A different, thinner cat, cramped at the top | The body shrinks to 14 px wide, the ears touch row 1 and the heart touches row 0, so cat and heart press against the top of the frame |
| R3 | React 2 | The heart reads as a pink plus or a flower | A 5x4 heart has 1 px lobes |

### Peek

| # | Frame | What you see | Why |
|---|---|---|---|
| P1 | Peek 1 to 3 | Cropping, not peeking | The "edge" is just the bottom of the frame: no paws on it, nothing holding on. Peek 1 is two dots |
| P2 | Peek 4, 5 | Lopsided eyes again | G1 |

## Fix plan for v2 (each fix maps to a finding)

1. Move to a **48 px canvas** so the eye can be 8 px (G1 to G4). Fill at rest is the whole 6x6 rounded inside, so the ring is a clean 1 px O like her reference. To look, the fill narrows by 1 px on the axis it moves along (5x6 for left and right, 6x5 for up and down, 5x5 for diagonals) and shifts. It stays round, and the ring never breaks or touches the fill's edge. A narrower pupil is also how a real eyeball looks when it turns.
2. Proportions measured from her reference, then fixed for every frame: head 22x19, eyes 8 px with a 2 px gap, legs 3 px wide and 10 rows long, body 35 px long with the front legs under the head (S1, S2).
3. Draw every shape by hand as an ASCII grid: tail, ears, cheeks, sitting body, loaf. Only feet positions are computed, and leg slants use clean even steps (S3, S5, S6, T1, T2, L1, L2).
4. Legs in a pair are either fully overlapped or at least 1 px apart, never touching (S4). The walk follows a real gait (front and back pairs a quarter cycle apart, far feet 1 px higher, body 1 px higher when the legs pass).
5. Whiskers: the far-side pair sits inside the body silhouette (black on black, so it disappears, as it would in life). Near-side whiskers only stick out into empty space (G5, R1, L3).
6. Breath = the back line rises 1 px (standing) or the head and chest rise 1 px (sitting). Widths never change (S7, T3).
7. Yawn as a whole-body action: sleepy eyes, then a small mouth, then a big yawn (body stretches 1 px, ears flatten, eyes squeezed as clean > <, a tall rounded mouth below the eyes and clear of the whisker rows), then the mouth closes and two eyes come back (Y1 to Y5).
8. Inspect gets its own pose: lean toward the artwork, one paw lifted, a squint, then an "oh" (T4).
9. React keeps one cat: the same body squashes 1 px, hops, and lands, with a 7x6 heart well clear of the top edge (R1 to R3).
10. Peek gets paws on the edge (P1). Sleep gets a separate head on the loaf, a clean tail wrap and one Z that drifts up and fades (L1 to L4).
