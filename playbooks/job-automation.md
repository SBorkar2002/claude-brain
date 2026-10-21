# Job-hunt automation: playbook

State as of 22 Oct 2026. Built 19 to 22 Oct 2026 in one Claude chat ("Automation scripts") with Sejal.
Migration steps: `setup/job-automation-migration.md`. Traps and fixes: `lessons/automation-traps.md`.

## Where things live

| What | Where |
|---|---|
| Code (private) | github.com/SBorkar2002/job-hunt-automation, default branch `main` |
| Local checkout (old laptop) | `~/Documents/career/automation-scripts` |
| Tracker (single source of truth) | the repo's `README.md`: requirements, her answers, decisions with dates, status. Read it fully first, every session. Write new answers and decisions there, never in extra tracker files |
| Google Sheet "Job hunt tracker" | https://docs.google.com/spreadsheets/d/1tj34leK-HVtZBhOoofL1ZZaOrc-_eXlE5gfaafy1E68/edit |
| Apps Script project "Job hunt bot" | https://script.google.com/home/projects/1wpIEesipTmHfU6vfUP5B73G0GZpspTfby8f32XTX-2SvgsuhBGFTT9CQ/edit (scriptId also in `.clasp.json`) |
| Google account owning Sheet + Apps Script + Gmail it reads | her personal Gmail, sejalborkar2002@gmail.com (confirmed by `clasp login` output, 20 Oct). Not Epifi |
| Flow page | `docs/workflow.html` in the repo (scroll-driven node diagram, one section per site). Was published as claude.ai/artifact/9No5UMQKk65HViTicyM6SB on the old Claude account: republish from the file |
| Rules for working on it | studio plugin skill `flow-doctor` (repo SBorkar2002/studio, `plugins/studio/skills/flow-doctor/steps.md`, `new-site.md`, `run-health.md`) |

## Goal and her standing decisions

- Goal: be among the first applicants on good-fit fresh design roles, so she can work on other projects while the hunt runs. Fit beats volume; filters stay strict.
- **Auto-apply, no approval step** (her call, 20 Oct): bots apply on their own within the rules below and log every action in the Sheet. She reviews the Sheet and asks the automation chat for changes. Anything needing her is a Sheet row with Action/Status "Needs you" plus the reason.
- **No Telegram, no pings** (dropped 20 Oct). The Sheet is the alert surface; email only to herself (health, weekly, Wellfound messages).
- **LinkedIn: never automated** (no login, no scraping). Alerts-by-email only.
- Each site is its own module; one shared Sheet, one shared config, one shared runner.
- Free tools only. Ask before anything paid.
- She accepted the account risk in writing for Instahyre (cap 10/day) and Wellfound (cap 5/day). Cutshort skipped after its terms check (permanent suspension clause). Naukri auto-apply: undecided (see Open).

## Architecture

```
GOOGLE CLOUD (Apps Script, runs with laptop off)        HER MAC (launchd timer, 8am to 11pm IST)
  checkAlerts   hourly  Gmail alerts -> rows             Instahyre  :00 hourly  -> apply (cap 10)
  checkPages    hourly  Lever/Greenhouse/Ashby -> rows   Wellfound  :30 hourly  -> apply w/ approved note (cap 5)
  checkReplies  hourly  company replies -> Status                                 + read Messages -> email her
  healthAlert   hourly  red 3h+ -> email her             npm run fill -- <link>  (manual, she submits)
  followUps     daily 9am  -> Follow-ups tab drafts      npm run doctor / status / sheet:peek
  weeklySummary Sun 7pm   -> email her
  doPost web app  <---- Mac scripts POST rows here (secret-protected) ----
                          |
                    Google Sheet (tabs below)
```

