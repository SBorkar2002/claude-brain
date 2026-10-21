---
name: feedback-pr-creation
description: Claude may create PRs without asking (never merge to master/main); every PR needs a company-standard title + full description
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4988f54d-18c3-4096-b6dd-7c1c487b9ec8
  modified: 2026-08-07T12:03:17.751Z
---

Sejal has given standing authorization: **Claude may create pull requests without asking each time.** Claude must **NEVER merge** a PR to master/main — creating/raising the PR is allowed, merging is the human's call.

Every PR must have:
- A **valid, company-standard title** (Conventional Commits, e.g. `feat(site): …`).
- A **description that covers everything**: a summary, all changes (grouped by area), the files touched, and any important notes / verification / open items.
- **If a PR description format is provided** — the repo's `.github/pull_request_template.md`, the `/pr` or `/pr-communication` skill, or a format Sejal gave — **follow it exactly.**

Do not ask permission to create a PR again, and don't hand back "want me to open the PR?" — just create it and return the link. See [[feedback-pr-description-format]] if present.
