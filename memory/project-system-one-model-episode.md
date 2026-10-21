---
name: project-system-one-model-episode
description: "`system one model` comic episode: script versions (Sejal v3, Prashasti, Mohit v2), review thread, Figma page, Jev facts verified against TypeSafe docs, open fixes as of 8 Oct 2026"
metadata:
  node_type: memory
  type: project
  originSessionId: 4db63ca3-02a1-4d9f-9bf3-8f53880ab15d
  modified: 2026-10-08T12:03:53.323Z
---

**Versions** (Prashasti's is the one being produced):
- Prashasti's script, artifact https://claude.ai/artifact/RoCuvW7uoVE6m9eXXsmVN4 (updated in place). As of 8 Oct it has 21 panels: AJ sends 80,000 support tickets to the big model, the $250 monthly budget runs out at 10,416, then the doctor/nurse teach, the playground how-to, the payoff card, and a loop back to P1.
- Mohit's v2, https://claude.ai/artifact/5z3Dju7kFeGUaxKszuRdeN. It has the same numbers but ends on a **blame turn**: "Whose fault was last night?" Intern / Not the intern, 51%, so it gets sent to Sameer, and AJ says "it wasn't sure." Mohit cut the loop on purpose because the skill only allows a loop when the term is about repetition. Prashasti then put the loop back and dropped the blame turn.
- Sejal's own v3, `comics/scripts/system-one-model.md`, uses an inversion engine.
- Review thread: Slack C0BAZG6RD7S, ts 1791362062.239149. On 8 Oct Sumit asked for "again but for a noob" (applied) and said the ending's last few examples get mixed up and need clarity.

**Figma (9 Oct):** page `system one model` (761:2) in file UM66oBdfGGPHkENjoPpN1S holds Sejal's 61 boarded frames (frame1..frame61, 720x1280). Sameer became **Ken**, AJ's manager (glasses, .env tee). Sejal's own ending: Ken says "yeah.. something's definitely wrong." There is no loop and no blame turn. She also added a coupon gag (f14-16).
- My explainer and screen frames are in section 797:2 at y=8000, named `exp-NN ...`. Explainers: 37 doctor, 38 nurse, 39 doors, 43a/b/c playground, 50 step five. Screens: 08, 11, 19, 20, 21, 34, 48, 52, 53, 55.
- Day monitor screen rect is {x:41, y:528, w:638, h:371}. The night plate's rect is about the same.
- VO line sheet: `comics/scripts/system-one-model-vo.md`. Takes are named `ken_fNN` / `aj_fNN` / `ai_fNN`. Ken isn't in the Character Sheet (use graph's Ken). AJ = Jet JOUWtlfdRuffI74LLmML, AI = David rWV5HleMkWb5oluMwkA7.
- Open issues on the board:
  - f48 (test result) sits before f49/50/51, so it is out of order.
  - f42 has a stray "you're done??" text node hidden under the art.
  - Captions in the top 90px: f14-16, f25-26.
  - Captions in the low right rail: f03, f57, f60.

**Jev facts (docs.typesafe.ai, 8 Oct 2026):**
- The term was coined by TypeSafe when it launched Jev on 15 Sep 2026.
- Price: $0.042 per M input tokens. Output is free.
- Rate limits: **100K tokens/s and 80 requests/s**. The docs say these change dynamically and are higher on enterprise plans.
- Context: 32k for state plus the longest question, 64k total.
- Same weights for every account, so it is not trained on your data.
- Choice options can carry what / not_for / examples. The docs' own examples are one short line each.
- A Playground exists. "Which team should handle this?" is TypeSafe's own example question.

At about 4,000 tokens per ticket, 69,584 tickets take about 46 to 50 minutes, not 9.

Related: [[project-comic-pipeline]], [[feedback-aj-ai-voice]], [[feedback-no-em-dashes]], [[feedback-no-end-cards]]

**Remotion build (9 Oct 2026):** composition `SystemOne` in ~/Documents/comics-video.
- Code: `src/SystemOne.tsx` and `src/S1mExplainers.tsx`. The explainers are drawn in 720-space and the stage is scaled 1.5x to 1080x1920.
- Data: `src/s1m_cut.json` and `src/s1m_caps.json`.
- Build steps: `v10/s1m_audio.py` cuts the three ElevenLabs takes into lines, then `v10/s1m_emit.py` handles levels, timeline, syllable flap, typing slices and the baked bed. `v10/ambience.py` now takes an optional output path as its 4th argument.
- Plates: `public/s1m/plates`, 77 of them. `_shut` versions are the same frame with the `hf_20260831_100404` open-mouth layer hidden.
- Reused AJ lines: f06 is insights `aj_p03`, f12 is graph `s12`, f42 is insights `aj_p21`, and f51 reuses f07.
- Choices I made without asking, all flagged to Sejal:
  - f48 plays after f51.
  - f23 "huh??" has no caption because it sits over a visual.
  - Captions on f14-16 and f25-26 were moved down to y=96.
  - The f42 stray text and the f54 "..." are ignored.
