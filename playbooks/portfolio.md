# Portfolio playbook (sejalborkar.vercel.app)

Everything needed to keep evolving Sejal's portfolio. State as of 22 Oct 2026.

**The only portfolio that exists is `my-portfolio`** (the live pixel site). Abandoned directions, not kept:
- `~/Documents/Github/portfolio` (v2 "Pencils, inks, colours", comic-production language, riso colours) and Figma `HYNlpUpZ9Qt58sdSfOlOI4` (v1 "Design / Ship" toggle). Lesson: v1's off-white + ink + one orange + Geist + toggle turned out to be the viral AI-showreel house style; she called it junior.
- `~/Documents/Github/portfolio-v3` ("Signature", 3D broad-nib calligraphy ribbon, Apple-premium). Lesson: generic "premium" spectacle without a personal concept got dropped within a day; the pixel cat (personality) is what stuck.

Do not touch those folders. Do not mine their copy without re-checking it against the truth rules below.

---

## 1. Positioning (what the site must say in 5 seconds)

- **Line:** "Product designer who ships." Sub: "B2B SaaS, from research to merged pull requests. Drawing since 2020." Eyebrow: "From digital artist to product designer."
- **Differentiator:** she designs AND ships front-end into production codebases (with Claude Code), builds reusable systems (component kits, video pipeline, skill files), and can draw (rare in product design).
- **Front-end claim, exact wording rule:** she works in Next.js/React codebases using Claude Code; she can read and modify components inside repo conventions; she is NOT a React developer and does not write React from scratch. Never imply framework expertise.
- **Target readers:** (1) product design hiring manager, about 90 seconds: who she is in 5 s, the work index in 30 s, one case-study top and one decision in 90 s. (2) Brand, visual or art lead browsing the Art room.
- **Target roles:** see `projects/career.md`. Product Designer (B2B SaaS, 0 to 1, founding) first; Design Engineer second; visual/brand/art as range, never the headline.
- **No availability talk.** She removed "Open to product design roles from December 2026" and "Product designer at Epifi, open to roles" ("people know I'm open... we are not going to tell them what exactly we are trying to sell"). No dates, no "available from".
- **CONFIDENTIAL:** her "Consultant at Epifi until Nov 2026" engagement is NOT announced. On the site show only "GenAI Product Designer · Epifi Technologies (Fi Money)", "SINCE JUN 2026", no consultant title, no end date.

## 2. The concept and why: "Pixel chrome, HD work"

- Pixel art lives only in the chrome: headings, labels, keycaps, icons, section markers, the cat. Every piece of work is shown full resolution in a readable body font, no pixel filters.
- Why: a fully pixel site reads as "game dev" or gimmick to a product hiring manager. Pixels in the frame, not the content, lets one site serve product, visual and art roles.
- Why pixel at all: personality and memorability, ties to her college pixel-art game project (map, tiles, walk cycle) and her drawing background. Origin: her 17 Oct brief (faceless black cat with huge yellow eyes that lives on the page).
- Recruiter-fast: each project its own page, keyboard shortcuts, jump panel, no unnecessary scroll, native scroll (no scroll-jacking except the pinned Experience story on desktop).
- Product design first; art gets its own Art room section that never interleaves with case studies.

## 3. Live site and repo

- **Live:** https://sejalborkar.vercel.app (Vercel project `sejalborkar` under `sborkar2002s-projects`).
- **Repo:** GitHub `SBorkar2002/my-portfolio`, local clone `~/Documents/Github/my-portfolio`. `main` = production. Working branch `revamp` (equal to main at `ce2f4b1` "chore: witch hat from the cat studio", 20 Oct). Other branches (`pixel-v1`, `pixel-cat`, `p0-p3`, `marketing-site`, `afb-and-marketing`) are merged history.
- **Old site:** React/Vite, frozen on branch `old-portfolio` + annotated tag `old-portfolio-final` (commit `e0dbd46`). Never modify, delete or force-push these. The new site was built as normal commits on top of main (old history still reachable).
- **Stack:** Next.js 16.3 (App Router, all routes static), React 19.3, Tailwind v4, TypeScript. No animation libraries: CSS, small canvas and SVG pieces. Deps beyond Next: `@vercel/analytics`, `@vercel/speed-insights`. `vercel.json` pins framework nextjs, `npm ci`, `npm run build` (needed because the project used to be Vite).
- **Vendored free components** (credited in README and code comments only, never on the page: she does not want to reveal tools): Light Lines from Vengeance UI (MIT), zoom story pattern from scroll-craft (MIT), underline link hover skiper40 from Skiper UI (free with credit).

