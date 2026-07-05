---
name: issues2okf
description: Convert user-provided requirements, bug reports, or development requests into one or more standardized `.issues/*.md` TODO files with YAML frontmatter and readable filenames.
---

# Issues to OKF

## Workflow

1. Treat this skill as direct requirement mode only:
   - convert the user-provided requirement text into one or more standardized `.issues/*.md` files
   - do not scan existing `.issues` notes for cleanup, normalization, or beautification
   - if the user wants historical `.issues` files rewritten, that is outside this skill's scope
2. Split the request only when it naturally contains more than one independently executable task:
   - keep one issue when the work is one coherent slice
   - split into multiple issues when the request clearly contains separate pages, separate bugs, separate integrations, or separate deliverables
   - prefer the smallest useful split; do not create artificial subtasks
3. Create new `.md` files under `.issues/` with readable titles.
4. Detect whether the user explicitly asks for a mind map before enabling the mind-map extension:
   - activate only when the prompt clearly contains intent such as `xmind`, `mind`, `思维导图`, `mindmap`, `markmap`, `Mermaid`, or an explicit request like `需求有点复杂，请创建思维导图`
   - do not create a mind map by default for ordinary issue requests
   - when activated, generate a Markmap markdown file at `.issues/.markmap/{same-name-as-issue}.md`
   - use the mind map to define the problem boundary: what to do, what not to do, and the scope edges that keep execution focused
5. Infer the smallest correct values from the source note:
   - `status`: `todo`, `doing`, `review`, or `done` (default `todo`)
   - `type`: `dev`, `bug`, or the closest simple category
   - `title`: short human title
   - `description`: one-sentence summary
   - `links`: source URL or URLs
   - `tags`: short lowercase labels from the page, module, or topic
   - `timestamp`: `YYYY-MM-DD`
   - `markmap`: relative path like `.issues/.markmap/{name}.md` only when the explicit mind-map trigger matched
6. Write the body as the original request text with only light formatting cleanup so it stays readable and executable.
7. When the explicit mind-map trigger matched, also write a Markmap outline markdown file:
   - file path must match `.issues/.markmap/{same-name-as-issue}.md`
   - the outline must stay problem-first and boundary-first
   - use only these three top-level core nodes:
     - `核心目标`
     - `需求边界：做什么 (In Scope)`
     - `需求边界：不做什么 (Out of Scope)`
   - do not add other top-level nodes such as affected modules, constraints, risks, open questions, or implementation plan unless the user explicitly asked for them
   - each branch under the three core nodes should stay short, concrete, and boundary-oriented
   - avoid turning the mind map into endless brainstorming; its job is scope confirmation, not idea expansion

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
- Keep the original request body, only normalizing spacing, punctuation, and markdown readability.
- Keep links exact unless formatting them as a YAML list improves clarity.