- **Mac side:** Node.js (ES modules) + Playwright 1.48.2 driving the real installed Google Chrome (`channel: 'chrome'`, headful). Nothing is injected into websites. Each site has its own persistent Chrome profile in `~/.jobbot/profiles/<site>` that she logs into once.
- **Cloud side:** Apps Script (V8, timezone Asia/Kolkata) in her personal account. Files in `apps-script/`: `Tracker.gs` (Sheet format, web app `doPost`, rows, Runs/Health, Messages), `Mail.gs` (Gmail alerts, replies, follow-ups, emails, triggers), `Pages.gs` (career-page watcher), `Config.gs` (GENERATED from `shared/config.json` by `scripts/sheet-deploy.sh`; never edit by hand), `appsscript.json` (web app: execute as deploying user, access ANYONE_ANONYMOUS).
- **Mac to Sheet link:** web app URL + `SHEET_SECRET` in `.env`. `shared/sheet.mjs` POSTs `{secret, action, tab, job, ...}`. Retries 0/5/15/30s; failed writes queue in `~/.jobbot/state/pending-rows.json` and flush next run.
- **Deploys:** `npm run sheet:deploy` = regenerate `Config.gs`, `clasp push --force`, `clasp deploy --deploymentId <id from SHEET_URL>` (same URL, new version; was at version 16 on 22 Oct), then calls the `setup` action to reapply formatting and migrate old rows.
- **Timer:** `scripts/timer.sh` writes `~/Library/LaunchAgents/com.sejal.jobbot.<site>.plist` (StartCalendarInterval hours 8..23 at the site's `runMinute`) and rsyncs the repo to `~/.jobbot/app` (macOS blocks launchd jobs from reading `~/Documents`). The timer runs that COPY, so after any code or config change: `npm run timer:install`. A missed run (Mac asleep) fires once on wake.

### Mac code map

| File | Role |
|---|---|
| `core/run.mjs` | Shared runner. `node core/run.mjs <site> [--live] [--inspect] [--limit N] [--only <jobId>] [--login]`. Default is a dry run (reads and decides, writes nothing) |
| `sites/<site>.mjs` | Five parts per site: `login` (loginUrl/loggedIn/loggedOut, `plainLogin` flag), `jobs`, `details`, `apply` (returns `{applied}`/`{needs}`/`{broken}`/`{dry}`), `isApplied`. Plus `watch` (collects the page's own JSON), `check` (start-of-run check), `sent` (plain-words resume/note), optional `messages` |
| `shared/config.json` | All filters, tracks, notes, caps, pacing, crossSite, careerPages. Edit here to change behavior |
| `shared/config.mjs` | loads config, `.env`, `private/answers.local.json`; `profileDir()`; `noteFor()` |
| `shared/filters.mjs` | `fits(job, site)` returns `{ok, reason, track, needs}`; `payTopLpa()` |
| `shared/sheet.mjs` | Sheet client, retries, offline queue |
| `core/state.mjs` | `~/.jobbot/state`: per-site handled/days/needs/crossWait, `applied-anywhere.json`, `runs.jsonl` |
| `core/forms.mjs` | in-dialog form filler from saved answers; unknown required field returns a "Needs you" reason |
| `core/fill.mjs` | `npm run fill` helper for company forms |
| `core/doctor.mjs`, `core/status.mjs`, `scripts/peek.mjs` | health tools |

Runner flow per site: open list → logged in? bot check? page as expected? (else stop, capture, Health "Login expired" / "Bot check" / "Needs fix: ...") → (Wellfound) read Messages → recheck "Needs you" jobs (if she applied herself, flip row to Applied) → for each job: handled before? already in Sheet? `fits`? cap left? crossSite hold? → `details` → `fits` again (pay, years) → `apply` → Sheet row → pause → finally Runs row + Health line.

## Sources and status

| Source | How | Status (22 Oct) |
|---|---|---|
| Instahyre | Mac bot, logged in. Reads "recommended" feed JSON (`candidate_opportunities/candidate_matching`), newest job id first. One-click Apply (no note, sends her Instahyre profile resume). In-dialog forms filled from answers. Redirect to company site → Needs you | LIVE on timer since 20 Oct. Cap 10/day, 90 to 180s gaps |
| Wellfound | Mac bot. Login via Google in plain Chrome (`plainLogin`). Reads her saved search via GraphQL `JobSearchResultsX`. Profile is the application. Each apply needs a per-job note SHE approved (`~/.jobbot/state/wellfound-notes.json`, `{"<jobId>": "note"}`); otherwise row = "Needs note". External ATS jobs → Needs you | LIVE on timer since 20 Oct. Cap 5/day, 180 to 360s gaps. 1 live apply (Intempt, AI Design Engineer) |
| Wellfound Messages | Same hourly run reads `CandidateConversationList`; latest message from company (sender slug != `sejal-borkar`) → email to her + row at top of Messages tab, once per message | Built, Apps Script side deployed (v16), test email sent. **Mac side is PR #11, OPEN, not merged; timer copy does NOT have it yet** |
| LinkedIn | Gmail alert emails only (`jobalerts-noreply@`, `jobs-noreply@linkedin.com`) → Needs you rows. Her own "application was sent to X" emails → Applied rows | LIVE in cloud since 21 Oct |
| Glassdoor | Gmail alerts only (site terms ban scraping; Glassdoor shares accounts with Indeed) | LIVE in cloud |
| Indeed | Gmail alerts only | LIVE in cloud |
| Naukri | Gmail alerts only. Parser ready, but her Naukri emails so far were promos, not job alerts | Waiting on her to create a Naukri job alert. Auto-apply decision open |
| Career pages | Apps Script reads public ATS JSON: Lever `api.lever.co/v0/postings/<slug>`, Greenhouse `boards-api.greenhouse.io/v1/boards/<slug>/jobs`, Ashby `api.ashbyhq.com/posting-api/job-board/<slug>`. Boards: CRED, Meesho, Zeta (lever); Razorpay (`razorpaysoftwareprivatelimited`), Groww, InMobi, Figma (greenhouse); Atlys, Sarvam AI (`sarvam`) (ashby). Matches → Needs you with the `npm run fill` command in Notes | LIVE since 22 Oct. First run: 4 rows (Groww, Sarvam AI) |
| Company forms | `npm run fill -- <link>` (Lever adds `/apply`, Ashby `/application`; also Greenhouse, Rippling, simple forms) | Built 22 Oct, proven on a live Meesho Lever form (10 fields + resume, not submitted) |
| Cutshort | none | SKIPPED (terms: "any automated process", permanent suspension) |
| Hirist, YC Work at a Startup | none | Later list, terms not checked |

## Filters and criteria (`shared/config.json`)

- **Tracks** (first match on title, lowercase substring): product (product designer, ux designer, ui/ux and variants, interaction designer, ai/genai product designer, ai design engineer, "ai design enginner" typo on purpose, design engineer) and visual (ui designer, ui visual designer, visual designer, digital designer) use the **product note**. art (2d artist, illustrator, illustration, concept/comic/storyboard artist, motion (graphics) designer), brand (brand/creative/communication/visual communication designer), graphic (graphic designer) use the **visual note**.
- **Exclude words** in title: senior, sr., sr , lead, principal, manager, head of, director, staff, intern, internship, 5+/6+/7+/8+ years, sr product/ux/designer.
- **Locations:** bengaluru, bangalore, remote, work from home, wfh. Mumbai dropped 20 Oct. Blank location passes. Gmail side also passes "India" alone (her call 21 Oct: keep).
- **Experience:** skip if the job's minimum years > `maxYearsRequired` 2 ("2-4 years" passes).
- **Freshness:** `postedWithinHours` 24 globally; Wellfound 336 (14 days, her call 20 Oct). Instahyre shows no post date (newest id first). Gmail search window `newer_than:3d`. Career pages: no age filter (dedupe by link). Under-100-applicants is a preference only; not implemented anywhere.
- **Pay:** `minPayLpa` 6 on every site: shown pay under 6 LPA → skip. Shown but unclear (mixed units like "₹75,000 to ₹1.5L") → Needs you. Graphic track `minPayLpa` 8: no pay shown → Needs you (Mac). Gmail side: graphic and video-editor style titles skipped unless pay ≥ 8 LPA is clear (her call 21 Oct).
- `dreamCompanies` [] (would bypass excludes, level and pay floor) and `avoidCompanies` [] are empty: list pending from her.
- **crossSite** `after-days`, 7: same company+role (normalized) applied on one site → on another site logged once as Skipped "Already applied via X", applied there only if no reply after 7 days. Modes: `once`, `after-days`, `always`.
- **Notes** (both `approved: true`): product `note-v1` "Hi {company} team, I'm Sejal, a product designer at Epifi working on GenAI products. I'd love to bring that to the {role} role. My work is here: {portfolio}"; visual `note-visual-v1` "...a designer who works across product design, illustration and visual design...". `{portfolio}` = `https://sejalborkar.vercel.app/?ref=<site>`. Instahyre one-click sends no note.
- Resume: Instahyre/Wellfound use the resume on her site profile. `fill` attaches `~/Documents/Github/my-portfolio/public/Sejal_Borkar_Resume.pdf` (repo SBorkar2002/my-portfolio). Public URL sejalborkar.vercel.app/resume.
- Prefer (not coded): AI products, fintech, consumer apps, design-led startups. Avoid (not coded, avoid list empty): agencies, IT services, unpaid/contract-only, betting apps.

## Sheet structure

Created and formatted by code (`setupTracker`; reapplied by the `setup` action on every deploy). Timezone Asia/Kolkata; dates as real values `dd mmm yyyy, hh:mm`; wrap + vertical center; set column widths.

- **Health** (first tab): Site, Status (formula: "No good run in 3 hours" if OK but last good run older than 3h between 9am and 11pm, else Bot status; green OK, red otherwise), Last good run, Last run, Next run, Today ("3 of 10 applied"), Login, Problem, Bot status (hidden). Rows: Instahyre, Wellfound, Email alerts.
- **Messages** (tab 2, created on first message): Received, Site, Company, From, Message, Link, Replied (checkbox). Newest on top.
- **Site tabs**: LinkedIn, Instahyre, Wellfound, Cutshort (unused), Career pages, Glassdoor, Naukri, Indeed. Columns: Found at, Posted at, Applied at, Minutes to apply (formula), Company, Role, Location / mode, Applicants, Job link (dedupe key), Post link, Recruiter / poster, Resume version, Note used, Action (Applied / Needs you / Skipped), Status (Applied, Needs you, Viewed, Replied, Interview, Offer, Rejected, No reply, Skipped), Response at, Follow-up on, Notes (track, experience, pay, or the Needs-you reason).
- **Runs**: Run at, Site, Seen, Matched, Applied, Needs you, Skipped (count per reason), Near misses, Errors, Next run.
- **Follow-ups**: Due, Site, Company, Role, Job link, Recruiter / poster, Draft message, Done (checkbox).
- Value rule (her correction 20 Oct, now a flow-doctor rule): plain words saying exactly what went out ("Instahyre profile resume", "None (one-click apply, no note asked)"), never internal codes like site-v1/note-v1; IST real dates, never UTC text.
- Script Properties: `SHEET_ID`, `SHEET_SECRET`, `OWNER_EMAIL` (her alert address, set via the `owner` action), `LAST_HEALTH_ALERT`. Gmail labels it creates: `jobbot/seen`, `jobbot/reply-seen`.
- Web app actions: `has`, `add`, `update`, `run`, `lookup`, `setup`, `peek`, `mail`, `owner`, `message`, `pages`, `resetalerts`, `tail`, `mailraw`, `mailpeek`, `triggers`.

## npm commands

| Command | Does |
|---|---|
| `npm run doctor` | Checks Playwright, `.env`, private answers, Chrome, Sheet reachable, clasp login, each timer loaded, last live run health, queued rows, stale timer copy; prints the fix command for each problem. Run first |
| `npm run status` | Per-site health on the Mac (same picture as Health tab) |
| `npm run sheet:peek` | Prints Health tab and last Runs rows as the Sheet shows them |
| `npm run instahyre:dry` / `wellfound:dry` | Dry run: reads and decides, applies nothing, writes nothing |
| `npm run instahyre:inspect` / `wellfound:inspect` | Dry run + screenshots/text/JSON in `~/.jobbot/debug/<site>/` (pruned) |
| `npm run instahyre:live -- --limit 1` / `wellfound:live` | Real applies up to cap (use `--limit`, `--only <jobId>` for one job she named; `--only` skips filters, not caps) |
| `npm run instahyre:login` / `wellfound:login` | She logs in herself in the bot's Chrome profile |
| `npm run timer:install` / `timer:remove` / `timer:status` | Install (and refresh the `~/.jobbot/app` copy) / stop / show both timers |
| `npm run timer:run-now` / `timer:run-now:wellfound` | Kick a timed run now |
| `npm run sheet:deploy` | Push Apps Script + redeploy same URL + reformat Sheet |
| `npm run clasp:login` | One-time clasp auth (personal account) |
| `npm run fill -- <job link>` | Fill a company form; she checks and clicks Submit; logs Applied on Career pages tab only if a thank-you page appears |
| `npm run check` | `node --check` on all .mjs |

Logs: `~/.jobbot/logs/<site>.log`. Apps Script logs: the editor's Executions page.

## Safety rules (hard limits)

- Never get past CAPTCHAs or bot checks: stop the site, Health "Bot check", she clears it in the bot's Chrome (`npm run <site>:login`).
- No passwords, tokens or cookies in code, files, commits or chat. She logs in herself; Google sign-in only in plain Chrome.
- Private answers (phone, pay, notice, start date, email) live only in `private/answers.local.json` (git-ignored) and Script Properties; never printed in full.
- Unknown required form question: skip, mark "Needs you", never guess.
- Daily caps per site (no global cap); new or risky site starts around 5/day and is raised only after a clean week; human pacing.
- **Who clicks Submit:** Instahyre bot submits by itself (one-click and in-dialog forms with saved answers only). Wellfound bot submits only with a note she approved for that exact job. `npm run fill`: never submits, she clicks Submit. Gmail alerts and career pages never apply. Follow-ups, recruiter messages, cold emails: drafted only, she sends. Emails go only to her own address.
- Before building any new site: read its terms, quote them to her with the worst case, record her yes/no, date and cap in README (flow-doctor `new-site.md` stages 1 to 8: terms, profile check, recon from page JSON, five-part build, calibrate on ~10 real jobs with her, notes batch, one live apply with her OK, then timer).
- First live apply on any site = one job only, with her OK (Instahyre applications cannot be withdrawn).
- Never merge PRs to main without her OK (she has said "merge PR #N" each time). Commit and PR conventions: Conventional Commits titles.
- Warn about scams: the Messages email body already warns against moving to Telegram/WhatsApp, installing anything, or sharing ID/bank details (a fake "Recall Network" founder contacted her on Wellfound, 21 Oct).

## Done vs left

**Done (merged to main, PRs #1 to #10):** Sheet + web app + secret; shared runner and five-part sites; Instahyre live; Wellfound live; title tracks + two notes; Health/Runs tabs; Needs-you recheck; crossSite rule; offline queue; clasp deploys; Gmail alerts (LinkedIn, Glassdoor, Indeed, Naukri parser), reply tracker, follow-ups, health and weekly emails; career-page watcher; form-fill helper; doctor + "Fix it yourself" table in README; flow page.

**Built, not merged:** PR #11 `feat/wellfound-messages` (Wellfound Messages + `OWNER_EMAIL` fix). Its Apps Script half is already deployed. Merge it, then `npm run timer:install`. Do NOT run `sheet:deploy` from `main` before merging: main's `Mail.gs` still uses `Session.getEffectiveUser()`, which lacks permission and breaks every email to her.

**Not proven yet:** health alert email firing, Sunday summary, a real company reply flipping Status, Naukri alerts (none received).

**Open decisions / inputs from her:**
- Naukri: (1) auto-apply 3/day accepting risk (terms ban crawling, mention civil/criminal action), (2) find-only, (3) skip. Advisor view: alerts route already covers it safely.
- Years of experience (when freelance work started): `fill` leaves it blank; may change `maxYearsRequired`.
- Dream companies list (bypasses level filter) and more career-page companies.
- After Epifi ends (Nov 2026): update the product note (says "a product designer at Epifi"), `fill.mjs` hard-coded current company "Epifi", and answers (current CTC, notice period, earliest start).

## Ideas discussed for later

- Instahyre: also read search results and "Similar jobs" (recommended feed is mostly visual/graphic; search shows many more Bengaluru Product Designer roles). Was the planned next step after a week of live runs.
- Timer-side auto-fill of company forms (Greenhouse, Lever, Ashby) for jobs that leave Instahyre/Wellfound (she defined "apply" as the whole thing, including external forms with submit; today those become Needs you).
- Raise Wellfound cap after a clean week.
- LinkedIn hiring posts: drafted messages in the Sheet, she sends.
- Portfolio visit tracking: `?ref=<site>` tags are already in links; needs Vercel Analytics on the portfolio (code chat). Status unknown.
- Interview prep pack when Status becomes Interview (JD, company notes, best case study, likely questions).
- Calendar events from interview emails, with her OK each time.
- Hirist, YC Work at a Startup (terms check first).
- Glassdoor is for company research by hand (reviews, salaries), not a bot.

## How to work with her on this

- She is new to automation: explain flows as nodes and edges in plain words; keep one living `docs/workflow.html` (update it per site, check at 390px).
- Concise, plain English, no em dashes. Push back on risk; give a recommendation, let her decide, record it in README.
- Wellfound notes: when she says "draft notes", draft every waiting "Needs note" job in one batch, short and specific, only claims she can defend; after her OK, save to `~/.jobbot/state/wellfound-notes.json` keyed by job id; the next run sends them.
- After any change: dry run as proof, then one real item only after her OK, show the Sheet row, update README Status, `npm run timer:install`.
