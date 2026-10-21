# Script writing playbook

How Sejal and Claude write two kinds of scripts:
- **A. Comic shorts:** the *I Have No Idea What That Means* series on the AI FOMO channel. One AI/eng term per episode, taught inside a joke. 9:16 vertical, held comic panels, VO + burned-in captions.
- **B. Product and explainer VO scripts:** launch videos for Tetriz (B2B buyer, CTO audience) and SEO explainers (educational, no brand, e.g. DORA metrics).

Distilled from Aug to Oct 2026 sessions. Traps that cost revision rounds are in `../lessons/script-traps.md`. Channel thinking is in `channel-strategy.md`. Production of a comic after the script is approved (art, VO cutting, Remotion) is in `comics.md` and `video-production.md`.

**Where the originals lived (may be inaccessible after the company account shuts down):** comic rules in the company `product-brain` repo under `video/youtube/comics/` (`skills/comic-script-writer.md`, `characters/cast.md`, `topic-filter.md`, `scripts/*.md`). Copies of the launch/SEO refiner skills are in `../setup/launch-script-refiner.md` and `../setup/seo-script-refiner.md`. Where this playbook and an old skill file disagree, **this playbook and the memory notes win**: the old comic skill still describes stamps, bucket outros, "sir" and "bruh", all of which Sejal killed in Oct 2026.

---

## 0. Rules that apply to every script

