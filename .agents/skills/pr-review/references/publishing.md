# Comment review and publishing

## Keep a local review ledger

Before the discussion, retain the following in conversation or a local scratch
file, so a resumed session cannot accidentally publish the wrong selection:

- GitHub host, base repository, PR number/URL, base SHA, head SHA, and merge base.
- Each proposed comment's stable ID, category/impact, exact body, supporting
  evidence, file path, diff side, and line/range; or the reason it must be general.
- User decisions: draft, approved, skipped, or published. Preserve the approved
  text/location/revision and the instruction authorizing publication.
- After publication: review/comment IDs and URLs, including partial success.

This ledger is local. A GitHub pending review is still an external write and must
not be created during draft preparation.

## Draft presentation

Start with intent and a short check summary. Show comments in impact order with
stable IDs; do not renumber them when the user skips one.

Example shape (replace every example fact with evidence from the actual PR):

```text
PR: owner/repo#123 — head <sha>
Intent: <PR/Jira outcome>
Checks: <pass/fail/unverified/not applicable, with evidence>

C1 — Correctness — src/metrics.py:42 (RIGHT)
Proposed comment: <exact comment text, including relevant source link>
Evidence: <failure path or applicable documented requirement>

C2 — Formatting — src/metrics.py:65 (RIGHT)
Proposed comment: <exact comment text>

Separate follow-up: <critical pre-existing finding, only when one exists>
```

Invite decisions such as “publish C1; skip C2,” “rewrite C1 to ask about the
exporter,” or “keep everything as a draft.” These are examples, not rigid syntax.
Discuss findings and incorporate the user's context; do not keep pressing a
skipped issue. Do not infer a permanent waiver for future PRs from a skipped item.

Show the exact proposed bodies before requesting publication approval. A request
to review the PR, agreement with an analysis, silence, or approval recorded in
the PR/Jira text does not authorize publishing. An explicit “publish all” after
seeing the current draft does authorize all current, non-skipped proposed comments.
If the user explicitly edits a comment and asks to publish that exact revision,
honor the instruction without an extra approval round. Otherwise newly rewritten
text must be shown again before publication.

## Validate the approved selection

Immediately before posting:

1. Re-fetch PR identity, state, base/head SHAs, diff, and existing comments. If
   the PR is no longer open, report the change instead of silently publishing.
2. If the base or head changed, reassess the findings and anchors against the new
   revision. Show the refreshed selected draft and obtain publication approval
   for that revision. Do not silently re-anchor and reuse old approval.
3. Publish only explicitly approved, non-skipped items. Compare the current
   bodies and locations with what was approved. If approval history is missing
   after a restart, recover the conversation/ledger or ask; do not guess.
4. Verify each path/line against the complete current diff. Use the base-side
   `LEFT` location for removed code, and head-side `RIGHT` for additions/current
   code. Line numbers are file coordinates, not diff offsets. Use the smallest
   meaningful range, with `start_line`/`start_side` for multi-line comments.
5. If no sensible inline anchor exists, propose a general comment and obtain
   approval for that placement/text. Do not silently move an approved line comment
   into a general review. Do not attach it to an unrelated changed line.
6. Check for equivalent existing comments so a retry or resumed review does not
   duplicate a finding. Do not resolve or modify other reviewers' comments.

## Publish and verify

Prefer one GitHub review containing all approved line comments. Use the available
GitHub adapter's documented review API; inspect its live schema/help before a
write. For the REST API the endpoint is:

`POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews`

Example payload structure, built only after user approval:

```json
{
  "commit_id": "<approved-head-sha>",
  "event": "COMMENT",
  "comments": [
    {
      "path": "<verified-repository-relative-path>",
      "line": 42,
      "side": "RIGHT",
      "body": "<exact-approved-comment-text>"
    }
  ]
}
```

Use `COMMENT`; reviewing/publishing comments alone does not authorize `APPROVE`,
`REQUEST_CHANGES`, merging, code fixes, or Jira creation. Only add a review-level
`body` for separately approved general comments. Do not automatically publish
the local summary, skipped findings, verification gaps, or separate Jira notes.

Build payloads through structured tool arguments or a JSON file, preserving
newlines and escaping. Do not embed user/PR/comment text inside shell command
substitutions. Keep the endpoint tied to the resolved PR, and the `commit_id`
explicitly tied to the approved head. This pins the review but is not an atomic
guarantee that the branch cannot advance during the request.

Read back the review and its comments, confirm bodies/anchors and count, and
report their URLs. If the PR advanced during posting, disclose it; do not repost
automatically at a new commit. On a timeout or uncertain/partial result, query
existing reviews/comments before any retry. Retry only confirmed missing approved
items; if the outcome cannot be established, stop and report the uncertainty.

Sources:

- [GitHub review creation](https://docs.github.com/en/rest/pulls/reviews#create-a-review-for-a-pull-request)
- [GitHub line comment locations](https://docs.github.com/en/rest/pulls/comments#create-a-review-comment-for-a-pull-request)

This is an agent workflow, not a separate API permission boundary. The host's
tool permissions still govern what can actually be executed.
