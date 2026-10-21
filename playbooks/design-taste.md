# Design taste: Sejal's checklist

Apply this before showing Sejal ANY design: a web page, a Figma frame, a slide graphic, a chart, a case study. Every rule here came from a correction she made at least once, most of them more than once. A standing rule beats any reference image she or a manager shares ("the reference shows chips" is not permission to add chips).

Sources: memory notes `feedback-*` (Jul to Oct 2026), the Tetriz v1.5 feature-page build (Aug 2026), the quiz redesign (Jul 2026), the Instahyre take-home, Sourced / Green Gallery redesigns, the pixel portfolio (Oct 2026), and her own `studio` plugin rules (`~/Documents/Github/studio/plugins/studio/shared/`, pushed to private repo SBorkar2002/studio).

---

## 0. Posture: advisor, not assistant

- She asked for this directly, three times (16, 17, 19 Oct): "stop working like my assistant and start working like my advisor ... a senior designer who has achieved the peak in the career and knows every aspect of designing and development."
- Lead with a verdict and a recommendation with reasons. Name the risks in HER idea too. If she still disagrees after hearing the argument, do it her way and do not relitigate.
- Never side with whoever spoke last (her, a manager, a PM). Seniority is not evidence. If a premise is factually wrong, correct it with a measurement.
- Do not manufacture disagreement either. If a note is right, say so once and move on.
- Ask when confused, as a numbered list she can answer line by line. She explicitly invites this ("if you do not understand ask", "you can also suggest me things before you move ahead"). One question beats a wrong build.
- Scope is sacred: touch only what she asked. "Also tidied X" is a regression in her eyes.

## 1. How to present options and directions

- **Show the plan before the build** for anything new ("i wanna see how you plan on building the page"). For a page: build the hero only, get a verdict, then the rest ("make a small hero section only for now, i need to see how you come up with").
- **Style tile first** for any new direction or redesign: palette, type pair, one component, one motion idea, one real content block. Nothing past the tile until she approves. Skipping this is her single most expensive rework loop (Instahyre: 4 palette/style rounds; Green Gallery: herbarium rejected, tile rejected, then hero).
- **2 or 3 options only when the direction is genuinely open.** Label them (A / B / C or Option 1/2/3), one line each on the angle, then say which you recommend and why. Include the trade-off of your pick. Example that worked: quiz SDLC fix, Options A (full list) / B (7-segment bar, recommended: data exists, net simplification, one trade-off on mobile) / C (copy only).
- **Variants never touch the main frame.** Duplicate and build beside it ("don't touch this frame make two more frames").
- **Keep the previous version alive** when you rebuild on her pushback. Twice she said "revert, previous one looked better" (landing wireframes; org-scale pop-ups). Rebuild beside, not over.
- **Fidelity must match the stage.** Story/spine stage = low-fi. For the tetriz.ai rebuild she wanted section-outline flow-maps (teal tag + placeholder headline + note + grey "VISUAL" box per section, 1200 wide), not full pages and not hi-fi. "We won't be designing right now, I just want to get the story right."
- **Read the brief's actual scope.** On the feature pages she said three times "we are NOT doing the landing page" before Claude stopped producing landing pages. Re-read her last message and the manager notes before choosing what to build.
- Messages she will paste (Slack, DMs): type them in chat, never in a file. Brief, casual, in her first person ("change the message into me making these changes"). Default to short; she nearly always asks "make it shorter".

## 2. Copy rules

- **No em dashes. Anywhere.** Page copy, Figma text layers, layer and frame names, alt text, commit messages, PR bodies for her. Use a colon, comma, full stop or " · ". Check after every build (grep for the character, or her `copy-lint.py`).
- **Subtext under any title: one short sentence, about 14 words max.** Hero lede, section ledes, card descriptions, "how it works" leads. A long reference lede gets trimmed, not copied. She asked for this as a standing memory after repeating it across pages.
- **More visuals, fewer words.** Convert "title + bullet + subtext" stacks into one-liners. Cut line by line. Glean.com was her model for density.
- **Never repeat the same fact on one screen.** Quiz result showed the stage name three times and the score twice: she cut it to once each.
- **No internal vocabulary in user copy.** She killed Observe/Transform/Govern site-wide and in the quiz: "the audience shouldn't learn new terms." No scores where the product dropped scoring. No internal model pushed onto the user.
- **Every section headline is a story beat, not a label**, and headlines read top to bottom as ONE argument. Model (Why Tetriz): "AI adoption is accelerating. Advantage is not." → "There's a curve. Most orgs can't see where they stand on it." → "You can't improve a position you can't locate." → "So Tetriz locates you, then closes the gap." → "But why us, and not another dashboard?"
- **Never invent** metrics, quotes, dates, testimonials, URLs, customer names. Placeholder framing until real. Unsourced stats get cut, not footnoted with "sources before publish". Soften absolute claims you cannot prove ("no competitor has" → "most tools don't have").
- **Dummy people only.** Never use real employee names from a dashboard screenshot she shares; invent neutral dummy names. A dummy example name ("Jordan") stays an example: do not rename titles around it.
- **Timeline logic.** On a pre-event page nothing can already have happened (no "answered live on 24 Oct" before the event).
- **Flow logic.** If a form collects X, the copy cannot imply X happens later (Instahyre: asking the question happens inside registration, one step).
- **Honest counts.** Never justify a product pivot with one respondent; "25+" not a precise number she cannot defend.
- Copy should not sound AI-written: vary sentence length; avoid "seamless", "leverage", "elevate", "robust", "end to end", "so that" tails.

