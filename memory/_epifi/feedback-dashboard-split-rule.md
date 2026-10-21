---
name: feedback-dashboard-split-rule
description: "Mobile scrollytelling dashboards — split a lens into per-panel dashboards ONLY if its full hero overflows the mobile stage; measure, never split by default"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b052b1fd-19d5-4a58-84a2-2ffb394d9a9e
  modified: 2026-09-07T05:47:26.518Z
---

Sejal's standing rule (2026-09-04, tetriz.ai feature-page mobile scrollytelling, emphasized "REMEMBER THIS"): when deciding whether a lens's dashboard splits into one-panel-per-step on mobile, **measure the full hero at the mobile card size first**. Tiny panels that fit → keep all panels in ONE dashboard, no `panels` prop. Panels too big to fit the stage → splitting into separate dashboards is justified.

**Why:** Splitting everything by default makes short lenses feel needlessly stretched; cramming everything makes big lenses unreadable. The fit test (hero card height vs stage height at the mobile card width) is the objective tiebreaker.

**How to apply:** In [[project-ai-adoption-page]] repo (Documents/Github/core, site), `FeatureScroller` items take optional `dashTitle` + `panels`. Rule is documented in the `ScrollerItem` type docs in feature-scroller.tsx. Rollout DONE 2026-09-07 across all 7 scroller pages (21 lenses measured against the 368px stage at the 243px card): split = ai-adoption ×3, ai-impact ×3, ai-roi NetGain, harness-control-plane Fleet+Publish, session-security PII. Kept whole (they fit) = ai-drivers ×3, engineering-productivity ×3, roi Recoverable+Returns, harness Deny, sec Secrets+Commands. For any new lens, re-run the measurement (render hero with `panels` commented out, compare card height to stage height).

Related: [[feedback-panel-screen-time]], [[feedback-no-overlap]]
