---
name: project-comic-pipeline
description: Production pipeline for the "I Have No Idea What That Means" comic series — 9 steps, Drive/repo split, gates, Drive folder IDs, and tested Drive-tool limits
metadata:
  type: project
---

Pipeline for the comic series (decided 28 Aug 2026, with Sejal). Written up in
`Documents/product-brain/video/youtube/comics/PIPELINE.md` — read that first,
this is the pointer plus the things not obvious from the file.

**The core rule:** Drive is the review surface, the repo is the frozen record.
Repo scripts carry `Drive: <url>` + `Status: in-review | approved <date>`.
Steps 4/5/7 read only the repo copy. Without this, panels and voice get
generated from divergent script versions and nobody notices until assembly.

**Gates:** script review (step 3) always blocking. Figma review (step 6)
blocking for the first 5 episodes only, then visibility-only — two blocking
async gates cannot survive 2–3 episodes/week across Sumit's 90-day gate.

**Step 3.5 was added:** a rough voice pass immediately after script approval,
before any art. These gags lean on delivery; generating voice at step 7 means
learning the episode doesn't land after paying for 22 panels.

**Review surface is an Artifact, not a Google Doc** (changed 28 Aug, same day).
Artifacts can be revised in place keeping the URL and comment threads, and
threads where someone mentions `@claude` can be replied to and resolved — Drive
Docs could do neither (`update_file` is title/parent only). Script and panel art
sit on one page, which collapses the script gate and the art gate onto one
surface. Template: https://claude.ai/code/artifact/e39907fb-6bac-4b87-be36-3b3337390b6c

**Artifact constraints that shaped this:** strict CSP blocks all external hosts,
so a Figma prototype cannot be iframed — the clickable walkthrough is rebuilt
natively in the page. The `assets` capability is NOT on Sejal's roster, so panel
art goes in as inline data URIs under a 16 MB page cap; SVG export is strongly
preferred, which is another argument for the crude-components register.

**Unverified dependency:** whether Prashasti/Anandhi/devs can open a claude.ai
artifact link on their accounts. If they can't, the review gate has no surface
and it reverts to Docs. Drive tool gotcha if it ever does: `<b>`/`<i>` inside
`<td>` render as literal asterisks; use `<th>` and keep inline tags out of cells.