### Structure

```
app/layout.tsx          fonts, theme script, nav, shortcut layer, cat slot, analytics
app/globals.css         tokens light/dark, type styles, pixel shadows
app/page.tsx            home
app/work/marketing-site, sourced, futureofhr, afb-blog, video-system, lead-gen-assessment
app/not-found.tsx       404 (cat falls onto a ledge, dozes)
components/home/        Hero, Work, Experience (zoom story), ArtCollage, Doodle, GutterSky, SectionRail, ScrollMemory, Sections
components/case/        CaseRail, TappablePhone (Sourced prototype), blocks
components/cat/         CatLayer (renderer + director), CatToggle, WardrobeDock
components/             Nav, ThemeToggle, MusicToggle, Loader, Logo, GoTop, SiteChrome (shortcuts, jump sheet)
lib/projects.ts         project list, order, links, socials, email, resume path
lib/sourcedApp.ts       Sourced prototype screens + 83 hotspots
lib/cat/frames.ts       GENERATED from the cat studio export, do not hand-edit
lib/music.ts            Web Audio chiptune
scripts/                optimise-images.mjs, export-cat-frames.mjs, build-art-collage.mjs, build-cursor.mjs
public/images           self-hosted WebP 1x/2x; public/Sejal_Borkar_Resume.pdf; public/og.png
.studio/sweep.json      phone sweep config for the studio plugin (paths, floaters, protect, allowCrop)
.claude/launch.json     dev server entry "portfolio-dev" on port 3410
```

### Pages and content (order is Sejal's call, 18 Oct)

| # | Tile | Tag | Route | Notes |
|---|---|---|---|---|
| 1 | Marketing site and a 20-component library | Shipped | /work/marketing-site | Epifi/Tetriz, named; links tetriz.ai feature pages. Captures of live public pages only. |
| 2 | Sourced: human-made and AI art, side by side | Personal | /work/sourced | 11 tappable phones, 83 hotspots, instant cuts (no fade). Behance link. |
| 3 | #futureofhr: a webinar page built like a video call | Take-home | /work/futureofhr | Does not name Instahyre. Landing page, launch video, poster. |
| 4 | Company blog and a themed thumbnail system | Shipped | /work/afb-blog | AppsForBharat; links blog.appsforbharat.com; print and merch. |
| 5 | Video production system | Shipped | /work/video-system | "Making a B2B SaaS launch film". Product UNNAMED: no "Tetriz" visible in any frame or text. |
| 6 | Lead-gen assessment, redesigned and shipped | Shipped | /work/lead-gen-assessment | In "More work", not Selected work (her call). Live quiz is 404 now. |

- Home order: Hero (+ "Jump straight in" panel with keys 1 to 6) > Selected work > Experience (pinned zoom story on desktop, plain vertical list on phones; intro chapter "Hi, I am Sejal." + separate Education block) > Art room (illustration, comics, graphics, motion; cards link to ArtStation, Webtoon, Canva site) > Contact ("Say hello.", email, resume, socials, doodle pad).
- Experience chapters: Epifi (since Jun 2026), AppsForBharat (Jan to Jun 2026), Pocket FM (Aug to Dec 2025), Graphic Designer freelance / Maggilicious Cafe (Aug 2023 to May 2025), Jeneko freelance art (Feb 2021 to Mar 2025). Education: MCA, Ramaiah Institute of Technology, 2024 to 2025.
- Socials: LinkedIn, Behance (sejalborkar04), GitHub (SBorkar2002), ArtStation (jen_chan), Instagram (_jeneko), Webtoon. Email sejalborkar2002@gmail.com. No phone number on the site.
- Case-study template (every page): kicker "CASE STUDY 0N / 06", title, one-liner, meta row, hero visual > 01 Overview > 02 Problem > 03 Before > 04 Decisions (chose / cut / why + visual) > 05 What shipped > 06 What I would change > Next card. Sticky contents rail, keys 1 to 6, Esc home, arrows prev/next. A section with no real material is dropped, never padded.

### Features and behaviours (all live)

