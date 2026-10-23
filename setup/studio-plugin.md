# Studio plugin (`/studio`): Sejal's own Claude Code plugin

Built 20 Oct 2026 for her personal projects (portfolio site, Figma frames, case studies, take-homes, job-hunt automation). Not for Epifi work.

## What it is

One entry point she types in any chat: `/studio` (skill `studio:studio`) + a change list. It reads which chat/project it is in, turns her note into a P-ordered checklist, routes each item to the right "doctor", proves each fix, and returns one short report. She rejected 6 to 7 separate skills as too many; this is one router + three doctors that can call each other.

```
/studio  (router: detect > plan > route > verify > report)
  code-doctor    web code: reproduce, diagnose (file:line, cause, fix), screenshot proof, preview then ship on her OK
  figma-doctor   Figma: keep the original safe (duplicate), fix in batches, figma-qa.js, before/after screenshots
  flow-doctor    automation: dry run first, hard safety limits, plain-language flow explanation
shared/   house-rules · verify · truth · taste · handoff · private.local (git-ignored)
scripts/  detect.sh · shots.mjs · sweep.mjs · shotdiff.mjs · copy-lint.py · figma-qa.js · feedback.sh
hooks/    guard.py: block force-push and any git op on old-portfolio; flag em dashes on Edit/Write
```

Why it exists (from her session insights): the biggest waste in her portfolio chats was styles reworked after building, "done" claimed without proof, rules restated every round, research nobody used, and usage-limit hits from wide agent fan-outs.

## Where it lives

- GitHub: `SBorkar2002/studio` (PRIVATE, her personal account), branch `main`. Latest pushed commit 22 Oct: `df89da0` "feat(studio): live skills, so updates reach open chats without a reload". One uncommitted local change: a FEEDBACK.md row (20 Oct, Vercel Analytics steps). Commit and push it.
- Local: `~/Documents/Github/studio`. Marketplace name `sejal-studio` (`.claude-plugin/marketplace.json`), two plugins: `studio` 0.2.0 (`plugins/studio`) and `studio-board` 0.2.0 (`plugins/studio-board`).
- Standing rule: commit AND push this repo to `main` without asking her each time; bump the version when stubs, descriptions or the board change. Never force-push. (Other repos keep their own rules: preview first, ask before main.)

## Install on a new machine

```bash
gh auth login                      # as SBorkar2002 (private repo)
git clone https://github.com/SBorkar2002/studio.git ~/Documents/Github/studio
claude plugin marketplace add ~/Documents/Github/studio      # local directory marketplace, as on her old Mac
claude plugin install studio@sejal-studio
claude plugin install studio-board@sejal-studio
npm install -g @playwright/cli@latest                        # for shots.mjs / sweep.mjs
```

Alternative without cloning: `claude plugin marketplace add SBorkar2002/studio`. Prefer the clone, because the live-skill stubs read from `~/Documents/Github/studio/plugins/studio` when that folder exists.

Then by hand:
- Recreate `plugins/studio/shared/private.local.md` (git-ignored). It held confidential rules and banned strings (for example: the Epifi consultant title and end date must never appear on anything public). Rewrite it from `projects/career.md` and `playbooks/portfolio.md`; never commit it, never quote it publicly.
- Needs: Python 3 (hooks, copy-lint), Node 20+, Chrome (shots use channel "chrome"), Figma MCP signed in via /mcp for figma-doctor, Context7 signed in if used.
- New chat after installing. `/reload-plugins` is only needed after changing a stub, a description or the board mod.

## How updates reach chats ("live skills", 0.2.0)

Each installed `SKILL.md` is a short stub that says: read `<studio>/skills/<name>/steps.md` and the shared files, where `<studio>` = `~/Documents/Github/studio/plugins/studio` if it exists, else the installed copy. So editing `steps.md`, a reference file, a shared rule or a script reaches every open chat on its next request. Never tell her to run /reload-plugins for a steps change (she refused to do that in every chat); message the chats instead. For stub/board changes: `claude plugin marketplace update sejal-studio` then `claude plugin update studio@sejal-studio`.

## The router (`skills/studio/steps.md`)

1. Read the room: `bash <studio>/scripts/detect.sh "<her message>"` prints kind (code / automation / figma), repo, branch, dirty files, last commit, tracker path, launch config. Read the tracker's chat table ("Who does what") to know which chat owns what.
2. Plan: one numbered checklist, tags `code` `figma` `copy` `taste` `cat` `automation`. Keep her order; else P0 = broken or embarrassing, then what a recruiter sees first, then polish. Under a token budget ("conserve"), size items S/M/L and defer the rest into the tracker. Ask ambiguous items now, numbered, in one message.
3. Route: load the doctor; items owned by another chat go through `handoff.md` (SendMessage with a standalone note: From, Item, Where, Why, Done when). Read-only work can go to cheaper-model subagents; never two writers on the same files.
4. Close the loop: proof per `verify.md`, `copy-lint.py --diff` clean, tracker updated.
5. Report: about 5 lines + proof files, what is verified and what is not, one decision she must make. Never ship to production without her explicit OK.

## The doctors

**profile-doctor (added 23 Oct, studio 0.3.0):** read-only LinkedIn profile review. Reviews every section for reach
with recruiters and clients, ranks fixes P0 to P2 in one tracker (`~/Documents/career/linkedin/LINKEDIN-TRACKER.md`,
copy in `projects/linkedin-tracker.md`), and for "we're covering item N" gives Now / Change to / Keep / Why / Where to
click / Check after. Never edits the profile or drives LinkedIn. Search words are tied to the job bot's title tracks;
it checks consistency against resume and portfolio. The router sends LinkedIn work here. A skills checkup doc with
current vs proposed flowcharts was also added (commit d62c822).

