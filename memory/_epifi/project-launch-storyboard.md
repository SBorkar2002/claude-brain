---
name: project-launch-storyboard
description: "Transform Launch video v4.2 — script spine + the 10-frame Figma storyboard built from it, decisions, and open flags"
metadata: 
  node_type: memory
  type: project
  originSessionId: 31075b3a-f904-4fc8-ad39-928a6f634048
  modified: 2026-08-14T05:59:47.283Z
---

State as of 2026-07-15. The **Transform-scope launch video** (CTO/CXO, 2:15, ~279 words).

**Script v4.2** — manager authored it, Mohit 90% OK, Sumit not yet seen. Canonical repo copy:
`product-brain/working/drafts/transform-launch-video-outline-script-v4.md`. 8-scene spine:
S1 Hook (guess vs know) · S2a Reframe (AI Native Index curve) · S2b Tetriz enters (coaching-led) ·
S3 Prompts · S4 Loops · S5 Harness ("your agents' playbook") · S6 Agent Memory · S6b Stack ·
S7 Personalised Coaching (the heart) · S8 Close. Hard rules: product is "Tetriz" never "Tetriz Transform";
"coach/coaching" spoken exactly twice (S2b, S7); numbers in UI not VO; curve stage names + "AI Tax" screen-only;
CLAUDE.md shown never spoken. Faithfully implements the Jul 14 "Script catchup" meeting.

**Storyboard built in Figma** — file key `30sryhNZr624S6zxJMf6Xz` (Launch-Screens), page `0:1`.
10 new frames (1920×1080) in a titled **Section `284:37`** ("v4.2 STORYBOARD"), one row at **y=23000**,
x = 100 + i·2020, placed BELOW the pre-existing v2/v3 frames (which stop ~y=21560). Node ids: S1=273:2,
S2a=274:2, S2b=276:2, S3=277:2, S4=278:2, S5=279:2, S6=281:2, S6b=282:2, S7=283:2, S8=284:2.

**Design decisions locked with Sejal (this session):**
- Persistent map = **3 groups + Coaching wrapper**: chips Playbook (purple #7C6BF5) · Loops · Memory (teal
  #03A6CF), inside an orange (#F4652F) Coaching bracket. Focal glow follows scene order (Prompts→Loops→
  Harness→Memory); Playbook bracket spans the two non-adjacent Playbook scenes (S3 prompts, S5 harness) with
  a "▸ prompts/harness" sub-tag rather than blinking on-off-on.
- **Loops = BLUE #3B82F6** — NEW lever-identity color I assigned (object-identity memory only had Coach/
  Playbook/Memory); confirm with Sejal.