## 3. Typography

- Each project gets its own type voice tied to what the product means. Do not reuse a pairing from another of her projects ("do not keep the same typography that you used for Sourced").
- Default AI fonts to avoid unless the brand owns them: Inter, Roboto, Space Grotesk.
- **Numerals must sit on one baseline and read easily.** Display faces with uneven figures (Syne) are banned for numbers; she moved every number to Geist SemiBold.
- **Readability beats character.** Pixel headings with an unreadable "e": first tweak (weight, tracking) was not enough; swap the font (Pixelify Sans → Jersey 15). If she says a glyph is hard to read, change the face, do not fiddle.
- Hero copy on a busy background must stay legible: she flagged a hard-to-read hero subtext and a section title lost on a background photo (fix: bigger, heavier, or a scrim).
- **Known working systems:**
  - Tetriz site/brand: Mona Sans (ExtraBold display, KPI numbers) · Plus Jakarta Sans (body/UI) · Geist / Geist Mono (labels, eyebrows, numbers). Teal `#03A6CF` (site renders `#0096BB`), ink `#0D0D0D`, ground `#FAFBFB` / white, border `#E5E7EB`, coral `#FF6B6B` = problem/slow, amber `#F5A623` = waiting/cost, green `#06D6A0`/`#22C55E` = success only.
  - Instahyre "The Call": Funnel Display / Funnel Sans / Geist Mono, cobalt `#2A35E6`, lime `#D6FF3D` (live/action only), ink `#0C0D12`, paper `#F1F0EC`.
  - Sourced (night gallery): Syne ExtraBold titles (never numbers), Geist UI, Geist Mono meta; ink `#0E0E11`, lilac `#B8A9FF` brand/actions, vermilion `#FF5A36` = human-made ONLY.
  - Green Gallery (cute and bubbly): Fredoka headings/buttons/numbers, Nunito body, Gochi Hand only for handwritten donor notes.
  - Portfolio (pixel chrome, HD work): Jersey 15 headings, Silkscreen labels/keys, Rethink Sans body; CTA lime `#D9F860`, lavender/purple brand.

## 4. Colour

- **Colour carries state, icons carry identity.** Never use a state colour decoratively. Reserved: teal = good/resolved/brand, amber = cost/waiting/before, red/coral = problem/risk, green = success only.
- **Emphasis colour on the words that carry weight only** (a number, a threshold, an outcome word), never whole sentences.
- **Teal needs more opacity than red to read as teal.** Impact quadrant: target cell `rgba(0,150,187,0.26)` + teal outline; trap cell red at 0.07; neutral cells `rgba(38,38,38,0.04)`. Low-alpha teal reads grey.
- **Use the brand hue, not a murkier "art-directed" one** (teal stage gradient starts at brand `#0096BB`, not a muddier teal a reference suggested).
- **Recolour borrowed components to the palette.** "I said the card looks good, doesn't mean you have to follow the same color": liking a reference means its LAYOUT.
- **Dark-mode panels need their own token.** Reusing `--ink` as a dark panel background flips to light in dark mode → white text on light panel. Add an always-dark token (e.g. `--ink-panel`).
- Status icons/tiles on a result: colour by the user's actual answer (green / amber / red), a few colours, not one.
- Keep her palette once she approves it; change everything else around it if the look is wrong.

## 5. Layout and composition

