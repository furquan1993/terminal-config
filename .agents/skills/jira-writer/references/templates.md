# Ticket templates

Use the template for the ticket's project and type. Headings are written as markdown `###` headings in the description. Keep the heading names exactly as shown so tickets read consistently. Omit a section marked *optional* when the user has no content for it; never omit a mandatory section. Use the substance agreed during the content conversation in `SKILL.md`. Do not turn headings into a questionnaire or add plausible details just to fill them. Ask for mandatory missing information; write `TBD: <what is missing>` only when the user explicitly defers it.

Every template starts from the business point of view and is outcome driven. The first section must make sense to a product manager or support engineer. Technical detail comes later and stays at the level of services, behaviour, and outcomes. Link to code, PRs, logs, and dashboards instead of pasting them.

Keep each description **under 500 words** in total. Aim for a few sentences per section and a handful of acceptance criteria.

## SW Task

Summary: `<service or area>: <outcome>`

```markdown
### Why this matters
Who or what is affected and how much: customers, tenants, scans, cost, reliability, or team time. What happens if we do not do this. Link the ticket, incident, customer request, or discussion that triggered it.

### What's wrong today
Current behaviour or gap, with concrete evidence (counts, dates, environments, examples).

### Outcome
The end state once this is done, stated as a result (for example "Spark jobs on customers-oregon no longer lose work when Spot nodes are reclaimed"), and the services or systems involved. Include design decisions only when the discussion settled them and they affect scope or risk.

### Acceptance criteria
- Observable results that prove the outcome, phrased so someone outside the team can verify them. Avoid criteria that only restate implementation steps.

### Out of scope            (optional)
- What this ticket deliberately does not cover, when the discussion drew that line.

### References              (optional)
- Related Jira keys, PRs, design docs, dashboards, Kibana or Argo links.
```

## SW Bug

Summary: `<service or area>: <user-visible symptom>`

```markdown
### Impact
Who is affected, how badly, and how often: customers or tenants, features, data correctness, frequency. Whether a workaround exists.

### Environment
Cluster, tenant, product version or release, and where it was seen.

### Steps to reproduce
1. Numbered steps a tester can follow from a known starting state.

### Expected result
What should happen.

### Actual result
What happens instead, with evidence linked rather than pasted.

### Workaround              (optional)
Temporary mitigation already in place or available.

### References              (optional)
- Related Jira keys, incidents, PRs, dashboards, Kibana or Argo links.
```

**Steps to reproduce is mandatory.** If the user has not given reproducible steps, ask for them during content agreement; never write steps the user has not confirmed. If the bug is intermittent and cannot be reproduced on demand, say so and give the conditions under which it has been observed instead.

Leave the SW Bug RCA custom fields (such as *Was this a code regression?* and *Why wasn't it caught by QA?*) empty; they are filled when the bug is analysed.

## SW Epic

Summary: the business outcome, not an activity (for example "Scans recover automatically after Spot interruptions", not "Autoscaler work").

```markdown
### Goal
The business outcome in one or two sentences and who benefits.

### Why now
What triggered this: incident, customer commitment, cost, roadmap item. Include the evidence.

### Scope
- One line per child ticket (J# in the draft, keys after creation).

### Success criteria
- Measurable results that show the epic is done.

### Teams involved           (optional)
Components or teams whose work is included, and dependencies between them.

### Out of scope            (optional)
- Related work deliberately excluded.
```

After creating the children, update the epic's Scope list with the real keys only if the user approved that edit as part of the draft.

## OP Task

Summary: `<environment>: <action>` (for example `customers-oregon: Move Spark workers to memory-optimised nodes`).

This template follows the mandatory fields in [Process to create Operations Jira](https://concentricai.atlassian.net/wiki/spaces/CD/pages/80707586/Process+to+create+Operations+Jira). Keep the headings as below so DevOps can review against that page.

```markdown
### Business impact
The result this operation delivers, why it is needed, and the business impact of doing or not doing it: customers or tenants affected, risk, cost, deadlines.

### Environment
Every environment this applies to (for example poc-2, customers-2, customers-oregon).

### Can it be fixed via code changes?
Yes: why a hotfix or waiting for the next upgrade is not acceptable.
No: the long-term permanent fix that prevents this from recurring, with its SW ticket if one exists or is part of this draft.

### Steps to be executed
The operation in order. Any manual execution on production must run through a Jenkinsfile or a script that is already in the deployed service image, for audit. Link the Jenkins job or script rather than pasting it.

### Validation steps
How DevOps confirms the operation worked, ideally built into the same job or script.

### Due date
The date and its business justification.
```

OP constraints to respect in the content:

- Do not ask DevOps to share curl output in the ticket; results are shared over screen share.
- Do not ask for port-forwarding from FedRAMP environments to a local machine; only CLI access to Mongo, Elasticsearch, and Kibana is allowed there.
- Access requests are exempt from the Jenkinsfile requirement; state the access needed, for whom, and for how long instead.
