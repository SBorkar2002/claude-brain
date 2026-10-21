---
name: feedback-working-style
description: "How Sejal likes to work — collaboration style, what to avoid"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6405306a-a575-45b8-9ae6-d55c598295ee
---

- Builds iteratively — test one piece, validate, then move to next.
  Don't generate the full pipeline at once. Break into reviewable steps.
- Skill files should be global/reusable, not video-specific.
  If a rule only applies to one scene, it doesn't belong in a skill file.
- Pipeline has a required design review step between Figma brief and animation prompt.
  Never skip straight to animation. Always Figma first.
- Distinguishes clearly between SEO videos (educational, thumb-stopping, no brand)
  and launch videos (brand-first, product-led). Don't mix the rules.
- On-screen visual suggestions in raw scripts = mostly ignore.
  Generic AI-prompted visuals should be discarded. Only flag if it's a real
  engineering environment or shows tension the VO can't convey alone.
- When she shares meeting notes, extract what's actionable for skill files
  and memory. Don't just summarize — act on the gaps.
- Design stays human-driven. Automation handles repetitive steps, not creative ones.
- Treats developer and product team feedback as user research, not literal direction.
- Keep Mohit in the loop on product thinking via group message, not presentations.
- **Don't write message drafts (Slack/email text meant to be copy-pasted) to a file — just type them
  directly in the chat response.** Reason: she called this out directly after I filed a Mohit
  follow-up message as a scratch .md instead of just outputting the text. Files are for durable
  artifacts (scripts, spines, docs); a message that exists only to be copied into Slack isn't one.

- **When a new meta rule is established, update BOTH memory AND the skill md file
  (`~/Documents/tetriz-content/skills/launch-scene-prompt-generator.md` for launch videos,
  `scene-prompt-generator.md` for SEO) in the same turn.** Sejal checks that the skill files
  stay current — memory alone isn't enough, because the skills are what Divya/Anandhi reuse.

**Why:** Sejal is building a system that others (Divya, Anandhi) will also use.
Rules need to be portable and self-explanatory, not dependent on this conversation.

**Remote Control + keep awake (STANDING, 18 Oct 2026):** every portfolio chat (main/Figma, cat-studio, portfolio-code, and any new one) must have Remote Control ON and keep the Mac awake. App setting "Connect new sessions to Remote Control" is ON and "Keep computer awake while Claude works" is ON (incl. battery). For any session started via start_session, also call set_remote_control on its id right after it starts.
