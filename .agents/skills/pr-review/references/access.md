# GitHub and Jira access

Use authenticated capabilities already available in the harness. Read an installed
tool's skill/help before unfamiliar operations. Tool preferences are adapters,
not prerequisites that make this agent specific to one harness.

## GitHub

Prefer the user's `gh-axi` skill and CLI when available. That skill uses
`npx -y gh-axi`; respect the harness's network/package execution permissions.
With an explicit repository, put `--repo owner/repo` **after** the command.

Examples with placeholders to replace from verified context:

```sh
npx -y gh-axi pr view <number> --repo <owner/repo>
npx -y gh-axi pr checks <number> --repo <owner/repo>
npx -y gh-axi pr --help
npx -y gh-axi api --help
```

If that wrapper is unavailable, use an authenticated GitHub connector, `gh`, or
the GitHub API with equivalent read capabilities. Discover supported flags rather
than inventing wrapper options. With `gh`, useful read operations are:

```sh
gh pr view <number> --repo <owner/repo> --json number,url,title,body,baseRefName,baseRefOid,headRefName,headRefOid,isCrossRepository
gh pr diff <number> --repo <owner/repo>
gh pr checks <number> --repo <owner/repo>
gh api --paginate repos/<owner>/<repo>/pulls/<number>/files
gh api --paginate repos/<owner>/<repo>/pulls/<number>/comments
```

Treat the selected base repository as the PR's identity, even for a fork PR.
Verify clone/fetch URLs from repository metadata; do not interpolate PR text into
shell commands. GitHub PR refs can provide a fork's head through the base repo.
Fetch the base and PR head into the isolated clone, verify the head against the
recorded SHA, find the merge base, and review that comparison. Do not use a
moving branch name as the only identity for a review.

Read checks and their reports, not just a green status badge. If GitHub uses a
synthetic merge commit in CI, verify which base/head combination produced it and
whether coverage can be mapped reliably to head source lines. Otherwise treat
the report as supporting evidence and run head checks separately.

## Jira

Prefer the user's `twg` and `twg-jira` skills when available. The read command is:

```sh
twg help describe 'jira workitem get'
twg jira workitem get <JIRA-123> --fields summary,description --output json --agent-fields @evidence
```

Use a configured site or one verified from the linked Jira URL. When multiple
sites could contain the same key, resolve the site before reading. Read the
description from full/evidence output if compact output omits it. Render Jira's
structured description sufficiently to retain lists, acceptance criteria, and
links relevant to the change.

If TWG is unavailable, use an authenticated Jira connector or configured Jira API
client with equivalent read access. Do not create credentials, install tools,
change authentication, or guess an organization's Jira hostname. If access fails,
report the specific gap and continue checks that do not depend on Jira.

## Research and source freshness

Prefer the host's web search/browser integration. Search using public technology
names, versions, and symptoms. Read the source before citing it. A web search
result title alone is not evidence. If browsing is unavailable, report that
limitation and use repository evidence without inventing citations.

Adapter references (check current help when operating):

- [GitHub CLI PR view](https://cli.github.com/manual/gh_pr_view)
- [GitHub CLI PR diff](https://cli.github.com/manual/gh_pr_diff)
- [GitHub REST pull requests](https://docs.github.com/en/rest/pulls/pulls)
- [GitHub pull request refs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/checking-out-pull-requests-locally)
