# Automation traps (job-hunt bots, 19 to 22 Oct 2026)

Each: symptom → cause → fix that worked. Repo: SBorkar2002/job-hunt-automation.

## Browser and logins (Playwright + Chrome on macOS)

- **Login gone after Chrome quit.** First Instahyre login was lost when the bot's Chrome closed. Cause: persistent profile did not restore the session. Fix: `profileDir()` writes `session.restore_on_startup: 1` into the profile's `Default/Preferences` ("Continue where you left off"). Always prove "login survives a Chrome restart" before any recon.
- **Google sign-in fails in the bot's Chrome** ("Continue with Google" on Wellfound did nothing). Cause: Google refuses sign-in in a browser a script controls. Fix: `plainLogin` sites spawn plain Chrome (`--user-data-dir=<bot profile>`), she signs in and quits with Cmd+Q, then the bot reuses that profile.
- **Wellfound login saved but bot still logged out.** Wasted 3 login rounds on wrong theories (On startup setting, a 30-day cookie-extension workaround, closing Chrome too early mid sign-in). Real cause: Playwright launches Chrome with `--use-mock-keychain` and `--password-store=basic`, so it cannot decrypt cookies that plain Chrome encrypted with the Mac's real keychain. Fix: `ignoreDefaultArgs: ['--use-mock-keychain', '--password-store=basic']` for plain-login sites; macOS may prompt for "Chrome Safe Storage" (Always Allow). Workaround removed in commit 25b8095. Lesson: find the root cause before asking her to log in again; every retry costs her patience. Corollary: these profiles cannot be copied to another Mac.
- **Login window that closes itself** must wait for her, not for a URL: auto-closing mid Google sign-in broke it. Let her decide (quit Chrome), then verify.
- **Click times out on Instahyre "Apply now".** The button sits inside a link that catches the mouse. Fix: `button.dispatchEvent('click')` on the real button (found read-only in the page) instead of a positional click.
- **False "APPLIED".** "Applied" appears in both sites' menus. Fix: Instahyre = text "Application sent!" AND no Apply button left; Wellfound = "✓ Applied" tick AND no Apply button. Always confirm the first live apply on the site's own Applied list and in the Sheet.
- **Read data, not pixels.** Both sites load lists as JSON: Instahyre `candidate_opportunities/candidate_matching`, Wellfound GraphQL `JobSearchResultsX` (has `liveStartAt`, `compensation`, `currentUserApplied`, `atsSource`) and `CandidateConversationList` for messages. `--inspect` saves those responses; parse them in `watch()`. First Instahyre reader missed the format until the captures were checked.
- **Instahyre has no posted date or applicant count**: sort by job id (higher = newer). Its recommended feed is mostly visual/graphic roles.
- **Wellfound 24h freshness skipped everything** (few new posts). Calibrate on ~10 real jobs with her before the timer: she chose 14 days and a 6 LPA pay floor.
- **Pay text with mixed units** ("₹75,000 to ₹1.5L", monthly vs yearly unknown): mark "Needs you", never guess.

## Timer (launchd)

- **launchd job cannot read `~/Documents`** (macOS privacy). Fix: `timer:install` rsyncs the repo plus `.env` and private answers to `~/.jobbot/app` and runs that copy. Trap: edits do nothing until `npm run timer:install` again. Doctor md5-compares the copy to catch it. On 22 Oct the Wellfound Messages code was not in the timer copy for exactly this reason (PR unmerged, no reinstall).
- **"fetch failed" at 8:13am right after wake** (network not up). Fix: Sheet calls retry 0/5/15/30s, then queue writes in `~/.jobbot/state/pending-rows.json`, flushed next run.
- Missed runs while asleep fire once on wake (StartCalendarInterval behavior). The plist bakes the absolute node path at install time.
- The bot's Chrome window pops up for a minute or two each run; closing it mid-run stops that run safely ("The bot window was closed during the run").

## Google Sheet and Apps Script

