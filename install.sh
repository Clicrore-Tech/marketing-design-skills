#!/usr/bin/env bash
# Install the marketing and design skills for every AI coding agent found on this machine.
#   ./install.sh            copy into each agent's skills folder that exists
#   ./install.sh --link     symlink instead of copy (updates with git pull)
#   ./install.sh --claude   only Claude Code
set -euo pipefail
cd "$(dirname "$0")"
MODE=copy; ONLY=""
for a in "$@"; do case "$a" in --link) MODE=link;; --claude) ONLY=claude;; esac; done

targets=("$HOME/.claude/skills")
if [ -z "$ONLY" ]; then
  [ -d "$HOME/.agents" ] && targets+=("$HOME/.agents/skills")   # Codex and other Agent Skills hosts
  [ -d "$HOME/.codex" ] && targets+=("$HOME/.codex/skills")
  [ -d "$HOME/.gemini" ] && targets+=("$HOME/.gemini/skills")
  [ -d "$HOME/.hermes" ] && targets+=("$HOME/.hermes/skills")
fi

for t in "${targets[@]}"; do
  mkdir -p "$t"
  for s in skills/*/; do
    name=$(basename "$s"); dest="$t/$name"
    rm -rf "$dest"
    if [ "$MODE" = link ]; then ln -s "$PWD/$s" "$dest"; else cp -R "$s" "$dest"; fi
  done
  echo "Installed to $t"
done

mkdir -p "$HOME/.marketing-skills/brands" "$HOME/.marketing-skills/clients"
echo "Memory folder ready at ~/.marketing-skills"

if command -v npm >/dev/null 2>&1; then
  echo "Setting up the infographic renderer (Playwright and Chromium)..."
  for t in "${targets[@]}"; do
    d="$t/infographic-studio"
    [ -L "$d" ] && d=$(cd "$d" && pwd -P)
    (cd "$d" && npm install --silent && npx --yes playwright install chromium >/dev/null) && break
  done
else
  echo "Node.js not found. Install it from nodejs.org to render infographics to PNG."
fi
echo "Done. Restart your AI tool, then try: /social-growth-engine plan my week"
