---
name: web-of-belief
description: Build and maintain a local Web of Belief knowledge base of concepts, claims, evidence, cases, questions, and typed relationships. Use when organizing evolving understanding without treating inference as fact.
metadata:
  short-description: Maintain an evidence-aware belief web
---

# Web of Belief

Maintain a local, inspectable knowledge base rather than a single sprawling mind map. Its unit of change is a documented claim with a source, confidence level, and revision path.

## Start by locating the web

- If the user names a directory, use it. Otherwise look for `belief-web/` in the workspace root.
- If it does not exist, initialize it with `scripts/belief_web.py init <path>` after confirming the target when creating outside the current workspace.
- Read `INDEX.md`, `RELATIONS.md`, and only the notes relevant to the request before modifying anything.

## Model

Keep these distinct:

- **Node**: a reusable concept, actor, resource, rule, mechanism, role, or outcome.
- **Claim**: a falsifiable assertion that connects nodes. A node name alone is never evidence.
- **Evidence**: a source, observation, or record that supports, limits, or challenges a claim.
- **Case**: a bounded event or example; do not generalize it automatically.
- **Question**: an unresolved uncertainty or research task.
- **Relation**: a typed, directed connection between nodes, registered once in `RELATIONS.md`.

Use the schemas in [references/schema.md](references/schema.md) when creating or materially changing notes.

## Maintenance workflow

1. Capture the user's raw input in `INBOX.md` or create the appropriate note. Preserve exact wording for reported facts, quotations, and uncertainty.
2. Normalize duplicate terms, but retain aliases. Do not silently merge concepts with materially different meanings.
3. Create or update claims only when their scope, confidence, and support are explicit. Mark unsupported interpretations as `hypothesis` or turn them into questions.
4. Register only direct, named relations in `RELATIONS.md`; use a relation verb from the schema. Do not invent relationships merely because nodes appear related.
5. Run `python3 <skill-dir>/scripts/belief_web.py audit <web-path>` after structural changes, then run `sync` to refresh `MAP.md` when relations changed.
6. In the response, state what was added or revised, what evidence supports it, and which items remain unverified.

## Revision discipline

- New evidence should normally revise a case, evidence record, claim scope, confidence, or an edge near the perimeter before changing a core value or method.
- Never convert hearsay, a black-box “inside source,” a slogan, or one anecdote into a high-confidence claim.
- Preserve superseded claims with a `status: superseded` note and a link to the replacement; do not erase the reasoning trail unless the user asks to delete it.
- Do not represent people, groups, institutions, or allegations as facts without user-provided and attributable support.

## Operating modes

- **Initialize**: create the standard folders and empty register.
- **Capture**: turn pasted notes into inbox items, nodes, and questions without over-interpreting them.
- **Map**: add verified typed relations and refresh the Mermaid map.
- **Review**: audit links, missing evidence, stale review dates, duplicate candidates, and confidence mismatches.
- **Analyze**: trace a question across nodes, claims, and evidence; clearly distinguish source facts from your synthesis.

Use the script's help for commands. It uses only the standard Python library and does not make network calls.
