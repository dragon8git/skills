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
4. Infer the smallest correct values from the source note:
   - `status`: `todo`, `doing`, `review`, or `done` (default `todo`)
   - `type`: `dev`, `bug`, or the closest simple category
   - `title`: short human title
   - `description`: one-sentence summary
   - `links`: source URL or URLs
   - `tags`: short lowercase labels from the page, module, or topic
   - `timestamp`: `YYYY-MM-DD`
5. Write the body as the original request text with only light formatting cleanup so it stays readable and executable.

## Formatting Rules

- Only create new standardized issue files from the current user input.
- Write new `.md` files under `.issues/` instead of editing unrelated files.
- Do not scan, rewrite, rename, or normalize pre-existing `.issues` files as part of this skill.
- Do not invent requirements or add new work items.
- When splitting a direct requirement, preserve the source scope exactly; split for execution clarity, not for expansion.
- Default `status` to `todo` unless the source note clearly indicates otherwise.
- Keep the original request body, only normalizing spacing, punctuation, and markdown readability.
- Keep links exact unless formatting them as a YAML list improves clarity.
