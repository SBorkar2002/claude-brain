# Portfolio · Pixel (v4) · Plan

17 Oct 2026. Supersedes v3 "Signature" as the build direction. v3 repo (`~/Documents/Github/portfolio-v3`) stays untouched; reuse its copy and processed assets where useful.

## Thesis

Pixel chrome, HD work. The pixel layer (cat, type for headings, icons, nav keycaps, section markers) gives the site its personality. The work itself is always shown at full resolution, in a legible body font, with no pixel filters. A recruiter should never have to decode a pixel font to read a case study.

Why this matters: a fully pixel site reads as "game dev" or "gimmick" to a product design hiring manager. Keeping pixels in the frame and not in the content is what lets the same site work for product, visual and art roles.

## Decisions (her answers, 17 Oct)

1. Epifi / Tetriz: NAMED. Show only what was public (quiz, live feature pages, published videos) plus her own wireframes and process. No internal dashboards, no AIDLC curve, no sales collateral.
2. Interactivity: NATIVE rebuild of key flows in code (Sourced first), "Open the Figma prototype" link as backup. Figma files must move to her personal account before any link goes live.
3. Assessments: MIXED into the work, ranked by strength, each tagged "Take-home". Instahyre in product work; UXpective and AlterOffice in art/visual.
4. Cat sprites: I draft all states as editable pixel grids + a sprite sheet in Figma, she refines any frame.

## Figma build log (file hfj2locm0N5bssdEU6NaoH, page "Pixel portfolio · v1")