1. **Spine before script.** Write one line per beat plus the evidence that carries it (which screen, which picture) before any prose. If a script gets "surface level" or "doesn't flow" twice, stop polishing words and rebuild the spine. (Anandhi's method; `../memory/feedback-spine-before-script.md`.)
2. **Intent framing first.** Two sentences: *This video IS:* (what the viewer should realise or feel) / *This video is NOT:* (what to leave out). If you can't write them, you are not ready to write.
3. **Somebody has to want something.** Name the want, say it early, and aim it at something that can grant it (a request to the AI, a deadline asked for). No want means no ending can land. For product videos the "want" is the buyer's problem in the hook.
4. **Check the information flow.** For every character in every panel: do they have a stated reason to know or not know what they know? Does every number point unambiguously in the direction of the joke? Does the AI only know what its tools can reach? Most failed beats "worked emotionally" while this was broken.
5. **Picture first, then the term renames it.** Explain the mechanism with a concrete picture or behaviour, and let the jargon arrive only as a label for what the viewer already understood. Describe, don't name.
6. **The dialogue is fiction; the technical claim is not.** Every factual claim (what a tool does, defaults, limits, prices) is checked against real docs before shipping. Never invent a stat to fill a required slot: flag it as unverified and ask.
7. **Every opened question gets closed.** If a character asks something on screen, the film must answer it (or deliberately bury it on camera). Dangling questions are why endings feel unfinished.
8. **No em dashes in any on-screen text, captions, VO sheets or Figma layer names.** Cut-off lines end in a trailing hyphen (`"you need to calm dow-"`). Hyphens in compound words are fine.
9. **Delivery etiquette.** When she says "give me the script here, don't update the artifact", put it in chat only. When an artifact is updated, keep older versions (new tab or appendix, never overwrite). Make sure a shared artifact link opens on the newest script.

---

## A. Comic short: method

### A1. Inputs (from topic selection)
A term arrives with four things (see `channel-strategy.md` for the topic filter):
```
TERM:              the word itself (said out loud at work, not a trend or headline)
WHY THEY WON'T ASK: evidence people look it up privately
THE TEACH:         the one thing a viewer knows afterwards
CANDIDATE ENDING:  which ending engine, and what about this term gives it
```
Sometimes the input is a source document instead (e.g. a workshop deck for prompt engineering, a teammate's Slack + artifacts for `/insights`). Read it fully and extract the one teach; leave everything else for another episode (one term per episode).

### A2. Steps
1. **Read the cast and voice rules** (A5) and the latest memory notes. Pick only the characters the joke needs; casting is free (one dev, several, or AIs alone).
2. **Find the premise with a want.** A situation where a specific character wants something concrete, ideally with a number or deadline (be out by ten tonight, present at 10am, win the hackathon, get a PR merged while on a date).
3. **Pick the ending engine from the term**, before writing (A4). Know your ending before you commit.
4. **Write the beat outline as bullets and show it in chat.** Sejal often supplies her own bullet outline; when she does, refine it, don't replace it. Her structural instincts (the loop restart, the `/insights` report flow, the date premise, "I have a guy" as a callback) beat Claude's several times.
5. **Write the full panel table** (A6 format), with reused plates marked.
6. **Accuracy pass** against docs (and a batched engineer spot-check if needed).
7. **Information-flow pass** (rule 4) and **comedy pass** (A7).
8. **Read it aloud / rough voice pass** before any art. The voice pass is the cheapest kill gate: these gags live or die on delivery.
9. **ElevenLabs line sheet** per character, with tags (section C).
10. Review rounds (section E), then freeze the approved text as the script record.

### A3. Beat template (what the shipped episodes share)
Not every episode uses every beat; `remote control` deliberately dropped the signature. Typical 60s to 3:00, 20 to 40 panels; shorter is better (YouTube Shorts cap is 3:00; one episode was cut to 2:59 to qualify).

| Beat | Job | Shipped examples |
|---|---|---|
| **Cold open / hook** | First ~2s must stop the scroll with no context. A line or sound that is funny or tense on its own. | "you took all night for this??" (Ken to AJ); a 2.9s slurp; "hope your AI was less brutal than mine with /insights." |
| **Term drop + bluff** | Someone else uses the term; the protagonist bluffs. | "Riiiight. A loop." · "ohh /insights? nah nah, bet mine was worse" · "Right. No, obviously." |
| **Signature** | Thought caption, once, near the top: *I have no idea what that means.* | Every IHNIWTM episode except remote control. |
| **The want** | Stated as a request with stakes. | "yeah, got it. out by ten tonight." |
| **Private ask** | He asks his own AI, privately (asking a person costs status). | "yo what's /insights?" |
| **The plant** | The AI asks the one question that decides everything; the human waves it off. This keeps the AI blameless later. | AI: "On it. Do any of these depend on each other?" AJ: "whatever, go" |
| **Consequence** | Time skip or escalation; the want is lost. Time told by a header that changes with the light, not a prop clock. | `10:00 PM` asleep, then `8:50 AM` *ding* "-AH" |
| **The turn / reveal** | Something the viewer didn't expect but instantly accepts. | "Yes. Though you could've been home by eight." |
| **The teach** | Full-screen explainer takeover: a picture metaphor first, the term renames it. No captions over explainer visuals; icons over text. | Graph's doors and ID passes; system-one's doctor vs triage nurse; subagent's small mark at a clean desk bringing back one page. |
| **Try this** | One get-started thing the viewer could do. Often a screenshot-able card held ~2s. | "Next time, fill these in before you hit enter." |
| **Punchline** | Flat. Usually the human's own words (or the AI's earlier line) thrown back. | "You said 'whatever.'" · "You only get the page." |
| **Reset** | The character snaps back to type, which is *why it happens again*. | "…you know what? couldn't care less." · "cool cool cool. fix it" |
| **Loop seam** (if earned) | Last panel is frame 1's own plate; one sentence spans the cut. | Ken: "it's 9 am. you said you'd be done by 10 pm yesterday but-" → panel 1 finishes "you took all night for this??" |

**Comedy is a bracket, not a layer.** Joke opens and closes; the middle teaches straight. The joke never sits on top of the lesson, which is what keeps it from going cringe.

### A4. Ending engines (derive from the term, never from a template)
| Engine | How it works | Example |
|---|---|---|
| Structural loop | The form repeats the content. | `loop`: the next dev starts the same conversation; `graph`: Ken's scolding repeats every morning. |
| Accumulation | A list or quantity escalates past absurdity, then a flat reaction. | `subagent`: AJ's prompt box runs off the bottom of the frame like a printer feed. |
| Self-demonstration | The character causes the thing while learning about it. | `context window`: he fills it while asking what it is. |
| Callback | Plant a line, pay it off in a different mouth. Funniest when it **changes speakers**. | The AI says "I have a guy"; later the dev says it, smugly, to a confused colleague. |
| Inversion | Turn the machine's flaw onto the humans. | `remote control`: she jokes "which idiot sits there approving every single step?" about the man in shot. |

Loop rules (all learned the hard way):
- A repeat is not a loop. **Something must carry across the cut:** one sentence breaks on a conjunction or mid-word ("but-", "review th-") and panel 1 finishes it.
- The last panel reuses **frame 1's plate unchanged**, so the picture doesn't move; only the voice carries on. Last caption sits in the first caption's position.
- Record the seam line as **one take and split it**; two generations put different breath and room tone either side of the join.
- A continuation phrase a cold viewer can't parse ("as i was saying..") goes at the END of the film, never the opening seconds.
- The loop must not undo the lesson (replaying "I have no idea what that means" after he learned it). Sejal uses loops often; when the term has nothing cyclical, make the loop about the *character's habit* (AJ delegates without reading, so he asks for another review) rather than the term.
- **No end cards** (standing since 5 Oct 2026): no `TERM · CLEARED` stamp, no speed/cost/quality bucket outro, no "next: ___" tease, no bucket in the script header. The ending lands inside the story. One past exception: Sejal asked for a definition slate with a tiny "save this for later" pill on `system one model` (9 Oct); later asks (16 to 17 Oct) said no end cards again. If in doubt, ask.

### A5. Cast and voices
Personalities are backstage; scripts reveal them, nobody explains them. Each dev's AI is what their prompting made it (mirror or consequence of the dev).

| Character | Type | Voice rules | ElevenLabs voice used |
|---|---|---|---|
| **AJ** (the intern, old "Dev 4") | Backwards cap, feet on desk, reads nothing, tries everything, unbothered when it breaks. The breakout character. | all lowercase, no terminal punctuation, short, imperative, slang ("bet", "yo", "ty", "lol", "cool cool cool"). Hates typing more to the AI; would not jump with excitement over extra steps. | Jet (earlier Kai) |
| **AJ's AI** | Plain, dry, blameless (graph-engineering register). | "On it." Short plain sentences, asks the one question that matters, dry understatement ("Though you could've been home by eight."), never gloats, punchline = his own words or its own earlier line thrown back flat. **Never** "sir", "Certainly", "instantiate", "dispatched", "bruh". | David |
| **Peter** (the lead, old "Dev 1") | Most senior in the room, so he can't ask anyone. Says "obviously" about things he learned yesterday. Bluffs, competitive ("My time to shine now", "I'm winning the next hackathon for sure"). | Complete sentences, hedges, buys time, never asks a human a direct question. Sejal: **Peter is not apologetic** (the old cast note "apologising to software" was rejected). | Eric (keep ONE voice for all of him; a mid-film voice change was a defect) |
| **Peter's AI** | Burnt out: asked the same thing hundreds of times. | Flat, minimal, occasionally brutal ("I'm the same one from this morning."). "Go to sleep." is an optional runner, exact wording if used, often dropped. | David |
| **Ken** (senior, AJ's manager; glasses, `.env` tee) | Extremely cautious, keeps asking his AI until he gets an answer; anxious, burns credits researching. | Dry, unimpressed with AJ. Old "Dev 3" traits (numbers his questions, wants a source) fit him; exact mapping unclear from history. | Thomas |
| **Sameer** | Colleague who opens/closes `/insights`, sips coffee. Old dev mapping unclear from history (probably the coffee one, Dev 2). | Casual, slightly exhausted. | Andrew |
| **The date** (one-off, remote control) | Talks nonstop, never goes silent. | Runs under everything as background; captions cut short when she's background. | Vanessa |

Hard rules: the AIs never have faces or bodies; all share one teal six-petal mark with an eye (the AI is identified by how it talks). Greyscale art, teal only where the teaching happens. No ties (CEO note: nothing corporate). Unused device saved for later: AIs in a split screen interrupting each other while nobody acknowledges it.

### A6. Output format
Header, then a table, then short notes.
```
# Episode: `term`
Status · Cast · Premise (one line) · Ending engine (one line) · Runtime estimate · Source doc

| # | Direction | Line |
| 1 | WIDE. The office... (mark "frame 1's plate again, unchanged" for reuses) | **AJ** "bet." |
```
- Mark reused framings explicitly ("framing identical to panel 4", "graph plate s12"). Reuse is what makes cadence affordable and what makes structural gags read.
- Lines: `**SPEAKER** "line"`, thought captions in italics, SFX as `*click*` `*ding*` `*ping*` (every sound gets a word on screen, every SFX word pops on its sound).
- Sejal's notation: CAPITALS = shown on screen / full volume; lowercase continuation = keeps going in the background under other dialogue ("OKAY OKAY THAT'S ENOUGH, i've had enough of this...").
- Notes section: the teach in one sentence, why the numbers are what they are, accuracy notes with sources, pending sign-offs, what to record. Keep notes short; colleagues won't read long artifacts.

### A7. Comedy craft (what landed)
- **A gag = setup + turn.** No turn, no gag. A clever structural observation ("look, the cycle repeats") is a setup with no turn: "oh, ha", not a laugh.
- **Runner vs punchline.** A runner repeats and gets funnier ("Riiiight. A ___."). A punchline is a surprise and dies on repetition. Never reuse a punchline across episodes.
- **Numbers must point one way.** $4 against a $5 cap is under budget, so not a joke. If the joke is "tiny", make it absurdly tiny (forty cents); if two times are compared, anchor am/pm and use different numbers.
- **Reveal order: machinery first, purpose second.** Show the huge tree of agents, then the dumb prompt that caused it ("tell me if anyone's mad at me"). Bury the character-revealing item in a list of nonsense ("check if i'm the problem").
- **The AI stays blameless.** It asked; he waved it off. If the AI promises and fails, the ending moves onto the tool instead of the character (and onto the product's reputation).
- **The AI indicts itself first, then turns** (`/insights`: "ON MY SIDE" column fills before "ON YOURS").
- **Characters are inefficient, not villains.** The product's job is to convert an inefficient person, not shame a bad one. Reviewer line that settled it: "IDIOT >>> CRAZY PSYCHO EX."
- **The hook can't be bigger than the term.** A relationship joke that outshines remote control leaves viewers remembering the relationship. Land the last beat on the term/product, then let the character dodge.
- **Talking over > waiting.** He cuts her off mid-word to bury it; if he waits for her to finish, he's just rude.
- **Comic pauses are written in.** Give a beat (0.5s or more) after the line that indicts the character before he answers; Sejal tuned one comedic silence up to 2.5s.
- **Bridge beats.** A realisation followed instantly by action reads as "too sudden"; add a held beat (he looks down at the phone) between "my changes are uncommitted" and "Open the PR".
- **Unfinished sentences** (cut off by a human, by a ping, by the edit) read as character. Use with a reason.
- **Memes as inserts** (shivering dog over Peter, laughing cat on AJ's monitor) work as a hard-cut overlay when they say what the character feels; Sejal picks them.
- Two-rung explanations work: an impenetrable technical answer, a held blank face, then "again, but for a noob" and the plain one (CEO asked for exactly this on `system one model`).

### A8. Comic review checklist
- [ ] First 2 seconds stop a scroll with zero context.
- [ ] Someone wants something, stated early as a request, with a number if possible.
- [ ] Every character's knowledge is justified in every panel; the AI only knows what its tools reach.
- [ ] Every number is unambiguous about direction; am/pm anchored.
- [ ] Every technical claim verified against docs; sources noted.
- [ ] The teach is a picture first; the term only renames it; no bare jargon outside the "dense rung".
- [ ] There is a turn (not just an observation) at the end; punchline is new for this episode.
- [ ] Every question asked on screen is answered or deliberately buried.
- [ ] AI register correct (no sir/Certainly/bruh); Peter not apologetic; AJ lowercase.
- [ ] No end card, stamp, bucket or "next episode" panel.
- [ ] Loop (if any): one sentence spans the seam, frame 1's plate reused, one take split.
- [ ] Reused plates marked; panel count and runtime estimated (under 3:00 for Shorts).
- [ ] No em dashes anywhere on screen; cut-offs use trailing hyphens.
- [ ] One term only; zero product (Tetriz) content on the channel.

---

## B. Product / explainer VO script: method

### B1. Launch video (brand-first, product-led, CTA required)
Audience: CTO / VP Eng / CXO, time-poor, hype-resistant, pitched AI tools constantly. Bar: open on a problem they recognise, sharp editorial tone (not a walkthrough), tension then resolution, one insight they didn't walk in with.

**Spine (Anandhi's template, then dogfooded):** real-world problem for a CTO → how it can be solved = enter the product → how we solve with X (feature + the real screen + how it extends) → Y → Z → recap → CTA (even a small recall action) → closing slide.

The shipped 8-scene version: S1 hook (buyer's problem as questions, cost of inaction, "guess vs know") · S2a reframe (the real gap) · S2b product enters, named once, positioned by thesis · S3 to S6 one scene per lever, each "product owns the verb → evidence on a named screen → one-line takeaway" · S6b stack payoff (~11 words, the levers compound) · S7 the heart (crowning capability) · S8 close (hook's questions resolve to answers, end slate fixed copy).

Reusable rules (generalised from the Tetriz production rules):
- **Same explanatory template for every feature:** "X does this. For the individual it does A, for the org it does B." Show both the one-person effect and the org-wide spread.
- **A signature-word budget.** Decide how many times the core word is spoken and where (Tetriz: "coach" exactly twice, thesis and payoff).
- **Numbers live in the UI, not the VO.** A figure shown in a launch video is a published number: derivation owner and methodology before render, or ship directional tiles.
- **Screen-only terms** (file names, stage labels, internal taxonomy) are shown, never spoken. Don't use internal pitch-deck taxonomy as a product name. Don't name a feature/agent brand you can't introduce; describe the capability.
- **The product owns the working verb** in each scene; no actorless imperatives.
- **VO claim must match what the visual shows.** If the VO says "it fixes it and pushes org-wide" and the screen shows an Install button, the VO is wrong. Run an adversarial pass against the product docs (PRDs, sales walkthroughs) before review.
- **Frame features by who benefits, not who is mined:** "everyone gets taught best practices", never "we extract what your best engineers know".
- **Open with the literal contrast** ("everyone uses AI / not everyone is AI-native") before any oblique scenario; save scenario lines for evidence scenes.
- **A big claim ("AI-native") needs more than three stat cards**: check with the product owner what evidences it.
- **Flow:** the hook and the category claim must not say the same thing; introduce the product once; every scene change needs a bridge (carry-over element, breath, connective line); keep a persistent map of the pillars so the viewer knows where they are.
- Banned hype words: game-changing, revolutionary, cutting-edge, powerful, seamless, robust, leverage, unlock. Peer-to-peer, contractions, short lines, one longer line per scene max. Read it aloud; if it sounds like a sales deck, rewrite.
- Every scene footer names its **device** (cost of inaction, mechanism journey, exclusivity flipped positive). No device = no job = cut or merge. Avoid competitive negatives ("not another dashboard").
- Budgets: ~280 words for a 2:15 ceiling (~124 wpm); a later locked version ran ~267 words at ~148 wpm for 1:48. State duration ceiling, word count and wpm in the header, plus a fallback duration.
- **Document shape:** header meta → changes table vs previous version (old/new line + why) → outline (time window, role tag, concept, on-screen with sources, asset gaps inline) → verbatim VO per scene with word count + device note → timing table → production rules → open flags → prior versions appended verbatim → sources. Delivered as one artifact URL per video, updated in place with version labels, plus a repo copy.

### B2. SEO explainer (educational, no brand, no CTA)
Structure: **HOOK → CONTEXT → CONTENT → CLOSE**, ~166 words (hard ceiling 180) ≈ 60s. Every 14 words over ≈ 5 extra seconds.
- **Hook (~25 words):** a relatable scenario in second person, not a definition or stat. Right: "Your team shipped last Friday. But was it a good week or a bad week?" Wrong: "Four numbers tell you whether your team ships fast or ships broken." Never "Did you know", "Have you ever wondered", "In today's world". Keyword spoken within 15 seconds.
- **Context (~30 words):** what it is + one concrete surprising stat ("33,000 engineering teams", not "years of research"). Ends on the counterintuitive finding.
- **Content (~80 words):** name each term AND its benchmark immediately ("Deployment frequency: elite teams deploy multiple times a day"). Group pairs (speed pair, then stability pair). AI angle as a concrete consequence ("A weak prompt ships quietly and shows up three weeks later in your change failure rate").
- **Close (~25 words):** an aphorism, sentences of 8 words max, the most memorable line. No CTA, no product name.
- Add the current year when saying "now". Peer engineer voice, not explainer-channel narrator.
- **Ignore generic on-screen suggestions** in raw drafts ("show engineers collaborating"). Keep only real engineering environments (CI log, PR list, terminal) or tension the VO can't carry, as `VISUAL FLAG` lines in production notes.
- Always end with a **clean VO block** (no labels) for ElevenLabs and **production notes:** keyword timestamp, pronunciation, the pause cue ("one beat after ___"), where the VO rests while the visual carries, word count, duration.
- **Storyboard should guide the script, not illustrate it word for word.** Pick key frames as main beats and let them anchor the script. One metaphor, carried through and resolved (Anandhi's DORA note: a ship-sinking metaphor introduced then abandoned for gears breaks the thread).
- A paid teaser is not an SEO video: it keeps the product and CTA. Say which rules don't transfer instead of forcing them.

### B3. Product/explainer review checklist
- [ ] Intent IS / IS NOT written; spine agreed before prose.
- [ ] Hook is a recognisable problem or scenario; not repeated by the next scene.
- [ ] Each feature: named real screen, individual + org effect, one takeaway line.
- [ ] VO claims match the visual and the product docs; nothing shipped-as-future.
- [ ] Numbers in UI with an owner; every stat sourced or flagged.
- [ ] Bridges between scenes; product introduced once.
- [ ] Word count, wpm, duration, fallback stated; clean VO block present.

---

## C. Writing for VO (ElevenLabs)

**Casting**
- **Cast for register, not quality.** Presenter voices ("Fun & Informative", "Confident & Engaging") are upbeat at baseline, and a tag like `[exhausted]` loses to the voice's baseline. Filter for flat / dry / deadpan / tired first. Cloning copies timbre, not performance.
- One voice per character for the whole film. Two different voices for one character (e.g. lines regenerated later with another voice) reads as a different person mid-video.

**Generation**
- **Per line, grouped by character, never one multi-speaker pass.** A full-script pass is ~1,000 credits per retry; a single line is 30 to 50. It also allows per-character stability. Do one character's lines in one sitting so settings match.
- **Accent drift:** regenerating a single line has come back in a different accent (Indian to Russian). Partial regeneration of a long take is unreliable and full regeneration is expensive, so **fix lines at the script stage** and keep lines as independent takes from the start.
- Stability: Natural for flat/deadpan and narrow range; Creative only when one character needs wide emotional range. If tags are ignored, move toward Creative before rewriting tags.
- **Two tags per line maximum**, dominant first: `[amused]`, `[realising]`, `[nervous]`, `[venting]`, `[flat]`, `[panicked]`, `[low] [clipped]`, `[bluffing]`, `[distracted]`, `[caught]`, `[excited]`, `[suspicious]`.
- SFX (slurp, click, door) come from a library, never TTS. Breaths and sighs can be tags. One long effect beats three short ones (one 2.9s slurp across three panels reads as an uncomfortably long drink).

**Writing lines so they cut well**
- **Write the pause into the recording** when you can ("Long night." 3s gap "left a loop running").
- **Lines that get cut off must be recorded running past the cut at full energy.** If the take resolves or slows into the question mark, the interruption dies or leaves a dead beat.
- **"uh..." vs "uh-":** a trailing "uh" means he has time; cutting someone off needs a sharp, panicked "uh-" punched on top.
- **Loop seam lines are one take**, split at the break word.
- **Spell for the TTS, caption for the eye:** generate "noob", caption "n00b" (v3 reads 00 as digits). Add pronunciation notes for product names and acronyms (TET-riz, DOR-ah, "auth" as "awth").
- Elongations are written into the line when they are the joke: "Riiiight", "It ran aaalllllll-".
- Interruptions are hard cuts at full volume, not ducks; the interrupting cue is excluded from ducking.

**Pace**
- Typical speed-up is about 1.15x; Sejal has asked for 1.25x and 1.40x on rambling background lines. Same multiplier does not mean same pace: ElevenLabs picks its own delivery rate per generation, so measure **syllables per second** per take and override per take.
- Hold each panel ~1s after its line in long cuts (1.5 to 2s felt too long); shorts hold 0.3 to 0.5s. Explainer lines get a 1.2 to 1.5s pause after them so the picture can land.
- Runtime budget: Sejal's standing budget is ~2:30 for long cuts; YouTube Shorts must be under 3:00. The AI's explainer lines are usually what blows the budget (94s of AI lines in one 3:08 cut), so keep AI lines short.

**Line sheets** go per character with tags, in panel order, with a "must record / record at same time / unchanged, do not re-record" split when revising, so she only regenerates what changed.

---

## D. What Sejal rejects (quick list)
- Scripts that are "not funny enough": types instead of characters, showcases with no stakes, personality labels as the joke.
- Over-explaining: long artifact sections, gag explanations, explainer panels that restate what the script implies ("where the gag is" panels).
- End cards, stamps, buckets, "next episode" teases, branded intros.
- "sir"/"Certainly" AI, AI that is "too intentionally" sarcastic; AI doing implausible things (deleting tests without permission and many iterations).
- Actions with no concrete task ("what is he asking his AI to do? what's the task?").
- Endings where AJ comes out fine when she wanted him in a bad mood ("I want AJ to be in a bad mood at the end of the day, not be done").
- Explainers as boxes-and-arrows diagrams or walls of text; she wants icons over text ("viewers don't have the bandwidth to read everything") and visuals centred.
- Claude inventing a new premise when she asked for a swap ("the same script ... but instead of Ken, use Peter").
- Peter announcing the topic ("This is called prompt engineering") instead of the term arriving from someone else.
- Tagline-shaped answers when she asked for a structure.
- Drafted Slack messages that read like "telling it to an AI": she wants short, casual, lowercase, one paragraph per line, copy-pasteable, mentioning only what the recipient asked for. Messages go in chat, never in a file.

## E. Good lines vs rejected lines
| Rejected | Why | Kept |
|---|---|---|
| "A step cap. A budget. You didn't set either." | Bare nouns; nothing established what they cost | "You could've told it to stop after fifty steps. Or after it's spent five dollars." |
| "...it cost four dollars." (cap was $5) | Under budget is not a joke | Drop it, or make it absurd: "...forty cents." |
| "done by ten" / "home by ten" | Same number, no am/pm, inverted against 9 AM | AJ: "out by ten tonight." AI: "you could've been home by eight." |
| "I've generated three diagrams..." | Describes effort, explains nothing | Dense rung, picture rung, then "It runs out of room. Oldest thing goes first." |
| "Certainly. I have dispatched a specialised reviewer." | AJ's AI is not formal any more | "On it. I sent a helper to read it." |
| "You never left me a box for it" | Wrongly implies AI never asks unless told | "You said 'be VERY thorough.'" (his own words) |
| "Not more words. The four things I can't guess." | Shrinks a skill into a template | "That's prompt engineering. Not louder. Clearer." |
| "so my ex left me for a chatbot" | Dystopian frame on an AI channel; hook outshines the term | Keep the original story; land the product line ("which idiot sits there approving every single step?") then the dodge |
| "wait, what is that you were doi-" | Character line, closes one thread | "wait, have you been approving every step?" (closes her open question and her own joke; stays on the product) |
| "Sorry. One more thing and then I'll leave you alone." (Peter) | Peter isn't apologetic | "Okay, answer me this." |
| "Two engineers. Same tool. One ships. One doesn't." (launch hook) | Exec found the indirect metaphor confusing | State the literal gap first; use the scenario later as evidence |
| "AI has made writing code easy." | Observation, not a scenario | "Your team shipped more code last sprint than ever before. But your review queue is longer." |

## F. Review rounds (who catches what)
Reviewers across these projects, and the kind of note each gives (treat feedback as user research; weigh it, don't just obey the last speaker):
- **Anandhi (design lead, Sejal's manager):** structure, setup/payoff, whether a gag lands, flow between scenes, "too literal" storyboards, "if the opening could be replaced by a street and a cup of tea without changing the ending, the opening isn't doing work." Prefers a 10-minute discussion over hours of animating a script that may be scrapped.
- **Sumit (CEO):** messaging clarity for execs, plain contrasts, no internal taxonomy, "again but for a noob", whether creators would repost it.
- **Mohit (product/eng):** technical accuracy, actionable teaches ("viewers should understand the suggestions"), real file names, depth over surface; also writes his own versions.
- **Prashasti (content/distribution):** topic ideation and alternative scripts; her drafts got accuracy and comedy reviews from Claude.
- **Engineers:** fact-check claims; batch them (ten terms, one 20-minute pass) rather than a per-episode dependency.

When reviewers disagree: separate the defects (hook vs payoff are different problems), measure what can be measured (diff the frames, count seconds), say which note is right and why, and draft her reply. If Sejal still disagrees after hearing the argument, follow her lead.
