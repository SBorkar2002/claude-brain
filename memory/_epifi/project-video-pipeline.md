---
name: project-video-pipeline
description: "Current state of Tetriz SEO/launch video pipeline, tools, gaps, next steps"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6405306a-a575-45b8-9ae6-d55c598295ee
---

Last updated: 2026-08-12 (originally 2026-06-26; meeting attendees: Sejal, Divya, Mohit).

**Video code repo (2026-08-12): the v4.2 Remotion project now lives at
workloom-dev/tetriz-launch-video (private). PR #1 = frozen baseline of the
2026-08-10 team-share cut; the self-improving-loop rework (Sumit feedback)
builds on branches on top of it. Local: ~/Documents/Work/tetriz-launch-video-v4.2.**

**Skill files (as of 2026-07-22): all four video skills in product-brain are in
sync with the repo** — seo-scene-prompt-generator.md (RENAMED from scene-prompt-generator.md, 2026-08-10, PR #433) and seo-script-refiner.md were
already clean; launch-scene-prompt-generator.md merged via PR #299;
launch-script-refiner.md merged via PR #306. A shortlist of 8 proposed additions
to launch-scene-prompt-generator.md (icon-vector rule, no-em-dash captions,
illustrated portraits, panel rest rule, CTA keep-clear, stat screen-time,
camera-language section, pathLength draw-on correction) is logged in the
launch-video project's DECISIONS.md under "Skill-file state + pending additions
(2026-07-22)" — awaiting Sejal's go before editing the skill. Ask before
touching any skill file ([[feedback-anandhi-vo-cut-review]]).

**Why:** Tetriz is building a video content library — SEO educational videos
(purely educational, no branding, rank on search) and product launch videos
(brand-first, feature-led). Different pipelines, different tone rules.

**What's built:**
- `script-refiner.md` — skill for refining raw scripts to series standard. To be shared with Divya.
- `seo-scene-prompt-generator.md` — skill with Mode 1 (Figma brief) and Mode 2 (animation prompt) (renamed from scene-prompt-generator.md, Aug 2026)
- DORA metrics video: Hook + Context animated, Content frames in progress
- Established visual identity: light bg (#f5f5f5), teal (#00BCD4), near-black stats, white metric cards
- Tetriz Remotion project exists at `/Users/sejal/Downloads/tetriz-remotion-src/` — 
  built for launch video, 5 scenes, never run locally, no VO wired in

**Current toolchain:**
- Script: Claude Code + script-refiner skill
- Figma frames: Claude Design → manually edited → PNG export
- Complex SVG/vector animation: Higgsfield → export MP4 → reimport Claude Design
- VO: ElevenLabs (full script, one generation) → Whisper for word-level timestamps
- Final composition: Claude Design Animate

**Tool evaluations (as of this meeting):**
- Claude Design: good for deck-style animation. NOT suitable for product animation.
  Consistent limitation observed over 2-3 months.
- Hyperframe: tested, output quality poor. Not in pipeline.
- Remotion: to be re-evaluated and compared against Claude Design. 
  Existing project at tetriz-remotion-src. Best for programmatic/vector animation.
- Figma Make: flagged as option for direct animation in Figma. 
  Requires existing Figma design system — Epifi doesn't have one yet.
  Workaround: push Claude outputs to Figma first, then use Figma Make.
  Storybook-Figma integration may enable full design automation path.
- Manus: untried, flagged by Mohit as worth exploring for frames + product animation.
- Two-tool split is acceptable: one tool for frames, one for product animation.

**Known gaps:**
- Design remains the main non-automated step — AI produces generic deck-like output.
  Human creative input still required, especially for SEO videos.
- No single tool handles all dimensions: frames + product animation + voiceover.
- Figma export friction: HTML-to-design plugin has layer/bulk constraints.
- Dashboard screenshots need distillation before use (strip tables/clutter).
- Script refinement skill needs alignment with Divya on SEO vs product video differences.
- MCP server availability not yet checked for: ElevenLabs, Claude Design.
  Worth checking — could enable semi-automated human-in-the-loop pipeline.

**Workflow decisions:**
- Sejal to clone product brain repo and work within it.
  WIP skill files should live in the repo, not in isolation.
- Script refinement skill to be shared with Divya for review before freezing workflow.
- Align with Divya on skill requirements: SEO video vs product video use cases differ.
- Future automation path: design system in Figma + Figma Make + Claude MCP.

---

## Manager Meeting — 2026-06-29

### DORA Slide Feedback
- Numbers (33K, 15K) don't need front-and-center treatment — purpose is to convey research scale, not highlight stats as outcomes
- Search slide: same principle — good range shown, don't over-index on numbers
- Focus emphasis on DORA metrics themselves

### Color & Brand
- No gradients — not established in brand, not on website or production videos. Revisit only if brand expands.
- SEO videos: flat colors only; teal as primary anchor
- Refer to marketing site for color reference
- Key slides: teal primary, a few complementary colors if needed

### Video Priorities
- SEO videos near-complete — close them out this week
- Transform + Observe videos: Sumit flagged for client outreach during trial period
  - Divya needs to be looped in to start scripts — message her on existing thread with context on which two videos Sumit mentioned
  - Check with Mohit if he has additional points/context
- Goal: close at least one launch video with a feedback round this week (30–45 sec, similar to SEO)

### Production Efficiency
- Storyboard took 4 days on first SEO video — target 1 day going forward
  - Aim: 70% of a 30-sec video done in 2 days, one feedback round incorporated
- Use Claude to update flat colors in bulk (not frame-by-frame manually)
- Invest time today strengthening brand guidelines for AI generation
  - Goal: auto-apply brand style to story frames so launch video starts from a strong base
  - Tweaking = ~10% of effort, not rebuilding from zero each time

### Tools & Pipeline
- Manos tested with same Claude prompt — results not strong yet, may need more prompting; credits may be limited
- External pipeline suggestion: Manos + Perplexity/Canva for presentations (reportedly good results)
- Approach: find someone who solved a similar use case, test their pipeline, reject if it doesn't fit
- Flightbase videos shared Friday — use these + similar YouTube creators as ongoing references
- Video repo: review suggested pipeline structure; consider whether separate repo makes more sense than under main brand repo

### Next Steps (2026-06-29)
- Message Divya on thread about Transform + Observe scripts — give context on which two videos Sumit mentioned
- Check with Mohit on Transform + Observe context
- Update brand guidelines for AI-generated story frames (flat colors + brand style auto-apply)
- Review video repo pipeline structure — separate repo vs. under main brand repo?

---

## Next steps (from 2026-06-26 meeting):
- Clone product brain repo, move skill files into it
- Share script-refiner.md with Divya
- Align with Divya on SEO vs product video skill differences
- Evaluate Manus and Remotion for frame + product animation vs Claude Design
- Check MCP server availability for ElevenLabs and Claude Design
- Explore Figma Make + Storybook-Figma integration for design automation

**Repo + folder structure (from manager meeting 2026-06-26):**
- Clone product brain repo and work on top of it — don't start from scratch
- Use Claude plan mode to decide what to add/subtract for video use case
  Prompt: "I want to clone the product repo. This is my pipeline. Help me do it best for video."
  Let Claude ask clarifying questions rather than trying to answer everything upfront.
- PRD folder: not a priority for video work
- Key folders to focus on: storyboard and related content folders
- Scratch pad needed for WIP with retrieval ("dustbin" — saves accessible even after edits)
- Two-state folder structure:
  - WIP folder: active work in progress
  - Final folder: on push, auto-triggers copy/upload (e.g. private YouTube)
- Treat Claude as decision-support, not decision-maker — Claude draws out what you already know

**Automation scope (agreed):**
- Automatable: script refinement, scene generation, voiceover
- Not yet automated: design/frames (requires human creative input)
- Potential path to automating design: Figma design system + Figma Make + Claude MCP

---

## Transform video — status as of 2026-07-03

- Script went through v3 → v4 → v5 in one session: v4 tightened wording/runtime;
  v5 incorporated Sumit's (CEO) direct comments — dropped "Tetriz Transform" as a
  customer-facing name, centered "AI-native, faster" as the throughline, reframed
  Weekly AI Coaching from "extract from best engineers" to "teach everyone," and
  flagged the Scene 6 metrics-claim as unresolved pending a Mohit conversation.
- Files: `tetriz-content/scripts/tetriz-transform-script-v5.md` (source),
  `tetriz-transform-script-v5.docx` (formatted, generated via
  `tetriz-content/scripts/formatting/format-launch-script.js` — a reusable docx-js
  generator built to replicate the old teaser v4's manual Google Doc styling).
- Anandhi's manager review (call, 2026-07-03) redirected priority: the script still
  reads "surface level," features (Harness Intelligence, Weekly AI Coaching) don't
  land with depth. Her ask is a **spine first** — see [[feedback-spine-before-script]] —
  not more prose polish. Wrote `tetriz-content/scripts/tetriz-transform-spine.md`:
  bones-only beat structure naming the exact app.tetriz.ai screen that should carry
  each feature's depth (Harness Recommendations screen; Weekly Prompt Retro report).
- Confirmed directly by Anandhi: the teaser v4 doc's polish was NOT a formatting tool —
  it came from many manual feedback rounds (Divya did hands-on generation on that one).
- **Next steps (her plan, stated on the call):** show Mohit the script/spine today for
  feedback on whether Harness Recommendations / Prompt Retro are the right screens to
  represent the two features, and on the unresolved Scene 6 "AI-native" claim. Close
  the script today. Start thinking storyboard/transitions in parallel so video
  production can start ASAP — don't wait for 100% script lock to begin storyboarding.
- Mohit asked (Slack, 2026-07-03) for an adversarial review via "claude in product brain,"
  prioritizing product depth/correctness and GTM/sales focus, guessing it'd fix ~60% of issues.
  `add_repo`/`list_repos` MCP tools 404'd repeatedly (session-level issue, survived a restart) —
  worked around by cloning the repo directly with `git clone` (gh CLI was already authenticated
  at the shell level). See [[reference-product-brain-repo]] for repo details and this workaround.
- **Two rounds of adversarial review done (2026-07-03):** first without repo access (caught a
  real self-contradiction in Scene 4 — VO claimed auto-fix/auto-push, visual showed a manual
  Install button). Second, grounded in the real product-brain PRDs, confirmed that read and found
  a second, more serious one in Scene 5 — VO and visual mapped to two different real features
  (Org Prompt Intelligence Engine, org-wide, Draft status vs. Personal Prompt Retro, shipped but
  explicitly IC-private by design). Also found the "14% accept-rate drop" stat was fully
  fabricated, and that better, board-tested sales copy for Scene 5's exact claim already exists
  in `docs/sales/meesho-leave-behind-v2.md`.
- **Script is now v6** at `tetriz-content/scripts/tetriz-transform-script-v6.md` — Scene 4
  corrected to match the confirmed real mechanism; Scene 5 marked pending a product decision
  (Option A: Personal Prompt Retro / individual framing, vs. Option B: Org Prompt Intelligence
  Engine / org-wide framing, pending ship-status sign-off). Spine updated to match.
  `tetriz-transform-script-v5.docx` (formatted) is now stale — regenerate from v6 once Scene 5
  is resolved, don't send v5.docx to anyone as current.
