# Setup: rebuilding Sejal's Claude environment on a new Mac / account

Fast path: clone this repo to `~/Documents/Github/claude-brain` and run `./install.sh`.
It handles steps 1 to 4 below. Everything after that needs a human (logins, OAuth).

## 1. Global rules and memory (install.sh does this)

- `CLAUDE.md` → `~/.claude/CLAUDE.md` (loads in every session).
- `memory/*.md` → `~/.claude/projects/<home-path-with-dashes>/memory/`. Claude Code keys memory by
  the folder you launch it from. Sejal launches from her home folder, so on a Mac user `sejal` that is
  `~/.claude/projects/-Users-sejal/memory/`. Launch from somewhere else and memory won't load.
- Memory files mention paths like `/Users/sejal/Documents/...`. Keep the same macOS username
  (`sejal`) and the same folder layout (`~/Documents/Github/<repo>`) and they all stay valid.

## 2. Plugins (12) and marketplaces (4)

| Plugin | Marketplace | What it's for |
|---|---|---|
| figma | claude-plugins-official | Figma MCP + design skills (figma-use, generate-design...) |
| context7 | claude-plugins-official | Up-to-date library docs |
| code-simplifier | claude-plugins-official | Cleanup agent |
| chrome-devtools-mcp | claude-plugins-official | Drive/inspect Chrome, Lighthouse |
| hookify | claude-plugins-official | Turn "never do X again" into hooks |
| claude-md-management | claude-plugins-official | Keep CLAUDE.md current |
| playground | claude-plugins-official | Scratch playground |
| serena | claude-plugins-official | Code navigation MCP |
| impeccable | impeccable (`pbakaus/impeccable`) | Design build/review agents |
| taste-skill | taste-skill (`Leonxlnx/taste-skill`) | Frontend design taste |
| **studio** | sejal-studio (her own) | `/studio` entry point + code/figma/flow doctors. See `studio-plugin.md` |
| **studio-board** | sejal-studio (her own) | Side panel showing /studio progress |

Marketplaces: `anthropics/claude-plugins-official`, `pbakaus/impeccable`, `Leonxlnx/taste-skill`,
and `sejal-studio` = a local directory: clone `SBorkar2002/studio` to `~/Documents/Github/studio` first.

## 3. Skills (install.sh copies them to `~/.claude/skills/`)

Backed up in `setup/skills/third-party/` so nothing depends on upstream still existing:
- **HyperFrames video family:** hyperframes, -core, -cli, -media, -animation, -creative, -registry,
  general-video, faceless-explainer, motion-graphics, product-launch-video, website-to-video,
  pr-to-video, remotion-to-hyperframes, graphic-overlays, embedded-captions, slideshow
- **Higgsfield:** higgsfield-generate, -marketplace-cards, -product-photoshoot, -soul-id (PAID, only if she opts in)
- **Motion/design craft:** emil-design-eng, apple-design, animation-vocabulary, find-animation-opportunities,
  improve-animations, review-animations, web-design-guidelines, vercel-react-best-practices
- **Tools:** playwright-cli, deploy-to-vercel
- Upstream sources for the vercel ones are in `skill-lock.json` (`vercel-labs/agent-skills`).

Her own skill: `setup/skills/own/educational-video-intro.SKILL.md`. Her comic/video craft is
written up as playbooks in `playbooks/` rather than as skills (they were living in company repos).

## 4. Command-line tools (this Mac had, Oct 2026)

`brew install node pnpm ffmpeg gh uv git` then:
- `pip3 install openai-whisper pillow numpy` (word-level VO timestamps, image keying/diffs)
- `npm i -g @anthropic-ai/claude-code @playwright/cli`
- `npm i -g @google/clasp` (job-hunt Apps Script deploys) then `clasp login`
- `gh auth login` as **SBorkar2002**
- Remotion is per-project (`npm install` inside the project), no global install.

## 5. Connectors to reconnect on the new claude.ai account (manual, OAuth)

| Connector | Use | Note |
|---|---|---|
| Figma | All design work | Connect her personal Figma. Files on the Fi Pro team may become read-only or vanish: duplicate what matters into personal drafts NOW |
| Gmail | Job alerts, application replies | Connect PERSONAL Gmail. Job-hunt Gmail parsing must point at the personal inbox |
| Google Drive | Backups, comic deliveries, Sheets | Personal Drive |
| Google Calendar | Interviews | Personal |
| Mobbin | UI references | Optional |
| Claude in Chrome | Driving her real browser | Install the extension |
| Granola | Meeting notes | Was the Fi account; skip unless she signs up personally |

Slack (epifi.slack.com) is gone with the company. Not needed.

## 6. Desktop app settings she likes

- Remote Control ON for new sessions; keep computer awake while Claude works (incl. battery).
- Theme dark. Push notifications for agents ON.
- Permission mode: auto mode was used for most work.

## 7. Raw backups outside git

See `archive/README.md` for where the comic videos, frames and conversation exports were put.
