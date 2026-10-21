# Web build: how to build and change web pages with Sejal

How Sejal and Claude build sites together: Next.js pages, Figma-to-code, verification, PRs, deploys. Read `playbooks/design-taste.md` first for what things should look like. This file covers how to build them and ship them.

Her own codified version of this lives in her `studio` plugin (`~/Documents/Github/studio/plugins/studio/`, private repo SBorkar2002/studio): `skills/code-doctor/steps.md`, `ship.md`, `mobile.md`, `shared/verify.md`. If that plugin is installed, `/studio` routes to it. This playbook matches it and adds the history behind it.

---

## 1. Who does what

- Sejal makes the design calls and drives through Claude Code. She is a beginner in React and does not read Tailwind fluently (her words, Oct 2026). Explain changes in plain language: what changed on screen, not which hook.
- Claude writes the code, proves it works and ships it on her OK.
- She sometimes edits in parallel with ChatGPT ("tell me the location where the code is, I'll give it to chatgpt"). Give exact file paths when asked. Before your next edit, read the diff of what changed and keep their additions (she had asked ChatGPT for a hover effect and ghost panels; those were intended, not bugs).
- Teammates and other Claude sessions also push. Always `git fetch` and look at recent commits on the target area before editing (a teammate's PR #7214 had already shipped half of a quiz fix).

## 2. Stacks she has shipped

| Project | Stack | Notes |
|---|---|---|
| Tetriz marketing site (Epifi, Aug 2026) | Next.js 16 App Router, `output: export` (static), Tailwind v4 with `--site-*` tokens, framer-motion, lucide-react, pnpm workspace | repo `workloom-dev/core`, `client/workloom/site`; access ends with the Epifi account (Nov 2026) |
| AI-Native Index quiz (Epifi, Jul 2026) | Next.js 16, Tailwind v4, Framer Motion, GSAP, vitest | `client/workloom/quiz-app`; pure scoring in `src/core`, copy in `src/content` |
| Portfolio (personal, Oct 2026) | Next.js 16 + React 19, Tailwind v4, GSAP (ScrollTrigger, Flip), Lenis, Motion; v3 also R3F/drei | `SBorkar2002/my-portfolio` → Vercel `sejalborkar.vercel.app`; see `playbooks/portfolio.md` |

- Use the project's tokens, never raw hexes copied from an artifact or Figma. On the Tetriz site: `text-pr`/`bg-pr` (teal), `text-fg/fgm/fg2`, `border-bd`, `bg-bg`, `--color-site-stage-*` for the 5 maturity levels.
- Check current APIs with Context7 when touching Next 16, React 19, Tailwind 4, GSAP or Lenis. Do not trust memory for these.

## 3. The loop (every change request)

1. **Intake.** Turn her message into a numbered checklist, P0 first, one line per item. She often sends 5 to 10 numbered items in one message; miss none (she notices: "I also asked you to add a header ... did you miss that?").
2. **Read back visual specs** as `element · property · value` before building, using the project's token or hex, never "green". If two words could swap (left/right, belt/bell), name both. Ambiguous item → numbered question first.
3. **Reproduce.** See the bug yourself at the width and theme she named.
4. **Diagnose** one line per item: where (file:line), why (cause, not symptom), fix (smallest change).
5. **Fix** only what she asked. Touch nothing else.
6. **Verify** (section 5). Look at every screenshot yourself.
7. **Ship gated** (section 7).
8. **Report** in about 5 lines + the status block (section 7). Update the project's single tracker (TIMELINE.md or README status). Do not create new status files.

Build big things in steps: one section or page fully finished, she reviews, then stamp the template. On the Tetriz site the AI Adoption page was finished first, then its kits were reused for AI Impact, Session Security, AI ROI and Why Tetriz.

## 4. Running it locally

- She often asks "can you locally host it so I can test it": pull/checkout the branch, install, run the dev server, give her the URL.
- `preview_start` cannot start servers in some folders (macOS EPERM on `~/Documents`, pnpm workspace roots, new folders). Then run the dev server with Bash in the background (sandbox disabled if needed), and add a url-only entry to `.claude/launch.json` to attach the Browser pane. Example used: `pnpm --dir <site> exec next dev --turbopack --port 3001`.
- Anandhi's rule for the feature pages: build "locally only, so anyone can play": real code on a branch, not another HTML artifact. Artifacts were fine for the first exploration; once the direction was set, code.

## 5. Verification before "done"

She will not accept "done" without proof, and "I couldn't watch it" is a defect, not a footnote.

- `typecheck` and, before any ship, a full `build`.
- **Do not trust the in-app Browser pane for motion.** When the pane is hidden, `document.visibilityState` is `hidden` and `window.innerHeight` can be 0: CSS transitions and rAF (framer-motion) freeze at their start value, `whileInView` never fires, `100vh` sections collapse to 0, screenshots come back blank. Probing an animated end state there gives false readings; do not "fix" logic based on them. Cost hours on 4 Aug.
- Use a headless browser instead: her `scripts/shots.mjs` (studio plugin) or Playwright. Screenshot 1440 and 390 widths, light and dark themes if the site has both. For motion capture frames over time; for scroll capture beats (`--at "#work@0.5"`).
- For logic, read React-driven values (`className`, `aria-expanded`). For a transition's end state: set `style.transition='none'`, force reflow (`void el.offsetHeight`), then read `getComputedStyle`.
- For charts: measure, do not eyeball. `getBBox()` for labels, `getPointAtLength()` to check markers sit on the curve and labels clear it by ~20px, and that everything stays inside the plot bounds.
- Lint copy for em dashes (`copy-lint.py --diff` in the studio plugin, or grep for the character).
- Phones: emulate touch at 390 (not just a narrow desktop window). Most bugs she finds herself are phone bugs. Her `sweep.mjs` runs four phones in both themes.
- Pages nobody asked to change: before/after screenshot diff; any unexpected change is a regression.
- Send her the key screenshots and say what each proves. If something truly cannot be verified (scroll feel, Figma Present mode), say exactly what, and give her the exact steps to check in under a minute.

## 6. Code patterns and traps from her builds

**Motion that actually runs in her browser (Tetriz site, Aug 2026):**
- framer SVG transforms (`motion.g` x/y, `motion.circle` cx/cy keyframes) and `AnimatePresence` animating `height: auto` did NOT animate for her. Reliable: CSS transitions on `opacity` and `cx`/`cy` (via `style.transition`), `strokeDashoffset`, framer `pathLength`, `opacity`, and the `grid-template-rows: 0fr ↔ 1fr` trick for expanders.
- `AnimatePresence mode="wait"` stalls when the swapped child has `whileInView` descendants (new child never mounts). Fix: plain keyed remount (`<motion.div key={active} initial animate>`), and inner animations animate-on-mount so they replay on each swap.
- Easing: expo-out `cubic-bezier(0.16,1,0.3,1)`; marker glide `cx 0.7s` / `cy 0.7s` on that curve.

**Scrollytelling recipe (her standard "how it works" section):**
- Outer section `height: N*100vh`; child `sticky top-0 h-screen` pins.
- `useScroll({ target, offset: ["start start", "end end"] })` + `useMotionValueEvent` → discrete active index; `useTransform` for a progress bar (divider `scaleX`).
- Left: editorial list, no boxes, dividers double as progress; active item expands (title + lead + bullets).
- Right: clipped stage (`overflow-hidden rounded-[32px]`, brand teal gradient `linear-gradient(135deg,#0096BB,#06788F,#064A5C)`), one sharp hero dashboard + one skeleton dashboard peeking behind; hero fully inside with padding.
- Click-to-jump: each lens is a `<button>`; `goTo(i) = window.scrollTo({ top: wrapTop + ((i + 0.5) / N) * (el.offsetHeight - innerHeight) })`.
- Mobile: split a lens into per-panel dashboards ONLY if the full dashboard overflows the stage at phone size. Measure first; never split by default.

**Layout and platform traps:**
- Fixed-position nav buttons drift when the card is vertically centred (`justify-center`): any height change moves the footer. Fix with consistent container heights (`min-h-[...]`) AND top-anchored cards, footer `mt-auto`.
- GSAP parses inline `translateY(%)` into px `y`: use `fromTo` with `{ y: 0, yPercent: 125 }`.
- Grids around fixed-width demos blow out on phones without `grid-cols-[minmax(0,1fr)]`.
- Full-height sections: `100dvh`/`svh`, not `100vh`.
- Anything animating in from off-screen widens the page and jumps scroll: clip the container (`overflow-x: clip`).
- Sound needs a completed tap (`pointerup`/`touchend`/`click`); "autoplay with sound" is impossible, say so.
- No hover on phones: anything revealed on hover needs a tap or always-visible state.
- `visibilitychange` pauses must resume cleanly; a loader/intro must never stay stuck after a tab switch.
- A page reload should land on the hero (she asked for this on the portfolio).
- SVG needs explicit `width`/`height` attributes or it can collapse; CSS `var()` works in SVG `fill` attributes.
- Dark mode: give always-dark panels their own token; never reuse a text token as a panel background.
- Results that depend on user state near an edge (a "You?" label at the top of a chart) must flip side so they never get cut off.
- State that should survive refresh (quiz progress) goes in `localStorage` with resume-on-refresh.
- Share links: LinkedIn's `share-offsite/?url=` accepts only a link, not post text. Working pattern: copy a short caption (several rotating variants) to the clipboard synchronously on click BEFORE opening the LinkedIn tab (async `writeText` loses focus and fails silently), show "caption copied", and show the text inline if copying fails. A teammate later merged a "prefill LinkedIn share" fix (#6857); its method is unclear from history.

**Assets and credits:**
- Self-host images; reuse what she already provided (search `public/` before drawing or generating). Official SVG logos for tools (simpleicons). Distinct avatar per person.
- Never print library credits on the page ("Some effects adapted from ...": "we're basically giving away our information"). Credits go in the README.

## 7. Git, PRs, deploys

**Branches**
- Always `git fetch` and branch fresh off `origin/master` (or `main`) before new work. A quiz batch built on a 2-PR-stale base had to be ported, and she asked to close that PR and open a fresh one on updated master.
- Branch names used: `sejal/<topic>` (e.g. `sejal/site-feature-pages`, `sejal/quiz-v3-followups`); portfolio previews on topic branches (`revamp`, `pixel-v1`).
- Never force-push. On the portfolio never touch branch `old-portfolio` or tag `old-portfolio-final` (the old site's history).

**Commits**
- Conventional Commits, scoped: `feat(site): feature-page scrollytelling, org-scale template, maturity-curve redesign`, `fix(site): distinct team avatars on AI ROI`, `feat(quiz-app): position chart, required details gate, mobile UI on v3`. No em dashes. End with the Co-Authored-By line.
- Commit only the files for this change (`git add <paths>`), not everything dirty.

**PRs (standing authorization, Aug 2026)**
- Create PRs without asking. She was angry at being asked again ("you are allowed to create PRs ... do not make me ask you this again"). Return the link. If she says "only the link", give only the link.
- **Never merge to main/master.** Merging is the human's call. (Exception: her own `SBorkar2002/studio` plugin repo, which she lets Claude push directly.)
- Title: valid Conventional Commits, company standard.
- Description must cover everything: summary, changes grouped by area, files touched, verification, open items. If the repo has `.github/pull_request_template.md` or she gave a format, follow it exactly.
- **Two description modes:**
  - New branch: lead with WHAT changed and WHY.
  - More commits on an existing PR branch: one-line summary, one sentence of overall intent, then per-area tables `| | Before | After | Why |`, then a Verification line. Model: PR #6800 in workloom-dev/core.
- The PR body describes the FINAL diff only. She caught "Product Overview" listed in a body after the page had been removed: "why is it in the pr body".
- Push follow-up commits to the same branch; the PR updates itself. Say so.
- Repo merge gates are real work: Epifi core needed a linked issue (`Closes #N`), a green local `lci` run, the `RunWorkflows` label, and a grounded reply to every Codex bot review thread. In any new repo, read CONTRIBUTING and `.github/` before opening the PR.

**Status, every time**
She repeatedly had to ask "is it pushed?", "is it merged?", "will it show on the live URL now?". End every ship report with:
```
Preview: <url> · <commit>        (or "none")
Live:    main <commit> · deployed yes/no · checked in both themes yes/no
Waiting: <what she needs to do>, or "nothing"
```

**Deploys**
- Personal sites: Vercel. Push the branch → Vercel makes a preview → she reviews → only on her explicit OK ("Preview looks good, merge revamp to main and ship it live") fast-forward `main`, push, wait for the production deploy, then check the live site in both themes and on a phone.
- Vercel previews sit behind Vercel login: curl gets a redirect. Check the preview in the browser pane or via `gh api` deployment status.
- If a permission check blocks a production push, tell her the exact command to run. Do not work around it.
- If the stack changes, check Vercel's framework preset and build command before the first deploy.
- If design is still in Figma, say so before she asks why nothing redeployed; offer a preview branch so she can scroll the real thing early.
- Company site (tetriz.ai / workloom.dev): Sejal pushed branches and PRs; teammates merged and deployed. A manager reference build ran on Netlify. Who deployed production is unclear from history.

## 8. Figma side (wireframes, hi-fi frames, Figma-to-code)

- Load `figma:figma-use` before any `use_figma` call; `figma:figma-design-to-code` before `get_design_context`. Batch-load Figma tool schemas in one ToolSearch call.
- **Re-inspect node ids every session.** She edits frames between turns (renames, re-centres, swaps icons); old ids go null. Re-screenshot before touching.
- **Never edit an original.** Duplicate the frame/page and work beside it. Use File > Duplicate, not copy-paste: copy-paste breaks prototype links and component access across accounts.
- `figma.createAutoLayout()` frames default to a solid WHITE fill and `clipsContent = true`. On any non-white ground they show as faint white boxes behind text. Set `.fills = []` on every wrapper at creation. To retrofit, clear white fills where `cornerRadius === 0 && no strokes && no effects` (that spares real cards). `clipsContent` does not tell wrappers from cards.
- `resize()` after setting `layoutSizing` resets FILL to FIXED: set sizing after resize. After resizing a text box, re-set `textAutoResize` or it collapses to one line. Confirm exact font style names with `listAvailableFontsAsync` ("SemiBold" vs "Semi Bold").
- A transport/connection error does not mean the script failed: re-read the node before retrying or you duplicate work.
- Nested-node `get_screenshot` sometimes returns 1x1: retry or screenshot the root frame.
- Figma has no on-scroll trigger. For scroll-like reveals use interactive component variants (Static → Idle → phases → Done) with MOUSE_ENTER or ON_CLICK and Smart Animate. Push/slide transitions are not settable inside components via the API: use dissolve or instant and tell her.
- Claude cannot play Present mode. List the exact hotspots and keys she should try, in order.
- QA every changed frame for overlap, text spilling out of its parent, em dashes in text AND layer names, off-system fonts, collapsed text boxes (her `figma-qa.js` in the studio plugin does this).
- Her Epifi Figma files die with the account in Nov 2026. Anything worth keeping must be duplicated to her personal account first.
