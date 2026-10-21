---
name: feedback-artifact-stays-lean
description: "The comic series artifact is a script review surface — keep it lean; production history and metrics belong in the repo, not on the page"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c94d5c4d-feea-4244-a796-6ec866e0d0e6
  modified: 2026-09-07T10:56:47.577Z
---

The series artifact (*I Have No Idea What That Means*) is a **review surface for
the scripts**. Keep it short. Sejal has cut it back twice now — once telling me
it "seems too long", and again deleting three production-note blocks I added
about what changed in the film, the six explainer passes, and the open items.

**Why:** people open it to read panels and comment on them. Process history,
version narratives and measurements are for whoever is building, and they push
the scripts down the page. A review surface that has to be scrolled past to
reach the thing being reviewed stops getting used.

**How to apply:** panels, plus at most one short block per script — and only when
it tells a reviewer something they need in order to review (e.g. "panel 8 is
being replaced, here is the new line"). Production history goes in the repo:
`comics/scripts/*.md`, `HANDOFF.md`, or the skill files. Measurements and
per-pass reasoning go in code comments next to the thing they explain.

If she asks for a handoff summary, write it **into the reply as text** — she
pastes it elsewhere — rather than adding it to the artifact or creating a file.

Related: [[project-comic-pipeline]] (artifact = review surface, repo = frozen
record, Drive = archive).