- **Internal codes confused her** ("site-v1", "note-v1" implied a portfolio PDF and note were sent when Instahyre sent its own profile resume and no note; Applied at was UTC text). Fix and standing rule: plain words saying exactly what went out, or "None"; IST real dates. Old rows migrated by `migrateRows_`.
- **New rows lost the date format** (appendRow resets to US default). Fix: set number format on each new row.
- **Sheet format by hand drifts.** Fix: format is code (`setupTracker`), reapplied on every deploy via the `setup` action.
- **Pasting Apps Script code by hand** was slow and error-prone. Fix: clasp. She enables the Apps Script API once and runs clasp login; then `npm run sheet:deploy` pushes and redeploys the SAME deployment id (URL unchanged).
- **`npx @google/clasp` failed with EACCES** on `~/.npm/_cacache` (root-owned files from an old `sudo npm`). Fix: install clasp as a project devDependency and call `node_modules/.bin/clasp`. Permanent fix is `sudo chown -R $(whoami) ~/.npm`, which she runs herself.
- **Deploy script ran clasp in a temp folder with project-relative paths.** Fix: run from the project root; fetch only the manifest via a temp `clasp clone`.
- **`Session.getEffectiveUser()` threw** "You do not have permission" (needs the userinfo.email scope). Fix: store her address once in Script Properties (`OWNER_EMAIL`, via the `owner` action). Health and weekly emails were silently failing before this.
- **Config drift between Mac and cloud filters.** Fix: `sheet-deploy.sh` generates `apps-script/Config.gs` from `shared/config.json`. Never edit Config.gs. After a filter change: `timer:install` (Mac) AND `sheet:deploy` (cloud).
- **Deploying from the wrong branch** overwrites live cloud code. The live Apps Script (v16) came from the unmerged PR #11 branch; deploying `main` would revert the email fix. Merge first, deploy from main.

## Gmail alert parsing

- Alert layouts differ per sender (seen 21 Oct): Glassdoor = company, title, place, [pay], age, link; Indeed = title, "company - place", [salary], link; LinkedIn = title, company, place, ..., link. Each job = block of lines ending at its link; a NOISE regex drops "Easy Apply", "Just posted", ages, salary lines.
- First run leaks fixed: "Sr" titles (added `sr `, `sr product` etc. to excludes), junk "Create alert" links, the same job on two alert sources (cross-tab `lookup_` by normalized company+role), and her own "your application was sent to X" LinkedIn emails being counted as company replies (now logged as her Applied rows and skipped by the reply tracker).
- Half of Glassdoor was "Graphic Designer & Video Editor" at small agencies, and alerts rarely show pay. Her rule: graphic/video roles from emails only with clear pay of 8 LPA or more.
- Locations listed only as "India": kept (her call), since some are remote.
- Naukri emails were promotions, not job alerts: the source stays empty until she creates a real Naukri alert.
- Thread labels `jobbot/seen` and `jobbot/reply-seen` prevent re-reading; `resetalerts` action clears recent rows and labels for a re-parse.

## Forms

- **auxi (Rippling) form, 21 Oct:** Claude's permissions blocked clicking the real Apply, several custom inputs refused automatic fill, and the window timed out and closed, losing the half-filled form. Lesson that shaped `npm run fill`: fill what is known, attach the resume, draft the note, list required fields left, never submit; she clicks Submit; log Applied only if a thank-you page appears before she closes the window.
- Forms keep asking "years of experience": unanswered until she gives her freelance start date. Paid freelance client work counts; overlapping months count once.

## Process

- **Terms check before every new site** saved her accounts: Cutshort skipped (permanent suspension clause), Glassdoor and Naukri moved to the email-alerts route, LinkedIn never automated. Quote the terms, state the worst case, record her decision and date in the README.
- **First live apply is one job only** (Instahyre applications cannot be withdrawn).
- **Usage limits cut sessions mid-task** twice. The README-as-tracker made resuming trivial: a fresh session reads it and continues. Keep that habit.
- **She asked "why didn't it apply here?"** Answer from the run log with the exact skip reason; the near-misses line in Runs shows titles that almost matched so she can widen tracks.
- **A secret pasted in chat** (she pasted SHEET_SECRET on purpose): low risk (it only writes to her Sheet), but rotate with `makeSecret` when convenient.
- **Wellfound gave no notification for a founder message**, which turned out to be a likely scam (fake "Recall Network" founder, India excluded, known Web3 recruiting scam pattern). Now the bot emails her every new company message with a scam warning line.
