# Portfolio traps: what cost rounds, and what worked

Oct 2026, Sejal's portfolio (directions v1 to the live pixel site), the pixel cat, the resume and career copy. Format: **symptom** → cause → fix / rule now. Instahyre, Sourced and Green Gallery design traps are in `lessons/design-traps.md`; not repeated here.

---

## A. Direction and taste

1. **"Looks like a junior designer made it"** (Figma v1 "Design / Ship", 11 to 16 Oct). → Off-white + ink + one orange accent + Geist + a hero toggle is the default house style of viral AI showreels; it reads anonymous. → Before proposing a palette, check it against the ban list in `playbooks/design-taste.md` / studio `taste.md`. Give the site a concept with personality, not generic "premium".
2. **Three full rebuilds in a week** (v1 Design/Ship, v2 Pencils/inks, v3 3D calligraphy "Signature", then pixel). → Big directions were built out (code-first, whole sites) before she had approved a style tile; each was impressive but not hers. → Gate every new direction with a style tile + one hero; build the rest only after she picks. The pixel direction survived because it came from her own brief (the cat) and was gated: answers > style tile + sprite sheet > cat prototype > home > case studies.
3. **Fully pixel would read as "game dev".** → Rule: pixel chrome, HD work. Pixel type only for headings/labels/keys; work at full resolution in a readable body font.
4. **Pixel heading font unreadable** ("the letter E is hard to read"). → Pixelify Sans' "e" fails even at Medium. → Jersey 15 for display. Test the letters e, a, s at real size before locking a pixel font.
5. **Hero subline hard to read; odd fill behind it.** → Low-contrast muted text and a decorative fill on body copy. → Muted text at 7.5 to 9.4:1; never put a fill behind a text line unless asked.
6. **"Use the libraries I gave you" / "check the libraries, bro".** → Claude kept hand-rolling effects she had pointed to libraries for (Experience still read as stacked cards after two rounds). → When she names libraries, survey their full catalogue first and say which component was used (scroll-craft zoom story, Vengeance UI light lines, Skiper underline). Free/MIT only; animmasterlib was paid-only, so skipped.
7. **"I didn't mean the checkered background everywhere."** → An example she gave was applied literally to every section. → An example is one option, not a template; give each section its own treatment (hero grid, work dot matrix, experience zoom frames, art pixel ice, contact dot paper).
8. **Logo "looks like a fucking spider".** → Cat ears + whiskers on a tiny badge. → Plain rounded-pixel "SB" badge, no ears, no whiskers, fill and text colours swap with theme, show the brand lilac/purple.

## B. Copy, truth and confidentiality

9. **Availability and title lines on the site** ("Consultant at Epifi until Nov 2026", "Open to product design roles from Dec 2026"). → Claude carried status copy from the plan. The consultant role is confidential and she does not want to "sell" availability. → Site shows only "GenAI Product Designer · Epifi Technologies (Fi Money)", since Jun 2026, no end date, no availability talk.
10. **Credit line "Some effects adapted from Vengeance UI (MIT)..." on the page.** → Licence credit placed in the footer. → Credits live in README and code comments only; she does not want to reveal tools to visitors.
11. **Resume bullets she could not defend** ("React kits", "removed internal taxonomy across 7 surfaces", the LinkedIn share loop that a colleague built, "sole designer", 30k views placed under the wrong employer). → Claude over-read memory notes into claims. → Every bullet passes: did she do it, where is the source, can she explain it in an interview. Ask her what she owned before writing.
12. **"I don't know Next.js / Tailwind, should it be on my resume?"** → Skills row overstated her front-end. → "Next.js/React codebase work with Claude Code, GitHub PR workflow, design tokens". Volunteer the Claude Code part early.
13. **Sourced count drift** (resume "Interviewed 25+", handover "27 responses", data in 1/28 steps). → Numbers copied between documents without checking the source. → "Surveyed 25+" everywhere; it was a survey.
14. **Unannounced launch film.** → Any frame with the product name leaks it. → Only the recommendations stretch up to the mouse click, product unnamed ("a B2B SaaS launch film"); check frames before cutting a loop.

## C. The cat

15. **"Cute at some places, distorted at others"** (cat v1, 32 px). → A 6 px eye on a 32 px canvas can only shrink into a corner when looking. → 48 px canvas, 8 px ring eyes, the fill narrows 1 px and slides, ring never breaks. Diagnose distortion frame by frame (audit.md) before redrawing.
16. **Head looked tilted.** → Eyes off-centre by a pixel (1/3/2 px). → Symmetric 2/2/2 eye spacing; check symmetry on every frame.
17. **Yawn "looks vulgar"; > o < read as a scream; a 4x4 mouth read as a nose; paws over the chin read as teeth.** → Facial marks on a faceless cat carry strong unintended meaning at small sizes. → Yawn = flat shut eyes + small V mouth + 2 fangs; peek paws beside the face. Compare variants side by side before choosing.
18. **Walk "unsettling", legs "connected to a common point", "jumping jacks".** → One-colour silhouette hid which legs were near or far; shared hip. → Each leg on its own hip, diagonal pairs, far legs in a second colour (`cat/body-far`), thicker hind thighs tapering to 5 px. Study real walk GIFs she sends.
19. **"Not what I want at all"** (a lilac neck line added to separate head and body). → Claude solved "distinct head" with a line instead of reshaping the pose. → Head on the front-top of the body, jutting past the chest, measured from her reference image. Later a lime belt + yellow bell joined head and body when walking.
20. **Belt and bell colours swapped twice; cat dropped on the left when she said right.** → Ambiguous pairs passed between chats in loose words. → Spec lines read back before building: `cat belt · colour · lime #D9F860`, `cat bell · colour · eye yellow`, `hero cat · drops on · right side of Jump Street`. Name both members of any swappable pair.
21. **Sitting cat stood up to glance.** → The idle loop borrowed Look frames, which became a standing pose. → Use Sit frames for glances and the no-room pet fallback; a sitting cat never pops up.
22. **"The cat spins insanely" / "takes its sweet time" / "randomly pops up".** → Too many spins, slow chase, peeks firing mid-scroll on unsettled tiles. → One clean fall (a couple of spins), 1 s delay then a fast run to the laser, peeks only on settled tiles and never while the walking cat is on screen, cat enters a section from the side it left by, rides its ledge off screen instead of vanishing.
23. **Accessories clash.** → "Any combination" was allowed. → Her rules: bow excludes hat and tie; glasses with anything; restored saves follow the same rules.
24. **Witch hat tip clipped on two frames.** → Accessories drawn inside the fixed 48 px frame. → Deferred; needs a taller canvas and an unclipped export. Plan headroom in the frame for future accessories.
25. **Cat edits in the wrong chat.** → Main chat tweaked sprites inline. → Standing: all cat art goes to the dedicated cat agent; the code chat only imports `frames.json` with `scripts/export-cat-frames.mjs`.