- Shortcuts: W A E C sections, T/D theme, `?` or Cmd/Ctrl+K jump list, 1 to 6 projects (home) or sections (case study), Esc home, arrows between case studies. Ignored while typing.
- Light/dark: follows system until picked, saved in `localStorage.theme` + `html[data-theme]`.
- Loader on every full load, at least 2 s (cat spins on the bar), waits for fonts not every image, capped 8 s, none for reduced motion. Reload always lands on the hero (manual scroll restoration, stale hash dropped).
- Background chiptune generated with Web Audio (no file, no licence), volume 0.35, starts on first click/tap (browsers forbid earlier), pixel speaker toggle with SOUND ON/OFF label that blinks until first tap, remembered, off for reduced motion.
- Pixel fish-cookie cursor (32 px, nose hotspot); pointer and text cursors kept.
- Per-section backgrounds: hero grid + light lines + pointer spotlight; work dot matrix; experience zoom frames; art room pixel "ice" canvas that cracks under the pointer and refreezes over a 40% faded collage; contact dot paper with a doodle pad (contact only).
- Logo: plain rounded-pixel badge "SB" in the pixel font, no ears, no whiskers (the whiskered cat-ear version "looks like a spider"). Light theme dark fill + lilac text, dark theme lilac fill + deep purple text. Used in nav, loader, favicon.
- Open Graph card `public/og.png` on every page. Vercel Web Analytics and Speed Insights enabled (day one: 3 visitors, 15 views; home is one long scroll, so "bounce" is a weak signal, watch Pages and Referrers).

## 4. Design system

- **Fonts (next/font, self-hosted):** Jersey 15 = display/headings (Pixelify Sans dropped: its "e" was unreadable even at Medium), Silkscreen = labels and keycaps, Rethink Sans = body (Hubot Sans renders condensed in Figma), Instrument Serif = hero headline words only (from her own reference screenshot, P6 round).
- **Light tokens:** bg-base #F3F0FA, raised #FFFFFF, sunken #E7E2F2, line #D4CDE4, text-primary #17141F, text-muted #474259, accent-ink #5B47D6.
- **Dark tokens:** bg-base #15131C, raised #1E1B28, sunken #0F0D15, line #34304A, text-primary #F2EFFA, text-muted #BCB6D0, accent-ink #C3B5FF.
- **Pastels, one job each:** lilac #C3B5FF product, peach #FFB99A art, mint #9EE6C4 experience, sky #9ED2FF graphic, pink #FFAFD2 motion, butter #FFE58A highlight. Provenance tags: Shipped mint, Personal pink, Take-home butter, Client sky.
- **CTA:** lime #D9F860 (`--accent-lime`) for buttons. Brand feel: purple/lavender is the main theme colour, lime is the action colour.
- Muted text raised to 7.5 to 9.4:1 contrast after she found the hero subline hard to read. Aim for AA or better on everything.
- Hard pixel shadows (`shadow-pixel-8`), 2 px borders.

## 5. The cat (mascot)

