# Design traps: what cost revision rounds, and what worked

Mistakes from Jul to Oct 2026 on Sejal's web, Figma and product-design work (Tetriz feature pages, the AI-Native Index quiz, tetriz.ai wireframes, the Instahyre take-home, Sourced / Green Gallery redesigns, the pixel portfolio). Format: **symptom** (what she said or saw) → **cause** → **fix / rule now**. Rules themselves live in `playbooks/design-taste.md` and `playbooks/web-build.md`; this file is the why.

---

## A. Reading the brief wrong

1. **Built the landing page when she asked for feature sub-pages.** She said three times "we are not focusing on landing page", ending in "NOOOO, remake the artifact". → Claude anchored on the bigger artifact instead of the meeting notes. → Before building, restate the scope in one line ("Building: AI Adoption page only, as the template for Impact/ROI/Drivers") and build only that.
2. **Wrong fidelity, twice in one hour.** Section outlines → "these aren't low fi wireframes"; full-page wireframes → "revert, previous one looked better"; the old frames had been deleted. → Misread fidelity and overwrote the earlier version. → Ask or show one sample section before building all options. Never delete the prior version while she is still comparing.
3. **Style reworked after the build.** Instahyre went palette 1 → warm editorial ("looks Claude-coded") → back to palette 1 → 20+ micro rounds → a full v4 rebuild. Green Gallery: herbarium rejected, style tile rejected, then a hero. She: "I think I picked the wrong theme." → No approved style gate before building whole pages. → Style tile (palette, type, one component, one motion idea, one real block) approved first; for a new direction, only the hero next.
4. **Visual misled about the audience's motive.** Instahyre contest section built around a giant microphone; HR attendees come to learn or win a prize. → Designed for the event mechanic, not the attendee. → Ask "why is this person here?" and lead with that (prize-first section).
5. **Logic holes in the flow.** "Ask a question" placed after registration; a prize pass that said a question was "answered live" before the event existed; the quiz result CTA said "See where you stand on the Index" on the page that already shows it. → Copy written per section, never read as a sequence. → Read the page top to bottom as the user, checking time order and what each step already did.
6. **Intro graph over-promised.** The quiz intro showed a destination curve; the manager: too specific, "we cannot promise that they will be reaching there", and the "~5 minutes · 15 questions" line added nothing. → Visual implied an outcome the product cannot guarantee. → What worked: a masked "hidden result" teaser (skeleton stage bar, "?" score ring, "In 2 minutes, you'll get" list, "Reveal my stage →").
7. **Two independent data tracks fused into one visual.** Quiz context answers (never scored) were shown as "evidence" under the scored pillars; Sejal called it nonsensical. → Visualised before understanding where each number came from. → Read the logic/data doc first; one visual per data source.
8. **Internal model pushed onto users.** Observe/Transform/Govern pillars, "capped at 60", feedback-loop meter, gate boxes on the quiz result; pillar names across the site. → Team vocabulary leaked into user copy. → Removed everywhere; plain questions instead ("Can you see it? / Are you improving it? / Is it under control?").

## B. Looks AI-generated

9. **"Looks Claude-coded" / "very AI generated".** Editorial serif + mono specimen labels + hairlines on paper (Instahyre v2, Green Gallery). → The default "premium" formula of AI tools. → A register tied to the product's meaning (Instahyre v4: the page IS a video call; Green Gallery: cute and bubbly).
10. **Motion "like what GPT or DeepSeek does".** Fade + bouncy pop-ins. → Generic entrance animations. → Mask reveals, draw-ons, wipes with inner parallax, expo-out / quart in-out; no bounce, no pop.
11. **Clip-art "forced on the screen".** A glossy vector gift box on a flat typographic page; a question queue that "looks pasted, like bad VFX on a green screen". → New graphics drawn in a different style from the page. → Build from the page's own motifs (the gift became a "prize pass" ticket in the same family as the event pass; the queue became a white card panel with queue numbers and status pills).
12. **Dashboards "look like mocks" / "jagged and very AI like".** Busy invented dashboards with pills, deltas, tables, sparkline chips. → Designed from imagination, not from the real product. → Look at the live product and the sales deck first; rebuild as the real UI simplified (Ramp-style: title, big teal number, unit, soft area chart, nested light cards).
13. **Decorative chips and capsules.** Below-CTA proof chips, black `#0d0d0d` "label chips" on cards, "YOUR POSITION" / "GAP CLOSED" capsules. She: "What are the black blocks?", then "remove entirely". → Chips used as decoration. → Plain text label right below its marker; no chip unless it carries state.
14. **A bordered ring on a glowing chart marker** "looks very AI generated". → Default glow styling. → Marker plus a wave pulse only.
15. **Pixel headings hard to read.** First fix (weight, tracking) was ignored; she: "maybe the font itself is the reason". → Tweaked instead of replacing. → When a glyph is unreadable, swap the face.

