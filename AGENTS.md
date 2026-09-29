<!-- BEGIN pr-review routing -->
## Personal PR review workflow

Whenever I ask to review a GitHub PR/pull request by number or URL, load and follow
the `pr-review` skill before reviewing. Use the same skill when I continue the
discussion or ask to publish that review. If native skill loading is unavailable,
read `~/.agents/skills/pr-review/SKILL.md` and its applicable linked references.
Show me the proposed comment summary and exact line comments first. Publish only
the comments I select and authorize after reviewing them with you.
<!-- END pr-review routing -->

<!-- BEGIN argo-cli routing -->
## Argo CLI workflow

Whenever an Argo Workflows CLI interaction is needed, load and follow the
`argo-cli` skill before running commands. This includes installation, connection
setup, token discovery, inspection, and lifecycle operations. If native skill
loading is unavailable, read `.agents/skills/argo-cli/SKILL.md` in this repository
or `~/.agents/skills/argo-cli/SKILL.md` for the global installation.
<!-- END argo-cli routing -->

<!-- BEGIN kibana-logs routing -->
## Kibana logs workflow

For Kibana log queries through curl, index-pattern discovery, or Kibana cookie
refresh, load the `kibana-logs` skill. If native loading is unavailable, read
`.agents/skills/kibana-logs/SKILL.md` or the global
`~/.agents/skills/kibana-logs/SKILL.md`. Resolve cluster patterns from data views,
ask for unspecified time ranges, and keep session cookies out of chat and Git.
<!-- END kibana-logs routing -->

<!-- BEGIN jira-writer routing -->
## Jira writing workflow

Whenever I ask to write, raise, file, or create a Jira, ticket, OPs Jira, bug, or
epic, or to turn a discussion into Jira work, load and follow the `jira-writer`
skill. If native loading is unavailable, read `.agents/skills/jira-writer/SKILL.md`
or the global `~/.agents/skills/jira-writer/SKILL.md`. Use its fixed templates, but
agree with me on the substance of each ticket before drafting; use only very obvious carry-overs without asking.
Show all drafts and create only the tickets I explicitly approve.
<!-- END jira-writer routing -->
