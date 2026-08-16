---
name: on-my-goal
description: Prepare a concise, verifiable implementation plan and acceptance checklist for `/goal` requests with an objective and completion criteria. Use when Codex must clarify a goal before implementation, turn vague completion criteria into testable evidence, and obtain user confirmation before starting work; do not create or execute the system `/goal` command.
---

# Goal Intake

Prepare the goal; do not begin implementation, edit files, create a system goal, or run destructive actions before the user confirms the resulting plan.

## Clarify only what matters

1. Read the stated objective and completion criteria. Preserve their intent; do not silently broaden them.
2. Identify only decisions that would materially change the solution, scope, acceptance evidence, or risk.
3. Ask one concise question at a time. Ask no more than five questions unless the user explicitly requests a different depth.
4. Do not repeat facts the user supplied. Make and disclose reasonable assumptions for non-critical details.
5. Stop asking as soon as the plan and acceptance evidence are determinate. If a critical decision cannot be safely assumed, ask for it instead of planning around a guess.

## Produce the confirmation package

After questions are resolved, respond in Chinese when the user writes Chinese. Keep the package concise and use exactly these sections:

### 1. Goal and plan

Restate the goal in one sentence. List the smallest ordered steps needed to deliver it. Every step must name both its tangible output and how it will be checked.

### 2. Acceptance checklist

Write checkable items with observable pass conditions and the intended verification evidence. Adapt the categories to the task; do not invent UI requirements for non-UI work. Consider the relevant items below:

- Completion deliverable and the stated completion criteria
- Core user or system flow
- Error, invalid-input, permission, retry, and boundary behavior
- Empty and loading states for data-fetching UI
- Device, viewport, platform, browser, or accessibility coverage for UI work
- Build, tests, runtime verification, data integrity, or document-render verification as appropriate

Mark an irrelevant category as `N/A` with a short reason. Mark a required check that cannot yet be performed as `blocked`, identify the dependency, and do not call it passed.

### 3. Assumptions and scope

List assumptions, explicit inclusions, and explicit exclusions. Separate user-confirmed facts from assumptions.

### 4. Unfinished work and risks

State what has not started, external dependencies, and any decision still needed. Do not disguise uncertainty as completion.

End with a direct request for confirmation. Do not start implementation until the user confirms.

## After confirmation

Treat the accepted checklist as the execution contract. Implement only the confirmed scope. Run the real project or task-appropriate validation, verify every applicable checklist item, and report the evidence plus all blocked or unverified items. Do not invoke or create the system `/goal` command; this skill only supplies the plan and acceptance contract.