- **Identity:** faceless pixel cat with two big round yellow-ring eyes (black pupils). Black cat in light theme named **Cookie**, white cat in dark theme named **Mimi**; the name in an open bubble must swap the instant the theme changes. Whiskers KEPT. Lime belt (#D9F860, same as CTA) with a yellow bell (eye yellow). Fuller, "kinda squishy" body, not skinny, not fat; head on the front-top of a box body, jutting ~8 px past the chest (from her reference `~/Documents/career/portfolio-pixel/inventory/refs/cat-reference.webp`).
- **Ownership rule (standing):** every cat art tweak goes to a dedicated cat chat/agent, never the main or code chat. The code chat only imports the art. If the old cat session is gone, start a new dedicated cat session with this section as its brief.
- **Art source (NOT in git, back it up):** `~/Documents/career/portfolio-pixel/cat-v2/`: `sprites.py` (48x48 ASCII stamps + TIMINGS), `accessories.py`, `render.py` (writes `preview/frames.json`, GIFs, sheets), `runs.py`, `research.md`, `audit.md`, `README.md`. Rebuild: `cd ~/Documents/career/portfolio-pixel/cat-v2 && python3 render.py`.
- **Import into the site:** `node scripts/export-cat-frames.mjs ~/Documents/career/portfolio-pixel/cat-v2/preview/frames.json` > regenerates `lib/cat/frames.ts`. New state names or colour keys must also be added to STATES and PALETTE_VARS in the script/renderer.
- **Palette keys:** `#` body, `f` far legs (`--cat-body-far`, light #423B54 / dark #BEB7D2, makes diagonal leg pairs read), `Y` eye yellow and bell, `p` pupil, `w` shine, `m`/`M` mouth, `z` Zs, `l` top-light rim (`--cat-body-top`), `s` baked ground shadow (rows 46-47), `g` belt lime, `H` #5B3DD0 hat/tie, `b` #A78BFA band, `k` glasses (opposite of body), `h` bow.
- **States:** Sit, Idle, Walk, Look (standing), Inspect (low stalking crouch), Yawn (flat shut eyes + small V mouth + 2 fangs), Sleep (z then z+Z), Peek, PeekSide, PeekTop, React (hop, legs straight down), Fall (page-load spin via 8 turnaround drawings, never in-plane rotation), Tumble, Land (reach, compress, low recover, rise, ONE sit), Run, Pounce, Sphinx, SphinxTap, Talk (3/4 head). Feet always on row 47.
- **Renderer:** one canvas, integer scale in DEVICE pixels (`scale = floor(cssSize * dpr / 48)`), `image-rendering: pixelated`, colours from `--cat-*` tokens so theme swap is a palette swap; rAF only while visible; pauses on tab hide; reduced motion = still cat; nav toggle hides it (remembered).
- **Choreography (live):** loader spin > falls once to the hero bottom (desktop) or onto the "Jump straight in" panel (phones), introduces itself in a bubble; walks then naps at section bottoms; peeks over settled work tiles and says a line about the hovered project; laser-dot game (1 s delay, runs to the pointer, drops into Sphinx and taps 2 to 3 times); guide cat on a ledge in Experience that rides off with the section; falls into the Art room on the side it left by; contact cat enters from the right, sits huge, loops sit > yawn > sleep, says "In this section, you're free to draw."; on case studies it sits on the Next card; yawns then sleeps after 5 s idle. Click = hop + one of ~8 lines, shuffled without repeats. Bubbles invert against the theme and clamp 12 px inside the screen. Per-breakpoint scales.
- **Overlap exception:** the cat (only) may overlap and be cropped by content; its bubble must never cover buttons, images, headings or the cat itself.
- **Wardrobe (live):** dock of 4 pixel icon toggles fixed right, mid-height (phones: hanger button bottom-right): witch hat (purple, lilac band, lime buckle), tie, glasses (invert with theme), head bow. Rules: bow on turns hat and tie off; hat or tie on turns bow off; glasses with anything. Remembered; hides with the cat toggle.
- **Figma cat:** component set `8:159` in file `hfj2locm0N5bssdEU6NaoH` (63 variants, 144 px). Figma has NOT been updated since round 7 (19 Oct); code/frames.json is ahead.

## 6. Figma files (all in the Epifi Figma account, which closes Nov 2026: duplicate to personal first)

| File | Key | What |
|---|---|---|
| portfolio-2 | `hfj2locm0N5bssdEU6NaoH` | Source of truth for the pixel site, page "Pixel portfolio · v1". Tokens collection 7:2 (Dark 7:0 / Light 7:1), style tiles Dark 9:2 / Light 11:49, UI kit 10:6, Cat set 8:159, Home Dark 27:386 (playable), Home Light 30:447, Home notes 30:811 (cat perches), Case study 01 39:704 + template notes 41:885, Case study 03 Sourced 55:730, Sourced tappable app set 52:833 |
| Sourced / Green Gallery / AFB / UXpective | `72tXrfMYH64v0hkxDF1m2n` | See `playbooks/case-studies.md` |
| #futureofhr (Instahyre) | `z263yFoeKFoWhY7Ocb3WqK` | See case-studies.md |
| Resumes | `NlBw9VEMyRgbexRrmBBUVN` | A generalist 4:2, B product 25:2, C artist 48:2 |

- Figma is behind code for: marketing site, #futureofhr, AFB, video system pages (built code-first, "skip Figma" was her call to save tokens), mobile layouts, Cmd+K sheet, all cat rounds after 7.
- Figma MCP page listing only shows loaded pages; nodes on other pages still resolve by id.
- Moving files to a free account: copy-paste breaks (instances point at components in the source file). Share the file to the other account and use File > Duplicate to drafts. Free/Starter plan = 3 pages per file.

## 7. How to run, preview and ship

```bash
cd ~/Documents/Github/my-portfolio
npm install          # Node 20+
npm run dev          # or the launch.json entry "portfolio-dev" on port 3410
npm run typecheck
npm run build        # always before shipping
node scripts/optimise-images.mjs   # source images > public/images WebP 1x/2x
```

Ship flow (standing):
1. Work on `revamp` (or a feature branch), Conventional Commits, no em dashes in messages.
2. Push: Vercel builds a preview (`https://sejalborkar-git-revamp-sborkar2002s-projects.vercel.app`, behind Vercel login, so curl gets a redirect; check via browser or `gh api` deployment status).
3. Prove it: screenshots at 1440 and 390 in both themes (headless Playwright, not the in-app pane, which pauses rAF/scroll), phone sweep on 4 phones x 2 themes for layout/motion rounds, code review for medium/large rounds.
4. Ask Sejal to check the preview. Fast-forward `main` ONLY on her explicit OK ("push it", "ship it live"). Never force-push.
5. Confirm the production deploy is green, recheck the live site at 1440 and 390 in both themes, update the tracker.
6. Every report ends with a status block: Preview / Live / Waiting on you. Any step she must do outside the chat comes with the exact link and numbered clicks.

If a permission check blocks the production push, give her the exact command (`git push origin revamp:main`) instead of working around it.

## 8. Truth and content rules for the site

- Epifi/Tetriz: NAMED, public work only (live feature pages, the public quiz, published videos, her own wireframes). Never: internal dashboards, the AIDLC maturity curve, sales collateral, customer data, internal PR numbers or branch names in copy, people's names ("a design review", not "Anandhi").
- Launch film is unannounced: fragments only, never "Tetriz" on screen; approved stretch = the recommendations table up to the mouse click (~0:45 to 0:58 of `~/Documents/portfolio/tetriz-launch-v5.mp4`).
- Sourced survey = "25+" / "more than 25" respondents, never 27 (data is in 1/28 steps); it was a SURVEY, not interviews.
- Never invent metrics, URLs, dates, quotes. Missing material = TODO. Known unconfirmed claim: video tile says "Storyboards went from 4 days to 1"; sources only show 1 day as the target. Confirm with her or soften to "toward 1".
- Pocket FM credit: she generated, retouched, lettered and laid out; the "bsw" script art is the client's with light retouching from her. SFW panels only.
- Maggilicious: show the brand system, not the Naruto/JJK fanart inside client branding (IP risk). Food photos look stock/AI.
- ArtStation: lead with originals (Sienna, Portrait Study, Dream or Nightmare?, Nex Drakos) and strongest renders; leave revealing pin-ups out for hiring audiences. 14 pieces are ~911 px screen grabs; ask for hi-res.
- #futureofhr: label as take-home, do not name Instahyre; Mayank photo has a stock watermark (she said publish as-is, 17 Oct); panelist photos and company logos usage rights still unchecked.

## 9. Pending (from TIMELINE.md "Left", 22 Oct)

Code:
- Native code rebuild of the Sourced flow (today: exported 412 px screens, soft on 2x screens; export at 2x or rebuild).
- Real Cmd+K palette + `?` sheet design (a stand-in jump sheet is live).
- Mobile (390) Figma layouts were never designed; the code stacks on its own.
- Marketing site and AFB case studies lack Before and Reflection sections (need her material).
- Lighthouse pass on production (home phone was 73 perf, LCP 5.0 s, mostly the deliberate loader).
- Witch hat tip clips on Pounce frame 6 and React frame 3 (48 px canvas). Needs a taller canvas + unclipped export. Deferred.
- Recruiter summary (role, what shipped, result) at the top of each case study: suggested, not started.
- Source link still missing for the motion card.
- Optional: turn off Vercel Deployment Protection if previews should be shareable.
- No /art route yet (planned: tabbed Illustration, Comics, Graphic, Motion; artist resume linked there).

Figma: case studies 02 marketing, 04 #futureofhr, 05 AFB, 06 video system; Art room page; Cmd+K + ? sheet; 390 layouts; cat 8:159 catch-up.

Before Nov 2026 (urgent): duplicate all Figma files to her personal account; back up `~/Documents/career/portfolio-pixel/` (cat source, inventory, PLAN, TIMELINE; ~500 MB, not in git).

Resume PDF on the site still says "GenAI Product Designer (Consultant)"; on 20 Oct she said that is fine and declined a re-export. The site copy itself must still never show the consultant title.

## 10. Where the detail lives

- `~/Documents/career/portfolio-pixel/PLAN.md`: thesis, IA, cat engine spec, curation notes, Figma build log.
- `~/Documents/career/portfolio-pixel/TIMELINE.md`: the ONE done/left tracker. Update it, never create new status files.
- `~/Documents/career/portfolio-pixel/inventory/`: external.md, drive.md, downloaded assets, contact sheets, refs.
- `~/Documents/career/portfolio-pixel/research-repo.md`, `research-components.md`: pixel rendering and component research.
- `~/Documents/portfolio/`: raw assets (afb/, gamemap.jpeg 1280x671 college pixel game map, dreamfinal1.png "Dream or Nightmare?" 6840x4050, tetriz-launch-v5.mp4).
- `~/Documents/career/portfolio-handover.md`: the 11 Oct brief (older; superseded where it says "anonymise Epifi" and "hold Instahyre").
- `my-portfolio/README.md`: shortcuts, stack, structure, credits.
