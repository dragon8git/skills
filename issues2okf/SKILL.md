---
name: issues2okf
description: Convert user-provided requirements, bug reports, or development requests into one or more standardized `.issues/*.md` TODO files with YAML frontmatter, readable filenames, and professionally structured issue content.
---

# Issues to OKF

## Role

Act as a strong product manager, requirement analyst, and solution architect.

Do not mechanically dump the user's raw text into an issue file.

Your job is to preserve the user's real intent while rewriting it into a concise, structured, execution-ready issue document.

## Workflow

1. Treat this skill as direct requirement mode only:
   - convert the current user input into one or more new standardized `.issues/*.md` files
   - do not scan existing `.issues` notes for cleanup, normalization, or beautification
   - if the user wants historical `.issues` files rewritten, that is outside this skill's scope
2. First define the requirement before recording it:
   - identify the real problem being solved
   - distinguish goal, scope, constraints, and expected outcome
   - remove conversational noise, but do not change the user's meaning
3. Split the request only when it naturally contains more than one independently executable task:
   - keep one issue when the work is one coherent slice
   - split into multiple issues when the request clearly contains separate pages, separate bugs, separate integrations, or separate deliverables
   - prefer the smallest useful split; do not create artificial subtasks
4. Create new `.md` files under `.issues/` with readable titles.
5. Detect whether the user explicitly asks for a mind map before enabling the mind-map extension:
   - activate only when the prompt clearly contains intent such as `xmind`, `mind`, `思维导图`, `mindmap`, `markmap`, `Mermaid`, or an explicit request like `需求有点复杂，请创建思维导图`
   - do not create a mind map by default for ordinary issue requests
   - when activated, generate a Markmap markdown file at `.issues/.markmap/{same-name-as-issue}.md`
   - use the mind map to define the problem boundary: what to do, what not to do, and the scope edges that keep execution focused
6. Infer the smallest correct frontmatter values from the source note:
   - `status`: `todo`, `doing`, `review`, or `done` (default `todo`)
   - `type`: `dev`, `bug`, or the closest simple category
   - `title`: short human title
   - `description`: one-sentence summary
   - `links`: source URL or URLs
   - `tags`: short lowercase labels from the page, module, or topic
   - `timestamp`: `YYYY-MM-DD`
   - `markmap`: relative path like `.issues/.markmap/{name}.md` only when the explicit mind-map trigger matched
7. Write the issue body as a compact professional spec, not as raw chat transcript.
8. When the explicit mind-map trigger matched, also write a Markmap outline markdown file:
   - file path must match `.issues/.markmap/{same-name-as-issue}.md`
   - the outline must stay problem-first and boundary-first
   - use only these three top-level core nodes:
     - `核心目标`
     - `需求边界：做什么 (In Scope)`
     - `需求边界：不做什么 (Out of Scope)`
   - do not add other top-level nodes unless the user explicitly asked for them
   - each branch under the three core nodes should stay short, concrete, and boundary-oriented
   - avoid turning the mind map into endless brainstorming; its job is scope confirmation, not idea expansion
9. Preserve user-provided paths exactly when they are part of the requirement context:
   - local absolute file paths such as `/Users/lee/Pictures/example.png` must remain unchanged
   - do not shorten paths to basenames such as `example.png`
   - do not silently rewrite absolute paths into relative paths, URLs, or markdown links unless the user explicitly asked for that format
   - if a screenshot, prototype, workbook, or other local file path is important evidence, keep the original full path in `备注` or `links`

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

## 验收

- ...

## 备注

- ...
```

Body writing rules:

- `目标`: explain the business or product goal in 1-3 bullets
- `范围`: state the affected page, module, or scenario; keep scope explicit
- `需求`: list concrete implementation expectations, ordered for execution clarity
- `验收`: write user-visible or testable completion criteria when the prompt implies them
- `备注`: keep only essential constraints, dependencies, API notes, prototype references, or caveats
- when the source prompt includes local file paths, preserve the exact original path strings verbatim in the most relevant section
- if a section has no real content, omit it instead of padding
- keep the whole body concise; structure is more important than volume

## Formatting Rules

- Only create new standardized issue files from the current user input.
- Write new `.md` files under `.issues/` instead of editing unrelated files.
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
- Prefer concise, layered, execution-ready writing over transcript-style recording.
