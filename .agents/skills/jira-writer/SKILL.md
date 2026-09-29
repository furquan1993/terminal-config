---
name: jira-writer
description: Draft and create Jira tickets (tasks, bugs, epics) from a discussion or rough input using fixed templates for the SW and OP projects. Use whenever the user asks to write, raise, file, open, or create a Jira, ticket, OPs Jira, bug, or epic, or to turn a conversation into Jira work. Drafts every ticket for review and creates only after explicit approval, using twg.
---

# Jira writer

Turn the current discussion and input into one or more Jira tickets on `concentricai.atlassian.net`. Each ticket follows a fixed template, is drafted for review, and is created with `twg` only after the user approves. Load the root `twg` skill and `twg-jira` for Jira safety rules. Use the command shapes in [project rules](references/project-rules.md); do not run CLI help on every invocation. Consult `twg help describe "<path>"` only when using a command not covered here, a flag fails, or the CLI contract has changed. Still read live Jira field metadata and values where needed.

**Agree on substance before drafting.** Templates and field defaults are fixed; do not ask the user how to structure a Jira. The user decides what each ticket says. Start with facts they supplied. You may carry over an unambiguous detail (such as the only named environment), but do not invent business impact, scope, dates, reproduction steps, or acceptance criteria. External evidence can help verify or suggest content, but identify its source and ask before including any new substantive claim.

## Workflow

1. **Extract outcomes and break down big work.** List the distinct outcomes the discussion wants, not the activities. Break larger work into multiple tickets, one per independently deliverable outcome. Group changes into a single ticket **only if they are related and belong to the same component or team**; related changes owned by different components or teams become separate tickets, each with its own component. Do not split one outcome into trivial activity tickets. A ticket that cannot state the result it delivers is not ready; fold it into another or ask. Apply the epic rule in [project rules](references/project-rules.md) when the breakdown produces several tickets.
2. **Classify each unit** using [project rules](references/project-rules.md):
   - Operations work on a running environment (run a script or job, change infra or config on a cluster, data fix, access, tenant setup) → **OP**, type **Task**.
   - Everything else → **SW**. Type **Bug** for defects, **Epic** only when the epic rule applies, otherwise **Task**.
3. **Resolve metadata** per project rules: component, existing labels, `cross-team`, priority, sprint, and parent epic. Read live values; never guess IDs, labels, or account IDs.
4. **Agree on content.** Before drafting, present a concise proposed breakdown (J1, J2, …). For each ticket, state the outcome, business reason, scope, and what would count as done **using the user's words**, and call out any obvious carry-over or proposed fact from a source. Ask: "Is this what you want each Jira to say? What would you change or leave out?" Ask focused follow-ups only for material gaps or mandatory information (for example, OP due date and justification or bug reproduction conditions); do not turn every template heading into a question. If the breakdown is wrong, revise it and confirm again. Wait for the user to confirm the substance before writing descriptions. Do not treat "whatever you think" as confirmation of an unstated claim.
5. **Check for duplicates.** Search existing tickets for each agreed outcome (`twg jira workitem search` / JQL, or `similar` where supported). Surface likely duplicates and ask whether to create or use an existing ticket; do not silently drop or create one.
6. **Draft** every ticket with [templates](references/templates.md), using only agreed content and obvious carry-overs disclosed in the content check. Rephrasing for clarity is fine; adding facts, promises, or acceptance criteria is not. Present all drafts together in the review format below. Do not create anything yet.
7. **Review loop.** Apply the user's edits and re-show only the changed drafts. Creation requires an explicit instruction such as "create all" or "create J1 and J3". "Looks good" alone is not approval; ask whether to create.
8. **Create** approved tickets in dependency order: epics first, then children with `--parent <EPIC_KEY>`. Write descriptions from a private temp file with `--description-format markdown`. Stop at the first failed create and report what was and was not created; never retry blindly into duplicates.
9. **Verify** each created ticket with one batched `twg jira workitem get` and check project, type, summary, component, labels, priority, sprint, parent, and assignee. Report a table of key, summary, and URL, plus any field that did not apply.

## Review format

Number drafts `J1`, `J2`, … and show for each:

```text
J1  [SW Task]  <summary>
Component: <name>        Labels: <existing labels>         Priority: <P>
Parent: <epic or J#>     Sprint: <none | DevOps Priority Queue>  Assignee: <auto: component lead | devops-jira-user>
Possible duplicates: <keys with one-line reason, or none found>
Words: <description word count>

<full description exactly as it will be written>
```

End with a short summary: the ticket count by project and type, any obvious carry-overs or sourced claims the user approved, and labels considered but not found.

## Writing rules

- **Business point of view first.** Every ticket opens with why it matters: who or what is affected (customers, tenants, scans, cost, reliability, team time), how much, and what happens if it is not done. A reader outside engineering should understand the first section.
- **Outcome driven.** The summary, first section, and acceptance criteria describe the result the business gets and how anyone can tell it happened, not the steps or code to get there. Test each acceptance criterion: could a PM or support engineer check it without reading code? If not, rewrite it.
- **Under 500 words** per description, counting every section. Check the count before presenting each draft. If a ticket needs more, cut background and implementation detail first, link to the source instead, or split it into separate outcomes.
- Describe the change as an outcome, not an implementation. Name the service or system affected, but leave the design detail to the assignee unless the discussion settled it and it changes scope or risk.
- **No code snippets** unless absolutely necessary, meaning the ticket cannot be executed or verified without them (for example, the exact query that identifies affected records). Prefer a link to the PR, file, script, or Jenkins job over pasting code, config, stack traces, or logs. Mention identifiers inline only when a reader needs them to find the thing.
- Plain, concrete language; short sentences. State evidence with numbers, names, times, and links rather than adjectives.
- Summaries: `<service or area>: <outcome>` for SW, `<environment>: <action>` for OP. Specific, about 80 characters or fewer, phrased as the result the business gets rather than the code change.
- Link related Jira keys, PRs, dashboards, Kibana or Argo evidence already in the discussion. Never include secrets, tokens, cookies, customer data excerpts, or raw curl output.
- Omit optional template sections that the user has no content for; never pad with filler. Mandatory sections must be filled with confirmed content before the draft is shown; if the user explicitly defers one, write `TBD: <what is missing>` there and list it in the summary.
- Do not use `--` as punctuation in ticket text.
