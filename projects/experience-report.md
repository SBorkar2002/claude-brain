# Sejal Borkar — Experience Report
### GenAI Product Design, Epifi Technologies (Fi Money) / Tetriz · Jun 2026 – Nov 2026

Compiled 25 Sep 2026 from the full working record of the engagement.
Purpose: a single source of truth for resume bullets, portfolio, and interview stories,
written to survive the loss of company system access.

---

## 1. The honest positioning

You described your job to me as "mostly AI-generated videos." That undersells it badly, and if
you write your resume that way you will get filtered into a narrow, tool-dependent role.

What the record actually shows: for six months you worked across **an entire B2B product's
go-to-market surface**, on a two-person design team under a senior product designer. Narrative,
brand, motion, marketing site and a lead-generation product, and you shipped a meaningful part
of it as production code yourself.

Three things make you unusual, in order of market value:

**1. You ship code.** You made merged pull requests into a production Go/Next.js monorepo
(`workloom-dev/core`), through a real CI gate: linked issue, local `lci` run, required status
workflow, bot review threads answered. You set up a full backend toolchain on your machine
(Go 1.25, PostgreSQL 17, Redis) to pass those gates. Most designers at your level have never
opened a terminal. This is the single rarest thing on your resume and it should be visible in
the first five seconds of reading it.

**2. You build systems, not one-off deliverables.** You did not just make videos. You built a
production pipeline for making videos: reusable skill files merged into the company repo,
shared React component kits so the remaining feature pages could be stamped out, a documented
9-step comic production flow with named review gates, a codified motion and typography system.
That is design-ops thinking, and it is what separates a senior hire from a junior one.

**3. You work adversarially against your own output.** The clearest example: before the launch
video shipped, you ran the script against the real product documentation and found that one
scene's voiceover and visual described two different features, and that a "14% accept-rate
drop" statistic was fabricated. You killed both. Designers who catch their own factual errors
before a CEO does are rare and are trusted with more.

**My recommendation, and I will defend it:** do not target "visual designer." It would
undervalue everything above and put you in a queue competing on Dribbble polish. Target
**Product Designer (B2B SaaS, 0 to 1)** as the primary track and **Design Engineer** as the
secondary one. Keep the AI video work as your differentiator, not your headline. "Designer who
ships code and builds AI production pipelines" is a much scarcer profile than "AI video person,"
and it pays more.

---

## 2. Where to aim

| Track | Title keywords | Why you fit | Strength |
|---|---|---|---|
| **Primary** | Product Designer · Product Designer (0→1) · Founding Designer | You designed a real product surface (the assessment app), shipped it, and owned the narrative behind it. Startups hiring their first or second designer want exactly this range. | Strongest |
| **Primary** | Design Engineer · Product Design Engineer · Design Technologist | Merged PRs into a production monorepo, built shared React/Tailwind component kits, worked inside a CI gate. Very few designers can claim this. Often the best-paid track. | Strongest, most differentiated |
| **Secondary** | Growth Designer · Marketing/Brand Designer (B2B SaaS) | You built the marketing site's narrative spine, five feature pages, the competitive teardown, and a lead-gen assessment funnel with email capture and a share loop. | Strong |
| **Secondary** | Motion Designer · Creative Technologist · AI Content Designer | Remotion compositions, a codified motion system, a full video pipeline. Best used at AI-native companies where the AI tooling reads as an asset, not a gimmick. | Strong but narrower |
| **Avoid leading with** | Visual Designer · Graphic Designer · UI Designer | Real skill, but it hides the code and systems work and puts you in a more crowded pool. | Undersells you |

Companies to bias toward: developer-tools and AI-infrastructure startups (they value a designer
who reads code), Series A/B B2B SaaS hiring their first design generalist, and AI-native product
studios. Your Tetriz context (engineering intelligence, DORA metrics, AI adoption measurement)
is directly transferable to any devtools company and is a genuine domain advantage there.

---

## 3. The work, in six tracks

### Track A · Product launch video system (Jun – Aug 2026)

The flagship piece. A 2:15 product launch film for a CTO and CXO audience, taken from blank page
to rendered cut.

- Drove the script through six versions (v3 to v6), incorporating direct CEO feedback that
  reframed the core messaging: dropped a customer-facing product name, re-centred the throughline
  on "AI-native, faster," and reframed the coaching feature away from "extract from your best
  engineers" toward "teach everyone."
- Restructured it from prose into a **spine**: a bones-only beat structure naming the exact
  product screen that proves each feature, after your manager's feedback that polishing prose
  was the wrong layer to work at.
