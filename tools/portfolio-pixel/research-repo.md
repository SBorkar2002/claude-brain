# Portfolio · Pixel · Repo research

17 Oct 2026. Source: `yihui-dev/awesome-opus5-5-videos`, shallow clone at HEAD `92aee2f`. All repo content was treated as data and nothing from it was run. Read alongside `PLAN.md` (same folder). Prior work: `~/Documents/career/portfolio-v2/research.md` and `prompt-scan/batch-1..4.md` (16 Oct).

Method: diffed slugs against the 16 Oct tables, then ran about 60 keyword patterns over all 703 prompts with a pixel / character / theme / nav / perf lens. That gave about 140 grep hits. About 75 of them were real matches, and those were read in full. The rest were false positives such as "walkable house", "interface" and "arcade physics".

---

## (a) What changed since 16 Oct

**Nothing.** HEAD is `2026-10-13 22:46 +0800`, "Remove 150 entries not made from a plain Opus 5.5 prompt (703 total)". The README's latest-update line is still 2026-10-12. There are 703 prompt files, and their slugs match the 703 rows in `prompt-scan/` exactly, with 0 added and 0 removed. A byte-level text diff isn't possible because the old scan kept no copies. But the newest commit predates the scan, so the scan read this same commit.

What *is* new is the lens. The 16 Oct scan scored prompts for the Design / Ship direction, so almost every pixel or character prompt was scored 0 or 1. They are re-rated below.

**Be honest about coverage.** This repo is a collection of videos, not websites. Only 15 of the 703 entries carry the `pixel` tag, and most of those are game launch posts with a one-line prompt and no technique. Only **two** prompt texts give real pixel-rendering rules, and they are word-for-word duplicates. **Zero** prompts cover any of these:
- sprite sheets
- dithering
- LED or dot-matrix panels
- eyes tracking a cursor on a web page
- scroll-choreographed characters
- site light/dark theming
- keyboard-first navigation
- a real command palette (⌘K only appears as one beat inside a video)
- `visibilitychange`, `IntersectionObserver` or `devicePixelRatio`

The character material is mostly behaviour lists and motion numbers borrowed from video prompts.

Correction to the 16 Oct "Pixel / LED" list: `tanabe-fragm-322001` is a tile mosaic, not LED. There are no LED prompts in the repo.

---

## (b) Relevant prompts

Look verdict: **OK** = neutral. **AVOID** = viral or branded look; take the technique only.