- Variables: collection "Portfolio · Color" (VariableCollectionId:7:2), modes Dark 7:0 / Light 7:1. bg/base, raised, sunken, line, text/primary, text/muted, text/on-pastel, cat/* (body, eye, pupil, shine, mouth, mouth-inner, zzz, heart), pastel/* (lilac product, peach art, mint experience, sky graphic, pink motion, butter highlight), accent/ink.
- Text styles: Display XL/L/M + Heading S = JERSEY 15 (XL 120/112, L 75/72, M 45/46, Heading S 30/32, +1%). Pixelify Sans dropped: its 'e' was hard to read even at Medium.
- Cat component set 8:159 (v2 art from her reference cat: big front head, round O eyes with black fill, whiskers, upright tail, longer legs; yawn = squeezed > < eyes + small round mouth; 35 variants, State x Frame, colours bound to cat/*, AFTER_TIMEOUT loops, click a sitting cat to hop). Walk lane set 12:106 (Mid/Start/End, smart animate slide).
- UI kit 10:6: icons (arrow-right 10:7, sun 10:9, moon 10:11, download 10:13, cat 10:15), Keycap 10:17, Tag set 10:27 (Shipped mint, Personal pink, Take-home butter, Client sky), Button set 10:36.
- Style tile Dark 9:2 (0,0), Light 11:49 (1560,0). Playground 12:109 (0,3200), flow start "Cat playground", Dark/Light toggle via SET_VARIABLE_MODE. Sprite sheet Dark 12:246, Light 12:558.
- Sprite source: cat/sprites.py (edit), cat/render.py (preview PNG + JSON), cat/runs.py (run data pushed to Figma).

## Home page v1 (17 Oct, no cat yet)

Figma: Home Dark 27:386 at (0,5800), playable (flow "Home"): nav fixed (28:567), sections Hero 27:388 / Work 27:447 / Experience 28:418 / Art room 28:466 / Contact 28:524, tiles 01-06 = 27:454, 27:483, 27:499, 27:516, 27:532, 27:548, jump-in panel 27:404. Light static copy 30:447 (reactions stripped). Notes board 30:811. Keys in Present: W A E C, 1-6, T light, D dark; nav, CTAs, jump rows, brand and back-to-top scroll. Display XL is now Jersey 15 105/100 (two-line hero). Image hashes for all 24 uploaded crops: figma-image-hashes.json. Cat perches planned (in notes): hero panel top edge, work gutter walk, peek behind tile 03, inspect art room, sleep by footer. Next: case study template, art room page, cmd K + ? sheet, mobile 390.

## Case study 01 + template (17 Oct)

Figma: "Case study · 01 Lead-gen assessment (Dark)" 39:704 at (0,11700), playable (flow "Case study 01"): fixed nav clone 41:775 (links go Home), fixed contents rail 41:812 (rail items 41:821..841 scroll to sections; numbers = keys 1-6; Esc = Home), sections Hero 39:706, 01 Overview 39:733, 02 Problem 39:766, 03 Before 39:783, 04 Decisions 40:705 (chose/cut/why + visual; D3 native two-track diagram), 05 Shipped 41:710 (PRs #6611 #6649 #6686), 06 Reflection 41:746, Next card 41:763. Template anatomy notes 41:885 at (1560,11700). Home tile 01, jump row 1 and key 1 now NAVIGATE to it. New icon: Icon / arrow-left 41:845.
Sources: original quiz rendered from core git (origin/artifact/ai-native-index-quiz e32cecb8b, client/workloom/site/public/tools/ai-native-index-v2.html) with its internal with/without-Tetriz chart cropped out; wireframes from Figma nyj8rbPsYnRozDmtHJgQzq. Live quiz (workloom.dev/quiz/ai-native-index, tetriz.ai) returns 404 as of 17 Oct.

## Case study 03 Sourced (17 Oct)

Figma "Case study · 03 Sourced (Dark)" 55:730 at (0,21400), flow "Case study 03 Sourced"; nav 56:959, rail 56:986 (5 = The design), sections Hero 55:732 (tappable phone + tips), 01 55:780, 02 55:813 (problems + survey charts + quote), 03 55:838 (2025 screens from the old Behance case study), 04 56:733 (5 decisions, each with two LIVE phones), 05 The design 56:905 (IA/flow + DS images, 20 screens / 42 components / 5 tokens / 83 hotspots), 06 56:929 (her reflection), Next 56:947. Home tile 03, jump row 3 and key 3 open it.
Tappable app: component set "Sourced · App (tappable)" 52:833 at (4400,11700): 20 variants (images of the redesign screens) + all 83 original hotspots with CHANGE_TO. Figma API rejects PUSH/SLIDE/MOVE transitions on CHANGE_TO, so pushes became 0.25s dissolves; smart animate kept for tabs/feed toggle/menu. Copy grounded in the night case study 48:414 text.

## Reader and time budget

Primary: product design hiring manager, about 90 seconds. Secondary: visual / brand / art lead.
- 5 seconds: who she is, what she does, that she ships.
- 30 seconds: the work index, each tile readable without hovering.
- 90 seconds: one case study top (title, role, timeframe, outcome, visual) and the decision she made.

## Information architecture

```
/                 home (index, about 4 viewports)
/work/[slug]      one page per project, sticky section nav, prev/next
/art              visual and art work, tabbed (Illustration, Comics, Graphic, Motion)
/resume           redirects to the PDF (product variant), artist PDF linked from /art
```

Home, top to bottom:
1. Intro: name, role line, one sentence, status ("Product designer at Epifi, open to product design roles"), CTAs Work / Art / Resume. Cat sits here on load.
2. Work index: large tiles, each with type tag (Shipped, Personal, Take-home), one-line outcome, role, year. Hover plays a short silent preview.
3. Experience: compact timeline (Epifi, AppsForBharat, Pocket FM, freelance graphic design, Jeneko freelance art).
4. Art shelf: one row per category, thumbnails, link to /art.
5. Contact footer: email, socials, resume. Cat sleeps here.

## Content (draft, pending her answers)

Work (product design):
1. Lead-gen assessment redesign (Epifi, shipped)
2. Marketing site: 5 feature pages, ~20-component library, nav restructure (Epifi, shipped)
3. Sourced (personal, mobile app, research-led) with a native interactive phone demo
4. #futureofhr webinar landing page + launch video + poster (Instahyre take-home)
5. AppsForBharat blog + themed thumbnail system (shipped, live)
6. Optional: video production system (Epifi), storyboard 4 days to 1

Art and visual:
- Illustration: Jeneko (ArtStation), competition placements
- Comics: One Last Chance (Webtoon, solo), The Last Over (AlterOffice take-home), Pocket FM panels and posters, "I Have No Idea What That Means" episodes (30,000+ views)
- Graphic: Maggilicious Cafe brand, AFB merch and printables (buddy tee, appreciation cards, Women's Day card, keychain), UXpective "2025 UX Challenges" carousel (take-home), #futureofhr poster
- Motion: comic episodes, #futureofhr launch video, AFB AI videos

Dropped: Green Gallery (her call), Moduvo, Indeed redesign.

## Navigation and shortcuts

- Persistent top bar: monogram, Work, Art, Experience, Contact, Resume, theme toggle, cat toggle.
- Cmd/Ctrl+K command palette: every project, copy email, open resume, socials, toggle theme, hide cat.
- Keys: 1-6 open projects from home, W A E C jump to sections, R resume, T theme, ? shortcut sheet, left/right arrows between case studies, Esc back to index.
- Keycap hints shown in the nav so recruiters discover them without reading instructions.

## The cat

Faceless cat, two huge yellow eyes. Black in light mode, white in dark mode (eyes keep a dark slit pupil so they still read on white).

Rendering: one canvas at native sprite resolution, scaled by an integer factor in DEVICE pixels (not CSS pixels: an integer CSS scale gives uneven pixels on 1.5x / 1.25x screens; compute `scale = floor(targetCssSize * devicePixelRatio / spriteSize)` and set CSS size = scale * spriteSize / dpr), `image-rendering: pixelated`, whole-pixel positions, motion quantised to the grid at 8-12 fps. Sprites pre-rendered once to offscreen canvases per palette. See research-repo.md (majidmanzarpour-927543, twoclipping-041659, heyiamnick-119558, leowenai-125931). Frames authored as palette-indexed grids in TypeScript (editable by hand), so the theme swap is a palette swap and eye direction is a per-pixel pupil offset (quantised to -1/0/+1). Zero animation libraries.

States: idle (breath, blink, eye drift), walk (4-6 frame cycle), look (pupils toward cursor, highlighted tile or artwork), yawn (silhouette opens, then back to two eyes), sit, sleep (eyes to lines, slow bob, at most one Z at a time), react (hop + eye widen on click), peek (rises from behind a section edge or tile), inspect (sits beside a project title, looks at it).

Choreography: a small director with "perches" declared on DOM elements (`data-cat-perch`). IntersectionObserver picks the active section; the cat leaves one perch and enters the next with a short purposeful move. Never follows the cursor continuously, never covers text or artwork (perches are placed in gutters and checked against content boxes).

Rules: rAF only while animating and visible; pause on `visibilitychange`; `prefers-reduced-motion` gives a static seated cat at intro and footer with no walking; mobile gets fewer perches, tap to pet, no cursor tracking; a visible toggle hides the cat entirely. Pet = stroke gesture over the cat (purr eyes) or click (hop + one line from a short list of messages, some of which teach shortcuts). Accessories (hat, bow tie) come last.

## Stack

Next.js on Vercel, Tailwind v4, native scroll (no scroll-jacking), View Transitions for opening a project, custom canvas cat. Images self-hosted and optimised, not hot-linked from Drive.

Components (research-components.md, all MIT): one primitive layer = Space UI (Base UI + Tailwind v4 + Motion): Command + Kbd (Cmd+K, keycaps), Section Scrollspy (case-study nav), Theme Toggle (reveal turned into a stepped pixel wipe), Showcase Gallery (/art), Popover/Toast (cat speech bubble). Pull single pieces from Componentry (Pixel Canvas, Dither Gradient, Hover Transition strips/wipe, Split Flap status line) and Arc (Image Compare, Timeline, Shortcut Recorder display parts for the ? sheet). Build ourselves: lightbox, Figma/video stage with Fit/Mobile/Full controls, global hotkeys. Planes and Skecher = reference only (no license).

## Curation notes (from inventory)

- ArtStation: 38 pieces, only 4 originals (Sienna x2, Portrait Study, Nex Drakos) + 1 commission (Wanda); 14 are ~911px screen grabs, need her hi-res files. Lead with originals + strongest renders; leave out the revealing pin-ups for a hiring audience.
- Webtoon One Last Chance: 1 episode, ~100 panels, 2022, solo. Only public proof of original sequential storytelling.
- AlterOffice The Last Over: PAGE 1, PAGE 2, character sheet, shot plan, process note. Character sheet has 2 Gemini sparkles to remove. Helmet continuity slip (partner) P1 to P2.
- Pocket FM: 72 PNGs (Saving Nora, Rekindled Heartache, Badass Billionaire Doctor; bsw unconfirmed and looks like licensed source art). Heavy mature content: pick SFW panels only. Needs an exact credit line for her part.
- Canva/Maggilicious: logo, offer poster, banner, 3 socials, 2-slide carousel. Food photos look stock/AI. Naruto/JJK fanart inside the client's branding is an IP risk: show the brand system, not that piece.
- AFB: buddy tee, 4 appreciation cards, Women's Day card + illustration, blog (live, 390px mobile overflows sideways on the live site). Keychain PNG not reachable via the Drive connector.
- UXpective carousel: 7 slides, "2025 UX Challenges", cat-meme stickers (nice tie-in with the cat).
- Socials found: linkedin.com/in/sejalborkar, behance.net/sejalborkar04 (+ older behance.net/jenarts), github.com/SBorkar2002, instagram.com/_jeneko, x.com/_Jeneko, artstation.com/jen_chan, Webtoon creator page, jeneko.vercel.app, emails sejalborkar2002@gmail.com and jen.art410@gmail.com. Old site shows a public phone number: drop it.

## Phases (each ends on her approval)

1. Answers to open questions.
2. Figma (file hfj2locm0N5bssdEU6NaoH): style tile, cat sprite sheet with all states, home at desktop and mobile.
3. Cat engine prototype page she can play with.
4. Site shell, home, nav, shortcuts, theme.
5. Case studies.
6. /art.
7. Cat choreography across the site, then accessories.
8. QA (mobile, reduced motion, Lighthouse) and deploy.

## Facts found during inventory

- Figma MCP page listing is unreliable: it shows only loaded pages. Nodes on other pages still resolve by id (Sourced night case study 48:414, #futureofhr landing 7:2 both exist).
- Figma files live in the epifi account (sejal.borkar@epifi.com), which ends with the company in Nov 2026. Anything embedded from it will break. Move files to her personal account first.
- AFB zips are in ~/Downloads (Buddy Tshirt, Employee Appreciation Cards, Women's Day checklist card) plus Blog Home Page.png. Keychain PNG only in Drive.
- Sourced night case study exported: ~/Documents/portfolio/Sourced · Case Study (Night).png
- #futureofhr deliverables: ~/Documents/instahyre-launch-video/out/
- Comic episodes: ~/Documents/comics-video/out/
- Resumes: Figma NlBw9VEMyRgbexRrmBBUVN (A generalist 4:2, B product 25:2, Artist 48:2).
- Artist resume lists a college pixel-art game project (map, tiles, character turnaround and walk cycle). Strong tie-in for a pixel portfolio.

## Deploy plan (decided 17 Oct, run only once the new site is finalised)

- Repo: SBorkar2002/my-portfolio, default branch `main`, live at sejalborkar.vercel.app.
- Step 1 DONE 17 Oct: `old-portfolio` branch + annotated tag `old-portfolio-final` on GitHub, both at e0dbd46 (main untouched).
- Step 2: build the new pixel site as new commits on `main`. No force-push and no orphan branch, so the old history stays reachable from main as well.
- Step 3: Vercel redeploys `main`, so the new site goes live at the same URL. If the stack changes, update the Vercel framework preset and build command first.
- Bonus: Vercel gives `old-portfolio` its own preview URL, so the old site stays viewable.
