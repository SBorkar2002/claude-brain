# Job-hunt automation: move to a new Mac

Goal: the cloud half keeps running untouched; the Mac half (Instahyre and Wellfound bots, timer, form helper, deploys) is rebuilt on the new Mac. Context: `playbooks/job-automation.md`.

## What depends on what

| Piece | Lives in | Survives the laptop return? |
|---|---|---|
| Sheet, Apps Script, its triggers, Script Properties (`SHEET_ID`, `SHEET_SECRET`, `OWNER_EMAIL`) | Google, personal account sejalborkar2002@gmail.com | Yes, nothing to do |
| Gmail alert reading, reply tracker, follow-ups, career-page watcher, health/weekly emails | Apps Script triggers on that account | Yes, keep running with no Mac |
| Code | GitHub SBorkar2002/job-hunt-automation (private, personal GitHub) | Yes |
| `.env` (`SHEET_URL`, `SHEET_SECRET`) | old Mac only, git-ignored (also copied into `~/.jobbot/app/.env`) | NO: copy or recreate |
| `private/answers.local.json` | old Mac only, git-ignored (also in `~/.jobbot/app/private/`) | NO: copy or recreate |
| `~/.jobbot/state/` (handled jobs, daily counts, `applied-anywhere.json`, `wellfound-notes.json`, `runs.jsonl`, seen Wellfound messages, `pending-rows.json`) | old Mac only | NO: copy (recommended) |
| Chrome profiles `~/.jobbot/profiles/{instahyre,wellfound,forms}` with her logins | old Mac only | NO, and do not copy: Wellfound cookies are encrypted with the old Mac's keychain. Log in again |
| launchd timers `com.sejal.jobbot.{instahyre,wellfound}` | old Mac only | NO: reinstall |
| clasp auth `~/.clasprc.json` | old Mac only | NO: `npm run clasp:login` again (never copy tokens) |
| Flow page artifact claude.ai/artifact/9No5UMQKk65HViTicyM6SB | old Claude account | Likely lost with that account. Source is `docs/workflow.html` in the repo: republish from the personal Claude account |
| Chat history and project memory (`~/.claude/projects/-Users-sejal-Documents-Personal-career-automation-scripts/`) | old Claude account / laptop | NO. This brain repo replaces it; the repo README is the real tracker |

**Company-account dependencies found:** none in the Google/GitHub side. Sheet, Apps Script, Gmail alerts, clasp and GitHub are all personal (sejalborkar2002@gmail.com, SBorkar2002). Job alerts were set up to arrive at the personal Gmail (LinkedIn, Glassdoor and Indeed alerts were read there on 21 Oct). Unknown: which email her Instahyre login uses (if it is the Epifi address, that account loses its inbox for OTPs; check). What WILL go stale when Epifi ends is content, not plumbing: see step 9.

## A. Before the old laptop goes back (Sejal, about 10 minutes)

1. Merge PR #11 (`feat/wellfound-messages`) on GitHub so `main` has the Wellfound Messages code and the `OWNER_EMAIL` email fix. Its Apps Script half is already live; leaving it unmerged means a future `sheet:deploy` from `main` breaks all emails to her.
2. Copy these three things to a private place (USB drive, AirDrop to the new Mac, or a private personal Drive folder; NOT GitHub, NOT a chat):
   - `~/Documents/Personal/career/automation-scripts/.env`
   - `~/Documents/Personal/career/automation-scripts/private/answers.local.json`
   - the folder `~/.jobbot/state/`
3. Stop the old timers so the old Mac stops applying: `cd ~/Documents/Personal/career/automation-scripts && npm run timer:remove`.
4. Expect the Health tab to turn red ("No good run in 3 hours") until the new Mac runs, and `healthAlert` to email her at most every 6 hours (9am to 11pm). That is harmless. The cloud sources keep filling the Sheet meanwhile.
5. Optional: if she wants a fresh secret (the current one was pasted in the old chat once), skip copying `.env` and do B6 "recreate" instead.

## B. New Mac setup checklist

1. **Base tools.** Xcode Command Line Tools (`xcode-select --install`; gives git and python3, both used by `timer.sh` and `sheet-deploy.sh`). Node.js LTS 22+ (old Mac ran v24.16.0 at `/usr/local/bin/node`; `core/status.mjs` uses `import.meta.dirname`, needs Node 20.11+). Google Chrome in `/Applications` (the bots use the installed Chrome via Playwright `channel: 'chrome'`). GitHub CLI `gh`, then `gh auth login` as SBorkar2002.
2. **Clone.** Keep the old path so docs match:
   ```
   mkdir -p ~/Documents/Personal/career && cd ~/Documents/Personal/career
   git clone https://github.com/SBorkar2002/job-hunt-automation automation-scripts
   cd automation-scripts && git checkout main && git pull
   ```
   Also clone `SBorkar2002/my-portfolio` to `~/Documents/Personal/Github/my-portfolio`: `core/fill.mjs` attaches `public/Sejal_Borkar_Resume.pdf` from that exact path (hard-coded).
