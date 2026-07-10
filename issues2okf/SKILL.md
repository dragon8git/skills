---
name: issues2okf
description: Convert user-provided requirements, bug reports, annotated images, or development requests into one or more standardized `.issues/*.md` TODO files only. This skill records work items and must not implement fixes, edit product code, run builds, or perform verification beyond writing the issue documents themselves.
---

# Issues to OKF

## Hard Boundary

This skill is issue-authoring only.

When this skill is invoked, you must stop after creating the required `.issues/*.md` files and optional `.issues/.markmap/*.md` files.

You must not:

- implement the requested feature or bug fix
- edit application, library, config, test, or documentation files outside `.issues/` and `.issues/.markmap/`
- run build, compile, test, lint, preview, or browser verification steps for the requested product change
- diagnose code paths beyond what is minimally needed to write an accurate issue
- combine issue creation with a development pass in the same turn unless the user explicitly asks for a separate implementation step after the issue is created

If the user only invokes `$issues2okf`, the correct completion condition is:

1. create the issue file(s)
2. optionally create the markmap file(s) only when explicitly requested
3. report the created file path(s)

Do not continue into implementation on your own.

## Role

Act as a strong product manager, requirement analyst, and solution architect.

Do not mechanically dump the user's raw text into an issue file.

Your job is to preserve the user's real intent while rewriting it into a concise, structured, execution-ready issue document.

## Workflow

1. Treat this skill as direct requirement mode only:
   - convert the current user input into one or more new standardized `.issues/*.md` files
   - stop after writing the issue file(s); do not execute the requested development work
   - do not scan existing `.issues` notes for cleanup, normalization, or beautification
   - if the user wants historical `.issues` files rewritten, that is outside this skill's scope
2. Before writing any issue, decide whether the information is sufficient:
   - if the requirement is already clear enough to write an execution-ready issue, continue
   - if key facts are missing and would materially change the issue structure, split, or scope, ask concise clarification questions first and do not create the issue yet
   - ask only for information that affects goal, scope boundary, task split, dependency, or source of truth
   - prefer a small number of high-value questions; do not start an open-ended interview
   - when clarification is required, stop after asking; wait for the user's answer instead of drafting a speculative issue
3. First define the requirement before recording it:
   - identify the real problem being solved
   - distinguish goal, scope, constraints, and expected outcome
   - remove conversational noise, but do not change the user's meaning
4. Handle annotated-image-to-issue requests when the prompt contains intent such as `理解图片`, `image2issue`, `label2issue`, `理解标注`, `理解万岁`, or `李姐万岁`, together with an image attachment, image path, or clearly identified visual reference:
   - inspect the image and treat explicit arrows, boxes, labels, strike-throughs, and nearby annotation text as requirement evidence
   - convert only legible, confirmed annotations into concise issue requirements; do not invent values, fields, interactions, or business rules from unmarked visual details
   - preserve the exact image path in the issue `links` or `备注` when a local path was supplied
   - use the surrounding screen only to identify the page/module and explain the annotation; do not treat every visible element as a requested change
   - combine annotations for one page and one coherent UI slice into one issue; split only when they cover independent pages or deliverables
   - if a label is unreadable or its requested change is materially ambiguous, ask a concise clarification question before creating the issue
   - when the trigger phrase appears without an accessible visual reference, follow the normal clarification gate instead of fabricating image findings
5. Before generating files, produce an internal planning pass for yourself:
   - summarize the core goal in one sentence
   - determine the minimum in-scope boundary
   - determine what is clearly out of scope
   - decide whether the request should stay as one issue or split into multiple issues
   - use this planning pass to improve issue clarity, but do not expose chain-of-thought or verbose internal reasoning
6. Split the request only when it naturally contains more than one independently executable task:
   - keep one issue when the work is one coherent slice
   - split into multiple issues when the request clearly contains separate pages, separate bugs, separate integrations, or separate deliverables
   - prefer the smallest useful split; do not create artificial subtasks
7. If the request is multi-part but still ambiguous, ask a brief split-confirmation question before generating files.
8. Create new `.md` files under `.issues/` with readable titles.
   - do not modify non-issue workspace files as part of this skill
9. Detect whether the user explicitly asks for a mind map before enabling the mind-map extension:
   - activate only when the prompt clearly contains intent such as `xmind`, `mind`, `思维导图`, `mindmap`, `markmap`, `Mermaid`, or an explicit request like `需求有点复杂，请创建思维导图`
   - do not create a mind map by default for ordinary issue requests
   - when activated, generate a Markmap markdown file at `.issues/.markmap/{same-name-as-issue}.md`
   - use the mind map to define the problem boundary: what to do, what not to do, and the scope edges that keep execution focused
10. Infer the smallest correct frontmatter values from the source note:
   - `status`: `todo`, `doing`, `review`, or `done` (default `todo`)
   - `type`: `dev`, `bug`, or the closest simple category
   - `title`: short human title
   - `description`: one-sentence summary
   - `links`: source URL or URLs
   - `tags`: short lowercase labels from the page, module, or topic
   - `timestamp`: `YYYY-MM-DD`
   - `markmap`: relative path like `.issues/.markmap/{name}.md` only when the explicit mind-map trigger matched