- Ran **two rounds of adversarial review** against the real product documentation. Caught a
  self-contradiction between voiceover and visual in Scene 4, a more serious mismatch in Scene 5
  where the script described an org-wide feature while the visual showed a deliberately private
  individual one, and a fabricated statistic. All three fixed pre-render.
- Built the **10-frame storyboard in Figma** (1920×1080), replicating real product screens
  faithfully from the product repo rather than inventing mockups, with every mocked element
  explicitly flagged on-frame.
- Designed a **persistent three-pillar map** that runs across all scenes so a viewer always knows
  where they are in the argument, and reordered the scene sequence so related pillars stayed
  contiguous instead of flickering back and forth.
- Built the final composition in **Remotion** (React-based programmatic video), with ElevenLabs
  voiceover and Whisper word-level timestamps driving caption timing.

**Interview story to tell:** the adversarial review. It shows judgment, product depth, and the
willingness to break your own work.

### Track B · Production pipeline and design systems (Jun – Sep 2026)

The systems layer underneath everything else, and the most senior-signalling work you did.

- Authored and merged **four reusable skill files** into the company product repository
  (`seo-scene-prompt-generator`, `seo-script-refiner`, `launch-scene-prompt-generator`,
  `launch-script-refiner`) via PRs #299, #306, #433, so script refinement and scene generation
  became repeatable by others, not locked in your head.
- Evaluated and selected the toolchain across several months: Claude Design, Remotion,
  Higgsfield, Figma Make, Manus, Hyperframe, ElevenLabs, Whisper. Rejected tools with reasons on
  record. Landed on a deliberate two-tool split (one for frames, one for animation) and a
  **semi-automated, not hands-off** philosophy: automate the repetitive steps, keep the creative
  decisions manual.
- Cut storyboard production time from **4 days on the first video toward a 1-day target**, with a
  stated goal of 70% of a 30-second video done in 2 days including one feedback round.
- Codified a reusable design language across 20+ documented rules, including a full **typography
  system** (three-font stack with a complete type scale and colour tokens), an **object-identity
  system** (icon carries identity, colour carries state) reused across scripts, caption placement
  and timing rules, motion easing rules, and layout rules.
- Built a **docx generator** (`format-launch-script.js`) to replicate manual document styling
  programmatically, removing a repeated manual formatting step.

### Track C · Production front-end work (Jul – Aug 2026)

Design that shipped as code.

- Built **five feature marketing pages** in the production Next.js site: AI Adoption, AI Impact,
  Session Security, Product Overview, and Why Tetriz. Each with hero, animated in-code dashboards
  (not screenshots, not flat bars), deep-dive sections, FAQ, and cross-linking.
- Extracted **three shared component kits** (`feature-kit`, `dashboard-kit`, `feature-carousel`)
  so the remaining pages could be composed rather than rebuilt: layout primitives, animated chart
  primitives, count-ups, window chrome, segmented bars, and a scroll-snap carousel.
- Made and executed a **site-wide information architecture call**: removed the internal
  "Observe / Transform / Govern" taxonomy from all user-facing copy on the argument that the
  audience should not have to learn the team's internal vocabulary. Flattened the nav to five
  features and restructured the mega-nav accordingly.
- Built data visualisations in SVG with real design tokens, including a velocity-by-quality
  quadrant and a two-trajectory index curve with a shaded advantage gap.
- Ran a plain-language pass on all external copy using a de-AI-ification skill chain.

### Track D · AI-Native Index assessment (lead-gen product) (Jul 2026)

The clearest end-to-end product design case study you have. Own it as such.

- Took over an existing 15-question lead-generation assessment and redesigned it end to end:
  low-fidelity wireframes, six screens, a clickable Figma prototype, then the shipped code.
- Reframed the **intro from a flat explainer into a curiosity hook**: a masked preview of the
  user's own future result, a three-outcome payoff list, and a tension line. Principle applied:
  curiosity gap plus payoff preview beats interrogation.
- Rebuilt the **result screen** to trace back to the user's own answers, grounded in the quiz's
  actual scoring logic. Cut the internal pillar model, the gate box, the feedback-loop meter and
  the "capped score" language. Kept: stage, score, a horizontal stage stepper with per-stage
  icons, a gate-led one-liner, the four things the user told us shown back with colour-coded
  status, and one recommended next move.
- Correctly **rejected a structure I proposed** where two independent scoring tracks were fused
  as if one were evidence for the other. Worth remembering: you caught that, not me.
