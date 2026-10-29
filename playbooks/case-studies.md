# Case studies and take-home assessments

How Sejal runs a case-study revamp or a take-home, and the record of every past one. State as of 22 Oct 2026.

---

## 1. The process (what worked, in order)

1. **Read the brief literally.** List the deliverables, grading criteria, deadline, size limits and what is NOT in the brief. Her catches: the Instahyre brief never named Instahyre or its palette, never promised "one seat left", and the contest question is asked at registration, not later. Design only what the brief and real user flow support.
2. **Advisor breakdown first.** Give a verdict and a plan like a senior designer or art director: the spine/concept, the order of sections, what to cut, how to save time. She asks for this explicitly ("act like an art director", "think like a senior designer"). No menus of equal options.
3. **Research that gets used.** At most ~8 references, each with one line: what to steal and which section it goes to. Flag paid or unlicensed sources. Wide 4-agent fan-outs over hundreds of prompts burned usage limits and produced little; keep research narrow.
4. **Pick a distinct register tied to the product's meaning.** Sourced = night gallery; Green Gallery = cute and bubbly; #futureofhr = "the page IS the video call"; portfolio = pixel chrome with HD work. Check it does not look like her other projects.
5. **Style tile gate.** Palette, type pair, one component, one motion idea, one real content block. She approves before anything past the tile is built. Building 20 screens on an unapproved style is the most expensive mistake in this history.
6. **Tokens, then build in Figma in batches.** Variables and text styles first; never hard-coded hex. For redesigns, never edit the original: Duplicate the frame/page and build side by side (copy-paste breaks prototype links). Note before/after node ids.
7. **Prototype.** Figma has no on-scroll trigger: use interactive component variants (Static > Idle > phases > Done) with MOUSE_ENTER + ON_CLICK, AFTER_TIMEOUT for loops. The API cannot set PUSH/SLIDE on CHANGE_TO inside components: use instant or dissolve. Claude cannot play Present: list the exact hotspots and keys for her to try.
8. **QA before showing.** Em dash scan of every TEXT node and layer name; bounding-box overlap check; text overflow; numerals readable; image crops centred on faces; no repeated images side by side. The studio plugin's `figma-qa.js` automates this.
9. **Write-up with the truth rules** (section 3). Case study spine: one-line summary, context, problem (as a problem, not a task), research/grounding, decisions (chose / rejected / why), what shipped, what she would change.
10. **Publish only when safe.** Take-homes go public after the hiring process closes (or with recruiter OK); label as "Take-home" / design assessment, not client work.

### Case-study page anatomy (portfolio template)

Top: kicker, title, one-liner, meta row (no "Role" tag in a project case study; use e.g. "Focus"), hero visual. Then 01 Overview, 02 Problem, 03 Before, 04 Decisions (chose / cut / why + a visual each), 05 What shipped, 06 What I would change, Next card. Sticky contents rail, keys 1 to 6. Drop any section without real material.

## 2. Take-home rules she set

**Behance rule (23 Oct):** Behance case studies get their own visual identity from each project's real brand and
product, never screenshots of the portfolio pages (that made every project look the same, in the portfolio's pixel
chrome). Style tile per project first, she picks, then the full boards. Never reuse the portfolio chrome on external platforms.

