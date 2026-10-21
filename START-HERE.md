# START HERE

You are picking up from a Claude that worked with Sejal every day from July to October 2026,
on a company account that was shut down. This repo is everything that Claude knew. Read this page
(2 minutes), then `CLAUDE.md` (how to work with her), then only the playbook for the task in front of you.
Don't ask her to re-explain context that is written here. Do check facts against the real files:
this was true on **22 Oct 2026**.

## Who she is, in one paragraph

Sejal Borkar, product designer, Bengaluru. Master of Computer Applications (Ramaiah Institute of
Technology, 2024 to 2025). Draws (comic artist since 2020; ArtStation jen_chan, Instagram _jeneko). Before Epifi:
AppsForBharat, Pocket FM, freelance graphic and art work. From June to November 2026 she was GenAI Product Designer
at Epifi Technologies (Fi Money) on Tetriz, a B2B engineering-intelligence platform: she made the
launch and explainer videos (Remotion), designed and shipped marketing-site feature pages and a quiz
app through Claude Code, and created a comic shorts series for the company's YouTube channel. Epifi
wound down in November 2026. She is now job hunting for **product designer (0 to 1, B2B SaaS),
design engineer, or brand/growth design** roles. Positioning: **"product designer who ships."**

Two facts to never get wrong:
- **Resume title is Consultant, not Intern** (HR retitled it, backdated to June). See `projects/career.md`.
- **Don't say her role ended or show an end date publicly** on the portfolio. Show the Epifi product design
  role without an end date. She ships front-end with Claude Code; never call her a "React developer".

## How she wants you to work (the short version of CLAUDE.md)

Senior advisor, not assistant. Verdict first, evidence second, then build. Push back, including on her,
and don't flip to whoever spoke last. Measure (diff frames, check bounding boxes, time it) before
opining. Small reviewable steps. Verify with your own screenshot before saying done. No em dashes,
no tilt, no overlaps, no paid tools, no AI-generic editorial look, After Effects-grade motion.

## What's live and where it stands

| Area | State (22 Oct 2026) | Read |
|---|---|---|
| **Portfolio site** (top priority) | Live at sejalborkar.vercel.app, repo SBorkar2002/my-portfolio. "Pixel chrome, HD work" concept with a pixel cat mascot. Six case-study pages live (marketing site, Sourced, #futureofhr, AFB blog, video system, lead-gen assessment). Pending list in the playbook | `playbooks/portfolio.md` |
| **Job-hunt automation** | Instahyre (hourly) and Wellfound (:30) auto-apply bots on the Mac, logging to a Google Sheet; Apps Script cloud half parses Gmail alerts and career pages. Runs on her personal Google account. Mac half must be reinstalled on the new laptop | `playbooks/job-automation.md`, `setup/job-automation-migration.md` |
| **Comic shorts** | 5 episodes + a prompt-engineering episode finished for the AI FOMO channel ("I Have No Idea What That Means"). The craft is her portfolio material now | `playbooks/comics.md`, `projects/comic-series.md` |
| **Case studies / take-homes** | Sourced (done, on the site), #futureofhr / Instahyre take-home (done), AlterOffice cricket comic, UXpective. Green Gallery was DROPPED; do not revive unless she asks | `playbooks/case-studies.md` |
| **Studio plugin** | Her own Claude Code plugin: `/studio` routes change requests to code/figma/flow doctors, with a progress side panel. Repo SBorkar2002/studio | `setup/studio-plugin.md` |

## Your first session on the new account: check these

1. `~/.claude/CLAUDE.md` exists (if not, run `./install.sh` in this repo).
2. Figma: which account is she logged in as now, and can you open her portfolio file? The old Figma login
   was the company email; file ids in `memory/` may have changed if she duplicated files to a new account.
   Ask her for the new links rather than guessing.
3. Job bot: run `npm run doctor` in `~/Documents/career/automation-scripts` and follow the migration doc.
4. Then ask her what she wants to do first. Likely candidates are in "Next moves" below.

## Next moves (as of 22 Oct 2026)

1. **Portfolio:** work the pending list in `playbooks/portfolio.md` section 9: an /art route (illustration, comics,
   graphics, motion; the comic episodes belong there), recruiter summary at the top of each case study, missing
   Before/Reflection sections, a Lighthouse pass, the Cmd+K palette, phone layouts.
2. **Job bot:** reinstall on the new Mac; then add the next sources (Cutshort, Naukri, Hirist, YC Work at a
   Startup). LinkedIn stays manual (ban risk). Update answers that mention Epifi as current company.
3. **Resume and positioning:** keep in sync with the portfolio (`projects/career.md`).
4. **Comics:** optional, if she continues the series personally; backlog in `projects/comic-series.md`.

## Map of this repo

```
CLAUDE.md          standing rules (installed globally by install.sh)
install.sh         restores rules, memory, skills, plugins on a new Mac
memory/            76 atomic facts from 4 months, indexed in memory/MEMORY.md
playbooks/         how to do each kind of work, step by step
lessons/           traps that cost hours (symptom, cause, fix) and what worked
projects/          state of each live project
setup/             plugins, skills backup, connectors, tools, studio plugin, job-bot migration
tools/comics-video comic Remotion source + Python build scripts
archive/           raw conversation exports and saved artifacts (grep for details)
```

## When a playbook and memory disagree

`memory/` files are dated facts written in the moment. Playbooks are later syntheses. If they conflict,
the more recent dated statement wins; if still unclear, ask her. When she gives a new standing rule, add it
to `CLAUDE.md` (if it applies everywhere) or the relevant playbook, AND to memory, then commit and push
this repo (`SBorkar2002/claude-brain`). Keeping this repo current is part of the job.
