---
name: project-quiz-app-dev
description: "AI-Native Index quiz app dev work in workloom-dev/core — merged PRs, local setup, and the merge-gate workflow"
metadata: 
  node_type: memory
  type: project
  originSessionId: 25acf17b-8c3a-4df0-9914-e9443d493d19
---

Sejal now does code changes on the AI-Native Index quiz (`client/workloom/quiz-app/` in `workloom-dev/core`, clone at `~/Documents/Work/Github/core`, Surya's feature). Merged to master (July 2026): PR #6611 (Figma color alignment: page #FAF6F0 / white containers / #F7F7F7 panels; tone-driven "what you told us" tiles — icon = identity, chip color = answer strength; dot-on-curve fix; tiered breadth gate so a perfect 100 needs 5/5 lifecycle coverage) and PR #6649 (LinkedIn share captions via synchronous clipboard copy + inline fallback, resume-on-refresh via localStorage, low-emphasis retake link). PR #6686 (2026-07-24) ported the second batch onto the v3 quiz (gtm backend, 19 questions, grid type): position chart (x = workflow-autonomy rung = Cherny ladder Gated→AI-native, y = score), REQUIRED name+email details gate (name = tagged NAME proto answer), mobile vertical stepper + responsive pass, em-dash sweep. Lesson learned: the quiz moves fast — always `git fetch` + branch fresh off origin/master before new work (an earlier batch was built on a 2-PR-stale base and had to be ported).

**Merge-gate workflow for her PRs on core:** master PRs need a linked issue (`Closes #N`), a green local `lci` run (stamps the commit), then toggling the `RunWorkflows` label to run the mandatory "Check PR Status" workflow. Codex bot review threads must each get a grounded reply before the gate passes.

**Her Mac is now a full backend dev machine** (installed 2026-07-23 for LCI): Go 1.25 (`/opt/homebrew/opt/go@1.25/bin` — repo pins the 1.25 minor!), golangci-lint, PostgreSQL 17 (brew service, `root` superuser), Redis (brew service), `lci` at `~/go/bin`. Her git committer email is still the auto-generated `sejal@Sejals-MacBook-Pro.local` — suggest fixing to sejal.borkar@epifi.com.

Quiz app gotcha: the browser-pane tab being hidden freezes rAF, which stalls framer-motion transitions and eats clicks — front the pane before UI verification. Dev server must run via Bash (not preview_start): the preview helper lacks macOS Documents-folder permission.

Related: [[project-quiz-wireframes]] (the earlier low-fi wireframe phase), [[feedback-object-identity]] (icon=identity, color=state — applied to the result tiles).
