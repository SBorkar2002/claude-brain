# Tools evaluated for video and motion work

Every video, animation, voice and AI tool Sejal tried or evaluated (Jun to Oct 2026), with the verdict and when to reach for it. Companion to `playbooks/video-production.md` and `lessons/video-traps.md`.

Standing constraint: **no paid tools or credits on personal work unless she opts in** (memory `feedback-no-paid-tools`). Several tools below were used on the company account; on a personal account, assume free tiers only and ask.

---

## Verdict table

| Tool | What it is | Verdict | Use it for | Do not use it for |
|---|---|---|---|---|
| **Remotion 4** | React video framework rendered in headless Chrome | **Primary tool. Adopted.** | Everything programmatic: UI panels, charts, counters, path draw-ons, grids, camera moves, VO-locked timing, data-driven layouts, final composition | Particle sims, fluid morphs, true plugin effects (render elsewhere, composite) |
| **ElevenLabs** | TTS voice-over | **Adopted** | All VO; whole script in one generation | Expecting identical pacing across separate generations |
| **Whisper** (`openai-whisper`, base) | Local speech-to-text with word timestamps | **Adopted** | Word timestamps, verifying cuts, transcribing the render | Measuring gaps or exact word ends (use RMS) |
| **ffmpeg** | Audio/video CLI | **Adopted** (utility) | Slicing VO, fades, `volumedetect`, wav for RMS | n/a |
| **Figma + Figma MCP** | Design tool, Claude read/write bridge | **Adopted** for storyboard frames | Keyframes Sejal reviews and edits | Animation |
| **Claude Design** (claude.ai/design) | Prompt-to-HTML/GSAP designs and animations | **Deck-style only** | Static screen kits, simple deck-like animated clips, quick frame drafts | Product animation, complex SVG (branch trees), anything needing precise timing |
| **HyperFrames** (HeyGen's HTML video framework, `npx hyperframes`) | HTML + GSAP compositions rendered to MP4 | **Tested Jun 2026, output poor, dropped** from the pipeline. Its skills are now installed in Claude Code | Possibly quick HTML motion graphics if revisited | The launch/product pipeline (Remotion won) |
| **hyperframe.ai** (a separate website, not HeyGen) | Prompt-only browser video generator | **Tried once, unsuitable** | n/a | It takes no image references; it returned a wrong dark-background version of a light-theme scene |
| **Higgsfield** | AI image/video generation (many models) via CLI/MCP | **Used once, worked** for an organic branching-tree growth clip from start/end SVG frames, exported MP4 and composited | One-off organic/generative motion that code and Claude Design cannot do | UI, text, product screens. Paid credits: only if Sejal opts in |
| **Figma Make** | Prompt-to-app/screens inside Figma | **Usable for screens**, not animation; used for some launch-video screens | Dashboard-heavy static screens (code-backed charts render cleanly) | Motion; works best with a real design system (connecting a component library needs an Org/Enterprise plan) |
| **Canva** (via connector) | Template design tool | **Rejected for this work** ("this looks very basic") | Social posts, quick docs | Storyboard frames or motion for explainers |
| **Manus** | Agentic orchestration over other LLMs | **Not adopted.** Manager's early test "not strong"; deep research found no native SVG/vector animation and unreliable multi-step runs | n/a | Vector animation |
| **Veo 3 / Flow / Nano Banana** | Google generative video/image | Used by Sejal for other AI-video and employer-brand style work (per her profile), **not for product explainers** | Generative footage, mascots, stylised shots | UI motion graphics |
| **Sora / Runway / Kling** (Seedance etc. only seen in Higgsfield's model list) | Generative video | **Not used; ruled out** for product videos | Cinematic generative footage | Crisp UI text, exact product screens, precise cursor clicks (they hallucinate interfaces) |
| **After Effects** | Pro motion tool | **The quality bar, not a tool she used** | Reference standard; a hero flourish could come from an AE artist as Lottie | n/a |
| **Kokoro** (local TTS), **HeyGen** TTS/avatars, **Postiz** | Parts of the HyperFrames stack | **Dropped** (ElevenLabs is better; avatar and posting not wanted) | n/a | n/a |
| **Perplexity** | Research | Suggested by her manager for competitor research; Claude web research used instead | Competitor/content research | n/a |
| **heyruby** | Unknown | **Unclear from history.** No mention found in any transcript or memory note | n/a | n/a |

---

## Details per tool

### Remotion (primary)
- **Why it won:** deterministic per-frame rendering, so timing is a pure function of word timestamps; a new VO read means re-deriving numbers, not re-keying 60 keyframes. Data-driven panels are a `.map()`. Shared-element transitions across scene cuts are one shared transform constant. Claude can author and iterate it fast against stills.
- **Ceiling:** ~90 to 95% of an After Effects ad. Assessed against a Gmail/Gemini product ad Sejal shared: every move (icon scale-ups, full-screen shape wipes, drifts, overshoot, cursor clicks, typewriter, skeleton-to-content) is reproducible.
- **Gaps:** motion blur (AE gives it free; `@remotion/motion-blur` approximates it and multiplies render time); plugin effects (Deep Glow, Optical Flares, Particular, Element 3D); particles; mesh warp, roto, tracking; tactile graph-editor tuning (the loop is edit -> still -> read).
- **Upgrades considered, not adopted:** `@remotion/motion-blur`, `@remotion/three` (real 3D), `@remotion/lottie` (play AE-made Lottie), `gl-transitions` (WebGL transitions), CSS clip-path masked wipes (zero cost, recommended first), CSS blur "whip" on fast moves.
- **Render cost:** ~4 to 5 min for ~4300 frames at 1080p30, ~22 MB. Heavy filters/WebGL multiply that.
- **History:** she dropped Remotion once early on; the reason is unclear from history (Claude guessed React/TypeScript setup friction). Her manager asked her to re-evaluate it in late Jun 2026 and it became the main tool once there were clear programmatic scenes.
- **When:** any product, launch or explainer video with UI, charts and VO. Also the right home for "vector-ish" engineering visuals (contribution graphs, git trees, counters, feeds).

### ElevenLabs
- Generate the full script in one go for consistent flow. Re-record single lines only when copy changes; splice at scene cuts.
- Voices used: "Monika Sogam - Deep and Natural" (launch), "Mark - Natural Conversations" (DORA). Downloads are named with settings tokens (e.g. `sp95_s46_sb68_v3`, apparently speed/stability/similarity and model version; inferred).
- It chooses its own delivery rate per generation: same tempo multiplier, different syllables/s. Takes from separate sessions drift in timbre.
- Spell pronunciations in the text ("tetriz dot A-I", "awth", "P R").
- It was briefly down once ("elevenlabs isn't functioning right now"): plan VO work so visuals can proceed with the previous read.
- MCP availability for ElevenLabs was never checked (open item from Jun 2026).

### Whisper
- `whisper.load_model("base")`, `word_timestamps=True`, `language="en"`, `initial_prompt` with product nouns. Python package; no CLI binary on PATH.
- Ends undershoot, starts are late, segment-initial words are back-dated. Pair with a 20ms RMS silence map. To decide a cut, transcribe the candidate clips.
- HyperFrames also ships a `transcribe` command; not needed with the Remotion pipeline.

### Figma and the Figma MCP
- Storyboard home. Frames 1920x1080 in a titled Section per version; sub-frames per beat.
- claude.ai Figma connector = the only WRITE path (`use_figma`, load the `figma-use` skill first). If it dies with `net::ERR_FAILED`, start a new session.
- Desktop Dev Mode MCP at `http://127.0.0.1:3845/mcp`: read-only (metadata, screenshot, design context, variables, motion context), needs the file frontmost and one frame selected.
- Seat matters: a view-only seat blocks metadata/design-context even when screenshots work.
- "Figma Motion" (keyframes, MP4/GIF/WebM export, agent-generated keyframes from text) surfaced in research in Oct 2026; claims partly verified, never tried in production.

### Claude Design (claude.ai/design)
- Good at deck-style animation and static screen kits; consistently weak at product animation over 2 to 3 months (her and her manager's conclusion, Jun 2026).
- Produced the DORA intro clip (1280x720 GSAP HTML with a player bar), later distilled into the `educational-video-intro` skill (`~/Documents/Personal/skills/educational-video-intro.SKILL.md`): stage letterboxed on `#0e0e13`, Geist/Geist Mono, `back.out(1.4 to 1.5)` pops, `power2.inOut` camera at scale 1.85, 2x2 metric cards staggered 0.35s, wash before title, 2s final hold.
- Gotchas: no CSS initial opacity causes a flash; a localStorage resume made the video start mid-way; it cannot read local files; skill files do not work inside it (give it a merged prompt).
- Import into Claude Code via the claude_design MCP (`/design-login`) needs a claude.ai login with design scopes; it failed with an OAuth token in a Cowork-style session.
- Only on web, not in the desktop app (as of Jun 2026).

### HyperFrames (HeyGen) and hyperframe.ai
- Two different things. HyperFrames: `npx hyperframes init / preview / render / lint / inspect`, HTML + one paused GSAP timeline registered on `window.__timelines`. hyperframe.ai: a browser product that takes prompts only.
- HyperFrames first output for the DORA hook was broken (framework clip timing fighting GSAP); after a rewrite it rendered clean but the team judged quality poor. Dropped in Jun 2026 meeting notes ("Hyperframe tested but output quality was poor").
- Revisit only for short HTML motion graphics; its installed skills (faceless-explainer, product-launch-video, motion-graphics, embedded-captions) target generic workflows, not Sejal's system.

### Higgsfield
- CLI `@higgsfield/cli` (global npm install needs a user-level npm prefix), browser login (no API key), skills via `npx skills add higgsfield-ai/skills` (installer flagged them as high/critical risk: read before use).
- Proven use: branching-tree growth animation given start and end SVG frames, exported MP4, composited back. Her manager's notes: "Animated separately in Higgsfield, exported as MP4, re-imported into Claude Design. Worked successfully."
- Paid credits. Default to coding the animation instead.

### Figma Make
- Accepts text + image uploads in one prompt (not documents). Restate the design system as explicit tokens (hex, fonts, radii, spacing) next to the reference images; be content-specific (exact metric, chart type, numbers); one scene per prompt in the same thread; refine with point-and-edit rather than re-prompting.
- Used for launch-video screens that were then ported into Remotion scenes.

### Canva
- Generated four 16:9 storyboard variants per scene via the connector; Sejal: "this looks very basic". Its AI is built for social posts, not motion or timing. A manager-suggested stack (generative base video + Canva for captions/transitions + ElevenLabs) was superseded by Remotion.

### Generative video (Veo, Sora, Runway, Kling)
- Wrong tool for product/UI explainers: cannot render correct UI text, exact product screens, or precise clicks. Fine for cinematic or character footage in other projects.

### Earlier/side assets
- `tetriz-remotion-src` (an early 5-scene Remotion project in Downloads, `TransitionSeries`, shared `tokens.ts`) and a "Constellation Animation Sequence" Remotion port (deterministic seeded starfield, used as the launch outro). Where the constellation was originally authored is unclear from history.
- Script docs: a docx-js generator (`format-launch-script.js`) reproduced the team's Google Doc script styling; Google Docs had no connector.

---

## Decision guide

```
Is it UI, a chart, a number, a list, a line, or anything that must hit a VO word?
  -> Remotion.
Is it organic/generative (growth, liquid, character, footage) and Remotion can't fake it?
  -> Ask Sejal about credits; Higgsfield (proven once) or a generative video model; composite in Remotion.
Is it a static screen for review?
  -> Figma (by hand or via MCP); Figma Make for dashboard-heavy screens.
Voice?
  -> ElevenLabs full read -> Whisper + RMS -> playback windows.
Deck-like quick animation for a slide?
  -> Claude Design is acceptable.
```
