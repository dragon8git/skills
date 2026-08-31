---
name: prompt2specs
description: "Convert a natural-language product or engineering request into a reviewable specification with scope, acceptance criteria, constraints, and open questions. Use when the user asks to turn a prompt or requirement into a spec; do not implement code, choose an unrequested architecture, or split implementation tasks."
---

# Prompt2Specs

Turn an input request into a specification that states **what** must be achieved and **why**. Treat implementation choices as later planning work unless the user explicitly supplied them as constraints.

## Preserve Evidence

- Retain the original request in the output.
- Do not silently change requirements, resolve contradictions, or invent missing business rules.
- When a statement is unclear, record it under **Open Questions**. Ask the user only if it prevents a minimally useful specification.

## Separate Requirement Types

Classify information as:

- **Product requirement**: desired user or business outcome.
- **Acceptance criterion**: observable condition for considering the work complete.
- **Confirmed constraint**: a required platform, policy, compatibility target, deadline, or integration explicitly supplied by the user.
- **Deferred implementation decision**: a technical choice that is needed later but is not yet confirmed.
- **Out of scope**: an adjacent capability explicitly excluded or not supported by the source request.

Do not turn preferred technologies, database structures, API shapes, task estimates, or code designs into requirements unless the user stated them.

## Write the Specification

Use [references/spec-template.md](references/spec-template.md).

Make acceptance criteria specific enough to verify. Prefer user-visible or system-observable outcomes over implementation wording. Include failure or permission behavior only when the input establishes it or it is necessary to make a stated rule testable.

For each major requirement, add a short source note pointing to the relevant part of the original request.

## Completion Boundary

Deliver the specification for review. Do not write implementation code, create a technical plan, select a stack, or create task tickets unless the user explicitly asks for that next phase.