- Runtime is 3:08.7, over the 2:30 budget. The AI's lines alone are about 94s.
- Notes from Sejal on v1 (9 Oct), all applied in v2:
  - **Ken's mouth moved too much.** He now uses a calmer flap, about 2 toggles/s against 4-6 before. The rule in `flap_track`: a higher bar to open, dips of 5 dB or more to close, no 1-2 frame flicks, open runs up to 9 frames.
  - **The coding beat was too fast to follow.** f7 now holds 1.0s and f8 runs 4.8s: typing takes 2.6s and the test lands at 3.1s.
  - **She re-centred the "dashboards" (the playground cards) in Figma** to x=80 and centre y=640. In Remotion the card now re-centres smoothly as it grows: top = 640 - cardH/2.
- **Studio** cannot start from preview_start because macOS TCC blocks the app from reading ~/Documents. Run it in the user's terminal panel instead: `./node_modules/.bin/remotion studio src/index.ts --port 3334`.
- **Applied in v3 (9 Oct):**
  - AJ now uses the calm flap too.
  - UI sounds: synthesised by `v10/s1m_sfx.py` (pop, pop_low, tick, chime, error, whoosh, ripple, morph) and cued in the emitter through `ui()`, mirroring the explainer event times. The error sound fires on the usage-limit banner.
  - Ken's f26 caption is now just "i said a system one model."
  - f33: the AI mark shapeshifts in place (`AIMorph`): magnifier over code, thought chain, coin, two coins, three doors.
  - Doctor: the group is centred (+39, +19), the coat details are clipped to the coat, and the stethoscope is coral. The bill sits at x 90.
  - Every explainer line is followed by a 1.2-1.5s pause.
  - The nurse has a cap. "Broken feature" uses a warning-triangle icon.
  - Reorders:
    - f42 now plays after f39. The reason: AJ's excitement answers the nurse, not "sorting the mail".
    - Step five (f50) now plays before AJ's "skip the test".
  - The bed duck went from 0.45 to 0.62 with a 0.3s ramp. The bed never actually vanished; it was ducked under the dense ending.
  - The bench and its WAITING sign appear with the doors.
  - Figma frames were synced to match. Runtime is now 3:19.
- **v4 (9 Oct): the patients are meme cats.**
  - `v10/s1m_cats.py` keys banana cat and happy-happy cat (sources in s1m/cats/) into `public/s1m/cats/{walk,cry,happy}`.
  - The key uses g-max(r,b), because the banana suit is yellow. Banana switches from walking to crying at frame 264 (8.8s). Frame 385 is blank and is dropped.
  - Who is who: the happy cat is the one picked for the door, and it dances from the pick onward. Banana cats walk in and freeze while they wait. The last banana cat turns into the crying one on the bench.
  - The cats share one scale (K=0.282). The frozen happy cat uses `rest` frame 12, which is grounded.
  - The cats' audio (cat_walk, cat_happy, cat_cry) is kept at low gain and stops on the cut to f42. `CAT_AUDIO_MUTED` in the emitter mutes all three at once.
- **v5 notes (9 Oct), applied in Studio, not yet rendered:**
  - Bench moved right of the nurse (BENCH_SPOT [505,635], seat y 740). The crying cat is drawn 1.15x.
  - The happy cat stands grounded low in the doorway (DOOR_SPOT y 333, 0.85x) so it clears the door icon. Its audio was removed.
  - The first cat stays a banana cat until it reaches the door; only then does it become the happy cat.
  - Long captions now show in timed parts in the same box (`CAP_SPLITS` in the emitter → `capChunks`): f1, f3, f25, f31, f33 (3 parts), f57. f14/f15 captions split as well.
- **Customer-PDF script (artifact updated 9 Oct), mapped to our build:**
  - Sejal re-records ONE line: Ken's "80,000 customer PDFs in the backlog."
  - Audio trims I do from existing takes: f33 "of every ticket", f43b "Dark mode... feature request", f43c "real tickets", f53 ", not to a team". f39 "Your doors are the four teams..." is removed.
  - Plus about 11 on-screen visual swaps.
  - The artifact's "sir"/"Certainly"/panel-21 notes do not apply to our takes.
- **v6 (9 Oct):**
  - The second "okay okay" (f51) is cut.
  - The bench cat stops crying when the doors beat starts (calmAt).
  - The 50/50 → 94% example is now an icon resolver: an item card with two mini doors, dashed 50% routes, a coral ✕ on the loser, and 94% teal with a check on the winner.
- **v4 PDFs render (9 Oct), the customer-PDF version, applied:**
  - Audio: Ken's new take "80,000 customer PDFs in the backlog." is spliced onto "sorted by standup."
  - Audio splices in `PDF_SPLICES` (v10/s1m_audio.py): ai_f33 minus "of every ticket", ai_f43b minus the dark-mode sentence, ai_f43c minus "real tickets" (the one mid-word crossfade), ai_f53 minus "not to a team".
  - ai_f39 is cut. exp39 is now a 3.4s silent beat with labels d0..d3.
  - Folders, in order: Bank statement, ID proof, Address proof, Other. Bank statement comes first so the picked cat goes to door 1. Icons: bank, ID card, house, dots.
  - NOT FOR now sits on Address proof.
  - The example is "Statement with an address": ADDRESS (loser) vs BANK (94%).
  - Every screen now says PDFs or documents. The code is sort_doc plus pdf_to_text. Runtime is 3:08.6.
