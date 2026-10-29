---
name: project-portfolio-figma
description: "Personal portfolio home page built in Figma file HYNlpUpZ9Qt58sdSfOlOI4 (\"portfolio\"), direction \"Design / Ship\" (11 Oct 2026); node ids, system, open flags"
metadata:
  node_type: memory
  type: project
  originSessionId: fb6b27a3-5d27-4e0d-bd87-4e8d4356d916
  modified: 2026-10-10T22:56:24.484Z
---

Built 11 Oct 2026 from `~/Documents/Personal/career/portfolio-handover.md` (the brief for the Next.js rebuild). The Figma file was EMPTY when she shared it. Animation deferred to a later pass.

**Concept "Design / Ship":** the hero object is a tactile hardware toggle (native gradients + inner shadows + NOISE grain, no plugin, no paid render). Flipping it is meant to swap every project visual between wireframe and shipped. Proves "designer who ships" instead of saying it.

**System:** variables collection "Portfolio · Color" (bone #EAE8E2, paper, ink #111110, graphite, stone #67645C, hairline, signal #FF4F12 = live/action only, on-ink, ink-line). Text styles "Type/*": Boldonse (display caps, needs line height ≥122% when multi-line: its glyphs are ~1.21em tall), Geist (text), Geist Mono (labels), Doto (LED readouts, device + marquee only).

**Nodes (page 0:1):** Home frame 8:2 (1440 wide): Nav 8:3, Hero 8:26, LED marquee 17:79, Selected work 10:12 (Card 01 compare plate 10:19/screen 10:26, row 12:12 with Card 02 12:13 + Card 03 12:78, Card 04 Sourced 14:12), How I work 15:12, Art room 16:12 (real comic PNGs from `Documents/Work/comic folder`), About 17:12, Contact 17:43. Direction board 18:12 at x=1600. Component set "Mode switch" 7:13 (Mode=Ship 6:3 reads LIVE, Mode=Design 7:2 reads DRAFT).

**Open flags:** AppsForBharat dates unknown (row says "Earlier"); portrait slot is an SB monogram placeholder; contact links have no URLs; "with Claude Code" named in the SHIP column is her call; Card 01 result-screen content is rebuilt mock copy, not product data. Type/palette were her decision per the handover, so the direction is swappable via variables/styles. Related: [[feedback-no-paid-tools]], [[feedback-motion-quality-bar]], [[feedback-no-em-dashes]], [[feedback-no-tilt]].

**16 Oct 2026 · v2 kickoff.** Sejal called v1 junior-looking and asked me to act as a senior advisor, not an assistant. Page 0:1 renamed "v1 · Original (11 Oct, frozen)". New page 35:32 "v2 · Working copy" holds clones: home 35:56, board 35:620, its own switch set 35:33 (instances swapped, so v1 stays frozen). Research (all 703 awesome-opus5-5-videos prompts + 5 component libs) is in `~/Documents/Personal/career/portfolio-v2/research.md` with per-prompt tables in `prompt-scan/`. KEY FINDING: v1's off-white + ink + one orange + Geist + toggle is the viral Opus 5.5 showreel house style, so v2 must change material/palette. Proposed v2: same Design/Ship thesis in a comic-production language ("blue line to ink"), code-first build (Next.js, Lenis, GSAP ScrollTrigger, Motion, R3F only where needed), with Figma for styleframes. Awaiting her decision. gh is logged in as SBorkar2002; no Vercel CLI.

**16 Oct 2026 · v2 BUILT (code-first).** Repo `~/Documents/Personal/Github/portfolio` (Next.js 16.4 + React 19.3, Tailwind v4, GSAP+ScrollTrigger+SplitText, Lenis, motion/react). Not committed yet. Run dev via Bash (`pnpm exec next dev --turbopack --port 3100`); GOTCHA: Turbopack sometimes serves a STALE globals.css after edits, so restart with `rm -rf .next` and verify by curling the served CSS. Spec is `DIRECTION.md`. QA scripts: `scripts/qa-shots.mjs` (scroll beats), `scripts/qa-interact.mjs` (blue mode, lens, nav, mobile), `scripts/keyframes.mjs`; assets come from `scripts/process_assets.py` (blue-line tracings via Sobel). Concept "Pencils, inks, colours":
- non-photo blue construction layer + B-key blue mode (live grid, measurements, sketchpad)
- Anybody variable type inks on scroll
- riso colours pass (blue #0078BF, pink #FF48B0, yellow #FFE800, multiply overprints, WebGL halftone field)
- comic panels with halftone print reveal
- adapted Componentry print-run band + text repel, React Bits VariableProximity

Sejal's feedback mid-build: "too black and white, where's the creativity", "use the resources", "think out of the box". The colours pass answered it. Figma page 35:32 renamed "v2 · Side by side", v1 clone 35:56 left, 13 v2 key-frame stills (39:62-39:74) right.
Open flags:
- Kalam/Shantell are placeholders for her handwriting.
- Contact links are TODO.
- The feature-page crop is from the live site with the product name painted out.
- Case studies 02-04 are draft copy.
- The assessment shows the "AI-Native Engineering Index" label.
- No resume.pdf.
- Images use public/ paths.

**16 Oct 2026 · v3 supersedes v1/v2.** She asked for a from-scratch v3 with no reference to v1/v2. See [[project-portfolio-v3]].