## D. Mobile and runtime bugs

26. **Phone scroll jumped back to the Art room (reported three times).** → The contact cat ran in from beyond the right edge, widening the page to 688 px, so the phone zoomed out (innerHeight 839 to 1402, no scroll call involved). → Clip the cat layer sideways; any off-screen element can widen the page. Reproduce on real device profiles with touch, measure innerWidth/innerHeight, find the root cause before patching.
27. **Experience blank on phones, pinned story buggy.** → Pinned scroll story assumed a desktop viewport. → Phones get a plain vertical list with reveals; reveals watch late content and only hide once running.
28. **Music silent on phones; first tap turned it off.** → `pointerdown` is not a user gesture on touch; toggle showed the saved preference, not actual playback; iOS silent switch mutes Web Audio. → Unlock on `pointerup`/`click`, remove listeners only once the AudioContext is running, play a silent sample + `audioSession` playback, toggle shows real state and blinks until the first tap.
29. **Cat intro stuck after a tab switch or tile hover during the drop.** → `visibilitychange` stopped the intro tick and nothing restarted it. → Finish (snap) the intro instead of stopping it; a two-reviewer code review found 15 such bugs before main.
30. **Bubbles leaking off screen or covering photos and the cat's own head.** → Bubble placement checked only against buttons. → Clamp 12 px inside the viewport, flip near edges, keep clear of images, headings, buttons and the cat (`data-bubble-keep-clear`). The phone sweep flags floaters over protected elements.
31. **Two go-to-top buttons in contact; doodle mode blocked scrolling up.** → Features added without checking overlaps with existing fixed controls and touch capture. → One go-to-top on desktop only; touch doodle captures only inside the pad.
32. **Repeated images side by side in the art collage.** → Random placement without an adjacency check. → Never the same image next to itself; rule is in house rules.
33. **Reload landed mid-page.** → Browser scroll restoration + stale hash. → Manual scroll restoration, always land on the hero.

## E. Process

34. **"Why is the new code not redeployed?" / "is it live?"** → Reports did not say what was on preview vs production. → Every report ends with Preview / Live / Waiting on you.
35. **"Give link n steps for Vercel, why do I even have to say it out loud?"** → Asked her to enable Analytics without the link or clicks. → Any outside step comes with the exact URL and numbered clicks.
36. **"Why do I have to run it? Why do I have to repeat myself?"** (/reload-plugins in every chat, retyping /studio). → Tooling put chores on her. → Live skills read steps from the repo; sticky studio mode; message other chats directly instead of asking her to.
37. **"Done" that she then found broken.** → Checks ran in the in-app browser pane, which pauses rAF and scroll when hidden, or not at all on phones. → Headless Playwright screenshots at 1440 and 390, both themes, plus the 4-phone sweep, looked at before reporting.
38. **Usage limits hit mid-round; office work at risk.** → Wide parallel research fan-outs and whole-page rebuilds. → When she says tokens are tight: P-ordered list, S/M/L sizes, do only what fits, park the rest in TIMELINE.md, one build and one deploy per batch.
39. **Production push blocked by the session's permission check.** → Expected. → Give her the exact command (`git push origin revamp:main`); never work around it.
40. **Figma files in a dying account.** → Everything was built in the Epifi Figma account (closes Nov 2026); copy-paste to her free account broke component instances. → Share + File > Duplicate; keep files at 3 pages for the free plan; do it before Nov.

## What worked (repeat these)

- **Advisor stance:** verdict + reason + risk in her own idea, then build. Questions she answered in a numbered list (17 Oct) settled scope in one round.
- **One tracker, many chats:** PLAN.md (detail) + TIMELINE.md (done/left, chat table with session ids). Separate chats for Figma, code, cat, automation and the skills workshop, coordinated with standalone hand-off notes.
- **Ship gate:** branch > Vercel preview > her OK > fast-forward main > check live. Old site frozen on a branch + tag, so replacing it was safe.
- **Cat as data:** ASCII sprite grids in Python > `frames.json` > export script > one canvas with integer device-pixel scaling and token colours. Theme swap, accessories and mirroring came almost free.
- **Motion review page** (an artifact with every cat state animated) before swapping art into Figma or code; she approved or rejected per state.
- **Real proof:** Playwright sweeps on four phones in both themes, recordings for scroll bugs, two independent code reviewers before main.
- **Recruiter-fast structure:** jump panel with keys 1 to 6, W A E C, Cmd+K, a case-study template with a sticky rail and a "what I would change" section.
- **Native, free polish:** generated chiptune (no licence), pixel cursor, OG card, Vercel Analytics + Speed Insights.