- **v5 (9 Oct): the doors line is back as "Your doors are the four folders."**
  - Source: `s1m/vo_src/ai_f39_pdf.wav`, wired as `ai_f39` in `PDF_SPLICES` (0.45s to the end).
  - The labels land from "folders" (d0 = folders - 0.05, then +0.35s each). Panel hold is 1.5s. Runtime is 3:08.7.
  - Why the line came back: it ties the nurse's doors to AJ's PDFs before "WAIT. YOU CAN DO THAT??", and it gives "the doors it's allowed to pick" in 43a its meaning.
- **v5b (9 Oct): the bed was raised** (high-pass at 140 Hz, a 2 kHz shelf, +6 dB, a 5 dB duck). A desk knock in the source is patched at each repeat.
- **v6 (9 Oct): end card.**
  - `EndCard` in S1mExplainers.tsx is the panel `exp_end` (4.6s). It plays after aj_f60 "system one model. obviously." and before ken_f61, matching GE's slate-then-reaction rhythm.
  - Layout: GE's slate scaled to 720-space and re-centred (DY 120).
  - Definition: "Built to choose. You give it the options, it picks one and says how sure it is."
  - No TIME or credits meter (Sejal). A tiny "Save this for later" pill with a bookmark that fills teal, with a tick sound.
  - Fonts MonaSans and Jakarta were copied to public/s1m/fonts. Runtime is 3:13.3.
- **v7 (9 Oct): bed brought down 4 dB** (BED_GAIN_DB 6 to 2, EQ kept) because Sejal said +6 felt too loud. It now sits at -30 dB in gaps and -34 dB under voice. **Drive still holds v6** (04 Cuts and the office bed mp3).
- **v7 render (9 Oct), 3:13.7:**
  - Bed at +2 dB.
  - ai_f13 now cuts at 3.44s in ai_all: "But without a-". At 3.46 the "l" of "limit" is already in. The caption sits in frame11's column (x 92, w 535, y 282). Frame 13 holds 0.63s.
  - `ambience.py` had an off-by-one in its probe slice, which the new timings exposed. Fixed.
- **f34 redesign: approved and APPLIED in v8 (9 Oct).**
  - `DenseScreen` was rewritten to the four-beat card design. UI sounds: a tick per card, a ripple on the parallel pass, a chime on the pick.
  - Figma frames:
  - Frames 825:2 / 825:79 / 825:168 / 825:265 ("exp-34 v2 · 1..4"), in section 797:2 at y 3120. The section grew to 4560 tall.
  - Cards sit at screen y 140. In beat 3 the PDF chip fans out to all four cards, and all four light up at once. In beat 4, a struck-through row of token pills sits in the top band and the bank card gets a check.
  - The original proposal: Swap the 11-row API log for 4 big folder cards, using the door icons, keyed to the VO:
  - "outputs": the cards drop in.
  - "calibrated / every": a % and a bar on each card.
  - "parallel": one PDF, one scan line that hits all four cards at once.
  - "token": a typing strip struck out, and the answer clicks to BANK 97%.
  - The VO stays fast; it is the setup for "again, but for a noob".
  - The plan is Figma frames first, waiting on Sejal's go-ahead.
- **v8 (9 Oct): the interruption overlaps.**
  - Frame 13's panel ends on the AI's last sample.
  - aj_f14 is cued at AJ_OVER = -0.105s. His take has 75ms of air before the M, so the M is already rising under the AI's "a" and "Man" lands at full level as the AI is cut.
  - Sejal heard the old ~0.1s gap as "not abrupt enough".
- **v8 bed:** BED_GAIN_DB -3, high-pass only (the treble shelf is removed). The printer patch now runs at PRINTER_OVER 3.0 over multiple passes (57 bursts). It sits at -35.3 dB in gaps and -39.4 under voice.
- **Drive (9 Oct): v8 uploaded to 04 Cuts** (1IEmRwNXleEFEpVnRM2OmekL2QVbfS-qU); v6 moved to 04 Cuts/old. Still v6-era on Drive: the office bed mp3, ai_f13.wav, and the f34 still in Explainers.
- **v9 Shorts cut (12 Oct), 2:59.2 to fit YouTube Shorts' 3:00:**
  - Cut: exp50 (step five), aj_f49 ("skip the test") and f48 (test result), -10.7s.
  - Holds trimmed to ~1s: f33, f34, exp37, exp38, exp43a/b/c.
  - Night: f19 is 2.2s and f20 is 2.4s. The end card is 3.8s.
  - Kept: f47 (AJ's "..." plus typing) and f52 (the diff). ai_f53's line ("And anything she isn't sure about...") continues f52's sentence, so f52 can't be cut.
  - Lost: the "ten for ten is how we got here" callback.

