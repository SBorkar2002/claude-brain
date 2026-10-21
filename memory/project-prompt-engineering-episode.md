---
name: project-prompt-engineering-episode
description: "`prompt engineering` comic episode (Script A, Wait, What?): Remotion build PromptEng, file map, audio sources, flap pairs, open flags as of 20 Oct 2026"
metadata:
  node_type: memory
  type: project
  originSessionId: aaa5348d-b6e2-4e86-afa2-9f19305a3125
  modified: 2026-10-20T09:24:24.115Z
---

Built 20 Oct 2026 from Sejal's Figma page `Prompt engieering` (828:3, file UM66oBdfGGPHkENjoPpN1S, frame1..frame36)
and the review artifact claude.ai/artifact/CQdn2a1tiasejEXMzyUV2L (Script A "Wait, What?" recommended over B "Free lunch").
Repo script `comics/scripts/prompt-engineering.md` is the OLDER free-lunch / five-row version, not what was built.

**Build:** `~/Documents/comics-video`, composition `PromptEng`.
- `v10/pe_audio.py` cuts the takes in `public/pe/vo_src/` (peter=Eric, aj=Jet, ai=David, ai_card=David re-record), then `v10/pe_emit.py` writes `src/pe_cut.json`.
- Code: `src/PromptEng.tsx` + `src/PeScreens.tsx`. Plates are in `public/pe/plates`.
- Studio runs in the terminal panel on port 3335. Render: `out/prompt_engineering_v1.mp4`, 2:12.

**Decisions:**
- The card read (f32) uses ai_card.mp3. Sejal's call: "constraints" was mispronounced in the long take (37.4-46.9s, unused).
- The board's monitors are placeholders, so every screen is built in PeScreens from the artifact: prompt contract rows, question chips, the Wait, What? app with the 40->41 counter, OfficeOS 212, leaderboard, wish-word strike, contract explainer, cost, card.
- Flap pairs, all measured: 14/16, 22/23, 34(=36)/35, and the two-shot 20/21 with `frame20_ss` (both shut) composited from the two real frames.
- The calm flap uses a LOCAL threshold (+-0.3s max minus 14 dB) and a recursive run split: open runs 3-9 frames, closes >=2 frames.
- Bed: the daylight stretch of EP005's printer-free amb_track.mp3 (from 44s), ducked under every voice.

**v2 (20 Oct), the leaderboard (f17), now 5.0s:**
- Circular profile pictures sit beside the names. AJ's is cropped from her full-body sheet; Peter's is the drooling head she supplied.
- At ev.dog (2.3s), Peter's picture hard-swaps to the crying-dog meme. The dog is keyed off green and cropped to the head, and it has no audio.
- Built by `v10/pe_avatars.py`. Sources are in `public/pe/dog_src`; output goes to `public/pe/avatars` and `public/pe/dog`.
- Runtime is 2:14.

**Open flags for Sejal:**
- The AI take has no line for script panel 18 ("He let me ask. You didn't..."), so f31 (cost) plays silent for 3.4s.
- AJ says "Thank you" but the caption reads "ty." (Figma text kept).
- No loop panel or NEXT HACKATHON caption: the film ends on f35/36.

Related: [[project-comic-pipeline]], [[feedback-lip-sync-real-frames]], [[project-system-one-model-episode]]