3. **Install.** `npm install` (installs playwright 1.48.2 and clasp as a project devDependency). Playwright browser download is not needed because it drives installed Chrome; if a launch error asks for it, run `npx playwright install chrome`. If npm fails with EACCES in `~/.npm`, Sejal runs `sudo chown -R $(whoami) ~/.npm` herself.
4. **`npm run check`** (syntax check of all .mjs).
5. **Private answers.** Put the copied `answers.local.json` in `private/`, or recreate `private/answers.local.json` (JSON object) with these keys, values from Sejal only, never committed or printed:
   - `email` (personal Gmail for applications)
   - `phone` (with +91)
   - `noticePeriod`
   - `currentCtc`
   - `expectedCtc`
   - `earliestStart`
   - `relocate`
   Any blank key is safe: forms that ask it become "Needs you". Not yet a key: years of experience (open question).
6. **`.env`.** Copy it, or recreate from `.env.example`:
   - `SHEET_URL=` the web app URL: Apps Script editor > Deploy > Manage deployments > the existing Web app deployment URL (ends `/exec`). Do NOT create a new deployment: `sheet-deploy.sh` reads the deployment id from this URL and redeploys it in place.
   - `SHEET_SECRET=` the current secret, or make a new one: in the Apps Script editor run `makeSecret` (Tracker.gs), copy the value from the execution log into `.env` (never into chat or the repo). A new secret instantly invalidates the old Mac's copy, which is fine.
7. **clasp.** Confirm Apps Script API is On at script.google.com/home/usersettings (personal account; already on, per-user setting). Then `npm run clasp:login` and pick sejalborkar2002@gmail.com. The terminal must say "You are logged in as sejalborkar2002@gmail.com". `.clasp.json` (scriptId) is in the repo already.
8. **Sheet link test.** `npm run sheet:peek` should print the Health and Runs tabs. "bad secret" means `.env` secret does not match Script Properties.
9. **Update content that goes stale after Epifi (do with Sejal, through the truth check):**
   - `shared/config.json` `notes.product.text` says "a product designer at Epifi working on GenAI products": rewrite, bump `version`, keep `approved: true` only after her OK.
   - `core/fill.mjs` hard-codes current company `'Epifi'` for "current company" fields.
   - `private/answers.local.json`: `currentCtc`, `noticePeriod` (likely immediate), `earliestStart`.
   - Her Wellfound profile text (account side) mentions Epifi.
   Then `npm run sheet:deploy` if config filters changed (writes `Config.gs` for the cloud side).
10. **State.** Copy the saved `state/` folder to `~/.jobbot/state/` (create `~/.jobbot` first). Without it nothing breaks badly (the bot also dedupes by the Sheet's job links and the site's own "applied" marks), but she loses approved Wellfound notes, the crossSite memory, and may get one repeat email per existing Wellfound conversation.
11. **Site logins** (Sejal types her own credentials; Claude never does):
    - `npm run instahyre:login`: bot Chrome opens on Instahyre login; she logs in (OTP if asked); window closes itself when on a `/candidate/` page.
    - `npm run wellfound:login`: a plain Chrome window opens (Google sign-in refuses automated browsers). She clicks Continue with Google, picks the personal account, waits for her name/photo, then quits that Chrome with Cmd+Q. If macOS asks about "Chrome Safe Storage", click Always Allow. The script then reopens and reports "Logged in and saved. The login survived a Chrome restart."
12. **Dry runs.** `npm run instahyre:dry` and `npm run wellfound:dry`. Expect "Found N jobs", skips with reasons, "Health: OK". Wellfound should also read Messages without error.
13. **Timer.** `npm run timer:install` (copies the repo, `.env` and private answers to `~/.jobbot/app`, writes the two LaunchAgents, Instahyre :00, Wellfound :30, 8am to 11pm). The plist bakes in the absolute node path at install time: rerun after changing Node install (nvm/Homebrew upgrades).
14. **Prove one timed run.** `npm run timer:run-now` (Instahyre) and `npm run timer:run-now:wellfound`, then `npm run timer:status` and check the Runs tab got a row and Health is green.
15. **Doctor.** `npm run doctor` must end with "All good." It checks: Playwright installed, `.env` present, private answers present, Chrome installed, Sheet reachable, clasp logged in, each timer on, last live run OK, no queued rows, timer copy matches the repo.
16. **Keep it running:** Mac on and plugged in 8am to 11pm (asleep = no applies; a missed hour runs once on wake). Do not close the bot's Chrome mid-run.
17. **Flow page.** Republish `docs/workflow.html` as an artifact on the personal Claude account and update the "Workflow page" link in the repo README.
18. **Studio plugin.** Reinstall her studio plugin (repo SBorkar2002/studio) so `flow-doctor` rules are available; see the brain's main setup notes.

## Cloud side: only if something is wrong

- Triggers missing (Apps Script > Triggers is empty): run `authorize` in `Mail.gs` from the editor (re-creates `checkAlerts`, `checkPages`, `checkReplies`, `healthAlert` hourly, `followUps` 9am, `weeklySummary` Sun 7pm).
- No emails to her: `OWNER_EMAIL` missing in Script Properties; the Mac's `owner` web-app action sets it (`call('owner', null, { email })` from `shared/sheet.mjs`).
- Stop everything (job found, holiday): `npm run timer:remove` on the Mac and delete the triggers under Apps Script > Triggers.