## C. Rules that had to be repeated (each one now standing)

16. **Chips came back under the hero CTAs** on AI Impact after being removed on AI Adoption ("i told you ... again and again, and asked you to make it a memory too"). → Porting a reference that had them. → A standing rule beats any reference image.
17. **Long subtexts** copied from a reference lede. → Reference treated as spec. → One short sentence, about 14 words, everywhere.
18. **Em dashes** kept appearing in copy, Figma text and layer names. → Default writing habit. → Grep for the character after every build, including layer names.
19. **Asked "want me to open the PR?"** after standing permission ("DID YOU CREATE A PR YET OR DO I HAVE TO PUBLISH IT?"). → Permission not remembered. → Create the PR, return the link, never merge.
20. **Overlap and tilt** crept in on ghost panels and pop-ups ("they're tilted ... don't do it"). → Trying to add "organic" depth. → Depth from position, size, opacity and shadow only.

## D. Charts and graphs

21. **Curve labels overlapping the line or seeping past the plot edge** (the "trailing curve" caption, three rounds). → Positioned by eye against the SVG viewBox, not the plot bounds. → Measure: `getBBox()` vs `getPointAtLength()` samples, ~20px clearance, inside the plot (e.g. x ≤ 1140, not the viewBox's 1180).
22. **Markers on the curve but at the wrong level** (Integrating sat on Deploying's row). → Placed on the curve at an arbitrary x. → Put each marker where the curve crosses its own level's label y; verify distance ≤ ~1px.
23. **Six graph defects in one message:** cropped text under a curve, gap label outside the gap, dots off the curve, last x-axis label cropped, dotted connector off its line, level labels emerging from the text instead of centred between gridlines. → No measurement pass, and not comparing against the Figma source. → Compare against the source frame, then check every label, dot and line programmatically before showing.
24. **Levels shown as buttons inside the plot.** Manager: an ideal graph keeps levels outside. → Interactivity crammed into the plot. → Levels on the axis or below; the interactive accordion beside the graph, driven by shared state.
25. **Dense side panel** next to the curve ("looks data dense"). → Every attribute per level shown. → Keep two items per level: "You're here if" and "What moves you up".
26. **Exit CTA graph declined after the median.** → Shape drawn without thinking about what it claims. → A rising climb + dashed median line + "You" dot.
27. **Axis label overlapped the quadrant** on the radar chart. → Label inside the chart area. → Axis labels outside.
28. **Teal target cell read as grey.** → Same low alpha for teal as for red. → Teal at ~0.26 + outline; red trap at ~0.07.
29. **A metric chart on a "problem" card** "doesn't make sense". → Every card got a viz. → Problems get words or an illustration of the problem, not a metric.
30. **Session Security metric line charts "don't make sense, any of it".** → One dashboard template applied to every feature. → Pick the visual the feature produces (live detection feed, redaction sample, blocked-command terminal). "Not everything needs a dashboard."

## E. Following her instructions precisely

31. **Org-scale pop-ups: she asked for one change, got five.** Pop-ups were shrunk, repositioned over the card, the provided avatar replaced by an illustration, and the card title renamed to the dummy name "Jordan". She: "NO you messed it up, revert", then "PAY CLOSE ATTENTION if you do not understand ask". → Over-interpreting and "improving" untouched parts. → Change only the named property; keep everything else pixel-identical; ask when unsure.
32. **Same avatar for every team member**, though she had supplied three. → Did not search `public/` for existing assets. → Inventory provided assets before drawing or generating anything.
33. **Real employee names** copied from a company dashboard screenshot. → Screenshot treated as content. → Dummy names only; treat screenshots as layout reference.
34. **Liked a card → copied its colours.** "I said the card looks good, doesn't mean you have to follow the same color." → Read "I like X" as "copy X". → Liking a reference means its layout or idea; recolour to the palette.
35. **Checkered grid used everywhere** after she showed it once as an example (portfolio). Same with Axiom's grid: she meant grid lines forming cells around each deep-dive, not a background. → Example treated as a theme. → Ask where it applies; apply only there.
36. **Missed items in a numbered list** ("I also asked you to add a header ... did you miss that?"). → Working from memory of the message. → Turn her message into a checklist and tick every item in the report.
37. **"Hover" built as click.** → Defaulted to the existing accordion behaviour. → Match the interaction verb she uses.

## F. Build and verification

38. **Animations that "don't run" in her browser** (no loop in two of three cards; markers not gliding). → framer SVG transforms (`motion.g`, `motion.circle` cx/cy) and `AnimatePresence` height animations did not run for her. → CSS transitions on opacity/cx/cy, `strokeDashoffset`, `pathLength`, grid-rows 0fr↔1fr.
39. **False "stuck" readings, hours lost.** → The hidden in-app Browser pane freezes CSS transitions and rAF, `whileInView` never fires, `innerHeight` is 0. → Verify with headless screenshots; never change logic based on a frozen pane.
40. **Back/Next buttons still shifting** after a min-height fix shipped. → The card was vertically centred, so any height change moved the footer. → Consistent container heights AND top-anchored layout, footer pinned with `mt-auto`.
41. **Work built on a stale base** (two PRs behind) had to be ported, then the PR closed and reopened on fresh master. → No `git fetch` before branching. → Fetch and branch fresh every time.
42. **PR body listed a removed page.** → Description written from session history. → Write the body from the final diff.
43. **White boxes behind text in Figma.** → `createAutoLayout()` wrappers default to a white fill. → `.fills = []` on every wrapper at creation.
44. **White text on a light panel in dark mode.** → A text token reused as a panel background. → A dedicated always-dark panel token.
45. **"See how it works" CTA did nothing.** → Button added without an anchor target. → Every CTA scrolls or links somewhere real; test it.
46. **"Why is the new code not redeployed?" / "is it pushed? is it merged?"** → Reports did not state deploy status. → End every report with the Preview / Live / Waiting status block.
47. **Library credits shown on the live site.** She: "we're basically giving away our information." → Credits put in the footer. → Credits in the README only.

## G. Copy and truth

48. **Pivot justified by one survey respondent.** → Over-reading one quote. → "Several respondents ... half of all answers asked for separate sections."
49. **Framing that contradicts the product.** "Human-made vs AI" on a platform that hosts both. → Catchy contrast over accuracy. → "and", not "vs".
50. **Hedge footnotes and invented stats** ("Sources linked before publish", $632B, 3.6×). → Filler to make a section feel weighty. → Cut unsourced numbers; use only grounded, attributed stats.
51. **Slack messages too long.** She nearly always asked "make it shorter" or "keep it very brief". → Over-explaining. → Default short and casual, in her first person.

---

## What worked (repeat these)

- **Problem-first narrative with interconnected headlines** (Why Tetriz): each headline answers the previous one, so the page reads as one argument. She called "sections must talk to each other" her major requirement.
- **Studying a reference for structure, not look:** Glean for story order and density (problem couplet, numbered payoff, customer stat-cards, quiz low); Axiom for grid-line cells; Ramp for clean product dashboards.
- **Section-outline flow-maps** at the story stage (teal tag, placeholder headline, note, grey "VISUAL" box). She preferred them to full wireframes.
- **Left-aligned hero copy + real dashboard on the right**, replacing a centred wall of text.
- **Her idea over the dropdown:** titles always visible, bullets cascade in one by one on scroll. Accordions for marketing copy felt clunky.
- **One shared scrollytelling template** (pinned left list with progress dividers + clipped teal stage + click-to-jump), finished on one page, then stamped onto four.
- **Two-layer stage**: one sharp, fully readable hero dashboard + one skeleton peeking behind for depth. Simpler beat the three-card fanned stack.
- **Interactive charts with one shared state:** curve markers, band colours and the field-guide accordion all driven by the active level; radar chart with a fixed marker, wave pulse, cursor tooltip and hover-to-expand context.
- **Open stat band**: big numbers without cards, vertical dividers, count-up on scroll.
- **Feature-true visuals:** feed / redaction / terminal for security instead of charts.
- **Icon = identity, colour = state** on quiz result tiles (icon per question, chip colour by answer strength).
- **Options written up with feasibility:** the quiz "Option B" note (data already exists, pure presentation, net simplification, one named trade-off) got straight to a decision.
- **A concept that makes the page mean something:** Instahyre "The Call" (visitor = an empty tile "You · on mute"; agenda = a video chapter bar). Sourced as a night gallery. Each looked like no other project.
- **Figma scroll reveals via component variants** (Static → Idle → phases → Done) when the prototype has no on-scroll trigger.
- **Codifying rules in her studio plugin** (house rules, taste gate, verify, ship checklist) so they stop being restated every round.
