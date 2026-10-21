# Script traps

Mistakes that cost revision rounds on comic and product-video scripts (Aug to Oct 2026), as **symptom → cause → fix**, then the approaches that worked. Method lives in `../playbooks/script-writing.md`.

---

## Story and structure

**1. "It's still surface level" / "the features don't come out", twice in a row.**
Cause: polishing VO wording when the problem is structural; no decision on what each scene proves or which screen proves it.
Fix: stop, write a bones-only spine (one line per beat + the real screen/picture carrying it), agree it, then write prose.

**2. Four attempts at an ending all fail (`context window`).**
Cause: nobody in the script wanted anything; three devs passively learning a thing. No want, no loss, no ending.
Fix: if you can't name the want, don't write the ending, fix the premise (e.g. he has to present at 10am; or he secretly caused the outage).

**3. Stakes never register even though the deadline is in the script (`graph`).**
Cause: the intern agreed to a deadline with a nod mid-film; a deadline you nod at is a line.
Fix: move the number into a request he makes early ("out by ten tonight"), then pay it off against that number.

**4. "Lacks setup and payoff" on a cut that looked complete.**
Cause: same as 3; every reveal landed as information because nothing could be lost.
Fix: one line of want at the top makes the existing payoffs land without rewriting them.

**5. The ending reads "clever, not funny" / "isn't landing as a gag".**
Cause: an observation (the cycle repeats, a new person nods) is a setup with no turn.
Fix: supply a turn: push the AI until it breaks, reveal the absurd prompt, throw his own words back.

**6. Punchline planned as the ending of every episode.**
Cause: confusing a runner (repeats, gets funnier) with a punchline (a surprise, dies on repetition).
Fix: the signature repeats; the final joke is derived from each term's own absurdity using a different engine.

**7. The loop "reads as the video starting again".**
Cause: the last panel handed back to panel 1 with nothing connecting them.
Fix: one sentence spans the seam (breaks on "but-", panel 1 finishes it), last panel = frame 1's plate unchanged, one take split in two.

**8. The loop undoes the episode (`system one model` draft).**
Cause: it replayed "I have no idea what that means" right after the character showed he understood.
Fix: end inside the story, or loop on the character's habit, not on his ignorance.

**9. Ending feels unfinished even after restaging (`remote control`).**
Cause: her question "who are you talking to??" was asked and then the film changed subject; an open question never closed.
Fix: answer it on screen. The winning line closed two threads at once and stayed on the product: "wait, have you been approving every step?" with him talking over her to bury it.

**10. "Too sudden" jump from realisation to action.**
Cause: "oh shit, my changes are uncommitted" cut straight to him typing on the phone.
Fix: a bridge beat held ~1.8s (he looks down at the phone; thought caption "wait. i can just remote control it."). Bridges also needed between product-video sections that "lose context fast".

**11. The hook is dead (first seconds need context to parse).**
Cause: opening on "so then my sister books the whole thing" / "as i was saying".
Fix: open on something scroll-stopping with no context ("you took all night for this??", a 3s slurp); continuation phrases go at the END of a loop.

**12. A stronger hook took over the episode.**
Cause: "so my ex left me for a chatbot" was funnier than the term, read as dystopian on an AI channel, and the follow-up "ex fact-checks me with AI" made the comparison a villain (and Peter by extension).
Fix: keep the landing on the term/product; characters are inefficient, not bad ("IDIOT >>> CRAZY PSYCHO EX"). Changes to the opening and the ending are separate problems; don't let a hook fix move the payoff.

**13. The episode doesn't do the feature justice (`/insights` v1).**
Cause: jokes about the AI being sarcastic, no actionable teach; the sarcasm felt "too intentional".
Fix: make the AI read real sections, give actionable suggestions the viewer could apply (the file name, the hook, the skill), self-indict first, and keep the comedy in the human's reaction.

**14. Actions with no concrete task ("what is he asking his AI to do?").**
Cause: panels gesture at work without saying what the work is.
Fix: every request is a specific task on screen ("build the API, write the tests, docs, and the changelog. do all four.").

**15. Implausible AI behaviour.**
Cause: the AI deleting tests on its own, or knowing payroll, Slack, billing.
Fix: the AI does only what a real agent would with permission, and knows only what its tools reach. Unreachable requests bounce ("Can't see payroll."), which is funnier anyway.

**16. Emotional end state wrong.**
Cause: AJ ended satisfied when Sejal wanted him in a bad mood.
Fix: decide the character's final mood as part of the beat outline.