- **IC→org propagation on all four levers** (Anandhi's "same template every pillar").
- Dark bookends (#08090D) S1/S8, light middle (#F0F2F5). Two-tier captions: big emphasis + bottom CC band.
- **3.7× = mockup curve** (Sejal's call), flagged on-frame "shown in UI, never spoken · MOCK — derivation TBD".
- Fonts: **Inter + Roboto Mono stand in** for brand Mona Sans/Plus Jakarta/Geist Mono (brand fonts not
  guaranteed installed in the Figma file) — swap if installed.

**Real screens replicated** from `product-brain/docs/sales/assets/alpaca/`: S3 session-quality-detail (6-dim bars,
coral Efficiency), S5 harness-recommendations (add) + harness-skill-conflict (prune), S7 prompt-retro
("review this" / 4-of-5 / /scoped-review). **Loops dashboard = now REAL** — Sejal supplied the actual Tetriz
screenshot 2026-07-15, replicated faithfully (KPIs Active Loops 5 / Runs 184 ↑23% / Cost $8.60 ↑$1.40 /
Verification 73%; Loop Type Distribution bar; Configured loops & goals table; emphasis changed to "Every loop,
held accountable" to match the visual, drift line stays in the CC/VO). **Mocked (asset gaps still open):**
S3 Org Prompt Library (#1274), S7 EM/org health view, Harness add/prune pair (rebuilt as one clean
Recommendations view with an inline amber PRUNE row — still a mock). Curve = `docs/strategy/
ai-native-index-curve.html` v11 (Mohit/Sumit/Divya), **"not for distribution"** — must be cleared before public use.

**Open flags to resolve before render:** PM review point 9 (arrived cut off); 3.7× derivation owner; curve
public-use clearance; CTA "book a demo" vs Observe video's 7-day trial. See [[project-video-pipeline]],
[[feedback-object-identity]], [[feedback-anandhi-storyboard-review]].

**Update 2026-07-15 (b) — conformed all 10 frames to the updated `launch-scene-prompt-generator.md`:**
- **Fonts:** Mona Sans is NOT installed in the Figma file; Plus Jakarta Sans, Geist, Geist Mono, JetBrains Mono, IBM Plex Mono ARE. Swapped Inter/Roboto Mono → Plus Jakarta Sans (display/UI, ExtraBold subs for missing Mona Sans) + Geist Mono (code/mono) across all frames.
- **Curve now replicates the REAL `docs/strategy/ai-native-index-curve.html`:** dark card `#0E0D1F`, With-Tetriz line = **GREEN `#78D4A0`** (not teal) + glow + green confidence band; Without-Tetriz = grey widening band whose **lower edge leaks *down* below the "same start" dot**; colored stage labels (Compounding green → Piloting `#A8A6C8`); monospace; **no AI-Tax wedge** (my earlier amber arrow was invented). ⚠️ The skill's chart-color section (teal `#1BA0D8`, CREAM AI-Tax wedge, LEAK `#FB5B28`) is **OUT OF SYNC** with the real HTML — real artifact wins.
- **Backgrounds:** flipped S1 & S8 from dark bookends to LIGHT `#F0F2F5` per the skill's "No dark backgrounds" rule (the curve is a dark *card* on light). This overrides the dark-bookend idea in [[feedback-object-identity]] — **pending Sejal's confirm; revert to bookends if she prefers.**
- **New node ids after rebuild:** S1=295:2, S2a=292:2, S2b=293:2, S8=294:2 (old 273/274/276/284 removed). S3-S7 unchanged (277/278/279/281/282/283).
- **Repo divergence:** local working copy of the skill has uncommitted edits AND `origin/master` has a *different* newer version (+172) — pull is blocked; not reconciled. Ask which is canonical.

**Update 2026-07-15 (c) — reordered levers for pillar-map consistency (Sejal's call):** because the map groups Playbook = Prompts + Harness, the script's Prompts→Loops→Harness order lit Playbook→Loops→Playbook (back-and-forth). Swapped Loops↔Harness so the storyboard order is now **Prompts → Harness → Loops → Memory → Coaching** (Playbook contiguous). Figma frames repositioned + relabelled: S4=Harness (0:52–1:10), S5=Loops (1:10–1:23). ⚠️ This DIVERGES from the v4.2 script Mohit was 90% OK with — the script doc's S4/S5 numbering and VO connectives ("Then loops" / "Now add the harness") must be updated to match, and the reordered spine confirmed with Anandhi/Mohit.

**Update 2026-07-15 (d) — Anandhi's full storyboard review applied:**
- **Dropped "Playbook" entirely** (not a known term). Persistent map is now **4 chips: Prompts · Harness · Loops · Memory** (Prompts + Harness share purple #7C6BF5 so they still read as the "setup" pair without the label). Applied to S2b/S3/S4/S5/S6/S6b.
- **Coaching only introduced at S7** — removed the persistent Coaching wrapper from all middle frames; the orange wrapper now appears only on S7 (wrapping the 4 chips). Anandhi: don't introduce coaching before its scene.
- **Harness (S4):** type icons (skill=⚡, rule=▤ ruler, prune=✕), prune is now a **minimal faded/struck-through row with a small "pruning…" chip** (no button — "a yellow item that blinks and drops out"); subtitle "SKILLS · RULES · HOOKS" (no Playbook). Prune doesn't ship yet — pitched as token-saving optimization.
- **Agent Memory (S6):** headline relabelled **"None of it is forgotten" → "Agent Memory."** (honest card kept per Sejal — sessions·code·conventions + org grid; did NOT use the Claude warm-start mockup, which is future Context plane).
- **S7 org health = glanceable trend sparklines** (Core/Growth/Payments green rising = healthy; **Platform red falling = needs attention**) instead of text rows — Anandhi: a CXO glances and sees "my org's fine / this needs attention," "connect once, check the health, Tetriz does the work."
- Curve stays the real artifact (represents **compounding** — deploying→integrating→reinventing→compounding). Still pending: S8 brief govern/native flash; further clutter trims; the Harness/Loops spine-reorder needs script-doc + VO update + Anandhi/Mohit confirm; Context-plane mockup needs Mohit shipped-status check.

**Update 2026-07-15 (e) — S3 Prompts split into 3 frames** (Sejal's direction), placed in a NEW row below the main section at abs y=24400, x=100/2120/4140 (on page, not in the section yet): **S3a — One engineer** (avatar placeholder + "John" + horizontal quality card: Quality Score 5.0/10 on top + 6-metric breakdown), **S3b — The team** ("Team" not "Team·core", + "Prompt quality", avatars beside each name), **S3c — The org** (SKILL/RULE/COMMAND buttons → icons: MD-file=skill, rules-list=rule, `>_` terminal=command; GUARDRAIL pill → teal shield icon). Node ids S3a=314:2, S3b=315:2, S3c=316:2. **Brown/gold bars retired** → teal scores, red for low (Efficiency 3.0), per skill palette. Old combined 'v4.2 S3 — Prompts' (277:2) still in main row — remove/replace once approved. More per-frame changes coming from Sejal.

**Update 2026-07-15 (f) — S3 & S4 split into sub-frames** in the "below row" (abs y=24400, on page, not in section). S3→S3a(one engineer, single card avatar+John+quality)/S3b(the team, avatars)/S3c(the org, icons+teal shield). S4 Harness→**S4a Recommendations** (uniform cells; rapid-prototyping = gray "✓ Installed" button, not struck) + **S4b Installed** (rapid-prototyping being pruned: faded amber row, "✕ pruned", count drops to 11 active). Node ids: S3a=317:2,S3b=318:2,S3c=319:2,S4a=320:2,S4b=321:2. **Captions = script only, distributed one part per sub-frame** (Sejal: don't invent captions, follow the script). Cards use **equal padding** all sides. Colors: teal scores / red for low / teal shield — no brown. Harness caption drops "your agents' playbook" per Anandhi (script doc still has it — needs same edit). Originals still in main row (S3=277:2, S4=307:2) — swap in the splits once approved. More per-frame splits likely coming (Loops, Memory, Coaching).

**Update 2026-07-15 (g) — S6b polished + S7 split into 3.** S6b: graph removed, order Prompts·Harness·Loops·Memory, clean icons (chat/sliders/loop/brain, no boxes). S7 split into **S7a Coaching-wraps-all** (4 icons in an orange coaching circle + wrapper map), **S7b The engineer** (simplified retro — banner + scoped-review box removed), **S7c Check the health** (org-health **bar chart**: Core 92/Platform 54 red/Growth 95/Payments 88 + threshold line). Node ids S7a=336:2,S7b=337:2,S7c=338:2. Split-frames now live in the "below row" at abs y=24400: S3a/b/c(317/318/319), S4a/b(320/321), S7a/b/c(336/337/338). All captions = script distributed 1-1-1; punchy emphasis headline added to every frame for consistency. Icon note: Prompts/Loops/Harness use authored stand-in vectors (Sejal OK'd loops/prompts; harness=sliders) — swap with Icons8 PNGs if provided; Memory brain + Harness are authored teal/purple vectors (no box). Originals still in main section row — swap splits in once Sejal approves the whole set.

**Update 2026-07-15 (h) — final lever colors + S7 polish.** Lever identity colors now LOCKED & distinct: **Prompts = magenta #EC4899** (was purple, changed because it clashed with Harness), **Harness = purple #7C6BF5**, **Loops = blue #3B82F6**, **Memory = teal #03A6CF**, **Coaching wrapper = orange #F4652F**. Applied globally (all map Prompts chips + S6b prompts card/icon). S7c org-health chart = **teal shades** (not green/red): healthy #03A6CF, needs-attention light teal #9AD9EA. S7a rebuilt: bigger SOLID-filled icons (magenta chat / purple gear / blue loop / teal brain), light circle (thin #F4A57F border, no fill), "Personalised Coaching" label ABOVE the circle with a gap. S7a/b emphasis headlines removed (Sejal). S7b How-often/Downstream-cost enlarged+bold. Animation intent for S7a (Mode-2): 4 icons drift in circular motion → light orange border draws around them closing the loop. NOTE: Sejal was frustrated this session — she'd manually edited some frames and rebuilds risk clobbering; prefer surgical edits and verify against current node state first.

**Update 2026-07-15 (i) — Remotion animation started.** Removed the "TETRIZ · LAUNCH v4.2" header + scene tag from ALL 18 Figma frames (Sejal: don't keep that on frames). Built **v4.2 Remotion project** at `Documents/Work/tetriz-launch-video-v4.2/` (node_modules SYMLINKED to `Documents/Work/tetriz-launch-video` to skip reinstall; same remotion@4). Conventions copied from the old project: `constants.ts` (updated to v4.2 lever colors — PROMPTS magenta/HARNESS purple/LOOPS blue/MEM teal), `WordReveal.tsx` (word-by-word, wordDelay 4), scenes in `src/scenes/`, composition registered in `Root.tsx`. Fonts via Google-Fonts `@import` in a `<style>` (Plus Jakarta Sans + Geist Mono) — loads even in headless still render. **Sequence 1 = "Prompts"** (`src/scenes/PromptsSequence.tsx`, comp id `Prompts`, 560f): map pop-in (Prompts magenta, no top chrome) → S3a (avatar+John/SDE II, quality bars fill L→R) → S3b (team rows name→bar one by one) → S3c (org library items one by one), 2-tier word-by-word captions. Verified via `npx remotion still src/index.ts Prompts out/x.png --frame=N` (all 3 beats render clean). Preview: `npm run dev` (Remotion Studio). NEXT sequence when Sejal asks = **Harness** (S4a/S4b).

**Update 2026-07-15 (j) — Harness sequence + accent-color RULE.** ⚠️ RULE from Sejal: **emphasis-caption accent words are ALWAYS TEAL #03A6CF (brand)** — never the lever color; she flagged my magenta accents in Prompts as a mistake ("don't repeat it in further frames"). Fixed in PromptsSequence. Built **Sequence 2 = "Harness"** (`src/scenes/HarnessSequence.tsx`, comp id `Harness`, 500f): continuation hard-cut (map static via shared `components/PillarMap.tsx`, chip handoff Prompts→Harness with pulse) → S4a Recommendations (3 rows all "+ Install"; **cursor moves in and CLICKS rapid-prototyping → button crossfades to grey "✓ Installed"** — Sejal: never show pre-installed, show the install) → S4b Installed (4 rows; rapid flags amber "✕ pruned" synced to the VO word "Pruned." → row **disappears entirely, NO strikethrough**, row below slides up to close the gap, count ticks 12→11). All beats verified via stills. NEXT sequences: bookends S1/S2/S8.

**Update 2026-07-17 (r) — launch-script-refiner skill rewritten to the v4.2 format.** `product-brain/video/skills/launch-script-refiner.md` (local, Sejal pushes) now mandates: every generated/refined launch script = a **claude.ai Artifact** (same URL per project, version-labeled deploys, prior versions appended verbatim as appendices for comparison) + parallel canonical md in `working/drafts/`. Structure locked to the v4.2 script artifact's nine sections (header meta → changes table → Part 1 outline → Part 2 script w/ word counts + device notes → timing table → 12 production rules → open flags → prior-version appendices → sources). Old 60s/166-word/5-block format retired. ⚠️ `launch-scene-prompt-generator.md` still has UNRELATED uncommitted local edits from an old session — don't let them ride along in her PR.

**Update 2026-07-16 (q) — VO-synced full video.** ElevenLabs VO (Monika Sogam, 109.95s) in `public/vo.mp3`; whisper sentence timestamps in `out/vo_segments.json`. ALL scene durations + captions + beats locked to the read (total 3360f = 112s incl ~2s outro tail; outro constellation clock ×2.4). Full = Intro(726)→Prompts(480)→Harness(402)→Loops(348)→Memory(321)→Stack(138!)→Coaching(465)→Close(312)→Outro(168). Also this session: S8 Close animated+polished (centered answer cards synced to their VO lines, bigger curve, 3.7× count-up), constellation outro (light theme, de-tiled icons, glyph/wordmark 0.8×, "Book a demo at tetriz.ai" headline), `VO-SCRIPT.txt` for regenerating VO. S9 static Figma frame 381:2 superseded by constellation outro.

**Update 2026-07-16 (p) — INTRO animated + new frame node ids.** Sejal added NEW intro frames (row at y=25664): **S1=364:63, S2a=370:188, S2b=368:3236** (old 295:2/292:2/293:2 superseded; there's also a new S8 draft at 374:3353 + old 294:2). Built `IntroSequence.tsx` (comp `Intro`, 900f, in `Full` ahead of Prompts → total 3930f ≈ 2:11): S1 hook (arrow FIRST then ?s pop, idle pulses, "guess" ORANGE per frame — deliberate exception to teal-accent rule), S2a chart build (axis, stage labels bottom-up, same-start dot, gray wedge drawn L→R), S2b continuation (With Tetriz + journey reveal, teal curve draws with camera 1.55× FOLLOWING the glowing tip, emphasis "It's who's becoming AI-native." teal, then CC — sequenced, never simultaneous). Coaching heart icons finalized: one size 124, diamond layout, equal gaps. **Outro S8 still needs a final frame + animation** (Sejal will design / may ask to create). SVG gotcha: fully-offset round-cap dash = stray dot at path end — gate draw-on paths until progress > 0.

**Update 2026-07-16 (o) — Coaching extended to full S7a→S7b→S7c** (Sejal: one sequence, NOT separate comps). `CoachingSequence.tsx` now 720f (SEQ_COACHING 310→720): S7a beats unchanged (exits ~246; orange wrapper + all-lit map PERSIST through the whole sequence); **S7b** (268-464): This Week card drops, CODE REVIEW eyebrow, headline word-reveals with "review this" purple, HOW OFTEN / DOWNSTREAM COST stats pop big+bold; **S7c** (470-end): header + On-track pill, dashed threshold line draws via clip-reveal, **bars grow one by one with % counting up** (Core 92 → Platform 54 light-teal "needs attention" → Growth 95 → Payments 88), emphasis "Connect once. Check the health." **accent TEAL per rule (frame has orange — rule wins)**. CC = script 1-1-1 sequential. Fixed "healthy ≥ 80%" label overlap (moved to gap between Core/Platform — it hides behind Core's bar in the static frame too). Verified stills 380/560/680.

**Update 2026-07-15 (n) — Coaching S7a sequence.** Built **Sequence 6 = "Coaching"** (`src/scenes/CoachingSequence.tsx`, comp id `Coaching`, 310f): continuation from Stack (all 4 chips stay lit via allActiveAt=-30); **four solid icons pop one by one** then keep a slow circular hover-drift; **light-orange circle (#F4A57F) DRAWS itself** from the top around the icons via strokeDasharray/dashoffset (solid stroke → pathLength technique is allowed, unlike dashed); then the **single "PERSONALISED COACHING" pill** pops above the circle with a gap. **De-duplication call (Sejal: "take the best call"): the label appears ONCE** — on the pill; the map gets only the orange wrapper fading in around the chips (wraps-it-all echo, no second text). No emphasis tier on this frame (she removed those). CC = script line. Verified stills 100/138/230. **Rework pass: Sejal changed the S7a frame icons → animation updated to match: OUTLINE-style icons (stroke, not solid), organic scatter positions (chat 848,555 / sliders 1048,478 / loop 901,733 / brain 1082,651), bigger circle (center 960,600 R=228), pill = tint bg + orange border + orange text.** ⚠️ Lesson: before animating a frame, re-screenshot it from Figma first — Sejal edits frames between sessions; don't trust my last-built version.

**Update 2026-07-15 (m) — Stack sequence.** Built **Sequence 5 = "Stack"** (`src/scenes/StackSequence.tsx`, comp id `Stack`, 360f): cards land one by one in the fixed order Prompts→Harness→Loops→Memory (identity colors incl. magenta Prompts), connector arrows follow each; **dashed "compounds" arc DRAWN right→left via growing clip-rect** (dash pattern stays real — per the skill rule, never pathLength on dashed lines), arrowhead pops onto Prompts at draw-end; then **all four pillars glow together** — cards pulse box-shadow in their own colors AND all 4 map chips light simultaneously (PillarMap gained `allActiveAt` prop, and `active` now accepts null = all gray — Stack starts with ALL chips gray per Sejal, no Memory carry-over; the group glow is the first light-up). Resting glow breathes so the frame stays alive. Emphasis "Stack the four — they compound." accent TEAL. Verified stills 105/145/250.

**Update 2026-07-15 (l) — Memory sequence.** Built **Sequence 4 = "Memory"** (`src/scenes/MemorySequence.tsx`, comp id `Memory`, 420f): handoff Loops→Memory; Agent Memory card pops first (Sejal's minimal card: eyebrow + icon + title + WHAT IT KEEPS pills one by one); **12×6 grid cascades in ALL GRAY first**, then after the "Learned once → the whole org starts smarter" label reveals, a **left→right tint wave**: cols 0-3 stay gray, cols 4-7 → light blue #7FCBE0, cols 8-11 → dark #03A6CF (matches static frame; Sejal said "rows" but confirmed "like how the visuals look" = column groups). Dark cells breathe subtly so the frame never freezes. CC split in two sequential lines; emphasis "Every week starts smarter." accent TEAL. Verified via stills at 140/212/320. Polish round (Sejal): pills re-laid with equal 18px gaps (computed cumulatively, not hardcoded); eyebrows "KEEPS WHAT TETRIZ LEARNS"/"WHAT IT KEEPS" made prominent (17/16px bold mono, wide tracking) — animation only, frames untouched; **teal radial glow added behind the hero card** (radial-gradient + blur 70px, fades in as card settles) — remember the glow-behind-hero-card rule for future sequences.

**Update 2026-07-15 (k) — Loops sequence.** Built **Sequence 3 = "Loops"** (`src/scenes/LoopsSequence.tsx`, comp id `Loops`, 470f): continuation handoff Harness→Loops; **4 KPI cards land ONE BY ONE 32f apart** (Sejal's pacing rule: visuals must keep animating while captions reveal — never freeze), each number counts up from 0 (5, 184, $8.60, 73%), sub-lines fade in after count; distribution bar draws L→R (real dashboard colors #6C5CE7/#34C77B/#4A90D9/#E8944A), legend items one by one; table rows stagger with runs counting; green status dots pulse continuously (sin-based) so the frame never sits static. CC split into two sequential lines (never simultaneous): "Your engineers aren't just prompting agents…" then "Tetriz holds every loop accountable…" (wordDelay 5). Emphasis "Every loop, held accountable." — accent TEAL per rule. All beats verified via stills.

⚠️ Figma GOTCHA learned: once frames are inside a Section, `page.findChildren` (direct children only) does NOT find them — use `section.findChildren` or `page.findAll`. Using page.findChildren for delete-before-rebuild silently created duplicate frames; fixed by removing stale section copies and re-appending the rebuilt ones.

Figma write mechanics (worked): `use_figma` runs Plugin-API JS; supports top-level `return`; errors roll back
the whole call (partial nodes vanish). `get_screenshot` of a Section pads to canvas origin (looks huge — a
render quirk, the section is fine). Build one frame per call; `createNodeFromSvg` is great for curves/arrows.

**Update 2026-08-14 — PENDING HANDOFF: build the "loop-visible" frame in Figma (fresh session needed).**
The Aug-13/14 session's claude.ai connector bridge died mid-life (EVERY connector — Figma, Granola — returns
instant net::ERR_FAILED; Sejal reconnected Figma in claude.ai settings and it still fails, because the stale
session can't re-open the transport; a NEW session should connect fine — verify with `whoami` first, and load
the figma-use skill before `use_figma`).
TASK: create a 1920×1080 frame in Launch-Screens (`30sryhNZr624S6zxJMf6Xz`, page `0:1`) replicating
**`/Users/sejal/Desktop/pc-loop-visible-frame.svg`** — that SVG is the approved-direction mock (open it for
exact geometry/colors/copy; it uses the v4.2 tokens: Plus Jakarta Sans + Geist Mono, BG #F0F2F5, coach
#F4652F, lever colors magenta/purple/blue/teal). Concept (Anandhi Aug-14 Slack feedback: "moving up the curve
doesn't show what the self-improving loop IS; stats should visibly change across speed/quality/cost"):
the S6 coaching tableau (PC card cx≈700 + 4 engineers + ghosts + threads) compresses LEFT; NEW right column
(x≈1360, w≈480) = Card A "Coaching impact, compounding" (eyebrow PER ENGINEER · WEEK OVER WEEK; John/Megha/
Priya rows with W1→W4→W8 dot trails that densify, lever-tinted; stats strip SPEED ↑1.8× / QUALITY +18% /
COST −31% in green #12A150) + Card B "AI-Native Index — whole org" (ascending coach-orange curve, engineer
dots grey→orange climbing, W1→W12). Place near the v4.2 section frames (below-row y≈24400 area). Titles were
already de-placeholdered with Sejal. After the frame is approved she wants it ANIMATED into the video
(extend PCWrapSequence line 2). ALSO PENDING in the video repo: Anandhi reported a visible glitch at the two
audio-gap seams (after the Loops hold and after "handled" ~1:40) — scrub `src/scenes/LoopsSequence.tsx` /
`CoachingSequence.tsx` exits vs the FullVideo audio windows and fix.
