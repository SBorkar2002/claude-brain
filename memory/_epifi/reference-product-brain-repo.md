---
name: reference-product-brain-repo
description: "Where to find Tetriz product ground truth (PRDs, sales docs, GTM) — the product-brain repo — and how to actually get repo access in a session"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3c2f4407-ffe6-4c1a-b5e0-59845720b9dc
---

- **Repo:** `workloom-dev/product-brain` on GitHub (private org). Cloned locally at
  `/Users/sejal/Documents/product-brain` as of 2026-07-03 — re-clone/pull if it's missing or stale
  in a future session, don't assume it's still there or current.
- **Key folders:** `docs/prd/` (feature PRDs, each has a Status line — Draft vs. shipped matters,
  don't assume a described feature is live), `docs/sales/` (vetted, board-tested sales copy —
  check here before writing new marketing language, it may already exist and be stronger),
  `docs/gtm/`, `docs/decks/`, `context-library/agent-feature-map.md` (canonical list of real
  feature names — "a claim that doesn't trace to a feature listed here is either undersold or
  overclaimed").
- **`docs/sales/tetriz-product-walkthrough.md`** is likely the exact "product walkthrough doc"
  Mohit references when asking for adversarial review against product truth.
- **Harness Intelligence / Transform pillar ground truth:** `docs/prd/ai-harness-meta-prd.md`,
  `docs/prd/org-prompt-intelligence-engine-prd.md`. Confirmed mechanism: recommend + human-install,
  NOT auto-fix/auto-push — that's an explicit PRD non-goal.
- **"Weekly AI Coaching" ground truth:** two separate real features, don't conflate —
  `docs/prd/promptly-weekly-insights-v0-prd.md` (Personal Prompt Retro, confirmed shipped,
  explicitly IC-private/no-manager-visibility by design) vs. `docs/prd/org-prompt-intelligence-engine-prd.md`
  (org-wide redistribution, Draft status as of 2026-07-03).
- **STALE WARNING (verified 2026-08-20): `context-library/agent-feature-map.md` NO LONGER EXISTS.**
  The five-agent taxonomy (AI Leverage / WorkPulse / DevInsights / Skillmax / AI Govern) was
  **retired 2026-08-03** — see `context-library/product.md` ~line 131: it "never survived contact
  with a live demo — no buyer has ever asked which agent a feature belongs to." The canonical
  framing is now the **Observe · Improve · Govern** pillars on a **Trust** foundation, using the
  language from the smallcase / ACR / InMobi / Navi / Shadowfax demos. Read `CLAUDE.md` and
  `context-library/product.md` first instead. The paragraph below is kept for historical context.
- **Read `CLAUDE.md` and `context-library/agent-feature-map.md` FIRST, before any grep-based review.**
  Two adversarial-review passes missed things a first read of these would have caught immediately:
  `CLAUDE.md` has the company's actual problem statement and stated moat ("prompt-to-PR
  attribution... no competitor can replicate this dataset") in the opening section; `agent-feature-map.md`
  (v3) is the canonical, authoritative mapping of every real feature name to its pillar and agent
  (Observe: AI Leverage, WorkPulse. Transform: DevInsights, Skillmax. Govern: AI Govern) — it would
  have resolved a whole round of "is this a real feature name" confusion (Skillmax vs. invented
  names like "Harness Intelligence") in one read instead of several rounds of grep-and-guess.
- **Grep-based review misses data baked into images.** A stat ("your accept-rate drops 14%") was
  wrongly flagged as fabricated because it only exists inside a screenshot
  (`docs/sales/assets/alpaca/harness-skill-conflict.png`), not as plain text anywhere greppable.
  When verifying a claim against this repo, check for a matching image in `docs/sales/assets/` /
  `docs/sales/_build/` and actually view it (Read tool renders images) before calling something
  unconfirmed.
- **Repo access mechanics (environment quirk, worth remembering):** the `add_repo`/`list_repos`
  MCP tools 404'd repeatedly in this session type even with GitHub shown as "connected" in
  connector settings, and survived a full restart — that path never worked. What actually worked:
  the session already has `gh`/`git` CLI authenticated at the shell level (`gh auth status` showed
  a logged-in token with `repo` scope) — plain `git clone https://github.com/<owner>/<repo>.git`
  succeeded immediately. If repo access is needed again and the MCP add-repo tool fails, try
  `gh auth status` and a direct `git clone` via Bash before assuming access is blocked.

- **Marketplace ground truth (checked 2026-08-20, repo current to 08-18):** the Tetriz
  marketplace **does not exist yet** — `docs/prd/ai-harness-meta-prd.md` PRD spawn map lists
  *Harness Recommendations: Marketplace* as **Status: Future**, no PRD, explicitly gated on the
  Govern push path ("a push button with no push path behind it"). What's **next to ship (v1.4)**
  is the *Harness Control Plane*. *Harness Recommendations: **Custom*** (org-specific rules +
  CLAUDE.md templates derived from the org's own session data) is **Done**.
- **A public cross-org marketplace is an explicit NON-GOAL** —
  `docs/prd/agentic-platform-product-note.md`: "Not defining a public marketplace / template
  exchange across orgs." Customer-authored templates are org-internal only: "Not marketplace —
  just 'our org's agents.'" So **an individual cannot publish a skill for the world via Tetriz.**
- **Tetriz does NOT build skills — it derives, recommends, and pushes.** Its sales claim is
  org-*specificity*: `docs/sales/locus-leave-behind.md` — "Not a generic recommendations list.
  Specific to your codebase, your team's patterns, your most common failure modes." A generic
  skill therefore *contradicts* the pitch.
- **`docs/strategy/oss-buzz-strategy.md` (owner: Mohit, updated 2026-06-23) is the doc to read
  before any content/vocabulary strategy work.** Stated goal: ship free local-only OSS tools,
  launched **weekly**, "**to own the category's vocabulary**" — the same thesis as the phrasebook
  YouTube idea, already committed company strategy. Real tools: `disclose`, `skillsec`,
  skill-stats, `agentsmd`, hallucination gate, `agentic-pr-pipeline`. Distribution is genuinely
  public (npx / GitHub / **Anthropic plugin marketplace** "for credibility"), and it funnels to
  **single-player Tetriz** (own key, no org needed). Category claim: "AI-Native Engineering
  Intelligence." See [[project-youtube-employer-brand]].
