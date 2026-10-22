# Pixel portfolio · timeline

The one place to check what is done and what is left. Every chat working on the portfolio updates this file when it finishes something. Details live in PLAN.md.

## Who does what

| Chat | Session id | Owns |
|---|---|---|
| Main (Figma) | local_633c2f75-4daa-4320-bffb-4a1f299ead17 | Figma file hfj2locm0N5bssdEU6NaoH, page "Pixel portfolio · v1": pages, case studies, copy |
| Code | local_db62f9af-2f68-49fe-bf70-6ae5741c6604 | Repo SBorkar2002/my-portfolio, clone at ~/Documents/Github/my-portfolio, Vercel deploys |
| Cat studio | local_d9bf54fb-935a-4612-8b8f-dce9e35a64b8 | The pixel cat: sprites, states, cat v1 vs v2 |
| Automation | local_541ca8a1-3e5e-4344-9e81-c1a398d29f36 | Job-hunt scripts in ~/Documents/career/automation-scripts |
| Studio skills workshop | local_1b7f89f8-41d6-4559-ac44-b1caf075ff70 | The /studio skills, board and hooks (repo SBorkar2002/studio). Skill feedback goes to ~/Documents/Github/studio/FEEDBACK.md via scripts/feedback.sh |

## Done

- **17 Oct · Plan + research.** PLAN.md, research-repo.md, research-components.md, inventory/.
- **17 Oct · Design system.** Tokens (Dark / Light), type (Jersey 15 headings, Silkscreen labels, Rethink Sans body), UI kit, style tiles.
- **17 Oct · Cat v1.** 35-variant component, sprite sheets, playground.
- **17 Oct · Home page.** Dark (playable, keyboard shortcuts) + Light. HD portrait, centred.
- **17 Oct · Case study 01.** Lead-gen assessment, which is also the template for all case studies.
- **17 Oct · Case study 03.** Sourced, with a tappable app (20 screens).
- **17 Oct · Backup of old site.** Branch `old-portfolio` + tag `old-portfolio-final` on GitHub (commit e0dbd46). Main untouched.
- **17 Oct · Cat v2 approved and live.** Swapped into the Cat component 8:159 (63 variants, 144 px, incl. Fall + Land); every instance updated; v1 sheets frozen as archives.
- **19 Oct · Cat refined to her reference.** Whiskers kept, standing pose redrawn (head on the front-top, jutting past the chest), new walk, standing look-around, stalking inspect; yawn/react marks, z Z sleep, rebuilt landing. Live in Figma 8:159, exported to cat-v2/preview/frames.json.
- **19 Oct · Cat round 8.** Run (laser chase), Tumble (quarter-turn fall spins), side and top peeks, 3/4 Talk, pixel ground shadow, 2.5D top-light rim; exported to frames.json (Figma not updated yet).
- **19 Oct · Cat round 9.** Clean pounce (leap with four legs off the ground), sphinx tap loop, yellow belt with a bell on every frame, per-frame ground shadow, leg-kink fix; exported to frames.json.
- **18 Oct · Code: first deploy live.** Home + case studies 01 and 03 built in Next.js 16 + Tailwind v4 (light + dark, shortcuts, 11 tappable Sourced phones with all 83 hotspots), merged to `main`. No cat yet. Production: https://sejalborkar.vercel.app · Preview (branch `pixel-v1`, behind Vercel login): https://sejalborkar-2wrzcyg0v-sborkar2002s-projects.vercel.app
- **18 Oct · Cat live on the home page.** Cat v2 on the five Home-notes perches (lands on the panel, walks to "Selected work", peeks over tile 03, sits by the art room title, sleeps by the footer), pet to hop, nav toggle to hide it, still cat for reduced motion, two perches on phones. Merged `pixel-cat` to `main` (8dbaf1b); live at https://sejalborkar.vercel.app
- **18 Oct · P0 to P3 live.** Selected work reordered (marketing site, Sourced, #futureofhr, AFB, video system; lead-gen moved to "More work"), coming-soon states removed, AFB links to Figma + live blog, Sourced to Behance, art cards to ArtStation / Webtoon / Canva site, availability line and year removed from contact, cat about 30% bigger. `main` at 3915751. No source URL found for: marketing site, #futureofhr, video system, motion card.
- **18 Oct · Marketing site case study live.** Built in code (no Figma page) at /work/marketing-site from the tile copy and PLAN.md, with two captures of the live AI Adoption page and a tetriz.ai link. Overview and what shipped only: no material yet for problem, before, decisions or reflection. The home tile opens it. `main` at 43dc826.
- **18 Oct · Marketing site filled in, AFB blog case study live.** Marketing site now has problem, four decisions and what shipped (from Sejal's notes, captures of the live AI Impact, AI ROI and Session Security pages). New /work/afb-blog from the Figma file and local exports (themed thumbnails, mobile home, print and merch); the AFB tile opens it and it links the live blog. `main` at 7514575.

## In progress

- **Code · Revamp on branch `revamp` (19 Oct), MERGED to main 19 Oct (d7c18e7, fast-forward), live.** Preview: https://sejalborkar-git-revamp-sborkar2002s-projects.vercel.app (behind Vercel login).
  - Phase 1 done: library research (animmasterlib is paid only, so skipped; Skiper UI free pieces are mostly not a fit; Vengeance UI is MIT and fits best), home video loop (no Tetriz on screen), #futureofhr pack. Notes in the shared notes folder.
  - Phase 2 done (P6): layered hero (grid, glow, light lines, pointer spotlight), serif and pixel headline, floating cards, section index rail, lime #D9F860 buttons, displacement hover and scroll-driven scaling on work tiles, art trail behind the art cards, underline link hovers.
  - Phase 3 done: P7 loading screen, stepped section reveals, page wipe, cat falls into each section and lands at its bottom; P4 speech bubbles; P5 yawn and sleep after 5 s idle, wakes on scroll or move; video loop on the video system tile; #futureofhr case study.
  - Round 2 (19 Oct, commit 43e89dd, same preview): muted text raised to 7.5 to 9.4:1; constant loader loop; scroll-driven window reveal on work tiles (glitch removed); pinned experience scrollytelling with the cat beside each role; art collage with cursor spotlight (image trail removed); grid and glow on every section; video production case study (/work/video-system, product unnamed); cat bigger, walks then naps at section bottoms, peeks over tiles, hangs from a hovered tile with a line, big napping contact cat, more spins when falling, ground shadow, laser dot it runs to. Doodle mode skipped (cost). Tools: taste skill, web design guidelines, awesome design.md, image-to-code all found free and read as references (not installed globally); Playwright run via npx for screenshots.
  - Round 3 (19 Oct, commits fdc65b7 and ffe8e92, same preview, not merged): experience rebuilt as a pinned zoom story (chapters zoom in and out past the camera, pixel icon per role, concentric frames zoom behind, chapter rail), pattern from scroll-craft (MIT) since Vengeance UI has no zoom story and Skiper's source is gated; one guide cat on a ledge that hops and speaks per chapter; Epifi role shown with no consultant title and no end date (hero and experience); hero subtext fill removed; art collage rebuilt with no piece next to itself, under a canvas pixel grid that cracks under the pointer and refreezes; per-section treatments (hero grid and light lines, work dot matrix, experience zoom frames, art pixel ice, contact dot paper) replace the grid and glow everywhere; contact cat runs in from the left, sits beside the heading at 6.8x, loops sit, yawn and sleep, says "In this section, you're free to draw."; doodle mode (contact only, toggle and clear); cat falls once to the hero bottom at 1.3x, shadow follows it, tile hover sits on the hovered tile (wrong-tile race fixed), laser chase after 1 s at a run. Playwright screenshots and a recording are in the shared notes folder (round3-proof).
  - Round 3 follow-up (19 Oct, commit cfb43dc, same preview, not merged): the hero cat introduces itself as Cookie (black cat, light theme) or Mimi (white cat, dark theme); the experience guide sinks back out of the bottom of the screen when you scroll past; the contact cat comes back in from the side it left by, at 9x, centred in the open space; doodle, clear and back to top are pixel icon buttons; a "Reveal the art" button melts all the ice and freezes it again. The hero drop spot stays where it is (Sejal's call).
  - Round 3 follow-up 2 (19 Oct, commit e6fc3f0, same preview, not merged): first visit, the cat spins on the loading bar, then falls while the hero rises from the bottom to meet it, and the nav appears after it lands; cats no longer pop out of sight but stay put and scroll away with the page; the experience guide rides its ledge off screen; the art room cat falls on the left, and contact entry follows the side it left by; work peeks only on settled tiles and never while the walking cat is on screen; pixel stars and light pipelines in the work right gutter (the left gutter holds the section rail); bigger section rail.
  - Ship batch (19 Oct, commit e949040 on revamp): home reloads land on the hero (manual scroll restoration, stale hash dropped); loader on every full load, at least 2 s (none with reduced motion), capped at 8 s; speech bubbles invert against the theme; the contact cat always enters from the right; art collage faded to 40% behind the panels; on-page credit line removed (credits stay in README and code); pixel fish-cookie cursor (32 px, nose hotspot) with pointer and text cursors kept. Checked in Playwright. Fast-forward of main was blocked by the session's permission check (production deploy): run `git push origin revamp:main` to go live.
  - Batch (20 Oct, commit e4bea7f on revamp, not on main): education split into its own block under the intro; Sourced prototype cuts instantly (no dissolve); background chiptune generated with Web Audio (no file, no licence), volume 0.15, starts on first interaction, nav toggle remembers the choice, off by default for reduced motion; the cat's bubble name follows a theme change at once; eight click lines shuffled without repeats. Checked in Playwright. Main push is for the parent session once Sejal OKs it.
  - Batch (20 Oct, commit d68d20b on revamp, not on main): phones get a smaller hero cat on the jump-in panel and a plain experience list with reveals and the cat beside the role in view; bubbles clamped 12 px inside the screen; story mode fixed on load and width changes only (likely cause of the jump back to the art room: a height change near the bottom toggling the pinned story); touch doodle only inside the pad; fixed go to top button bottom-left; hero line "From digital artist to product designer", contact heading "Say hello." (availability talk removed); credit line confirmed gone. Checked at 390 and 1440.
  - Batch (20 Oct, commit 3f7f626 on revamp, not on main): music at 0.35, confirmed to start on the first click or tap; the music toggle is a pixel speaker (waves on, cross off) with a SOUND ON/OFF label on wide screens, visible on mobile and desktop; the name swap (Cookie light, Mimi dark) is asserted in Playwright on both sizes and both starting themes.
  - Code review (20 Oct, commit 25773e0 on revamp, not on main): two reviewers read everything since main (d7c18e7). 15 real bugs fixed and retested in Playwright: intro could get stuck after a tab switch or tile hover during the drop; moves frozen after a tab switch; cat landing a few px off when a scrollbar appears; loader could stay up forever if the app failed to start; a late page load jumped back to the top; Back from a case study lost the place on home; music silent after a first phone swipe; first tap on the sound toggle turned it off; doubled notes after a quick off and on; prototype stuck on the old screen if an image failed; doodle shifted after a zoom change; go-to-top lost keyboard focus; gutter lights repainted every frame; story section collapsed on its first render; a leftover loaderdone listener. Build, typecheck and copy-lint clean. Waiting for Sejal's code check before main.
  - LIVE (20 Oct): Sejal checked the code and approved; main fast-forwarded d7c18e7..25773e0, production deploy confirmed, live checked at 1440 and 390 in both themes (cat names, music on first tap, no console errors).
  - Mobile debug round (20 Oct, commit 1d0dfe4, LIVE 20 Oct after Sejal's OK; rechecked on the live site: no jumps, 0 sweep findings): ROOT CAUSE of the jump back to the art room on phones found and fixed: the contact cat ran in from beyond the right edge, widening the page to 688 px, so the phone zoomed out (traced in Pixel 7: innerHeight 839 to 1402, no scroll call); the cat layer now clips sideways. Reveals now watch late content and only hide once running (blank experience could not be reproduced in emulation, even on a slow network; this makes it impossible). Phone hero: the cat lands visibly on the jump-in panel, two short intro bubbles. Cat scales per breakpoint. Go to top: none on phones, one on desktop. Reveal the art removed. New SB pixel badge logo in nav, loader and favicon. Sweep on iPhone 13, Pixel 7, iPhone SE, iPhone 15 Pro Max in both themes plus all case studies: 0 findings after fixes; recordings in the shared notes (mobile-proof).
  - Batch (20 Oct, commit 6391106, LIVE 20 Oct after Sejal's OK; rechecked live): music unlock on iPhones (silent sample in the first tap, audioSession playback so the silent switch does not mute it) and a blinking sound toggle until the first tap, since no browser allows sound before one; phone experience cat moved to the right edge, its bubble keeps clear of the role pictures and the cat. Sweep on 4 phones x 2 themes: 0 findings.
  - Next-ideas round (20 Oct, commit d4eaf35, LIVE after Sejal's OK): cat on every case study (sits on the Next card with a line about the next one) and on the 404 page (falls onto a ledge, dozes); cat toggle in the nav everywhere; faster first screen (loader keeps its 2 s minimum but waits for fonts, not every image; art collage loads near the art room; right-sized images); Vercel Web Analytics added (needs one click in Vercel: Project, Analytics, Enable); tighter case-study stages on phones; work tiles named by their visible text; nav no longer spills at 1440. Lighthouse before: home phone 73 perf, LCP 5.0 s (mostly the deliberate loader). Link preview card approved and LIVE (913675f): public/og.png, Open Graph + large Twitter card on every page.
  - Speed Insights (20 Oct, commit 5523975, LIVE): @vercel/speed-insights component in the layout; Sejal enabled it in Vercel. Web Analytics confirmed working (3 visitors, 15 views on day one).
  - Cat wardrobe UI (20 Oct, commit 2365f1f on revamp, not on main): dock of 4 toggles (hat, tie, glasses, bow) fixed right, mid-height; phones get a hanger button bottom-right that opens them; hat hides bow; remembered; hides with the cat toggle; glasses colour key k swaps with the theme. Verified in Playwright with placeholder art in both themes, cat off/on, phone at 390. Waiting for the cat chat's sprites, anchors and icons (format sent).
  - Wardrobe rules (8730312 on revamp, not on main): bow on turns hat and tie off; hat or tie on turns bow off; glasses with anything; restored saves follow the same rules (an old bow+hat save keeps the hat). Verified by clicking every combo in Playwright, desktop and phone, both themes. Witch hat redraw coming from the cat chat.
  - Wardrobe LIVE (20 Oct, main ce2f4b1, after Sejal's "looks ok push and redeploy"): rules + witch hat; production green; live checked desktop and 390 in both themes (all combos pass). Witch hat tip clips on Pounce 6 and React 3 (canvas is the 48 px frame; fixing needs a taller canvas plus an unclipped export from the cat chat; deferred).
  - Experience copy v2 (22 Oct, 74f518f on revamp, not on main): summary + 3 points per role from experience-copy.md, verbatim, pixel bullets; fits the desktop story at 1440x900 and 1280x720 and the phone list; guide bubble never over the text (checked every chapter, both themes, 1440 and 390).

## Left

**Figma**
- [ ] Case study 02 · Marketing site
- [ ] Case study 04 · #futureofhr
- [ ] Case study 05 · AFB blog
- [ ] Case study 06 · Video system
- [ ] Art room page
- [ ] ⌘K palette + ? shortcut sheet
- [ ] Mobile (390) layouts

**Cat**
- [ ] Place the cat on the case study pages (home is live)
- [ ] Accessories (hat, bow tie)

**Code**
- [ ] Each new Figma page gets built as it is approved (02, 04, 05, 06 and the art room show "coming soon" until then)
- [ ] Native rebuild of the Sourced app flow
- [ ] Cat: pick and add perches for the case study pages
- [ ] Swap the stand-in jump sheet for the real ⌘K palette + ? sheet once designed
- [ ] Use the Figma mobile (390) layouts once designed (today the desktop layout stacks on its own)
- [ ] Point the case study "Next" cards back to 02 and 04 once those exist (today 01 and 03 point at each other)
- [ ] Sourced screens are 412 px exports and look soft on 2x screens: export at 2x or wait for the native rebuild
- [x] Replace the resume PDF (Sejal pushed a new one on 18 Oct, commit 76ff39f)
- [ ] Run Lighthouse on production and fix what it finds
- [ ] Optional: turn off Vercel Deployment Protection if preview links should be shareable

**Next batch (from Sejal)**
- [x] P4: cat sits at the bottom of each section, with a small speech bubble (on `revamp`, awaiting approval)
- [x] P5: idle tweaks everywhere, plus yawn then sleep after 5 seconds on one section (on `revamp`, awaiting approval)
- [x] P6: hero and section revamp to match her reference screenshot; buttons in #D9F860 (on `revamp`, awaiting approval)
- [x] P7: premium section-in and loading animations; on scroll down the cat falls from the top of a section to its bottom (on `revamp`, awaiting approval)
- [x] Looping video glimpse on home (the recommendations part) (on `revamp`, awaiting approval)
- [ ] Marketing site and AFB case studies: add before and reflection sections once Sejal has the material
- [x] Cat studio sprites wired: Sphinx and SphinxTap at the laser dot, the collar, and the shadow baked into each frame. Pounce is exported but unused (the laser spec says run, then drop into sphinx); say where it should play
- [x] Cat: Sphinx and SphinxTap tail back (a raised curl behind the haunch)
- [x] Cat: collar swapped: belt is lime on key 'g' (#d9f860, the CTA lime), bell is eye yellow 'Y', centred on the neck; live on main in 4aeb0b6
- [x] Cat: belt wraps the full neck in Walk, Run and every head bob or turn frame
- [x] Cat studio sprite fixes wired (d7c18e7): Sphinx tail back, green bell centred on a yellow belt, belt complete in Walk, Run and every head turn
- [x] Collar colours wired (4aeb0b6): belt in the CTA lime, bell yellow
- [x] Cat wardrobe art: hat, tie, glasses and bow overlays for every frame of every state, in frames.json (accessories, accessoryOrder, hatHidesBow, icons)
- [x] Cat wardrobe icons: 16x16 hat, tie, glasses and bow in cat-v2/preview/icons
- [x] Cat wardrobe live on the revamp preview (f4fc89e, not on main yet): dock and phone menu toggles, glasses swap with the theme
- [x] Cat hat redrawn as a witch hat (drooping tip, wide brim, lilac band, lime buckle) on every frame, plus a witch hat icon; on revamp in ce2f4b1 (not on main)
- [x] Cat bubble kept clear of the hero buttons (2f42954, live 20 Oct; checked on the live site at 1440 and 390 in both themes)
- [x] Cat wardrobe art imported (f4fc89e on revamp, not on main): hat, tie, glasses, bow and icons; verified in both themes and on a phone
- [x] Witch hat and its icon wired (ce2f4b1 on revamp, not on main); phone sweep only shows the known art-room fall passing over cards
- [ ] Witch hat tip clipped on Pounce 6 / React 3: taller cat canvas + unclipped export (deferred, M)
- [ ] Resume PDF still says "GenAI Product Designer (Consultant)": needs a new export from Sejal's source file
- [x] Art room sub-pages /art/comics and /art/motion (97d8d6b on revamp, not on main): One Last Chance panels, Pocket Toons strips and openings, The Last Over; Epifi comic episodes, full #futureofhr video, three launch film excerpts with no Tetriz (checked with whisper and frame sheets). Verified at 1440 and 390, both themes
- [ ] Comic videos: confirm which episode is the 30k-view one so it can lead the grid
- [x] Loader minimum 2 s to 1.5 s (eaba077 on revamp): exit starts at 1.51 s with the bar at the end of its track, gone at 1.74 s; reduced motion still skips (gone at ~0.45 s)
- [x] 22 Oct full checkup, live + revamp (report: https://claude.ai/artifact/KzQPUb8nqjEG47ZksjA6YL): 0 JS errors, 0 broken images, 0 axe violations, 0 sideways scroll on 10 routes x 1440/390 x both themes; all text tokens pass AA (lowest 4.99:1); Lighthouse phone perf live 93-100, revamp 87-99, a11y 100 on revamp; 33 of 36 links load, ArtStation and Behance block bots but open in a browser, LinkedIn not opened; phone sweep revamp 1 finding, live 5 (known cat over art cards, art pages not on live)
- [ ] Largest paint waits for the loader and intro rise (Motion 4.0 s, home 3.3 s on a local build): design trade-off, listed
- [ ] Home work tiles send 1168 px images to mid-size phones; an 876 px size would save ~120 KB (P2)
- [x] Findable worldwide (347976c on revamp, not on main): per-page title, description, canonical, hreflang en + x-default, OG and Twitter tags, generated pixel share image per page; sitemap.xml, robots.txt; JSON-LD Person + WebSite on home, CreativeWork per case study and art page; Lighthouse SEO 100 on the pages tested
- [x] Private stats page (revamp, review fixes in 0c26422: sign-in expires after 14 days, 31-day chart): secret path from STATS_PATH, password STATS_PASSWORD, noindex, unlinked, not in sitemap; visits from the Vercel Web Analytics API (documented May 2026, Hobby access unconfirmed), speed from Google PageSpeed (needs a free key); Speed Insights has no API so it stays in the dashboard
- [x] outreach-kit.md: Search Console, Bing (import from GSC), Yandex/Naver optional, stats env vars step by step, China reality check, free directories incl. Japan (foriio, pixiv, Skeb), Behance/Dribbble 6-week plan, 3 LinkedIn posts, cold message
- [x] 22 Oct: main at 0c26422 live (production build finished 14:50 UTC); sitemap.xml, robots.txt, share images and /art pages all 200 on production. The earlier 404s were checked before that build finished, not a code fault
- [x] 23 Oct: /analytics (cf97f51 on revamp, not on main): email + password sign-in from ANALYTICS_EMAIL / ANALYTICS_PASSWORD in Vercel, ANALYTICS link in the footer, noindex + robots disallow + not in sitemap; live visits, PageSpeed, and the 22 Oct checkup as site charts. Replaces the secret-path stats page and proxy.ts. Checked at 1440 and 390 in both themes; wrong password rejected; nothing leaks signed out
- [x] 23 Oct: asked the Studio skills workshop chat for a skills audit with current-vs-proposed flowcharts per skill (as a file, not an artifact); feedback logged: no artifacts unless asked
- [ ] Sejal: after the main push, verify Google Search Console + Bing, submit the sitemap, set the stats env vars (kit sections 1, 2, 5)
- [ ] Later, only if Japanese clients show up in stats: a real /ja/ version with hreflang (a ja meta description alone would not help)
- [x] Art round 2 (revamp, not on main): harness clip ends at 12.5 s before the blank; "coaching" clip replaced by "every week starts smarter" (5.7 s, product name on the memory card painted out frame by frame by scripts/film-mask.py, transcript clean); "How the videos were made" pipeline section from the comic memory notes; #futureofhr video and case-study preview card aligned in one column; AI-use note on each comic (One Last Chance none, Pocket FM generated then hand retouched/lettered/laid out, The Last Over Gemini + Claude with Photoshop handwork); art room nav (Illustration and Graphic open her other portfolios, no pages here); next-page card with the cat on Comics and Motion (shared NextPageCard); company logos in the experience tiles (Fi, AppsForBharat, Pocket FM from their own sites, Jeneko line art as a recolourable mask, freelance graphic keeps the cup icon)
- [ ] Video tile copy says "storyboards went from 4 days to 1"; the sources only show 1 day as the target. Confirm or soften
- [ ] #futureofhr: earlier directions v1 to v3 and the brief were not readable in Figma; add them if Sejal shares them. Check usage rights for the panelist photos and logos shown

**Before going public**
- [ ] Move the Figma files from the Epifi account to her personal account (Epifi account closes Nov 2026)