- **No overlap** unless she asks for a layered effect. Check bounding boxes of every absolutely positioned element. Pop-ups that "overlap a bit in the corners" were tried and removed: pop-ups fly out AWAY from the card.
- **No tilt.** Nothing rotated: cards, ghost panels, chips, images. Depth comes from position, size, opacity, shadow. Exceptions she granted (a sticker on the Instahyre gift box, the portfolio cat's fall spin) do not carry over.
- **Comparisons side by side on one screen**, same sizing and alignment, each side labelled. Before/after must visibly differ.
- **Stat card orientation follows position:** side column → vertical card; top/bottom strip → horizontal card.
- **Big numbers sit open, not boxed.** AI Impact stat band: numbers without cards, separated by vertical hairline dividers, count-up (odometer) on scroll.
- **Hero = eyebrow + headline + lede + CTA buttons. Nothing below the CTAs.** No chips, badges, proof rows, status dots. She removed them repeatedly and was angry when they came back.
- **Hero with no visual is weak.** Product pages: left-aligned copy, real dashboard on the right. Not centred text over nothing.
- **Hero spacing:** too much top/bottom padding reads empty; tighten padding and grow the type.
- **A plain section background** can take a subtle geometric line pattern at very low opacity. Do not spread a texture everywhere: the portfolio checkered background was "an example", not a theme.
- **Background imagery stays behind:** fade/dim background photos so foreground panels dominate.
- **Full-bleed photos she specifies get zero padding and zero radius**; only the text column has padding.
- **Faces:** never crop a head off; avatars zoomed out enough to show head and shoulders; centre the crop on the head outline, not the eyes. Give circular avatars a subtle 2px ring so they separate from their panel.
- **A team = several distinct people.** Overlapping avatar stack, each a different image. Never one image repeated; search `public/` for the avatars she already provided before drawing new ones.
- **No repeated images side by side.**
- **Consistent controls.** Back/Next stay in the same position on every step (fixed container heights, footer pinned). Kicker/eyebrow style consistent across sections, except where it makes no sense.
- **Icons:** equal padding on both sides inside their container; solid fill where an outline looks weak at size; brand/tool logos must be official SVGs (simpleicons), never background-stripped PNGs (jagged edges). Pick icons that mean the label (she rejected a share-like glyph for "Integrating"; asked for a power-pose figure for "motivation").
- **Spacing that feels cramped gets more room**; misaligned rows (a gap missing between blocks) get fixed before anything else.
- **Interludes (quiz, CTA bands) sit at story seams, never mid-argument.** Quiz/maturity tool = mid-scroll or nav, never the hero (too much friction for a CXO with 5 minutes).

## 6. Narrative structure for marketing / feature pages

- Arc: **problem → the shift → how it works (features) → at org scale → proof → next stage → CTA.** Benefits after features, not scattered.
- Lead with the problem; do not sell outright. Cost can be a hook but the thesis is the outcome.
- Visual hierarchy must say what matters: the loud beats (shift, proof) get weight; not every section the same size.
- **Finesse one page fully before stamping the template** onto the others.
- **Contextual interlinking**, not everything-to-everything: "Next stage" goes to the logical next page (Adoption → Impact → ROI; Session Security → Harness Control Plane), with a real headline ("Adoption proves AI ships. Impact proves it's worth it.").
- One clear primary CTA, repeated in nav and hero (that is normal). Do not duplicate the secondary: hero secondary is page-specific ("See how it works", which must scroll to the right section).
- Cut a section you cannot show visually ("We ran Tetriz on Tetriz" was removed on Impact for that reason) unless you propose a way to visualise it.
- Not every feature needs a dashboard. Session Security got a detection feed, a redaction card and a blocked-command terminal; line charts there "don't make sense".
- Testimonials only where they are specific to the page; no generic testimonial slot on every feature page.
- Steal structure, not narrative: Glean (problem couplet, numbered payoff triad, customer stat-cards, quiz low), Axiom (grid-line "cell" layout for deep dives), Ramp (clean simplified product dashboards), Graphite (layout density only; it is feature-first, which she avoids).

## 7. Charts and graphs

- **Labels never overlap the plotted line and never leave the plot area** (plot bounds, not the SVG viewBox). Verify with `getBBox()` + `getPointAtLength()` sampling, ~20px clearance. She asked for this in caps.
- **Levels/categories outside the plot**, on the axis or below, never as buttons inside it ("an ideal graph wouldn't have level inside the graph").
- **Band labels centred between their gridlines.** Dotted separators only at internal boundaries, never through a label.
- **Markers exactly on the curve at the right height** for their level (sample the path, distance ≤ ~1px). Dotted connectors exactly on top of the line they mark. Nothing cropped at the edges (last x-axis label, text under a curve).
- **Name the axes** ("Value captured" vertical, time horizontal). Strip decorative axis text that explains nothing ("ADOPTION →", "vertical = durable value captured", "Below the median (61)").
- **Interactive, not static** where the page pitches a model: hover a region → tooltip that follows the cursor (clamped to that region) AND the matching context on the side expands; hover, not click, when she says hover.
- A fixed "you are here" marker stays fixed; hover does not move it.
- Pulse = a wave expanding from the origin, easing out; not a breathe/scale. No border ring on a glowing marker ("looks very AI generated").
- Dashboards must look like the REAL product, simplified (Ramp-style): title, big number, small unit, soft area chart, nested light cards. No pills, deltas, tables and sparkline chips piled on ("looks like mocks", "jagged and very AI like"). If a dashboard gets "too elongated", restack: one full-width panel on top, two below.
- Chart fidelity in videos and decks: real shadows, icons paired with labels, smooth curves, dashed gridlines, real area fills.
- A metric viz does not belong on a problem card.
- Before shipping any chart, check: endpoints reach the plot edge, curve shape is honest (a "climb" curve must not dip after the median), and the "you" label flips below the point when the point is near the top.

## 8. Motion

- **After Effects grade, not "what GPT or DeepSeek does".** Use mask/clip reveals (type rising from behind a mask), line and strike draw-ons, cover wipes with inner parallax, playhead scrubs, choreographed staggers.
- **Easing:** expo-out `cubic-bezier(0.16,1,0.3,1)`, quart in-out `cubic-bezier(0.76,0,0.24,1)`. No bounce, no elastic, no scale pop on web, no fade used alone. (The spring "pop-in" rule in her notes is for VIDEO dot grids only.)
- **Calm swaps.** Content swaps on a feature stage: vertical enter/exit, ease-in-out, slight scale (.97→1); no spring, no horizontal slide, no crossfade with both visible.
- **No loops on content** unless asked; bars fill ONCE. A pulse or throb must ease in and out, never stop dead. Never fade something by scaling its geometry.
- **Don't over-animate.** Manager note on the landing page: everything moving takes the seriousness away. Animate what carries meaning.
- Speed: she often asks for faster (e.g. card cycle sped up by 0.5 s). Default to snappy.
- Prototype screen changes in her case studies: instant cuts, no fade.
- Respect reduced motion.

## 9. What reads as AI-generic (reject on sight)

- Editorial serif + mono "specimen labels" + hairline rules on paper (her top reject: Instahyre v2 Instrument Serif, Green Gallery Fraunces/DM Mono). "Looks Claude-coded."
- Off-white + black type + one orange accent.
- Purple-to-blue gradients, glassy blobs, generic 3D, glossy vector clip-art ("forced on the screen", "pasted on like bad VFX").
- Cards everywhere; stacked identical cards where a story or scrollytelling fits (portfolio Experience had to become scrollytelling).
- Fade-up-on-scroll for everything; bounce; scale pops.
- Chips, capsules and badges as decoration (she removed "YOUR POSITION" / "GAP CLOSED" capsules, label chips, below-CTA chips). Put a label as plain text right under its marker instead.
- Bordered rings around glowing markers.
- Em dashes in copy.
- **The fix:** an opinionated register tied to the product's meaning (Instahyre = the page IS a video call; Sourced = night gallery; Green Gallery = cute and bubbly with a growing plant; portfolio = pixel chrome + HD work). Derive new graphics from motifs already on the page (tickets, tiles, rules, the page's own strokes), never a new illustration style.

## 10. Hard "never" list (quick scan before sending)

- [ ] No em dashes in any visible text or layer name
- [ ] No tilt; nothing overlapping that she did not ask to overlap
- [ ] Hero: nothing under the CTA buttons
- [ ] Every subtext ≤ ~14 words, one sentence
- [ ] No invented numbers, quotes, names; no real employee names
- [ ] No internal jargon (Observe/Transform/Govern etc.) in user copy
- [ ] Chart labels clear of the curve and inside the plot; markers on the curve
- [ ] No repeated image side by side; distinct avatars for a team
- [ ] Brand palette and type from the project system, recoloured references
- [ ] Motion: no bounce, no pop, no lone fade; eases in and out
- [ ] No paid tools/credits (Figma AI images, Higgsfield) unless she opts in; get premium feel with grain, blur/glass, layered shadows, big type
- [ ] Nothing from the AI-generic list
- [ ] Both themes checked if the page has dark mode; phone width checked
- [ ] Screenshot taken and actually looked at before saying done