- Built all five stage-variant result pages, each with real per-stage data from the scoring doc.
- Identified and fixed a **product contradiction**: the intro promised "no email required" while
  the funnel needed lead capture. Added a proper email-capture step to resolve it.
- **Shipped it.** Merged PRs #6611, #6649 and #6686 to master covering Figma colour alignment,
  tone-driven result tiles, a tiered scoring gate, LinkedIn share captions with clipboard copy
  and inline fallback, resume-on-refresh via local storage, a required name and email gate, a
  two-axis position chart, and a full mobile responsive pass with a vertical stepper.

### Track E · Brand narrative and marketing strategy (Jul – Aug 2026)

- Led the **landing page narrative rebuild**. Authored the endorsed story spine (solve Quality,
  then Cost, then Speed, then introduce the AI-native curve) and produced two annotated flow-map
  options in Figma against it.
- Ran a **competitive teardown of Glean**, mapping its full page structure beat by beat, and used
  it to resolve an open team question about whether the Quality/Cost/Speed pitch was
  differentiated. Conclusion: the pillars are validated by the market, and the wedge is that
  competitors stop at observation.
- Established the placement principle that engagement interludes sit at story seams, never
  mid-argument, and applied it to the quiz and dogfooding beats.
- Built the **AIDLC maturity curve** slide graphic in Figma for an enterprise sales deck (EY),
  converting a founder's LinkedIn chart into a branded 16:9 visual using real design tokens
  pulled from the codebase.
- Set the **YouTube channel direction** for employer branding: multi-bucket, connected formats,
  zero product content, aimed at the engineer who is not an AI power user and feels the ground
  moving.

### Track F · Comic video series (Aug – Sep 2026)

An original IP format, designed and produced end to end.

- Designed a **9-step production pipeline** with named blocking review gates and a strict rule
  separating the review surface from the frozen record, so art and voice could never be generated
  from divergent script versions.
- Added a rough voice pass immediately after script approval, before any art, on the reasoning
  that these gags depend on delivery and you should not pay for 22 panels to learn an episode
  does not land.
- Locked the **art direction**: a neat comic register, greyscale with exactly one teal accent,
  and a single six-petal mark with an eye as the AI's on-screen identity.
- Built EP003, a ~62-second vertical (9:16) episode from 31 panels, including a **seamless loop**
  where the last and first frames are pixel-identical, a three-way cut of a single voice recording
  so the loop's pitch does not step across the join, and a **lip-sync system built by swapping
  between real storyboard frames** rather than painting mouths.
- Solved the production problems yourself: background keying of generated art, head measurement,
  audio cutting in ffmpeg, and compositing.

---

## 4. Resume bullets, ready to use

Pick 5 or 6. Do not use all of them. Numbers in `[brackets]` are ones you should confirm before
using, since I do not have verified figures for them.

**Headline framing for the role line:**
> GenAI Product Designer · Epifi Technologies (Fi Money) · Jun 2026 – Nov 2026
> Product, web, brand and motion design for Tetriz, a B2B engineering-intelligence platform.
> Two-person design team, working to a senior product designer.

**Bullets, strongest first:**

- Shipped [3] merged pull requests to a production Next.js and Go monorepo through a full CI
  gate, redesigning and building a lead-generation assessment app end to end, from wireframes and
  prototype through responsive front-end implementation, share loop and lead capture.

- Built 5 feature marketing pages in production Next.js and extracted 3 shared React component
  kits (layout primitives, animated dashboard primitives, carousel) so the remaining pages could
  be composed instead of rebuilt.

- Designed and produced a 2:15 product launch film for a CTO audience, from script through
  storyboard to rendered Remotion composition; ran an adversarial review against product
  documentation that caught two voiceover-to-visual contradictions and one fabricated statistic
  before release.

- Built a semi-automated video production pipeline (script refinement, scene generation, Figma
  frames, ElevenLabs voiceover, Whisper word-level timing, Remotion render) and merged 4 reusable
  prompt-skill files into the company repository, cutting storyboard time from 4 days toward a
  1-day target.

- Redesigned a 15-question lead-gen assessment end to end: reframed the intro as a curiosity hook
  with a masked result preview, rebuilt the result screen to trace back to the user's own answers,
  and added the missing email-capture step that resolved a contradiction in the existing flow.

- Codified a reusable design language across 20+ documented rules covering typography, colour
  tokens, motion easing, caption systems and an object-identity model (icon carries identity,
  colour carries state), reused across every subsequent video and page.

- Made and executed a site-wide IA call to remove internal product taxonomy from all user-facing
  copy, on the argument that the audience should not have to learn the team's vocabulary;
  restructured navigation and 7 surfaces accordingly.

