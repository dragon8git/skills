# Web of Belief schema

## Files

```text
belief-web/
├── INDEX.md
├── INBOX.md
├── RELATIONS.md
├── MAP.md
├── nodes/
├── claims/
├── evidence/
├── cases/
└── questions/
```

## Frontmatter

Use plain YAML scalars and comma-separated lists so the bundled audit script can read it without dependencies.

### Node

```md
---
type: node
category: resource
aliases: distribution, access
status: active
last_reviewed: 2026-08-21
---

# 渠道

## Definition

## Boundaries

## Related claims
```

Allowed categories: `actor`, `resource`, `rule`, `mechanism`, `role`, `outcome`, `concept`.

### Claim

```md
---
type: claim
status: hypothesis
confidence: low
scope: Specify the setting, population, and conditions.
evidence: ../evidence/source-or-observation.md
last_reviewed: 2026-08-21
---

# Claim title

## Statement

## Rationale

## Counterevidence / limits
```

Allowed status values: `hypothesis`, `active`, `challenged`, `superseded`. Confidence: `low`, `medium`, `high`.

### Evidence or case

Use `type: evidence` or `type: case`. Record origin, date, relevant quotation or observation, and limitations. For unverified reports, say so in both the title and body.

### Question

Use `type: question`, an explicit question, why it matters, and what would answer it.

## Relations register

`RELATIONS.md` owns every node-to-node edge. Keep one relation per row:

```md
| From | Relation | To | Confidence | Support | Notes |
| --- | --- | --- | --- | --- | --- |
| 渠道 | influences | 定价 | low | | Hypothesis; requires a scoped claim. |
```

Allowed relation verbs: `enables`, `constrains`, `influences`, `depends_on`, `governs`, `legitimizes`, `filters`, `transmits`, `incentivizes`, `competes_with`, `serves`.

The relation is not a claim replacement. Any non-obvious or consequential edge should link to a claim or evidence in `Support`.
