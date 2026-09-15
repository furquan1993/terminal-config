# terminal-config
My terminal config for any terminal

## PR Review Agent

The [PR Review Agent](.agents/skills/pr-review/SKILL.md) reviews GitHub PRs in
Claude Code, OpenCode, Codex, and other harnesses that support Agent Skills.
It checks formatting, meaningful and consistent names, cyclomatic complexity
(at most 13 per method), unit coverage (at least 80% of added executable lines),
PR/Jira intent, functional correctness, infrastructure usage, and Gradle practices.

It presents the exact proposed line comments for discussion before any GitHub
write. Choose which comments to publish, edit, or skip. Critical existing issues
stay separate as possible Jira follow-ups. Dedicated security and performance
reviews are outside this agent's scope.

### Shared files

```text
AGENTS.md                             Shared routing instructions
CLAUDE.md -> AGENTS.md                Claude-compatible instruction link
.agents/skills/pr-review/             Single skill implementation
.claude/skills/pr-review              Symlink to ../../.agents/skills/pr-review
.opencode/commands/pr-review.md       Thin /pr-review command adapter
```

Edit the open-standard `AGENTS.md` and `.agents/skills/pr-review/` sources.
Claude uses symlinks to the same files. The OpenCode command only loads the skill;
it does not contain another review policy. Preserve symlinks when cloning the
repository. On Windows, Git symlink support requires the appropriate system
permissions/configuration.

### Install across repositories

Keep this checkout at a stable location. From its root, link the skill into the
shared global directory and add the Claude-compatible link:

```sh
mkdir -p "$HOME/.agents/skills" "$HOME/.claude/skills"
ln -s "$PWD/.agents/skills/pr-review" "$HOME/.agents/skills/pr-review"
ln -s ../../.agents/skills/pr-review "$HOME/.claude/skills/pr-review"
```

These commands do not replace existing paths. If the agent is already installed,
compare the existing skill with this version before replacing its path with a
link. Keep any local customizations you want to retain.

OpenCode and Codex discover the shared global skill directory. For OpenCode's
explicit `/pr-review` command, also link the adapter:

```sh
mkdir -p "$HOME/.config/opencode/commands"
ln -s "$PWD/.opencode/commands/pr-review.md" "$HOME/.config/opencode/commands/pr-review.md"
```

For automatic routing in every repository, use the instructions in `AGENTS.md`
as your personal global rules. If you have no existing personal instruction
files, you can link this single source into each harness:

```sh
mkdir -p "$HOME/.claude" "$HOME/.codex" "$HOME/.config/opencode"
ln -s "$PWD/AGENTS.md" "$HOME/.claude/CLAUDE.md"
ln -s "$PWD/AGENTS.md" "$HOME/.codex/AGENTS.md"
ln -s "$PWD/AGENTS.md" "$HOME/.config/opencode/AGENTS.md"
```

If personal instruction files already exist, preserve their contents and add the
marked PR-review routing block instead. Preserve inherited Claude instructions
if creating an OpenCode global instruction file. Start a new session after
changing global routing. Another harness can load the same `SKILL.md` and linked
references from its own global configuration.

### Invoke and discuss

- In a repository: `Review PR #123.`
- Anywhere: `Review https://github.com/OWNER/REPO/pull/123.`
- Claude Code or OpenCode with the adapter: `/pr-review 123`
- Codex: `Use $pr-review to review PR #123.`

After the draft, say for example: `Publish C1 and C3; skip C2.` The agent checks
the current PR revision and publishes only the approved selection.

The host supplies GitHub/Jira authentication, web research, and permitted local
execution. The skill prefers `gh-axi` and `twg` when available and supports
equivalent authenticated tools. It uses current CI evidence or an isolated
checkout for checks; unavailable evidence is reported as unverified.

### References and validation

The layout follows [Agent Skills](https://agentskills.io/specification),
[Claude Code skills](https://code.claude.com/docs/en/skills),
[OpenCode skills](https://opencode.ai/docs/skills/), and
[Codex skills](https://learn.chatgpt.com/docs/build-skills).
Global routing follows [Claude Code memory](https://code.claude.com/docs/en/memory)
and [OpenCode rules](https://opencode.ai/docs/rules/).

Validate the skill's frontmatter, linked references, and symlinks when editing.
Review quality and repository-specific tool behavior still need validation on
real PRs; installing this configuration does not run or publish a PR review.