- Never name the hiring company if the brief does not (the #futureofhr page has no Instahyre name or logo; event identity is the hashtag).
- No invented scarcity, prizes, dates or quotes presented as real. If something is invented (a deadline, a quote, askers' names), it is a flagged placeholder.
- Timeline logic: a pre-event page cannot show anything as already answered or won.
- "I like that card" means its LAYOUT, not its colours: recolour to the page palette.
- Graphics must come from the page's own motif system (tickets, call tiles, rules), never glossy clip-art (a vector gift box was rejected as "forced on the screen").
- Photo slots she marks full-bleed get no padding and no radius.
- AI-generated art in art take-homes: generate ingredients (character on flat grey, empty plates, FX on black), not finished panels; character sheet first and attach it to every generation; hand-composite in Photoshop because they open the layers.
- Credit Claude honestly and narrowly: research synthesis, planning/prompt kit, design QA. Never "Claude designed it".
- Before publishing a take-home: check the email/brief for ownership or NDA terms, wait for the process to close, replace watermarked stock photos, note that panels/people are fictional. (For #futureofhr she chose on 17 Oct to publish as-is, including the watermarked photo, since the process seemed closed. Panelist photo and company logo rights remain unchecked.)

## 3. Truth rules for any case-study copy

- Never "human-made VS AI" for Sourced: the platform holds both, so "and" / "side by side".
- Survey counts: say "25+" / "more than 25" for Sourced, never 27, never "interviewed" (it was a survey).
- Never justify a product pivot with one respondent ("several respondents... half of all answers asked for two separate sections").
- Numerals never in a display face with uneven baselines (Syne); use a sans SemiBold.
- No invented metrics. No "Role" tag inside a project case study.
- Connectors in diagrams route as L-shapes through gaps, never through UI.
- Self-critique section ("what I would change") is always included; it reads as maturity.

---

## 4. Project records

### #futureofhr webinar landing page + launch video + poster (Instahyre take-home, 6 to 7 Oct 2026)

- **Brief:** landing page for a live webinar "The Future of Remote Hiring", 3 panelists (imaginary photos/names allowed: Mayank Singh HRBP Amazon, Ajit Singh HR Dell, Aniruddh Patel Head Target), registration form, #futureofhr best-question contest with prizes. Audience: corporate/enterprise HR. Graded on design quality, idea, graphics, palette. 72 h; design link + full-page screenshot. Assignment 2: 10 to 25 s launch video + LinkedIn poster, graded on design, idea, video, animation, palette.
- **Direction history:** v1 Instahyre-derived (navy/teal, Urbanist/Manrope) > v2 "warm editorial" (Instrument Serif, paper, signal orange) REJECTED as "Claude-coded" > v3 = v2 layout and content in the v1 look, plus variants A "Center stage" and B "Split editorial" > all called generic AI slop on 14 Oct > **v4 "The Call" (final)**: 2020 moved hiring onto a video call, so the page IS the call. Panelists = call tiles, agenda = video chapter bar, visitor = empty tile "You · on mute" > "Unmute." contest > "Seat for You" pass. Prize-first contest ("The best question wins."), prize pass ticket with a blinking caret, question queue panel.
- **System (v4):** Cobalt #2A35E6 field, Lime #D6FF3D live/action only, Ink #0C0D12, Paper #F1F0EC; Funnel Display ExtraBold/Bold, Funnel Sans, Geist Mono; photos greyscale + cobalt COLOR blend + 30% multiply; NOISE grain plates. Motion: every section is an instance of a reveal component (clip-mask type rises, strike/highlighter bars, ticket wipes with inner parallax, playhead scrub), expo-out and quart in-out curves, no bounce.
- **Figma:** `z263yFoeKFoWhY7Ocb3WqK` ("Assessment"). Page "06 · New direction · The Call" 5:2: landing 7:2 (1440x7400), direction board 18:2; prototype components page 26:2. Page 1 "Launch video + poster": poster 64:2, styleframes V01 to V06. Older v1 to v3: `TlNlTdAyC7LN0Xhs6QdVB0`.
- **Video:** Remotion project `~/Documents/Personal/instahyre-launch-video` (600 frames @30 fps, 120 BPM cuts, audio synthesised in numpy, -14 LUFS). Outputs `out/futureofhr-launch.mp4`, `out/futureofhr-linkedin-poster.png` (both 4:5 1080x1350).
- **Status:** submitted; no reply after a week, so she treats the process as closed. Live on the portfolio at /work/futureofhr (tagged Take-home, Instahyre unnamed). Open: watermarked Mayank photo, fictional askers Priya R./Karan M., invented 23 Oct deadline, logo/photo rights.

### The Last Over (TheAlterOffice "Visual Designer, Comics & Game Art" take-home, ~8 Oct 2026)

- **Brief** (`~/Downloads/Design_Test.pdf`): 4 to 6 h, 3-day window, AI assets allowed but page design manual in PS/AI. One PDF + layered PSD/AI: 1-page shot plan, 1 to 2 comic pages (6 to 10 panels, A4 2480x3508), Kabir Rana hero sheet (5 expressions + 1 action pose), half-page process note. Graded on character consistency, clarity, paneling, compositing, one unifying grade, cricket authenticity, lettering.
- **Direction given:** spine = the crowd's war drums stop when he walks out and return chanting RA-NA on the last ball; hand-built scoreboard HUD; 2 pages, 10 panels; face only in P2 and P10 (helmet carries identity elsewhere); one cyan accent on amber/blue-black. Generator: Gemini (free) with a 4-block prompt kit (STYLE, LOCK, KIT, GREY), anchor portrait attached to every Kabir prompt.
- **Her build:** 16 panels in a zigzag A4 layout, black caption boxes for inner monologue, white burst balloons for speech/commentary, hand-painted ball trails and swing effects, Photoshop background removal, lighting matched to plates. Review flagged: over the 10-panel cap, theme-stating captions, commentary in burst balloons, a ground-level four lettered as a SIX, duplicate crowd plate, blood-looking stains, two Gemini sparkle watermarks on the character sheet. Kept her beat "RUN, KID!" / "Don't need to."
- **Files:** Drive folder (TheAlterOffice); local copies in `~/Documents/Personal/career/portfolio-pixel/inventory/drive/TheAlterOffice/` (PAGE 1, PAGE 2, character sheet, ONE SHOT PLAN, process-note.txt). The 618 MB PSD was not downloaded.
- **Status:** unclear from history whether the final submission used the 10-panel remap or her 16-panel pages. Shown in the portfolio Art room comics card.

### UXpective carousel (take-home)

- 7-slide "2025 UX Challenges" carousel with cat-meme stickers. Figma `72tXrfMYH64v0hkxDF1m2n`, page "ux pective" (0:1). Planned for the Art room graphics group. Brief, date and outcome: unclear from history.

### Sourced (personal project, revamped 16 to 17 Oct 2026) · the ONE personal project kept

- **What:** mobile app (412x917) where human-made and AI art live side by side in separate feeds; verifies human artists, attaches process "evidence" to posts, pairs artists as Art Buddies who send daily WIPs to keep a "Flow" streak. Research: Google Forms survey of 25+ (mixed sample: traditional artists, hobbyists, non-artists, AI users).
- **Direction:** "Lilac + Vermilion" night gallery, dark. Ink #0E0E11, surfaces #16161B/#1F1F26/#2A2A33, text #F4F3F7/#A6A3B2/#6F6C7B, Lilac #B8A9FF brand/actions, Vermilion #FF5A36 = human-made ONLY (badge, evidence, Flow), Steel #8A93A6 = AI. Syne ExtraBold titles, Geist UI, Geist Mono meta. New Syne wordmark set 26:825.
- **Figma** `72tXrfMYH64v0hkxDF1m2n`, page "Sourced · Redesign" (4:187 / 8:414 area): **live case study = "Sourced · Case Study (Night)" 48:414** (1440 wide, ~28k tall); light version 33:414 superseded; Components frame 10:2 (42 components incl. icons 59:828 to 59:868, option card 59:895, buddy badge 59:908); 20 screens with 83 hotspots, flow "Sourced · App". Old original "screens" group was deleted; old screens survive only in the old Behance images.
- **Decisions to tell:** separate, do not exclude (two feeds, not a ban); make the process the proof (evidence timeline); pair artists as Art Buddies; AI-assisted create skips evidence; "Requested" not "Added"; nudge pings a buddy who has not sent today's WIP.
- **Behance:** new re-upload https://www.behance.net/gallery/257216237/Sourced-Artist-Accountability-Verification-Platform (older 249130267 is hidden from her grid).
- **Status:** live at /work/sourced (11 tappable phones). Pending: native code rebuild of the flow; 2x exports.

### Green Gallery (personal: plant donation/adoption) · DROPPED 17 Oct

- Originals on page "green gallery" 77:16303 in `72tXrfMYH64v0hkxDF1m2n`. Rethought as P2P adoption with a trust layer, India market. Directions tried: herbarium editorial (rejected as AI-generated), cute and bubbly (Fredoka/Nunito, mascot "Sprout"; style tile 92:141 called "bad"), growing-plant hero 96:207, then a "plant passport" with hanging listing tags (unfinished). She dropped it ("turning out to be ass"). Do not revive unless she asks. Lesson: three directions without an approved tile.

### Lead-gen assessment (Epifi work, NOT a take-home) · "AI-Native Index" quiz

- Shipped Epifi product work used as portfolio case study 06 (/work/lead-gen-assessment, in "More work"). 19 questions, 6 screens, 5 result states, desktop and mobile. Decisions: intro reframed as a curiosity gap with a masked result preview; result screen rebuilt around the user's own answers (cut the internal 3-pillar model); fixed the "no email required" vs lead-capture contradiction with an email step; rejected fusing two independent scoring tracks. Shipped via merged PRs (#6611, #6649, #6686) in the company monorepo (do not cite PR numbers or branches in public copy). Wireframes: Figma `nyj8rbPsYnRozDmtHJgQzq`. The LinkedIn share-caption feature was a colleague's (Surya), not hers. Live quiz returns 404 since mid Oct.

### Marketing site feature pages (Epifi) · case study 01

- Five feature pages in production Next.js, shared kits (~20 components), nav restructured (Product/Pricing/Company removed, FAQ added, all surfaces under Features, flat five instead of a pillar taxonomy). Problem: pages read flat, generic, AI-made and did not look like the product. Decisions: one "at org scale" story reused across pages; graphs that explain themselves (labels never touch the curve); match the real product; clear nav hierarchy. Built code-first on the portfolio; Figma page not made.

### AppsForBharat blog · case study 04

- Designed start to finish: home, article, category pages, cards, tab nav, mobile + desktop; live at blog.appsforbharat.com. Themed thumbnail system: one shared identity per category, each post customised within it. Plus print/merch (buddy tee, appreciation cards, Women's Day card, 3D-printed keychain). Source Figma: `72tXrfMYH64v0hkxDF1m2n` node 114:1729. Live blog's 390 px view overflows sideways (not hers to fix).

### Video production system (Epifi) · case study 05

- "Making a B2B SaaS launch film": spine first then frames, persistent 3-pillar map, 18 Figma frames, Remotion build, VO + captions. Product unnamed on the page. Storyboard Figma `30sryhNZr624S6zxJMf6Xz`. Claim "4 days to 1" needs her confirmation (sources say 1 day was the target).

### Concept art self-brief "The Last Hands" (not started)

- `~/Documents/Personal/career/concept-art-project-01.md`: a guild that certifies human-made work; design 3 ranks readable by silhouette alone, one accent colour, no AI at any stage, 4 to 6 weeks part-time, process (thumbnails, iterations, callout sheets) is the deliverable. Only relevant if she pursues concept art; see `projects/career.md`.