**17. Claude rewrote the premise when asked for a swap (`prompt engineering` v6, v7).**
Cause: over-creating. She said "the same script you used for AJ and Ken, but instead of Ken, use Peter."
Fix: do the literal instruction first; propose alternatives separately, labelled.

**18. Character says something out of type.**
Cause: generic lines (Peter apologising; Peter announcing "this is called prompt engineering"; AJ jumping with excitement about extra typing; AJ's AI calling him "sir").
Fix: check each line against the cast voice rules; the term should arrive from someone else, never from the protagonist announcing it.

## Information flow and accuracy

**19. Number that means nothing: "...it cost four dollars." against a $5 cap.**
Cause: under budget is not a joke; the beat was written for feel.
Fix: numbers must point unambiguously one way (absurdly small: "forty cents"), or cut the beat.

**20. Same number twice inverts the joke ("done by ten" / "home by ten").**
Cause: no am/pm anchor against a 9 AM reading, and the echo told him outright he'd missed it.
Fix: different numbers (ten vs eight) and "tonight" to anchor PM.

**21. A character fails to understand something simpler than what he just said.**
Cause: Dev 2 said "we blew the context window" and then didn't get "it ran out of room".
Fix: have him be WRONG instead of ignorant ("it forgets stuff sometimes" → "It doesn't forget. It runs out of room.").

**22. Thought caption refers to a term nothing on screen mentioned; or a premise doesn't connect to the term ("walk us through the outage tomorrow, 10am").**
Fix: let the term arrive from a colleague on screen (Slack thread: "root cause was the context window"), so "that" in "I have no idea what that means" points at something.

**23. Bare jargon lands on nothing ("A step cap. A budget. You didn't set either.").**
Cause: naming instead of describing; nothing had established that any of it costs money.
Fix: describe the behaviour ("You could've told it to stop after fifty steps. Or after it's spent five dollars."), or teach by consequence (show what happens without it).

**24. Technical claims wrong, caught by engineers or reviews.**
Examples: the AI telling him he consented to a step cap and budget (both default off; the "yes" was a tool-permission prompt); subagents spawning subagents (they can't in that tool); a model that "can't just say" a one-word answer; a triage nurse who "glances" (the model reads everything; the saving is that it writes nothing back); "test one first" (use ten known answers); "you never left me a box for it" (models do ask sometimes).
Cause: guessing.
Fix: check every claim against current docs, note the source in the script notes, batch an engineer spot-check. Funny-but-wrong is a credibility event for a company selling engineering intelligence.

**25. A teach that shrinks the skill into a template.**
Cause: "Not more words. The four things I can't guess." made prompt engineering sound like filling four boxes, and taught only "say more".
Fix: name the principle ("Not louder. Clearer."), and add the counter-lesson in one beat (AJ over-specifies "use a for loop"; AI: "Tell me what done looks like. Leave how to me.").

**26. Explainer reads as "too technical".**
Cause: boxes-and-arrows diagrams are exactly what the audience nods at without understanding; text-heavy cards nobody reads.
Fix: a picture metaphor taken from the AI's own line (graph's doors and ID passes; doctor vs triage nurse; a clean desk and one page back), centred, icons over text; the term appears only as a renaming.

**27. Invented statistics in a refined script ("40% more time in review", "a 2025 DORA report found...").**
Cause: the refiner skill demands a stat, so one got filled in.
Fix: never present an unverified number as fact; write the sentence to accept a real figure and flag it as blocking.

**28. Vendor-new term chosen.**
Cause: `system one model` was coined by one company three weeks earlier; the how-to section copied its console.
Fix: run the topic filter honestly (fails "senior would be embarrassed", drifts toward "it's product"); if locked, cut the vendor flow to one or two panels.

## Product / explainer scripts

**29. VO says one thing, the screen shows another.**
Cause: VO "it fixes it and pushes it to your whole org" over a screen with an Install button; the product only recommends, a human adopts.
Fix: adversarial pass against product docs (PRDs, sales walkthroughs) before review; the visual is usually right and the VO overclaims.

**30. Exec: "Confusing, what is this?" on a hook.**
Cause: an indirect scenario ("two engineers, same tool, one ships") the viewer has to decode.
Fix: state the literal contrast first; use the scenario later as evidence.

**31. "The script doesn't flow."**
Cause: hook and category claim say the same thing; the product is introduced twice; features jump with no link; a named agent/feature is never introduced.
Fix: the template spine (problem → product enters once → feature X, Y, Z each with a real screen → recap → CTA → close), a bridge line per transition, don't name what you can't introduce.

**32. Internal vocabulary leaks into VO.**
Cause: pitch-deck pillar names used as product names; file names spoken.
Fix: product name only; screen-only terms stay on screen.

**33. Feature framed as extraction.**
Cause: "your best engineers know things, we pull those patterns out".
Fix: subject of the sentence is "everyone gets taught best practices".

**34. Storyboard "too literal".**
Cause: illustrating the script word for word; a metaphor (ship sinking) introduced then abandoned for gears/speedometer; concepts never resolve into the term.
Fix: one metaphor carried and resolved; storyboard keyframes anchor the script rather than decorate it; serious tone for a B2B brand.

**35. "Charts must earn their seconds."**
Cause: 10s of a growing chart to say "improving".
Fix: a chart only if what it indicates is instantly clear; otherwise a stat or a before/after that visibly differs.

## Voice and timing (script-stage fixes)

**36. Interruptions go soft.**
Cause: the line being cut off was recorded resolving before the cut, or ducked instead of cut.
Fix: record cut-off lines past the cut at full energy; a "uh-" that interrupts is sharp, not trailing.

**37. Same character, different voices or pace mid-film.**
Cause: takes regenerated later with another voice; mixed tempo multipliers; ElevenLabs picking a different delivery rate per generation; a single-line regen drifting accent.
Fix: one voice per character, all of a character's lines in one sitting, measure syllables/sec, keep lines as separate takes so a fix is one line.

**38. Punchline answered too fast.**
Cause: no comedic gap after the indicting line.
Fix: write the beat in (0.5s or more; Sejal tuned one to 2.5s).

**39. TTS misreads stylised text.**
Fix: VO sheet says "noob", caption says "n00b"; pronunciation notes for product names and acronyms.

**40. Over budget on runtime.**
Cause: long AI explainer lines (94s of AI lines in a 3:08 cut).
Fix: cut AI lines first; holds ~1s after lines; Shorts cap 3:00; standing budget ~2:30.

## Process

**41. Flip-flopping with every reviewer.**
Cause: agreeing with Sejal, then Mohit, then Anandhi, each time siding with the last message. Her words: "if you're just agreeing to me you're not different from any other chatbot."
Fix: weigh all views, say which is right and why, separate defects (hook vs payoff), push back on her too, then follow her lead if she still disagrees.

**42. The thread argues about rewriting the story when the problem was on screen.**
Cause: nobody measured. The last 8.74s were the same drawing (0 px diff between two plates, the third differing only by a mouth).
Fix: diff the frames and time the stretch before treating a flat beat as a writing problem; post the number in the thread.

**43. Old skill docs contradict current rules.**
Cause: the comic skill and cast files still describe stamps, bucket outros, "sir"/"Certainly", `bruh`.
Fix: memory standing rules and the playbook win; ask before editing skill files (Sejal's instruction for the launch skills).

**44. Artifacts and messages too long.**
Cause: over-explaining for colleagues who won't read it.
Fix: shorten; Slack messages in her voice, lowercase, short, one line per point, only what the recipient asked for, typed in chat (never a file).

---

## Approaches that worked
- **Taking Sejal's own beat outline and refining it** (loop restart, `/insights` report flow, the date premise, "I have a guy" as a callback, the hackathon). Her structure won more than once; improve it, don't replace it.
- **The plant and the wave-off** ("Do any of these depend on each other?" / "whatever, go"): keeps the AI blameless and sets up the punchline "You said 'whatever.'", which later became a cross-episode callback.
- **Teach by consequence**: show what happens without the control instead of explaining the control.
- **Picture first, term renames it** (doors → dots and arrows → "it's a graph").
- **Two-rung explanation**: dense jargon answer, held blank face, "again but for a noob", plain answer.
- **Accumulation list running off the frame**, reveal order machinery first then purpose, the character-revealing item buried in nonsense.
- **AI reads section titles aloud** ("IMPRESSIVE THINGS YOU DID", "WHAT'S HINDERING YOU", "WHERE THINGS GO WRONG", "MEMORABLE MOMENT") as structure, each holding ~1s before its visual.
- **Self-indicting AI** (its own column first) before turning on the human.
- **Callback in a new mouth** ("I have a guy"; "You only get the page.").
- **Loop on the character's habit** (AJ asks for a review of the fix he didn't read: "can you review th-").
- **Reusing existing plates** so a new episode or short only costs VO (the shorts experiment used graph plates entirely).
- **Writing scripts in chat first, then the artifact**, keeping every prior version as a tab or appendix.
- **Measuring and posting the number** in a review thread to end opinion-vs-opinion debates.
