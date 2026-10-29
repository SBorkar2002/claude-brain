---
name: project-portfolio-v3
description: Portfolio v3 "Signature" (16 Oct 2026), built from scratch in ~/Documents/Personal/Github/portfolio-v3: 3D broad-nib calligraphy hero, six section worlds, live demos; state, files, flags
metadata:
  type: project
---

Sejal asked for v3 "entirely different" from v1/v2, Apple-premium, motion, calligraphy, 3D, a different interaction per section, flawless scroll and transitions. Repo `~/Documents/Personal/Github/portfolio-v3` (git init, NOTHING committed). Next 16.4 + React 19.3 ViewTransition, GSAP ScrollTrigger/Flip, Lenis, R3F/drei, Tailwind v4. Spec: `DIRECTION.md`. v2 repo untouched.

**Concept "Signature":** her name written by a broad-nib engine (`src/lib/nib.ts`, font EMS Allure = single-stroke Allura, OFL, JSON from `scripts/build-nib-font.py`) and swept into a 3D satin ribbon (`src/lib/ribbon.ts`, perspective pre-scaled so the front view is exact calligraphy). Scroll orbits it: front = signature, side = sculpture. Copy beats: "A signature, from the front. / A structure, from the side. / I design products both ways."

**Sections/worlds:** Hero (black, 3D) → Statement (scroll-lit words, nib writes "ship") → iris opens from the final full stop → Work (4 pinned tinted chapters, mask wipes + inner parallax, rolling counter, live demos rebuilt in code: assessment result card, kit composer, AFB browser autoscroll, Sourced survey bars) → Method (light bento sheet slides over; 5 working demo tiles incl. GSAP Flip nav flatten) → ink-bloom mask into Art room (draggable endless wall) → Contact (paper rises on a nib-stroke edge, "Your turn." + signing pad with the same nib). `/work/[slug]` case studies (stage morphs via ViewTransition, sticky scrollspy nav), `/art` (video first, click-to-expand morph).

**Gotchas:** preview_start can't exec/cwd into this new folder (macOS provenance/EPERM): run `next dev --port 3300` via Bash in background and attach with launch.json entry `portfolio-v3` (url only) in `~/.claude/launch.json`. GSAP: inline `translateY(%)` gets parsed into px `y`, so every fromTo on mask lines needs `{ y: 0, yPercent: 125 }`. Grid without explicit `grid-cols-[minmax(0,1fr)]` blows out on mobile around fixed-width demos. QA via `scripts/qa-shots.mjs` (headless Chrome, beats `selector@progress`).

**Open flags:** contact links/email/resume TODO; Sourced survey percentages are multiples of 1/28 though handover says 27 responses; brand art missing; stage names on the assessment card are the public quiz's; case studies 02-04 draft. Related: [[project-portfolio-figma]], [[feedback-motion-quality-bar]], [[feedback-no-em-dashes]], [[feedback-push-back]].
