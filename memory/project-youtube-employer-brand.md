---
name: project-youtube-employer-brand
description: "Tetriz/Epifi YouTube channel direction — employer-branding style, zero product, multi-bucket, practitioner audience (Anandhi call, 18 Aug 2026)"
metadata:
  node_type: memory
  type: project
---

**Decided direction (Anandhi call, 18 Aug 2026):** build a YouTube presence that is
**employer-branding style with NO product content at all** — terms, problem statements,
struggles, solutions, how to overcome them. Fun, engaging, spreadable. Must run
**multiple buckets** (fun / educational / influencer-led / pure-visual), and the buckets
must **connect to each other** — format and approach can vary per bucket, but the videos
cannot be unrelated one-offs.

**This supersedes the earlier pipeline-first memo** (founder-hosted interview show +
buyer-facing proof library, see [[project-video-pipeline]]). Different objective:
practitioner reach and employer brand, not CTO pipeline. Both can coexist but the
YouTube channel itself is now the no-product one.

**Anandhi's method rules (the important part):**
- Don't research by asking "which brand does exactly this" — nobody does. Survey the
  whole landscape, extract *larger themes*, then form a POV from the problem being solved.
- Look at adjacent spaces, not just direct competitors. Her fintech analogy: Groww
  (multiple regional IG accounts, own people as faces, daily posting, very personal),
  Jupiter, Scapia (famous-influencer promo ads). Then social leaders: Swiggy/Zomato,
  Ramp, Robinhood, Morning Brew, Daily Objects, Duolingo/Wendy's, museum accounts (MoMA).
- Swiggy's pop-culture/topical play works because they're 10 yrs in with total awareness —
  Tetriz does NOT have that advantage, so don't copy it directly.
- **Every decision needs a stated "why."** The strategy IS the reasoning chain; the
  content list falls out of it. First version does not need to be an approved all-in-one doc.
- YouTube ≠ Instagram: intent-driven, people arrive to learn/participate; longer videos viable.
- Don't post from the brand handle — use a human + YouTube's **collaborator feature**
  (two accounts co-post). "How do you not behave like a brand despite being a brand."

**Her audience insight (the sharpest thing in the call):** target the engineer who is NOT
an AI power user and feels the ground moving — 9-to-5 engineer watching feeds full of
"I built 5 agents this weekend," quietly scared of being left behind. Content ladder
should start at "how do you build your first skill / first agent / dumbest way to approach
a big concept," NOT at loop engineering.

**Format cues she gave:** the Indian-engineer-explainer trope (straight to the point,
whiteboard, no story arc) as a deliberate play; hand-drawn approachable diagrams, "not AI
sloppy" (referenced a maths channel with a "grimy screen" — exact channel not yet identified);
provocative titling ("4 mistakes you're already making" > "10 things you should know");
keep on-camera mistakes/retries in; always a GitHub link, possibly a dedicated GitHub handle;
build playlists deliberately.

**Prashasti's role:** not blocking. Best use is a **Monday-morning topical digest** — trending
AI/eng news filtered to ~5 postable options for the week, so topical reaction content is
possible alongside the planned calendar. She may already run something similar for GTM email.

**Open (asked of Sejal, 18 Aug):** is the left-behind engineer the locked audience; real face
vs synthetic persona (she has built an AI influencer before at a previous org); does employer
branding mean Epifi/Fi visible or fully unbranded; which "grimy screen" maths channel;
is 30 videos/month real.

**Separate open item from the same call:** ElevenLabs VO accent bug — a single regenerated
line comes back Indian→Russian (Whisper/11L confusion), and partial regeneration forces a
full re-gen at ~1k credits. Sejal's call: not worth it, ship the current cut, fix at the
script stage in upcoming videos. She planned to confirm this with Sumit rather than spend
the credits. See [[feedback-vo-cut-tails]].

---

## SPINE DECIDED — 19 Aug 2026 (after 2nd Anandhi review)