Drive is now index + archive: `01 Scripts` holds an archival export of each
approved script (the org record shouldn't depend on claude.ai), `04 Published
log` gains an Artifact URL column.

Topic backlog lives in the repo (Sejal's call, overriding a suggestion to put it
in Drive for Prashasti's access). Generator is ChatGPT only — no Higgsfield for
anything a character appears in. Steps 4–5 are provisional pending the art
register test — see [[project-comic-cast-lock]].

**Anandhi direction, 28 Aug 2026:** know the next 4-10 script ideas ahead (don't
build them, just know them); loop Prashasti in now, explicitly to stop Sejal
being a single point of failure; don't depend on engineers per video (a
spot-check on a technical claim is fine, a per-episode dependency is not); don't
wait for approval to move; assess cadence honestly. ChatGPT subscription
approved for generation.

**Ownership split:** Prashasti takes ideation (topic discovery via
`/content-engine`, filtered through `comics/topic-filter.md`) and distribution
(she wrote a Distribution Bible covering 5 platforms and a 9-post-per-episode
cascade). Sejal keeps script + visual production.

**Three unresolved conflicts between the Distribution Bible and locked
decisions**, as of 31 Aug: square master padded both ways vs the locked 16:9
master with middle-two-thirds safe crop; Reels-as-tier-1 vs Sumit's stated
preference for ~2-min YouTube over Shorts; one product mention per ten posts vs
the channel's zero-product-content brief. The nine-post cascade also has no
owner and no cost estimate.

Voice is deferred: the distribution plan says ship silent with burned-in
captions, so the ElevenLabs casting sheet is real but not urgent.

**Drive asset upload — the only path that works (4 Sep 2026).** The Drive MCP
`create_file` takes content inline, so every byte crosses Claude's context: fine
for text, unusable for a 26 MB frame set. Drive Desktop, rclone and gcloud are
not installed; System Events cannot drive the native file picker (no
Accessibility grant); and a page-context `fetch` to a local `http://127.0.0.1`
server hangs forever — Chrome's local-network block, the request never reaches
the server. What works: inject an `<input type=file>` into the Drive page, fill
it with `claude-in-chrome` `file_upload` (`paths`, ≤10 MB per call — the
extension reads from disk, so no context cost), then in page JS build a
`DataTransfer` from `input.files` and dispatch `dragenter` on `document` +
`window`, wait ~800 ms for Drive's drop overlay, and fire ONE `dragenter` /
`dragover` / `drop` on `document.elementFromPoint()`. Drive reads dropped items
via `webkitGetAsEntry()`, which returns null for synthetic items, so patch
`DataTransferItem.prototype.webkitGetAsEntry` to wrap the File first. Two drops
of the same batch triggers Drive's replace-or-keep dialog — drop once per batch.

**Two corrections from the EP004 upload (30 Sep 2026).** `file_upload` REJECTS
any file with >1 hard link, so staging a Drive-shaped tree with `ln` fails — use
real `cp` copies and delete the tree afterwards. And the single `__drop()` call
DOES work: do not re-fire drop to "check", because the first drop already
succeeded and the second raises the replace-or-keep dialog. Verify by screenshot
or `get_page_text`, never by dropping again. Each `file_upload` REPLACES
`input.files`, so the loop is upload-batch → drop → upload-next.

**EP004 Drive folder ids:** storyboards = 1UcWW4hKpAk-eYPHcHeRkw30MB7BBz8PM,
`Frames - no captions` = 18Z6ktMNFwEDzLF97d2e2si5azfSK19GH (46 plates); audio
= 1T5togim4A6yrUFBze8dAV4tPkhE_dleQ, `VO` = 10jzzPWFth6-0PAC2GdDKHm9d4UrX_7Gy
(42 takes). Episode SFX cuts go in the shared SFX folder; ambience shipped as
mp3 because the 2-min wav decode is over the 10 MB per-call cap.

**EP001 Drive folder ids:** storyboard `02 Storyboards/EP001 - LOOPS`
= 1xdK0hOVGHPMRZwJedfZqDl0qfHil6y_6, with `Frames - no captions`
= 1T_XLY-6BSjUq7w1HpD2pLouEo2xEUYpu and `Frames - with captions`
= 1uN0BfVm-7glFF5jrtCXrOVY5SYOrvtNP. Audio `03 Audio/EP001 - LOOPS`
= 1c-qaOZn-qVOXxdJGbBwnqmQBEylg52f7, with `VO`
= 1Afapuq6-2nmvd2-v4kDsWehyWgAmjqJ3. **`SFX` = 1k6MCHfABuXSzIvf-1IJVKRDVmGiG_SSv sits at
the SERIES root, not under an episode** (Sejal, 4 Sep): VO is per-episode, sound
effects are a shared library every episode draws from.
Series root `I Have No Idea What That Means`
= 1Oy6H1Zj5o89eUqZW9NzcdChezPYQ5LOR, inside `YouTube`
= 1cUMVZ5PuPY2yOFHRsiS9TiUypHRcrZQ1, which also holds the `Character Sheet`
voice-casting sheet and the Episode tracker. Also at the series root, added
4 Sep: `04 Cuts` = 1VhinX8kYknsCfqZb5_KKOSGogDOLrrZS (finished videos),
`AI mark` = 1DWh1hWYs60hdeghjKr6MPAaJQDY9w1L7, and `Characters`
= 1hFTxq4jsLolt_EjhQzNaZf_2FZ7fwkVN with `Expressions`
= 1n45URCBJISdEt8KYCZFjM1ijTEkqCf3C inside it.

**`04 Published log` was dropped, not built.** PIPELINE.md called for it, but the
Episode tracker already carries the published URL, approvals and outcome — a
second surface is one more thing to go stale. `04 Cuts` holds the files; the
tracker is the log. Both docs reconciled.

**Every link now lives in `comics/LINKS.md`** rather than in anyone's memory or
chat history. Add a row there when a surface is created.

**Storyboard frame sets.** The cut reveals captions one word at a time, so no
video frame ever shows a whole caption — a still pulled from the render is
useless as a storyboard. `v10/storyboard.py` rebuilds both sets instead: clean
plates, and plates with the full caption in Figma's layout. It needs the
ORIGINAL Figma boxes for any caption the cut moved (frames 18 and 46 here), and
a few px of slack on box width, because spec.py stores Figma's fractional node
widths as ints and a line that fits in Figma wraps in PIL.

**Repo shape after the 4 Sep cleanup.** `comics-video` went from ~980 MB to
447 MB (396 of which is node_modules) by dropping the whole ffmpeg path, the v9
16:9 pass, 232 pre-rendered sub-frames, the diagnostic dirs and every duplicated
asset. Two traps for whoever cleans next: **`v10/frames.py` looks like leftover
ffmpeg code but `emit.py` imports it** for caption reveal timing, and
`public/v10` is now the ONE copy of every plate and audio file — the Python
scripts read out of public/ rather than keeping a second copy. Verified by
re-emitting `cut.json` byte-identical and rendering a still.

**Artifacts vs the repo — settled 4 Sep.** Artifacts have no expiry timer, but
retention is an org setting (default indefinite; Enterprise can set a window
with a 30-day floor) and when it lapses the chat and its artifacts go together.
The real failure mode is losing the account, which already happened once here
(the Granola archive had to be pulled into Drive before the Fi shutdown). So
scripts stay as `.md` in the repo: artifact = review surface, repo = frozen
record, Drive `01 Scripts` = org-visible archive. Never fewer than all three.

**Docs are global rules only.** Sejal's standing instruction, 4 Sep: the skill
files carry rules reusable across scripts (captions, timing, positioning, the AI
mark prompt), not a log of one episode. Episode-specific facts go in that
episode's script file or the tracker. `comics/LINKS.md` is the new index of every
Drive folder, sheet, Figma file and artifact so no session has to ask for a URL.

Session handoff lives at `comics/HANDOFF.md`.

**Files over 10 MB: split, then rejoin in the page (EP005, 9 Oct 2026).** This is how the 16.7 MB v6 cut got into 04 Cuts.
- Run `split -b 8500000` on the file.
- Send each part with its own `file_upload`. In page JS, stash each one as a `new Blob([await f.arrayBuffer()])` before the next upload replaces `input.files`.
- Build `new File(parts, name, {type})` and check its SHA-256 against the local `shasum` before dropping.
- Drop ONE file.

Before dropping in a folder that has subfolders (04 Cuts has `old`, an EP audio root has VO), check that `elementFromPoint` isn't a folder row, or the files land INSIDE that subfolder.

The Drive list lazy-loads after about 50 rows, so page JS undercounts. Verify with `search_files` on `parentId` plus `title contains` filters, or with Drive's "N uploads complete" toast.

**EP005 Drive folder ids:**
- Storyboards: 1t1Rpo2ywEO1yHVwmxxAAsxQfqXIrBrPF. Inside it:
  - `Frames - no captions`: 1Gx7xOYU1rgpz-hQaOq5SbIFeNZ6xCuz4 (77)
  - `Explainers`: 1o7TiLRAaPXgzAn_TgtuLB5lZeNb_JdyC (18 stills)
- Audio: 1VSq4X_OuL7nT2_xphFSXvpUu8zCd6wpK. Inside it:
  - `VO`: 1ZJhI5-PgP9DqTPGTtLE1SkUYt3dlgOIr (43)
  - `Source takes`: 1MsS5kNPdkat4gYyZwOWS_tGnK5n6XGIX (5)
  - the office bed mp3
- The cut, in 04 Cuts: v8 = 1IEmRwNXleEFEpVnRM2OmekL2QVbfS-qU (v6 moved to `old`).
- The 8 ui_* sounds and 3 cat sounds went to the shared SFX folder.

