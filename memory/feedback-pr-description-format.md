---
name: feedback-pr-description-format
description: "How Sejal wants PR descriptions written — before/after/why tables when editing an existing branch, what/why when starting a new one"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 25acf17b-8c3a-4df0-9914-e9443d493d19
  modified: 2026-07-27T05:34:56.947Z
---

How PR descriptions should be structured, so a reader understands the change fast. Two modes, chosen by whether the branch is new or already in flight:

**Editing an EXISTING branch/PR (iterating on already-shipped or in-review work):** use the **Before → After → Why** table format. One-line **Summary** at top, a running **why** sentence stating the overall intent, then a per-area table for each screen/section with columns `| | Before | After | Why |` so every change is diffable at a glance. Close with a **Verification** line (what checks/flows were run). Model example: [PR #6800](https://github.com/workloom-dev/core/pull/6800) (Anandhi) — quiz copy/UI polish laid out as per-screen before/after/why tables.

**Starting a NEW branch:** lead with **what** the change is and **why** it was made — no before/after (there's no "before" to compare against). The existing `/pr` + `/pr-communication` evidence-bound style still applies.

**Why:** before/after tables make review fast for a non-engineer reader (Sejal is a product-design intern) and for reviewers scanning a large copy/UI diff; the what/why framing fits net-new work where a comparison table would be empty.

**How to apply:** detect the mode from the branch — new branch off master → what/why; adding commits to an existing PR branch → before/after/why tables. Still link the issue and keep the verification section. Relates to [[project-quiz-app-dev]] and the team's `/pr-communication` conventions.
