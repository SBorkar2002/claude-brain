#!/usr/bin/env bash
# Restore Sejal's Claude Code setup from this repo onto a new Mac.
# Safe to re-run: existing files are backed up with a timestamp before being replaced.
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
STAMP="$(date +%Y%m%d-%H%M%S)"
CLAUDE_DIR="$HOME/.claude"
MEM_DIR="$CLAUDE_DIR/projects/$(echo "$HOME" | sed 's#[^A-Za-z0-9]#-#g')/memory"

say() { printf '\n==> %s\n' "$1"; }
backup() { [ -e "$1" ] && mv "$1" "$1.bak-$STAMP" && echo "   backed up $1" || true; }

say "Global rules → $CLAUDE_DIR/CLAUDE.md"
mkdir -p "$CLAUDE_DIR"
backup "$CLAUDE_DIR/CLAUDE.md"
cp "$REPO/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"

say "Memory → $MEM_DIR"
mkdir -p "$MEM_DIR"
cp -n "$REPO"/memory/*.md "$MEM_DIR/" || true
cp -Rn "$REPO/memory/_epifi" "$MEM_DIR/" 2>/dev/null || true
echo "   $(ls "$MEM_DIR" | wc -l | tr -d ' ') memory files in place (existing files were kept)"

say "Skills → $CLAUDE_DIR/skills"
mkdir -p "$CLAUDE_DIR/skills"
for s in "$REPO"/setup/skills/third-party/*/; do
  name="$(basename "$s")"
  [ -e "$CLAUDE_DIR/skills/$name" ] || cp -R "$s" "$CLAUDE_DIR/skills/$name"
done
echo "   $(ls "$CLAUDE_DIR/skills" | wc -l | tr -d ' ') skills installed"

say "Her studio plugin repo"
mkdir -p "$HOME/Documents/Github"
if [ ! -d "$HOME/Documents/Github/studio" ]; then
  gh repo clone SBorkar2002/studio "$HOME/Documents/Github/studio" || echo "   !! clone failed: run 'gh auth login' as SBorkar2002 and re-run"
fi

say "Plugins"
if command -v claude >/dev/null; then
  claude plugin marketplace add anthropics/claude-plugins-official || true
  claude plugin marketplace add pbakaus/impeccable || true
  claude plugin marketplace add Leonxlnx/taste-skill || true
  [ -d "$HOME/Documents/Github/studio" ] && claude plugin marketplace add "$HOME/Documents/Github/studio" || true
  for p in figma context7 code-simplifier chrome-devtools-mcp hookify claude-md-management playground serena; do
    claude plugin install "$p@claude-plugins-official" || true
  done
  claude plugin install impeccable@impeccable || true
  claude plugin install taste-skill@taste-skill || true
  claude plugin install studio@sejal-studio || true
  claude plugin install studio-board@sejal-studio || true
else
  echo "   claude CLI not found: npm i -g @anthropic-ai/claude-code, then re-run"
fi

say "Done. Manual steps left: see setup/README.md sections 4 to 6 (tools, connectors, app settings)."
echo "   Then open Claude Code from your home folder and say: read START-HERE.md in ~/Documents/Github/claude-brain"