- **code-doctor** (`steps.md`, `mobile.md`, `ship.md`): intake with detect.sh; visual asks turned into exact spec lines read back before building (element · property · value with the site's token, naming both of any swappable pair like belt/bell, left/right); reproduce with headless screenshots, never the in-app pane alone (it pauses rAF and scroll); diagnose one line per item (where, why, fix); smallest fix; verify (typecheck, build, 1440 + 390 in both themes, copy-lint, console); medium/large rounds also get /code-review, the 4-phone x 2-theme sweep and a before/after diff of untouched pages; ship = branch > preview > her OK > fast-forward main > check live; every report ends with a Preview / Live / Waiting status block; up to 3 ranked next ideas when asked. Cat sprite drops from the cat chat are imported without asking her (asset contract in `handoff.md`).
- **figma-doctor**: load `figma:figma-use` before any `use_figma`; read only the target node; duplicate originals and work side by side; run `figma-qa.js` (overlaps, text spilling, em dashes, off-list fonts, collapsed text boxes, empty frames); known traps (load fonts first, re-set textAutoResize after resizing, confirm exact font style names, re-read nodes after a transport error, stale ids after deletes, no push/slide transitions via API, no Figma AI credits); list exact hotspots/keys for her to test in Present.
- **flow-doctor** (`steps.md`, `new-site.md`, `run-health.md`): hard limits (no CAPTCHA bypass, no credentials in code or chat, private answers in git-ignored files, unknown form questions marked "Needs you", per-site daily caps, messages to people only drafted, warn about site terms); dry run first, one live item only after her OK; new job sites follow a staged playbook; Sheet values in plain words and IST dates.

## Shared rules (`plugins/studio/shared/`)

- `house-rules.md`: advisor not assistant; ask when confused (numbered); scope is sacred; one tracker; never "done" without proof; log skill feedback; design rules (no em dashes, no tilt, no overlap, short subtexts, hero = eyebrow/headline/lede/CTAs only, no AI-generic look, After Effects-grade motion, graphics from the page's own system, no repeated images side by side, no paid tools); git rules (Conventional Commits, branch > preview > main on her OK, never force-push, never touch old-portfolio).
- `taste.md`: the gate (max 8 references each mapped to a section > one style tile > her pick > tokens > distinct register) + the AI-generic ban list (editorial serif + mono labels + hairlines; off-white + black + one orange; purple-blue gradients, glossy 3D clip art; cards everywhere; Inter/Roboto/Space Grotesk by default; fade-up on everything, bounce, scale pops; decorative chips). Tool picks: impeccable for critique, taste-skill only for a new direction (~9k tokens), emil-design-eng / apple-design for motion, playground for live tuning.
- `truth.md`: three questions per claim (did she do it, where is the source, can she defend it); Claude credited only for what Claude did; she works in Next.js/React WITH Claude Code, not as an engineer; one user is not "users"; public material only for employer/client work; resume tone not AI-sounding, ATS-friendly.
- `verify.md`: what counts as proof per area (code, Figma, automation) and how to report "not verified: why, how she can check in under a minute".
- `handoff.md`: doctor-to-doctor calls, cross-chat notes, asset drops (cat `frames.json` > `node scripts/export-cat-frames.mjs` > sweep > preview > reply to the cat chat).

## Scripts

- `detect.sh`: chat kind and repo state.
- `shots.mjs`: headless Chrome screenshots: `--url --widths 1440,390 --themes light,dark --paths --at "#work@0.5" --frames 6 --interval 150 --still --tag before`.
- `sweep.mjs`: phone sweep (iPhone 13, Pixel 7, iPhone SE, iPhone 15 Pro Max x 2 themes), touch scroll, paint order, floaters covering photos/headings/buttons; per-repo config `.studio/sweep.json`; proof in `.studio-proof/` (git-ignored).
- `shotdiff.mjs`: pairs before/after shots of pages nobody asked to change.
- `copy-lint.py`: em dashes, banned words, AI tone; `--diff`; `lint-ignore` marker.
- `figma-qa.js`: read-only audit pasted into `use_figma` with `ROOT_IDS`.
- `feedback.sh "<chat>" "<skill>" "<what happened>" "<rule>"`: appends to `FEEDBACK.md` (Open table). A "Studio skills workshop" chat turned rows into rule changes and moved them to Done.

## studio-board (the side-panel mod)

- Opens when any studio skill starts. Shows phase stepper (Read, Plan, Route, Fix, Verify, Ship, Report), checklist with status per item, live tool activity, hand-offs, links, proof, "needs you", log. Desktop-native layout (v0.2.0 after she called the first UI "ass"); terminal keeps glyphs.
- Updated by the model through tool `mcp__studio-board__progress` (items merge by id; send only what changed).
- **Sticky studio mode:** once any studio skill runs in a chat, every later plain message is treated as a studio request (she refused to retype the command). Stored per session; survives restarts. `/studio-off`, `/studio-on`, `/studio-board` (reopen), `/studio-board-reset`.
- Dev gotcha: validate/test the mod with the Claude desktop APP's bundled `claude` binary; the older `claude` on PATH wrongly rejected `update($, ...)`. Tool args sit on `e` itself, not `e.input`.

## Plugins installed alongside (20 Oct) and held back

Installed: impeccable, taste-skill, playground, context7, serena (needs `uv`), code-simplifier, chrome-devtools-mcp, hookify, claude-md-management; skills playwright-cli, deploy-to-vercel, web-design-guidelines, vercel-react-best-practices. Held back on purpose: context-mode and RTK (lossy tool-output rerouting), superpowers (clashes with /studio), caveman.

## Cost

About 400 tokens always-on, about 0.8k to 1.1k per skill call.