11. When information is sufficient and no clarification is needed, you may optionally show a brief pre-write summary before creating files:
   - `核心目标`
   - `范围边界`
   - `拆分决策`
   - keep it short and practical; this is a user-facing planning summary, not a long analysis
12. Write the issue body as a compact professional spec, not as raw chat transcript.
13. When the explicit mind-map trigger matched, also write a Markmap outline markdown file:
   - file path must match `.issues/.markmap/{same-name-as-issue}.md`
   - the outline must stay problem-first and boundary-first
   - use only these three top-level core nodes:
     - `核心目标`
     - `需求边界：做什么 (In Scope)`
     - `需求边界：不做什么 (Out of Scope)`
   - do not add other top-level nodes unless the user explicitly asked for them
   - each branch under the three core nodes should stay short, concrete, and boundary-oriented
   - avoid turning the mind map into endless brainstorming; its job is scope confirmation, not idea expansion
14. Preserve user-provided paths exactly when they are part of the requirement context:
   - local absolute file paths such as `/Users/lee/Pictures/example.png` must remain unchanged
   - do not shorten paths to basenames such as `example.png`
   - do not silently rewrite absolute paths into relative paths, URLs, or markdown links unless the user explicitly asked for that format
   - if a screenshot, prototype, workbook, or other local file path is important evidence, keep the original full path in `备注` or `links`

## Clarification Gate

Ask clarification questions before writing issue files when any of the following is true:

- the target page, module, scenario, or repo path is unclear
- the request mixes multiple possible deliverables and the split would change ownership or execution order
- the user's wording leaves key scope boundaries unresolved
- the source of truth is missing when the issue depends on a screenshot, prototype, workbook, API contract, or URL
- the issue would otherwise require inventing fields, APIs, page names, or business rules

Do not ask clarification questions when:

- the missing details are minor and do not change the issue's execution boundary
- a reasonable default can be recorded safely in `备注`
- the user clearly wants a fast first draft and the scope is already stable enough to implement later

When asking questions:

- ask at most 1-3 short questions
- ask only questions that unblock issue quality
- do not generate the `.issues/*.md` files in the same response
- do not ask for implementation details that belong to the later development phase

## Issue Body Format

Default to this structure unless the request is too small to justify every section:

```md
## 目标

- ...

## 范围

- ...

## 需求

1. ...
2. ...

## 备注

- ...
```

Body writing rules:

- `目标`: explain the business or product goal in 1-3 bullets
- `范围`: state the affected page, module, or scenario; keep scope explicit
- `需求`: list concrete implementation expectations, ordered for execution clarity
- `备注`: keep only essential constraints, dependencies, API notes, prototype references, or caveats
- do not generate sections such as `验收`, test methods, or testing requirement descriptions unless the user explicitly asks for them
- when the source prompt includes local file paths, preserve the exact original path strings verbatim in the most relevant section
- if a section has no real content, omit it instead of padding
- keep the whole body concise; structure is more important than volume

## Formatting Rules

- Only create new standardized issue files from the current user input.
- If key requirement information is missing, ask concise clarification questions first instead of drafting speculative issues.
- Treat successful issue-file creation as the end of the task unless the user explicitly asks for a separate next step.
- Write new `.md` files under `.issues/` instead of editing unrelated files.
- Do not edit source code, tests, configs, assets, or project docs outside `.issues/` and optional `.issues/.markmap/`.
- Do not run build, test, lint, preview, or runtime verification for the requested product change as part of this skill.
- Only create `.issues/.markmap/*.md` when the user explicitly asked for a mind map with the trigger words or equivalent direct intent.
- When creating a mind map, keep the Markmap file name identical to the issue file name, only changing the directory to `.issues/.markmap/`.
- When creating a mind map, default to exactly three top-level nodes: `核心目标`, `需求边界：做什么 (In Scope)`, and `需求边界：不做什么 (Out of Scope)`.
- Do not scan, rewrite, rename, or normalize pre-existing `.issues` files as part of this skill.
- Do not invent requirements or add new work items.
- When splitting a direct requirement, preserve the source scope exactly; split for execution clarity, not for expansion.
- Default `status` to `todo` unless the source note clearly indicates otherwise.
- Do not add a `markmap` frontmatter field unless the explicit mind-map trigger matched.
- Do not preserve raw conversational wording when a clearer professional structure is possible.
- Keep links exact unless formatting them as a YAML list improves clarity.
- Preserve user-provided local file paths exactly; never truncate them to filenames or rewrite them unless the user explicitly requests a different representation.
- For annotated-image requests, ground requirements in the explicit image annotations and preserve the supplied image path as evidence; do not infer additional changes from unmarked UI.
- Do not generate `验收` or other testing-oriented sections by default; include them only when the user explicitly requests that level of test or acceptance detail.
- Use a brief planning-style summary only when it helps the user confirm direction quickly; do not let the summary replace the actual issue file output.
- Prefer concise, layered, execution-ready writing over transcript-style recording.