**Anandhi's 19 Aug feedback:** the five formats were fine but had **no spine**, so the room
couldn't judge them. She wants the "music for everyone" equivalent — a central theme that
ideas are *derived from*, never retrofitted into. Explicit asks: survive the "why not just
film a real professor?" test; argue shorts-vs-long from research not hunch ("short attention
spans" and "it works on Instagram" both rejected); extend off-YouTube (newsletter, LinkedIn,
future coaching launch video); bring reference videos so a non-social-savvy room can see the
end product; present option A *and* B. Deadline was v1 for review 20 Aug morning.

**The spine we landed on: THE PHRASEBOOK.** Not a tagline — an *artifact*. The channel is the
visible surface of a plain-English reference being written in public for the words engineers
are hearing now (skill, MCP server, agent, context, eval, compaction). **Every video is one
entry read out loud. The book is the product; YouTube is the shop window.**
- Framing: phrasebook, NOT textbook. You carry one when you've landed somewhere and don't
  speak the language yet. Nobody's ashamed to look something up — the shame is asking a
  *person*. A reference removes the person, and the hierarchy with them. Everyone is a
  tourist in this, staff engineer and new grad alike → no audience narrowing needed.
- **The filter (the whole point):** *does it produce or clarify an entry?* Settles arguments
  objectively instead of on taste.
- **Professor-test answer:** a teacher teaches a syllabus that already exists; this one
  doesn't. Rules out the *lecture*, not a human presenter.
- **Shorts vs long, derived not guessed:** a short is ONE entry, a long is a CLUSTER of
  entries. So a short is never a cut-down of a long. Playlists = chapters in dependency order.
- **Rejected along the way:** "AI for people with actual jobs" (excludes students/laid-off
  engineers — the most anxious, most motivated segment; Sejal caught this) and its rephrase
  "AI for people who use it, not people who post about it". Sejal rejected tagline-shaped
  answers twice — she wanted a *shape*, not a line. Lesson: central theme ≠ tagline; it can
  be an artifact, a territory, or a behavior.

**Formats now FOUR (character removed 19 Aug):** Two Voices + The Ladder ship first,
Question Compilation next, Wrong Answer First held (supply ~30 myths, finite).
**Character/presenter deferred entirely** — Sejal's call: nail the spine first. It never
derived from the spine, so it can be layered on later without changing anything.
NEVER fabricate Reddit/Quora screenshots for Question Compilation — anonymise real ones or
source via own form.

**Visual system — the page IS the visual (don't depict a book):** design the real page first,
then the video is that page animated; one design system, two outputs. No skeuomorphic books,
page-turns, or paper texture. Three scales: entry typography (micro) → entry number/URL
(meso) → **sidebar index (macro, the signature shot)**. The sidebar grows visibly across
videos, so compounding is something the audience watches happen.
**Sidebar is a LANDING, never an intro** — branded intros kill retention. It arrives at each
format's turn (Two Voices: on search-submit; Ladder: rung 1→2; Myth: when the myth breaks;
Questions: after the last card). Same asset, different timing = variety without monotony.
Wide index shot is the OUTRO/CTA. Six page components (sidebar, header, body, footnotes,
search bar, diff state) replace the earlier 7-template library.

**Commercial bridge — one rule:** *the book never mentions the product; the product may cite
the book.* Bridges in order: authorship byline (day 1) → newsletter/sales use (anytime) →
entries only Tetriz can write from aggregate session data (month 3+) → the org-level question
the book can't answer for one person (month 6+). Precedent: DORA — a free report that
organised a whole product category. **What breaks it: bending the word list to match the
roadmap.** Also aligns with Sumit's rule against framing coaching as extracting from top
performers (a reference serves the whole distribution).

**Deliverables:** v1 doc artifact (10 sections) + an earlier format-ranking slate artifact
that is now partly superseded (it still lists the character as a "layer").

**Still open:** shorts-to-long ratio (needs survey of 5-8 adjacent channels + what YouTube is
currently pushing); reference videos per format — **Two Voices most urgent, Anandhi said
outright she doesn't picture it from a description**; who writes rung 3 of The Ladder (needs a
named staff engineer as standing input); whether the book sits on a Tetriz or neutral domain;
the book's name (must not sound like Tetriz).

---

## CORRECTION — 20 Aug 2026: phrasebook DEMOTED from spine to component

