# Portfolio Build — Handover Brief

For: a fresh Claude session that will build the site.
This document is self-contained. Assume no prior context.

---

## 1. Who this is for

**Sejal Girish Borkar.** Product designer based in Bengaluru, India.
Currently GenAI Product Designer (Consultant) at Epifi Technologies / Fi Money, through
November 2026, when the company winds down. Master of Computer Applications, Ramaiah
Institute of Technology.

**Roles being targeted**, in priority order:
1. Product Designer, 0 to 1 / founding designer / B2B SaaS
2. Design Engineer / Product Design Engineer
3. Growth or brand design at B2B SaaS (secondary)

**Positioning, in one line:** product designer who ships.
The differentiator is that she designs *and* ships front-end to production, and builds
reusable systems rather than one-off deliverables.

**Important nuance on the front-end claim.** She ships production front-end using Claude
Code. She can read and modify components and work inside repo conventions. She is not
writing React from scratch. The site must never imply framework expertise she does not
have. Phrase it as codebase work, never as "React developer."

---

## 2. What the site has to do

**Primary reader:** a product design hiring manager with about ninety seconds who wants to
find a case study and judge whether she can think.

**Secondary reader:** a brand, content or creative lead who cares about the motion and
illustration work.

**The job of the site:** get to substance fast, prove she ships, and show range without
diluting the product design pitch.

---

## 3. The governing principle

**Cinematic frame, fast core.**

She wants a premium scroll experience. The risk is that cinematic scroll buries the
substance and loses the hiring manager. So:

- **Scroll craft lives in the shell:** hero, transitions between projects, section reveals,
  and above all the art section.
- **Case studies stay fast:** scannable, deep-linkable, with a sticky section nav so a
  reader can jump straight to Research or Final design without scrubbing.

Reference sites for *feel*: Cappen, Minh Pham, Uncommon Studio (layered scroll, modular
systems, smooth transitions). Do **not** copy Bruno Simon's driving-game portfolio. It is a
brilliant developer showpiece and exactly the wrong model, because nobody hires a product
designer from it.

Do **not** take case study structure from any of those sites. They are showcase sites with
almost no written depth, which is the opposite of what she needs.

---

## 4. Structure

```
/              home
/work/[slug]   case studies
/art           craft and illustration (separate route, prominently linked)
/about         experience, skills, resume download
/contact       or a section on home
```

**The one structural rule:** separate the work from the art. A product design hiring manager
must never scroll past digital art to reach a case study. The art gets its own route. It is
linked clearly, never interleaved.

---

## 5. Content inventory

### Tier 1 — full case studies, these carry the hire

**1. AI-Native Index assessment (Epifi).** The lead project.
A lead-generation assessment, 19 questions, 6 screens, 5 result states, desktop and mobile.
She took it over from an existing build and redesigned it end to end: low-fidelity
wireframes, a clickable Figma prototype, then shipped front-end code merged to production
behind a full CI review gate.
Key decisions worth telling: she rebuilt the result screen to show users their own answers
back instead of an internal three-pillar model the audience had no context for, and she
found and fixed a contradiction where the intro promised "no email required" while the
funnel existed to capture leads. She also correctly rejected a proposed structure that fused
two independent scoring tracks as if one were evidence for the other.
Show as "a B2B engineering-intelligence platform," not by product name. See §9.

**2. Feature pages and component library (Epifi).**
Five feature marketing pages built in production Next.js. The repeated pieces (section
headings, tick lists, browser-window chrome, animated bars, count-ups, chart panels, a
carousel) were pulled into three shared files totalling roughly twenty components, so later
pages were composed rather than rebuilt.
Also: she restructured the main navigation, splitting a single Product mega-menu into Product
and Features and flattening the feature list from an internal taxonomy to a flat five, on the
argument that users should not have to learn the team's vocabulary.

**3. AppsForBharat blog.** Live at https://blog.appsforbharat.com/
Designed start to finish: home, article and category pages, card components, tab navigation,
mobile and desktop. Includes a **themed thumbnail system** — one visual identity per
category, with each post's thumbnail customised within it. That is a design system, and it
is her second systems proof point. Treat it as such.

### Tier 2 — supporting

**4. Sourced — artist accountability platform.**
https://www.behance.net/gallery/249130267/Sourced-Artist-Accountability-Verification-Platform
Mobile case study on separating human and AI artwork. Research-led: a survey across a
deliberately mixed sample (traditional artists, hobbyists, non-artists, AI tool users), 27
responses, quantitative findings, an IA sitemap, then UI where the core decision (separate
Non-AI and AI feeds) visibly follows from the research.
**Accuracy fix required:** older copy says "interviewed 25+ artists." It was a survey with 27
responses. Write it as surveyed, and say 27.

**5. Instahyre design assessment.** HOLD — do not publish yet. See §10.

### Tier 3 — craft and range, on /art only

- **AI FOMO Lab / "I Have No Idea What That Means"** — a short-form comic video series she
  created: format, script, art direction and edit. 4 episodes; the best performer drew
  30,000+ organic views on Instagram. This is the only externally validated number she has.
- **Product launch film** — a 2:15 film for a CTO audience, plus the production system behind
  it (reusable instruction files committed to the company repo, defined review gates,
  storyboard time cut from 4 days toward 1).
