---
name: prompt2specs
description: "Extract reusable development rules from a user's request into the project's AGENTS.md, then implement and verify the current request. Use when the user wants one-time prompts to become lasting project conventions while getting the requested work done. Do not turn one-off operations into permanent rules."
---

# Prompt2Specs

Turn a request into completed work and, where justified, a few lasting development rules in `AGENTS.md`. Extract rules selectively: completing the request does not depend on finding a rule to save.

## Distinguish Rules from Actions

Read the request, applicable `AGENTS.md` files, and the relevant project code. Separate:

- **Durable rules:** user-supported preferences or constraints that guide future changes beyond this task, such as import placement, naming patterns, or repeated validation requirements.
- **Current actions:** concrete edits needed now, such as renaming a file, correcting text, or fixing a particular bug.

Persist a rule only when its future applicability and scope follow from the user's request. Do not promote an implementation choice, isolated example, or temporary workaround into project policy. When no reusable rule is supported, leave `AGENTS.md` unchanged and complete the task.

Examples:

- “Put all imports at the top; rename demo.py to agent.py”: record the import-placement rule and perform both edits. Do not infer that the entry point must permanently be named `agent.py`.
- “Rename this file”: perform the rename and update affected references; no new rule is needed.
- “From now on, name test files test_*.py”: record the naming convention and apply it within the requested scope.

## Maintain AGENTS.md Concisely

- Use the project's `AGENTS.md`, or the applicable directory-level file when the rule is local to a component. Do not write project rules into global user configuration.
- Merge rules into the relevant existing section, matching its language and style. Prefer one short, actionable sentence per rule; include scope or rationale only when needed to avoid misapplication.
- Deduplicate equivalent rules. Update a rule when the user clearly supersedes it; clarify material conflicts only when intent cannot be resolved from the request.
- Preserve unrelated guidance. Create a minimal `AGENTS.md` only if a supported durable rule needs a home.
- Do not append raw prompts, task history, implementation plans, acceptance checklists, or completion reports. Generate standalone specifications or tickets only when explicitly requested.

## Implement the Current Request

Apply the requested changes in the same task, including necessary reference and documentation updates. Keep the work scoped to the request; saving a rule does not authorize unrelated repository-wide cleanup.

Do not stop after writing rules or introduce a separate implementation-approval step for already authorized work. Honor an explicit documentation-only or no-execution request and existing permission boundaries. If an action is blocked, complete independent authorized work and state what remains blocked; do not treat a rule entry as completed implementation.

## Verify and Report

Run the project's checks appropriate to the changes. Review the resulting rules for brevity, duplication, scope, and accidental generalization of one-off actions.

Report briefly: which lasting rules were added or updated (or that none were warranted), what was implemented, and what verification passed or remains incomplete.