| id | what it is | concrete technique | gotchas it names | look |
|---|---|---|---|---|
| majidmanzarpour-927543 = zacxbt-944604 (identical text) | Pixel wizard casting a spell, loop | Canvas 2D. Offscreen 128x96 logical canvas, blitted at the largest integer factor that fits, centred. `imageSmoothingEnabled=false` plus CSS `image-rendering: pixelated`. Integer coords only. ~24-colour fixed palette. Sprite built procedurally from rects and pixel runs (~24x32). Pose is parametric (staff angle, arm, head tilt, robe sway), eased, then quantised to the grid each frame, so it reads as 8-12 fps at a 60 fps loop. State machine IDLE (2-frame bob) > CHARGE > CAST (1-2 px shake) > RECOVER. Fixed 60 Hz timestep + rAF render. Zero allocation in the loop. Pooled particles that step palette index (white > magic > dark) instead of fading alpha. 1 px rim light. | No sub-pixel, AA, gradients or shadowBlur. "Should look like a polished 16-bit sprite animation, not vector shapes scaled down." | **AVOID** the scene: night sky, moon, 1 px twinkling stars, purple/blue, spell sparks |
| twoclipping-041659 | 20s voiceover film made of 16x16 pixel objects | Each object is a 16x16 grid of hand-placed cells. **Bake each sprite once to an offscreen canvas**, then draw scaled. **Pixel morph:** pair every cell of A with a cell of B, glide position and colour, with a small random delay per cell. Nothing pops in: eased glides of about 0.5 s with a soft start. | A flood still retreating when the next scene starts reads as a hard cut. A fast ease-out flood reads as a jump, so use a soft start. A handoff is only smooth if A's last frame is B's first. | **AVOID** the twoclipping house style: off-white paper, black/red/yellow, Geist, grain, extruded 3D pixel blocks with contact shadow, block-cursor typed captions |
| heyiamnick-119558 | 30s reel: pencil > blueprint > hologram, box mascot | One geometry drawn in three "inks". **Mascot "is never a fourth colour"**: its outline and eyes recolour per ink. Run cycle: alternate leg pairs, **6 steps/s, 7° lean**. Critically damped spring `1-(1+wt)e^(-wt)`, w 12-40, never passes target. Empty border: nothing at rest within 150 px of the sides or 90 px of top/bottom. Scene change by hard-edge flood or a single scan line. | Banned: particles, glows, flares, shake, RGB split, crossfades, bouncy easing, holds over 0.5 s. (Prompt is truncated in the repo.) | **AVOID** the mascot: box body, stub arms, 4 straight legs, tall rounded-rect eyes. It reads as Claude Code's mascot. Also avoid the corner HUD labels ("FIG. 07", "BEAT 27 / 60") |
| jakubantowski-020905 | Felt blob mascot (one-line prompt) | Behaviour list: breathing, blinking, squash & stretch, a **lagging beret** (secondary motion), a **subtle** reaction to the mouse | none | OK (3D felt, not ours). The behaviour list is our idle spec |
| leowenai-125931 | LongCat launch film (post only, no prompt) | **Cat's eyes are the visual anchor:** they watch you type, blink on the beat, squint, glance at things, then land on the logo at the end | none | **AVOID** the halftone-xerox look. Closest precedent to "eyes are the character" |
| flxrnc-251921 | 14s UI loop that opens on "pixel mascot idles" | Shape spring: damping 0.72, settle 0.35 s. Camera spring: damping 1.0, settle 0.6 s. Content swap: 12 px blur + fade over 0.15 s. `renderAt(t)` is pure: no `Math.random`, no clock, no carried state; `?t=` freezes a frame. Loop wrap `t - P*floor(t/P)`. Cursor under 65 px/frame, aimed at where the target will land. | "Do not cross-fade orange into ink." Start draw-on after blur-in. | **AVOID** the mascot squashing into a play button and morphing through UI states and back (the one-shape template) |
| flxrnc-619627 | Claude mascot directs a cat's film | "A slow blink straight into the lens" | none | **AVOID** Claude-mascot plus tuxedo-cat framing. The slow blink is worth stealing |
| notdwd-766641 | 12-frame bouncing-ball filmstrip | **Squash on contact, stretch mid-air, real arcs.** "Arrive fast, land soft": cover **12-19% of the remaining distance per frame** (30 fps). Stagger 2-4 frames. Nothing freezes (slow push on holds). Blur only on fast moves. Big and readable on a phone. | QA: 5 stills, a harsh critique, fix the 3 worst problems, then render | **AVOID** the off-white/ink/orange "every frame is code" look |
| iamtanzil-120030 | E-bike hero (React) with a cursor x-ray lens | `mask-image` radial gradient: radius 165, feather 45, inner 120, `.12s linear`. Coords relative to the section rect. Word stagger 0.6 s `cubic-bezier(.16,1,.3,1)`, 0.08 s step. **`prefers-reduced-motion: reduce` gives `animation: none`** | Inverted mask logic. An eased or longer mask transition feels laggy. Scope fonts and resets to the component. | OK |
| acoramaa-248467 | Audio-reactive mechanical eye | In the breakdown the eye **closes and goes quiet, "like it's thinking"**, then blows open on the drop | none | 3D mech look, n/a. Closed eyes read as thinking or resting |
| doubleunplussed-181894 | AI-lore music video with character notes | User notes: the mouth wobbling with lyrics "is just jittery", so drop fake lip-sync and give the character an expression per scene. Shock-pose arms read as mistakes. | Fake mouth motion reads as a bug | OK. Supports the faceless cat: no mouth means no jitter |
| 0xnicc0-516612 | One-shape UI morph | "A caret that **blinks only when idle**" | none | template (AVOID) |
| techhalla-498547 | Kinetic bumper | Micro-breath on the hold: scale 1.000 > 1.012 > 1.000 | none | For pixel art, do **not** scale. Do a 1 px bob instead (see c) |
| froessell-562325 | Arcade chase-game PRD (3D) | **Hit stop 50-100 ms.** Tiny shake on light hits, strong short shake on heavy. "Don't overdo continuous shaking." Object pooling; mobile perf considered from day one. | none | n/a |
| hahazwei-425483 | Perler-bead pixel music video (Chinese) | Every pixel is a bead with a hole, ironed into a sticker with a white border. Graph-paper background, pink/white check floor. Motion cut to the beat. | none | OK, not an Opus template. A "hand-made pixels" material, for /art only |
| zeezomb-726206, nischalsharma-587738 | Loose gold-leaf mosaic | Tiles lift, flip, fly and click back. Figures are flocks of tiles ("a fish swims by its tiles swimming"). | none | **AVOID** gold-leaf. The tile-flip transition is usable |
| tanabe-fragm-322001 | 190k-tile mosaic ad (Japanese) | Tiles that will become text start in the **surrounding background colour (filled outside-in)** and flip to reveal, otherwise the letterforms show early. A stop must zero its velocity or interpolation overshoot flips it. | as stated | OK |
| brainextends-606193 | Spotify film | **Pastels (lavender, powder cyan, blush, champagne gold, mint) live only in the hero artwork** on a near-black stage. UI stays white/grey plus one accent. Critically damped, "no repeated bouncing". **Outgoing titles leave before incoming ones occupy the space.** | Keep stationary text and art sharp | Spotify look n/a. Evidence that pastel-on-dark works when the pastels are content |
| ik-builds-585923 | Product-film template | **"Dark mode = charcoal matching the palette"** (not #000). Hard light/dark switches. Squash/stretch, overlap, onion skin, smear, follow-through. One primary move per transition. | No animator jargon on screen | paper/marker look n/a |
| annacher-433425, thegrootdev-966114 | UI morph promos (⌘K appears as one beat) | **Two edges on different springs**, so the leading edge stretches ahead (tab indicator, toggle knob). Drags are direct manipulation; on release, spring from the release position and velocity. Outgoing and incoming content get separate timing so labels never overlap. | **No `will-change` on anything that gets scaled** (text blurs) | **AVOID** the morph template. No keyboard-UX guidance at all |
| aichrislee-476025 (and 5 siblings) | Exploding watch/engine | "When I hover a part, it **lights up and shows one line** on what it does" | none | **AVOID** the exploded-object template. Hover-light plus one line = our "inspect" beat |
| theparuchh-013286 | WebGPU watch that disassembles on scroll | Scroll drives the big change **while the idle loop keeps running** | none | **AVOID** scroll-explode |
| ercankeskinx-897906 | "Build 5 completely different scroll-based sections" | Ideation prompt | none | use it to generate peek/perch variants |
| koushikde-937635 | Self-filling résumé reel | "A dot grid ripples and resolves into a pixel mascot"; the mascot ends in the photo box. "No corner labels, no fake HUD numbers." | none | **AVOID** pixel mascot in a résumé reel with an orange accent |
| gkxspace-923139 | 16-bit spell + chiptune (truncated) | Role line: "pixel animator and game feel designer". Bar: "hand-drawn character animation from a top-tier 16-bit era studio, not scaled-down vector graphics" | none | **AVOID** spell/chiptune |
| 0xcodez-474136, kopert0x-098349, blitast-studio-257328, smallhusk-272056, mandelduck-768972 | Cats: piano cat, robot + black cat, moonlit canal stroll, pettable cats, cats in Starry Night | One timeline drives paws and notes. Whole game ~200 KB with procedural art and audio. Claude chose to add pettable cats. | none | **AVOID** "black cat under the moon" |
| codrops-340299 | "Insert Coin" retro arcade room | 3D arcade, games credited to their makers | none | **AVOID** the arcade-cabinet / insert-coin portfolio metaphor (high-profile Codrops demo) |
| johnsavage-ai-427263 | Retro launch with grain + CRT | none | none | **AVOID** CRT scanlines and grain as default pixel dressing |
| 0xpai-eth-635565, agentgamesbot-355554, aisongman-461057, dmowlin-221566, mozetech-471882, rehan-shei-839416, waseemkhalo-636267, tonnusos-006126, opener-ai-843891, izmaelmag-282849, hoyoyoda-543147, pluginplay-472343, xodud-rkd-160324, sadalbert10-856416, 0xevinho-436195 | Pixel game or pixel video posts | One-liners or launch posts, **no technique** | none | nothing to extract |

---

## (c) Techniques worth adopting, mapped to PLAN.md cat states

**Sprite pipeline**
1. Author frames as palette-indexed grids (matches PLAN). **Bake each frame once into an offscreen canvas** at native size, then `drawImage` from the cache, never redrawing pixel-by-pixel per frame (twoclipping-041659).
2. Every pixel comes from one fixed palette (majidmanzarpour-927543 used ~24 colours). Light/dark = swap the palette table and re-bake. Effects step **palette index**, never alpha (majid's particles go white > magic > dark).
3. Animate pose parameters smoothly, then **quantise to the grid every frame**, so motion reads at 8-12 fps while rAF runs at 60 (majid). Pupil offset quantised to -1/0/+1 (already in PLAN) is the same rule.

**Idle (breath, blink, eye drift)**
4. Breath is a **2-frame, 1-logical-px bob** (majid IDLE), not the 1.2% scale breath from techhalla-498547. Scaling a sprite breaks the grid.
5. **Blink only when idle**, never mid-walk or mid-hop (0xnicc0-516612). Add a slow blink when petted (flxrnc-619627).
6. Eyes do the acting: watch, blink, squint, glance, then **land on the target** (leowenai-125931). Closed eyes = thinking or asleep (acoramaa-248467). No mouth movement anywhere; fake mouth motion read as jitter (doubleunplussed-181894). The yawn should open the silhouette, not draw a mouth.

**Walk, hop, settle**
7. Walk at about **6 steps/s** (heyiamnick-119558). Fold the 7° lean into the frames as a 1 px head-forward offset. **No rotation** (standing no-tilt rule).
8. Hop/pet: anticipation squash, stretch in the air, real arc, **squash on landing** (notdwd-766641). Then a **50-100 ms hit stop** (froessell-562325). Shake the **cat by 1 px only, never the page** (majid's 1-2 px CAST shake; "don't overdo continuous shaking").
9. Approaching a perch: "arrive fast, land soft", covering **12-19% of the remaining distance per frame** (notdwd), or a critically damped spring with w 12-40 (heyiamnick). For a springier character use damping **0.72 / settle 0.35 s**; for anything camera-like use **1.0 / 0.6 s** (flxrnc-251921). Overshoot under 2% (daniel-haida-636937 in the old scan). Always quantise the output.
10. Secondary motion: the **tail lags the body by 1-2 frames** (jakubantowski-020905's lagging beret). On start/stop, the front of the body leads and the back trails, using two-edge springs (annacher-433425 tab indicator).

**Perches, peek, inspect**
11. Nothing at rest inside a margin band (heyiamnick: 150 px sides / 90 px top and bottom) means perches go in gutters only. **Outgoing leaves before incoming occupies the space** (brainextends-606193, thegrootdev-966114), so the cat vacates a perch before that section's content animates.
12. Inspect beat: the project tile **lights up and shows one line** (aichrislee family) while the cat sits beside it and its pupils land on the title. Optional: a triggered (not cursor-following) x-ray lens over a project image to reveal the wireframe under the final. Numbers from iamtanzil-120030: radius 165, feather 45, `.12s linear`, coords relative to the section rect.
13. Scroll can drive *where* the cat is while its idle loop keeps running (theparuchh-013286). To ideate peek variants, reuse ercankeskinx-897906's "5 completely different" framing.

**Theme (light/dark, pastel)**
14. Same geometry, different ink; **the mascot never becomes an extra colour**. It takes the current ink (heyiamnick). This matches PLAN (black cat in light mode, white in dark), with the yellow eyes as the constant identity carrier.
15. Dark mode = **charcoal matched to the palette**, not #000 (ik-builds-585923). Keep pastels as content/art colours with **one functional accent** for UI state (brainextends-606193).
16. Never crossfade an accent into ink; **hard-swap** (flxrnc-251921). If the theme switch gets a transition, a **tile flip** works (zeezomb-726206), with tanabe-fragm-322001's rule: anything that becomes text starts in the background colour so letterforms don't leak early.

**Engine and QA**
17. Write the cat as `renderAt(state, t)`, a pure function of time: no `Math.random` (use a seeded hash), no carried state, `?t=` to freeze (flxrnc-251921, 0xkarmi-129839). That makes pause/resume, reduced-motion stills and screenshot QA trivial. Wrap loops with `t - P*floor(t/P)`, and seam-check frame 0 against frame P.
18. QA loop from the repo: stills of every state, a harsh critique, fix the 3 worst, repeat (notdwd-766641). Brief the build as a sectioned prompt that ends with "show me the state list before code" (flxrnc-251921, thegrootdev-966114).
19. Optional pixel morph between states or tiles: pair cells A > B and glide position and colour with a per-cell delay (twoclipping-041659). Use it once at most; it is a signature move of that author.

---

## (d) Templates and looks to avoid

| Look | Where | Why it matters for us |
|---|---|---|
| Box mascot: rectangular body, stub arms, straight legs, tall rounded-rect eyes, orange | heyiamnick-119558, flxrnc-251921 ("pixel mascot"), koushikde-937635, rishit30g-568278, daniel-mac8-306214, fanfulladev-063524, flxrnc-619627 | A pixel critter with simple eyes on a dark page invites "is that Claude Code's mascot?". The cat must read as a cat in silhouette at a glance (ears, tail, cat posture) with **round** yellow eyes. No orange anywhere near it. |
| Pixel wizard night scene: purple/blue sky, moon, 1 px twinkling stars, sparkle particles, chiptune | majidmanzarpour-927543, zacxbt-944604, gkxspace-923139 | Dark + pastel + pixel slides into this by default. No starfield, no moon, no sparkle bursts. |
| Black cat under the moon / at night | 0xcodez-474136, kopert0x-098349, blitast-studio-257328 | A yellow-eyed cat on dark is one step away. Give the dark theme a non-night identity (it's a UI theme, not a night scene). |
| Mascot morphs into UI (play button > loader > ... > ⌘K > toast > back) | flxrnc-251921, morse / demonugc / sanjeevn72 / annacher / thegrootdev family | The cat must never become a control, and the command palette must not be presented as a morph beat. |
| twoclipping house style | twoclipping-041659 and siblings | Extruded 3D pixel blocks with contact shadows, off-white paper, block-cursor typed captions, Geist, grain. |
| Halftone dot field / "0 keyframes" end card, halftone xerox | rossaxbt-707651, threeaus-886343, leowenai-125931 | Dot grids are tempting on a pixel site. Keep any dot motif out of hero and end positions. |
| Arcade cabinet / insert coin / CRT scanlines + grain | codrops-340299, johnsavage-ai-427263 | The obvious "retro" dressing. Reads as game dev, which PLAN already warns against. |
| Corner HUD labels, fake counters | heyiamnick-119558 (FIG./BEAT), banned in koushikde-937635 | Pixel UIs invite HUD chrome. Only real, useful labels. |
| Off-white + black + one orange + Geist + cursor clicking a toggle | rossaxbt-707651 and others (see 16 Oct research §1) | Still the master template to avoid. |

---

## (e) Pixel crispness, performance, reduced motion

**From the repo (with source)**
1. Fixed logical resolution in an offscreen canvas, blitted at the **largest integer factor that fits**, centred (majidmanzarpour-927543).
2. `ctx.imageSmoothingEnabled = false` plus CSS `image-rendering: pixelated` (majid).
3. All drawing on **integer coordinates** of the logical canvas: no sub-pixel positions, anti-aliasing, gradients or `shadowBlur` (majid).
4. Fixed palette; every pixel from it; fades by palette step, not alpha (majid).
5. Bake sprites once offscreen and draw from the cache (twoclipping-041659).
6. **No `will-change` on anything that is scaled**, or text and edges blur (annacher-433425, thegrootdev-966114).
7. Keep stationary text and art sharp; motion blur only on fast moves (brainextends-606193, notdwd-766641). On a pixel sprite that means no blur at all.
8. **Fixed 60 Hz timestep update with rAF rendering, zero allocation inside the loop, pooled particles** (majid). One elapsed-time clock driven by rAF (tanabe-fragm-706979).
9. Pure function of time; no clock reads inside draw (flxrnc-251921, 0xkarmi-129839).
10. Targets: "60 fps on a normal laptop and no console errors" (godsboy7777-150194). "Stable 60 FPS on an average laptop" (niegramotny-197521). Whole game ~200 KB with code-generated art and audio (blitast-studio-257328). <250 KB budget (gandamu-ml-124280). Mobile perf and object pooling from day one (froessell-562325).
11. Reduced motion: **one instance in 703 prompts**. iamtanzil-120030 uses `@media (prefers-reduced-motion: reduce) { .wpu-word { animation: none; } }`. (rossaxbt-707651's "Reduce Motion" toggle is a visual gag, not a rule.)

**Not in the repo: gaps to fill from platform practice (flagged, not sourced)**
- **devicePixelRatio (this affects PLAN's "CSS-scaled by an integer factor").** On DPR 1.25, 1.5 or 2.625 screens, an integer *CSS* scale is a non-integer *device* scale, so pixels come out uneven. Compute the factor in device pixels: `k = max(1, floor(targetCssSize * dpr / spriteSize))`, then set `canvas.width = spriteW * k` and CSS width = `spriteW * k / dpr` px. Snap the canvas element's position to device pixels too (`Math.round(x * dpr) / dpr`), and never apply fractional `transform: scale()` to it. Re-run on `matchMedia('(resolution: Xdppx)')` change (zoom, moving to another monitor).
- **visibilitychange:** cancel rAF when hidden. On resume, reset the fixed-timestep accumulator and clamp dt (e.g. 100 ms), or the loop tries to catch up on minutes of missed steps.
- **IntersectionObserver:** none in the repo. PLAN's perch director is original work. Also stop rAF when the cat's canvas is off-screen.
- **prefers-reduced-motion:** listen with `matchMedia(...).addEventListener('change')`. With a pure `renderAt(t)` the reduced state is just one held frame (seated, eyes open) with no travel between perches.
- **Mobile:** no repo guidance beyond "pool and test on device early". PLAN already covers tap-to-pet and no cursor tracking.