- **PocketFM / PocketToons** — comic panels arranged from writer scripts, AI image generation,
  Photoshop retouching (Aug–Dec 2025).
- **JENEKO digital art** — semi-realistic illustration, characters, fanart.
- **Mascots and brand illustration** from AppsForBharat.

### Cut entirely

- **Moduvo** — her decision. (It is well-executed, but it has no research step and its central
  claim, that no dedicated cross-org collaboration space exists, is false; Slack Connect,
  Teams shared channels, Basecamp and the whole client-portal category all occupy it.)
- **Indeed redesign** — the single most common portfolio cliché.
- **Green Gallery, Make it 10** — demote to a minor grid at most, or drop.

---

## 6. Case study template

Use the same spine for every Tier 1 and 2 piece. Sticky section nav, deep-linkable anchors.

1. **One-line summary** — what it was and her role
2. **Context** — what existed before, who it was for
3. **The problem** — stated as a problem, not a task
4. **Research or grounding** — what she knew and how
5. **Decisions** — the meat. Each decision: what she chose, what she rejected, why
6. **What shipped** — artifacts, screens, link if public
7. **What she would change** — include this. Self-critique reads as maturity and almost no
   junior portfolio has it.

Every case study needs a **scannable top**: title, role, timeframe, one-line outcome, visual.
A reader should be able to decide whether to keep reading in five seconds.

---

## 7. The art section — direction

This is where the scroll craft belongs, because here the reader is browsing, not evaluating.

- Let it feel **distinctly different** from /work while sharing the type and colour system.
  Fuller bleed, bigger imagery, more motion, less text.
- **Video first.** The comic episodes and the launch film are the strongest pieces. They are
  9:16 and 16:9 respectively, so the layout must handle both without letterboxing everything.
- Autoplay muted, loop, with a click-to-expand. Never autoplay with sound.
- Group into: **Motion** (comic series, launch film), **Illustration** (JENEKO, PocketFM),
  **Brand** (mascots, campaigns).
- One short line of context per piece. This section is for looking, not reading.
- Respect `prefers-reduced-motion` throughout.

---

## 8. Stack

- **Next.js on Vercel.** Confirmed. This doubles as proof of the front-end claim, so the repo
  should be clean and public-ready.
- Her current site is React on Vercel at sejalborkar.vercel.app. This is a **rebuild**, not a
  patch. The old site's copy is stale and should not be carried over.
- Typography and palette are open. Her current site is dark charcoal. She has strong
  typographic instincts and a documented type system from work (Mona Sans, Plus Jakarta Sans,
  Geist Mono) — that is a *reference*, not her personal brand. Let her choose.

---

## 9. Hard rules

**Confidentiality (Epifi work).** The company is winding down, but confidentiality and IP
terms survive. Until she has written clearance:
- Refer to it as "a B2B engineering-intelligence platform," **anonymised, not named**.
- Lead with **her own artifacts**: wireframes, prototypes, process. Not production screenshots.
- Never show: real customer or prospect data, sales collateral, unreleased product screens, or
  the AI-Native Index curve (explicitly marked not for distribution).
- Redact or rebuild anything showing live metrics.

**Her standing design preferences** (these are long-held and non-negotiable):
- **No em dashes** in any external-facing copy.
- **Never rotate or tilt** cards or any element. Create asymmetry with position, size and
  opacity instead.
- **Never overlap elements** unless explicitly asked. Check bounding boxes.
- **Short subtexts.** Any lede under a title is one short sentence. Trim aggressively.
- **No chips, badges or proof rows** below hero CTA buttons. A reference showing them does not
  override this.
- **Motion:** a pulse must ease out, never stop dead. Fade by opacity, never by scaling
  geometry.

**Tone.** Avoid AI-sounding copy. Specifically: vary sentence length, cut explanatory "so
that…" tails, and never use the phrase "end to end" more than once on the whole site.

---

## 10. Open items

| Item | Status |
|---|---|
| Epifi asset capture (screen recordings, page captures, Figma files) | **In progress, blocking Tier 1** |
| Written clearance on what Epifi work may be shown | Requested, unresolved. Default to anonymised + own artifacts |
| Instahyre assessment | **Hold.** Process still open. Before publishing: replace the watermarked stock photo (licensing), swap real company names (Amazon, Dell, Target) for invented ones, label it a design assessment not client work |
| Real metrics from the assessment (completions, leads) | Requested from the team. Would materially strengthen case study 1 |
| Typography and palette | Her decision |

---

## 11. What not to do

- Do not build a cinematic scroll that hides the case studies.
- Do not interleave art with product work.
- Do not carry over copy from the old site. It is stale, it describes her as an intern, and
  its Epifi bullets describe only video work.
- Do not claim React or Next.js expertise.
- Do not invent metrics. Several on the old site ("25% bounce rate reduction," "100%
  cross-device compatibility," "30% fewer pain points") are unsupported and are being removed.
- Do not name the Epifi product.
- Do not publish watermarked stock imagery anywhere.

---

## 12. Related files

- `Documents/Personal/career/experience-report.md` — full record of the Epifi engagement, with
  per-project detail useful for writing the case studies.
- Resume lives in Figma, file key `NlBw9VEMyRgbexRrmBBUVN`, two variants (generalist and
  narrow product design). Keep site copy consistent with it.
