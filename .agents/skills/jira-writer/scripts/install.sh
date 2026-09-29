#!/bin/sh
# Install the shared jira-writer skill for Claude, Antigravity, OpenCode, Codex, and Pi.
set -eu

if [ "$#" -ne 0 ]; then
  printf 'Usage: sh .agents/skills/jira-writer/scripts/install.sh\n' >&2
  exit 2
fi

source_dir=$(CDPATH= cd "$(dirname "$0")/.." && pwd -P)
if [ ! -f "$source_dir/SKILL.md" ]; then
  printf 'error: SKILL.md not found in %s\n' "$source_dir" >&2
  exit 1
fi

# Preflight every destination and its ancestors before making changes, so a
# conflicting parent path cannot leave a partially installed skill.
check_destination() {
  dest=$1
  parent=$(dirname "$dest")
  while [ "$parent" != / ]; do
    if { [ -e "$parent" ] || [ -L "$parent" ]; } && [ ! -d "$parent" ]; then
      printf 'error: %s is not a directory\n' "$parent" >&2
      exit 1
    fi
    parent=$(dirname "$parent")
  done
  if [ -L "$dest" ] && [ -d "$dest" ] &&
    [ "$(CDPATH= cd "$dest" && pwd -P)" = "$source_dir" ]; then
    return 0
  fi
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    printf 'error: %s already exists and does not point to %s\n' "$dest" "$source_dir" >&2
    exit 1
  fi
}

install_destination() {
  dest=$1
  if [ -L "$dest" ]; then
    printf 'already installed: %s\n' "$dest"
    return
  fi
  mkdir -p "$(dirname "$dest")"
  ln -s "$source_dir" "$dest"
  printf 'installed: %s\n' "$dest"
}

for dest in \
  "$HOME/.agents/skills/jira-writer" \
  "$HOME/.claude/skills/jira-writer" \
  "$HOME/.gemini/config/skills/jira-writer" \
  "$HOME/.gemini/antigravity-cli/skills/jira-writer" \
  "$HOME/.config/opencode/skills/jira-writer" \
  "$HOME/.pi/agent/skills/jira-writer"
do
  check_destination "$dest"
done

for dest in \
  "$HOME/.agents/skills/jira-writer" \
  "$HOME/.claude/skills/jira-writer" \
  "$HOME/.gemini/config/skills/jira-writer" \
  "$HOME/.gemini/antigravity-cli/skills/jira-writer" \
  "$HOME/.config/opencode/skills/jira-writer" \
  "$HOME/.pi/agent/skills/jira-writer"
do
  install_destination "$dest"
done

printf 'Start a new agent session (or reload skills) to discover jira-writer.\n'
