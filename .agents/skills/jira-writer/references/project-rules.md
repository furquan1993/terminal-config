# Project rules

Site: `concentricai.atlassian.net`. Reporter is the current user (`me`). Read live metadata before the first create of a session; the IDs below were verified on 2026-09-29 and are hints for recognising the right values, not substitutes for the live read.

## Defaults by project

| Field | OP (operations) | SW (all other work) |
| --- | --- | --- |
| Issue type | Task | Task; Bug for defects; Epic per the epic rule |
| Component | DevOps (id 10146, only OP component) | Best match from the live SW component list |
| Assignee | `devops-jira-user` (the DevOps component lead, so auto-assignment gives this; set it explicitly if auto-assignment does not) | Leave unset so the component lead is auto-assigned |
| Sprint | DevOps Priority Queue (sprint id 173, board 5) via `customfield_10020` | None (backlog) |
| Priority | Medium unless the discussion states urgency or impact that justifies another level | Same |
| Due date | Mandatory: agree on the date and business justification, write both in the description, and set Jira's `duedate` field to that same date. Do not create an OP ticket without both | None unless the user supplies one |
| Labels | Existing labels only (see Labels) | Existing labels only, plus `cross-team` when the component is not Platform |
| Parent | None | The epic, when the ticket belongs to an epic in the same draft or an existing epic named in the discussion |

## Choosing OP versus SW

OP is for an operation DevOps performs on a running environment: executing a script or Jenkins job, infrastructure or cluster configuration changes, data fixes, tenant or POV setup, access requests. If the discussion needs both an immediate operation and a permanent code fix, draft one OP Task for the operation and one SW ticket for the fix, and reference the SW draft in the OP ticket's *Can it be fixed via code changes?* section.

For a DevOps ask, the process page suggests cloning OP-557; for a new POV tenant, OP-505. The OP template already mirrors those mandatory fields, so create new tickets rather than cloning, unless the user asks to clone.

## Choosing the SW component

Read the live list with `twg jira space component query --key SW`. Match on the component description, which lists the services each component owns, not just the name. Known mappings from the descriptions:

- Platform: Aspirin, Pigeon (SOX), Autoscaler, Taskbroker, Data Services, Vault, Argo, init jobs, core infra (Kafka, ZooKeeper, and similar). The user leads Platform.
- DevOps: DevOps, SRE, operations, logging (ELK), monitoring (Prometheus, Grafana, Mimir).
- Data Application Layer (DAL): dbwriter, schema, db init, Query Engine.
- Activity - Data Freshness: unstructured data freshness, cloud activity, Delco.
- Connector: connectors, Transcriber. Knox: auth, Krawler, DIM. Onprem: proxy, Venti.

Use a component without asking only when the match is very obvious from its description. When two components fit, or none clearly fits, ask while agreeing on content and name the candidates; never create a component.

## Labels

- Use only labels that already exist. Check each candidate with a bounded JQL query (for example `labels = "reliability"` with a small limit); a label exists if at least one issue carries it. Prefer labels already common in SW, such as `customer`, `cicd`, `reliability`, `argo`, `cron`, `tech-debt`, `production`, `L1`, and customer-name labels.
- Never create a new label silently. If no existing label fits, leave labels empty and say "no suitable existing label" in the review summary. If a new label looks genuinely useful, propose it explicitly there, and apply it only if the user approves that specific label.
- Add `cross-team` to every SW ticket (including epics) whose component is not Platform. It may also be kept on a Platform epic whose children span other teams, if the discussion calls for it.
- The `cross-team` rule applies to SW. OP tickets are not labelled `cross-team` unless the user asks.

## Breaking down work

- Break larger work into multiple tickets, each delivering one outcome that can be completed, reviewed, and verified on its own.
- Keep changes in one ticket only when they are related **and** owned by the same component or team. Same outcome but different owners means one ticket per owner, linked through a shared epic or cross-referenced in *References*.
- Split by owner first, then by outcome within an owner. Never split purely by activity ("write code", "add tests", "deploy") within one outcome.
- A draft that exceeds 500 words or has acceptance criteria covering unrelated results is a sign the ticket should be split.
- Operations work and the code fix behind it are always separate tickets (OP and SW), as described above.

## Epic rule

Create an SW Epic only when the discussion produces three or more related tickets toward one outcome, or work that spans several teams or components. Otherwise create Tasks and Bugs without an epic. Child tickets link to the epic with `--parent <EPIC_KEY>`. The epic gets its own component and labels by the same rules.

## Fields and command shape

- Discover create metadata with `twg jira workitem field create-metadata --space <KEY> --type <Type>`. No custom field is required for OP Task, SW Task, SW Bug, or SW Epic as of the verification date; if that changes, ask the user for required values while agreeing on content.
- Create with `twg jira workitem create --space <KEY> --type <Task|Bug|Epic> --summary <text> --description <text> --description-format markdown`. Supported flags include `--assignee <account-id|me>`, `--reporter me`, `--priority <name>`, `--labels <comma-separated>`, `--parent <key>`, and repeatable `--field <id=value>` or `--fields-json <json>`. This command shape was checked with live `twg help describe "jira workitem create"` when the skill was written; do not re-run help on every invocation. Read help only if an option fails, the contract changes, or a new command is needed.
- Pass additional system and custom fields through `--field` or `--fields-json` using IDs from current field metadata (for example `customfield_10020` for Sprint). For the agreed OP due date, pass `--fields-json '{"duedate":"YYYY-MM-DD"}'` with the actual date, in addition to the description's Due date section. If other fields already use `--fields-json`, add `duedate` to that same JSON object. Do not also supply `duedate` through `--field`. If the date or business justification is missing, stop before creating the OP ticket. Resolve other value shapes from metadata or a verified existing issue, not a guessed format. Read the current component list and sprint before creating, and read back `duedate` to ensure it matches the agreed date.
- Fill *Customer Name* or *Tenant ID* only when the user supplied them and approved their inclusion.
- Descriptions: compose markdown in a private temp file outside the repository, supply its contents through `--description <text>` and set `--description-format markdown`. The CLI does not advertise a description-file flag. Do not use Jira wiki markup.