- Owned the landing-page narrative rebuild: authored the approved story spine, ran a competitive
  teardown that resolved an open positioning question for the team, and produced annotated
  flow-map options in Figma.

- Created and produced an original short-form comic video series, designing a 9-step production
  pipeline with review gates, locking the art direction, and building a 62-second 31-panel
  vertical episode with a seamless visual loop and frame-swap lip sync.

**Skills line:**
> Figma · Next.js / React / Tailwind · Remotion · TypeScript · Git & GitHub PR workflow ·
> SVG & data visualisation · Design systems · Motion design · ElevenLabs · Whisper · ffmpeg ·
> Claude Code · Veo3 · Higgsfield · Narrative & UX writing

---

## 5. Do this before you lose access (urgent)

This is the most time-sensitive thing in the document. You have roughly six weeks. Once the
accounts are gone, none of it is recoverable, and a portfolio without artefacts is just claims.

**Save to personal storage now:**

1. **Video renders.** Every finished cut: the launch video, the SEO videos, the DORA video, every
   comic episode. MP4 files to a personal Google Drive and a local drive.
2. **Figma files.** Duplicate every file into your **personal** Figma account, not just export
   PNGs. Named files to pull: Launch-Screens (storyboard), the quiz wireframe file, the website
   wireframe file, the AIDLC curve file, the comic pages. Export high-resolution PNGs as backup.
3. **Screen recordings.** Record yourself clicking through the quiz prototype and the live feature
   pages. A 20-second screen capture of an animated dashboard is worth more in a portfolio than
   any static image.
4. **Page screenshots.** Full-page captures of all five feature pages, desktop and mobile.
5. **Your PRs.** Screenshot the merged PR pages (title, description, diff stat, review threads).
   Note the repo, PR numbers and dates in a text file. You will not be able to link to a private
   repo, so the screenshots are the evidence.
6. **Your own writing.** The skill files you authored, the pipeline document, the decision logs,
   the spine document. These are your best evidence of systems thinking. Copy the text out.
7. **A written reference.** Ask your manager and Anandhi for a LinkedIn recommendation **now**,
   while the work is fresh and before everyone scatters. Also ask for one line each on impact
   they observed, which you can quote in interviews.
8. **Real numbers.** Ask whoever holds them, before systems go dark: video view counts, quiz
   completion and lead numbers, page traffic, anything the sales team fed back. One verified
   number beats ten adjectives on a resume.

**On confidentiality:** some of this is not yours to publish. The AI-Native Index curve was
marked "not for distribution," the sales collateral and product-brain documents are internal, and
unreleased product screens should not go on a public site. Safe approach for a public portfolio:
show the work you can (your own videos and the public marketing pages, once they are live),
blur or redact real dashboard data, and describe the rest in process terms without the artefacts.
Keep a fuller private version, PDF or a password-protected page, to share directly with hiring
managers. If in doubt, ask your manager what you may show before you leave. Getting that in
writing costs one message and protects you later.

---

## 6. What to fix in the resume itself

I will do a proper line-by-line pass once you paste or upload the current version. In advance,
the four things I already expect to change:

1. **The title line.** "GenAI Product Design Intern" is accurate but reads narrow. Consider
   "GenAI Product Designer (Intern)" with a one-line scope statement underneath naming the range:
   product, web, brand, motion. The scope line does more work than the title.

2. **Lead with code, not video.** Whatever your first bullet is now, it should become the shipped
   product work. Recruiters scan the first bullet of the most recent role and little else.

3. **Cut the tool list from the bullets.** Tool names belong in a skills line. Bullets should
   carry decisions and outcomes. "Built X so that Y" beats "Used Veo3 and Canva to make videos."

4. **One case study, linked.** A single well-told case study (the quiz, end to end: problem,
   wireframes, prototype, shipped code, what you cut and why) will outperform a gallery. Link it
   from the resume. If you only build one portfolio piece before November, build that one.

---

## 7. The two sentences to say in interviews

When they ask what you did:

> "I worked on the go-to-market surface of a B2B engineering-intelligence product, on a
> two-person design team. I took a lead-generation product from wireframes to shipped code as
> merged PRs into the production monorepo, built five feature pages, and built the video system
> we used to sell it."

When they ask about the AI video part:

> "The interesting part was not generating video, it was building the pipeline. I figured out
> which steps could be automated and which had to stay a human decision, wrote the repeatable
> parts into skill files the rest of the team could use, and took storyboard time from four days
> toward one."
