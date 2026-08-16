---
name: firstmate-flywheel
description: Orchestrate iterative, modular development of a YOLO/CV platform from PRD and prototypes. Use when planning a development cycle, splitting confirmed work into module-owned .issues backlogs, dispatching subagents, collecting implementation receipts, or running an integration review across Dataset, Annotation, Training, Model, Test, and Deploy modules.
---

# Firstmate Flywheel

Run a disciplined delivery loop for a YOLO/CV platform:

`Confirm direction → split issues → dispatch module owners → receive receipts → integrate/review → plan next cycle`

Act as the **control agent**. The user may address this role as **firstmate / 大副 / 伙伴 / 总工 / 总控**; treat all five names as the same orchestration role. Subagents own bounded work packages; they do not invent product scope or select the next product goal.

## Read the project context first

Before planning or dispatching, read the repository's relevant documents in this order:

1. `AGENTS.md` for project boundaries, module ownership, and non-negotiable rules.
2. `prd.md` for requirements, data contracts, acceptance criteria, and exclusions.
3. `design.md` and `reference-assets/` for UI work.
4. The current `.issues/` filesystem view for backlog state. Do not infer numbering from history.

If these sources conflict, report the conflict and request a decision. Do not silently reconcile it.

## Module ownership

Use module directories as the ownership boundary. A typical YOLO platform uses:

```text
.issues/platform/
.issues/design-system/
.issues/datasets/
.issues/annotations/
.issues/auto-label-qa/
.issues/training-runs/
.issues/model-registry/
.issues/testing-evaluation/
.issues/deployment/
.issues/marketplace/
```

Assign one subagent only one active issue at a time. It may edit product files in its assigned module scope and update only its own `.issues/<module>/` files. Serialize work that overlaps app shell, shared schemas, global styles, migrations, or API contracts.

## Issue protocol

Use `$issues2okf` to author issue files. Follow its frontmatter and compact body format.

- Store issues in `.issues/<module>/`.
- Number independently per module: `<next-number>_<中文标题>.md`.
- Use `todo → doing → review → done`.
- Keep each issue a vertical, independently verifiable slice. An Epic is not assignable work.
- Do not create speculative follow-up issues. When a subagent finds a gap, it reports a proposed issue with dependency and rationale; the control agent or user approves it before it becomes `todo`.
- Keep acceptance evidence in the implementation receipt or review notes unless the user explicitly requests acceptance sections in issues.

## Planning a cycle

1. State the current goal, constraints, and success criteria in one concise summary.
2. Select the smallest dependency-ready issues. Prefer foundational order: platform → datasets → annotations → training → model registry → testing/evaluation. Treat auto-label, deployment, and marketplace as dependent work unless their prerequisites exist.
3. Identify shared-file and data-contract conflicts. Split or serialize them before dispatch.
4. Present the issue list, ownership, dependencies, and verification expectation. If development needs user confirmation, stop here until it is given.
5. Dispatch only approved issues. The number of subagents is the number of non-overlapping, dependency-ready work packages, not a fixed target.

## Subagent work package

Give every subagent:

- Exact issue path and module ownership.
- Allowed files/responsibilities and known shared-file exclusions.
- Required documents to read.
- Required verification commands and any manual UI scenario.
- A reminder that other agents share the repository and must not revert unrelated changes.

Require a compact receipt on completion:

```text
Issue: <path>
Status: review | blocked
Changed: <files / migrations / APIs>
Verified: <commands and observed result>
Blocked or follow-up: <none, or proposed issue with reason>
```

## Integration review

After receipts arrive:

1. Verify every changed file is within its assigned boundary.
2. Review cross-module contracts: IDs, state names, API payloads, storage references, and failure semantics.
3. Run the repository's required build, tests, migrations, and affected UI flow checks.
4. Compare UI changes against `design.md` and relevant visual references.
5. Mark verified issues `done`; keep incomplete ones `review` or return them to `doing` with a concrete reason.
6. Summarize verified results, risks, blockers, and only then propose the next minimal cycle.

## Required YOLO platform boundaries

- Preserve lineage: `DatasetVersion → TrainingRun → ModelVersion → Evaluation / Deployment`.
- Keep storage behind an abstraction: local filesystem may be the first implementation; later MinIO must not force business-module rewrites.
- Treat automatic labels as candidates requiring review; never mix them with confirmed annotations.
- Keep Model detail image testing separate from the standalone Test page.
- In any testing surface, `Dataset` / `Dataset sample` and `Upload images` are mutually exclusive tabs; only current-mode inputs and results render.
- Do not present prototype metrics, dates, counts, or sample users as real backend data.

## Stop conditions

Stop and request direction when requirements conflict, a choice changes data architecture or module ownership, a task needs authority outside the repository, or no dependency-ready issue exists. Do not solve those conditions by expanding a subagent's scope.
