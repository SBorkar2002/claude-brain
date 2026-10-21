---
name: project-cat-v2
description: "Portfolio mascot Cat v2 (17 Oct 2026): 48px redraw in portfolio-pixel/cat-v2, Figma node ids, key craft decisions, swap-in caveats; all cat tweaks go to the dedicated cat session"
metadata:
  node_type: memory
  type: project
  originSessionId: eab77dde-6d76-4120-a90f-08a1b9dd1370
  modified: 2026-10-17T12:29:15.612Z
---

Cat v2 = redraw of the pixel-portfolio mascot after Sejal said v1 was "cute at some places, distorted at some places". Built by a dedicated cat session; she wants every future cat tweak routed to that cat agent, not the main portfolio session. APPROVED + LIVE 17 Oct: v2 art swapped into the live Cat set 8:159 (63 variants, 144px, moved to x6960 y2100); instances re-seated (up 24 / peek up 16 / left 8); v1 sprite sheets + comparison v1 cells detached as archives; 31:706 / 34:731 / 34:709 are superseded staging. Future cat edits go into 8:159.

**Where:** source ~/Documents/career/portfolio-pixel/cat-v2/ (sprites.py ASCII stamps + TIMINGS, render.py, runs.py, audit.md, research.md, README.md with swap steps). Figma hfj2locm0N5bssdEU6NaoH: comparison 35:564, v2 playground 34:731, component set "Cat v2" 31:706 (58 variants, 144x144 = 48px at 3px; moved to x6960 y2100 because main session's asset frames sit at x>=9720), walk lane 34:709. Motion review page: https://claude.ai/artifact/V49VCbcdBkAtMHav3f29yx (built from cat-v2/motion.template.html).

**Decisions that are not obvious from the code:**
- Root cause of v1 distortion: 32px canvas forces a 6px eye whose 4x4 fill can only shrink into a corner when looking. v2 = 48px canvas so the eye is an 8px ring; looking narrows the fill by 1px on the move axis (5x6 / 6x5 / 5x5) and slides it, ring never breaks.
- Yawn: tested side by side; "> o <" reads as a scream, flat shut eyes + tall narrow mouth reads as a yawn. Small mouth 2x3 (a 4x4 rounded mouth reads as a nose, v1's problem).
- Peek paws beside the face (paws carved over the chin read as teeth).
- Round 3 (her motion review): yawn mouth = small V + 2 white fangs (tall pink oval read as VULGAR, wide pink = lips); sitting base solid, no limb gaps; Inspect = side-view pounce crouch + butt wiggle; walk legs each on own hip (no shared-hip downward V); NEW Fall = page-load loop, mid-air landing pose (legs ~30 deg, tail straight up) spinning 360 around the vertical axis via 8 turnaround drawings (never in-plane rotation); NEW Land = plop on the hero divider then Sit; React hop reuses the mid-air pose. Look + Sleep approved as-is.
- Round 4: Land = 7 frames with a beat (land, stunned hold, blink, stand on 4 legs, lower, sit; ~1.5s); Inspect pounce crouch = paws stretched AHEAD of the face, tail UP, hind paws gathered + treading in the wiggle (her rule; sources only say low, coiled, tail twitch); walk = diagonal pairs (she expects opposite limbs together); Peek = pop, 2px overshoot, dip, settle, slow looks; React hop = legs straight down (she disliked splayed hind legs; splay stays only in the approved Fall spin). Approved as-is: Fall spin, Yawn, Peek pose.
- Round 5 (from her 2 reference walk GIFs): one-colour silhouette made diagonal pairs read as jumping jacks -> added variable cat/body-far (VariableID:75:817, Dark #BEB7D2 / Light #423B54) for far legs; hind legs = 8px thigh growing out of the rump (no notch) tapering to 5px, front legs thinner; Land = bent down on all fours to recover, then ONE sit (she disliked 'sitting twice'); load demo = ease-in page rise + spin ends facing front 0.3s before touchdown (ease-out felt like time stopped).
- Body direction (her words 17 Oct): "fuller, fluffier, not skinny... not a fat cat, a normal looking, kinda squishy cat". So: round rump bulging behind a plump tail (5px shaft, 6px tip), 5px legs with heel-cut paws, 26px soft-pear sit with convex shoulders, rounder loaf, React squash 2 rows shorter / 2px wider each side. Head stays 22px so it never tips into fat.
- Legs: pairs either fully overlapped or >=1px apart (5px legs step +3/-3); squash frames widen (mass conserved), breathing never changes width.

- Round 6 (19 Oct, her refined reference inventory/refs/cat-reference.webp): no whiskers; lilac 'f' line where the body touches the head (distinct head/body); yellow 'Y' marks for yawn + react (heart dropped); sleep z then z+Z; landing rebuilt on the standing front body (reach, compress, low recover, rise, one sit). Site reads cat-v2/preview/frames.json via my-portfolio/scripts/export-cat-frames.mjs (legend # f Y p w m M z h); its STATES list lacked Fall.

- Round 7 (19 Oct, her direct notes): KEEP whiskers; NO lilac neck/head-separation line (she hated it: 'not what I want at all'); standing pose measured from the reference: head on front-top of a box body jutting ~8px past the chest (chin overhang), legs: white near-hind at the very back, lilac far-hind ahead, white near-front under the head's back half, lilac far-front under the chest; Look = standing pose; Inspect = low stalking crouch (not the pounce). Yawn/Sleep/Peek approved, do not change.
- Rounds 8-10 (19-20 Oct, via code chat): Run, Pounce, Sphinx/SphinxTap (tail = raised curl), baked ground shadow 's', top-light 'l'. Collar: belt = key 'g' mapped to CTA lime #d9f860 (--accent-lime), bell = eye yellow 'Y', centred on the neck, belt wraps the full neck in every head bob or turn frame. Live on main in commit 4aeb0b6. Figma 8:159 NOT updated since round 7.
- Wardrobe (20 Oct): hat/tie/glasses/bow overlays via sprites.ACC + wear() hooks in every head drawer; accessories.py rebuilds all frames per accessory and keeps the diff, so overlays follow mirrors/rotations/flips for free. Keys H #5B3DD0, b #A78BFA, k = opposite of body (glasses), bow h + M knot. Hat brim 12 wide and bow beside right ear leave a 1px gap so they never clash. Exported by render.py into frames.json (accessories, accessoryOrder, hatHidesBow, icons).

**How the swap was done (repeatable):** clone each staging variant's vectors into the same-named 8:159 variant, resizeWithoutConstraints to 144, copy reactions by remapping destination names, then move unscaled instances up 24 (peek 16) and left 8; scaled auto-layout instances need nothing (SCALE constraints).

Related: [[project-portfolio-pixel]], [[feedback-no-tilt]], [[feedback-no-em-dashes]], [[feedback-push-back]].