Anandhi reviewed the phrasebook v1 and **rejected it as the spine** (kept it as a device).
Her verdict: *"a credit scene does not make the movie"* — the phrasebook is brand recall that
ends in the first 10 seconds of a video, not a strategy.

**The subtractive test — keep this tool.** She applied it: *take the phrasebook out; does
anything change?* No — same shorts, same ladder, same episodic drops. A real lens changes what
you make; a device doesn't. (Remove "music for everyone" and the vernacular billboards stop
making sense.) Use this to kill weak ideas fast.

**Her ASMR probe found a real hole:** she kept asking "why can't I do AI ASMR?" not because
she wants it but to test whether the framework can *reject* it. "Does it produce an entry?"
can't — Sejal correctly said "I'd still be introducing terms." **A working filter must be
about who's speaking and why, not about output format.**

**She reframed the ask from "singular idea" to "singular LENS,"** and a lens must answer four
things the phrasebook didn't: (1) who is speaking — she asked 3× whether there's a face, and
removing the character dodged rather than answered it; (2) their attitude — authority vs peer
vs learner; (3) why come back tomorrow — a glossary has no cliffhanger, and she supplied the
fix herself: **a challenge** (100 days, "build a product using only skills"); (4) how it stays
topical — she said twice that everything must tie to what's happening in AI *right now*, which
makes the phrasebook's evergreen nature a weakness not a strength.

**Casper shape:** a lens = name + descriptor that pre-decides behaviour ("Casper the friendly
ghost" — you already know what the episodes are). Also the "jingle test." She floated "your
everyday AI coach" and showed how it instantly generates cadence and content.

**Three lenses now on the table (artifact built 20 Aug):**
- **The Authority** — "the place engineers check before they believe the hype." Best
  topicality, worst feasibility (no authority yet, needs senior eng time daily, crowded).
- **The Learner** — an engineer learning in public including failures. Best differentiation,
  episodic pull, topicality, employer-brand fit; phrasebook becomes native (the notebook being
  filled). Risks: needs a sustained real person, severe bus factor.
- **The Everyday Coach** — "one thing a day." Cheapest, best product tie, most generic; weakest
  topicality.

**Recommendation given: THE LEARNER, BUT SENIOR.** The learner needn't be junior — a senior
engineer learning something genuinely new is the most relatable position available. Line:
*"I've shipped for twelve years and I still didn't know what an MCP server was."* Stronger
employer-brand signal than claiming expertise, and it aligns with Sumit's rule about not
extracting from top performers. **Do not blend lenses** — a lens works because it forbids.

**Sejal's own research win (keep):** on educational channels, shorts frequently out-perform the
long videos they point to; shorts sometimes feed the long. Anandhi accepted the
"shorts are not cut-downs of longs" position as "a pitch we can make."

**Now owed:** who the person is (if Learner); brand channel vs separate channel (still a hunch);
the 10-AI-education-creator research pass; operating boundaries (max shorts length, frequency,
where the brand may appear — her model: shorts are the entryway, brand only in long form);
the name + descriptor in Casper shape.

---

## Channel identity + real performance numbers (confirmed by Sejal, 26 Sep 2026)

The employer-brand videos ship under **AI FOMO Lab**; the series is *I Have No
Idea What That Means* (see [[project-comic-pipeline]], [[project-ep003-remote-control]]).
**These are Epifi/Workloom work, NOT AppsForBharat** — I inferred AppsForBharat
from "intern video = employer brand" and was wrong. AppsForBharat's video work
was separate employer-branding campaigns (Veo/Flow/Nanobanana, mascots).

**Reach as of Sep 2026:** 4 videos produced. One ("the intern video") has
**30,000+ views on Instagram**; the other three sit at 200–1,500 each.
YouTube 500+. TikTok has no usable data (VPN-suppressed reach).

Resume/portfolio rules she set: quote the 30k only, never the weak numbers,
never write down the TikTok situation (fine to say out loud). The ~20x gap
between the hit and the rest is the interview story, not the view count.
TODO (hers): screenshot Instagram insights — views, reach, saves, shares,
follows, follower count — before account access ends in November.
Saves and shares matter more than views.
