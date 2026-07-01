---
name: issues2okf
description: Normalize `.issues` markdown notes into standard TODO docs with YAML frontmatter, readable filenames, and preserved body text. Also use when the user directly provides a requirement, bug report, or development request and wants it split into one or more standardized `.issues/*.md` files. Skip files that are already in the target format.
---

# Issues to OKF

## Workflow

1. Choose the input mode first:
   - existing notes mode: scan the target `.issues` directory
   - direct requirement mode: convert the user-provided requirement text into one or more standardized `.issues/*.md` files
2. Leave a file unchanged if it already has the standard TODO shape:
   - YAML frontmatter exists
   - frontmatter includes `status`, `type`, `title`, `description`, `links`, `tags`, `timestamp`
   - body starts after the frontmatter block and is already clean enough to read as a task note
3. For each raw note, rewrite it into:
   - YAML frontmatter with `status`, `type`, `title`, `description`, `links`, `tags`, `timestamp`
   - a body that preserves the original request text with only light formatting cleanup
4. For direct requirement mode, split the request only when it naturally contains more than one independently executable task:
   - keep one issue when the work is one coherent slice
   - split into multiple issues when the request clearly contains separate pages, separate bugs, separate integrations, or separate deliverables
   - prefer the smallest useful split; do not create artificial subtasks
5. Create or rename each file to a readable title. Keep numeric prefixes when present, for example `01.md -> 01_省市区接口对接.md`.
6. Infer the smallest correct values from the source note:
   - `status`: `todo`, `doing`, `review`, or `done` (default `todo`)
   - `type`: `dev`, `bug`, or the closest simple category
   - `title`: short human title
   - `description`: one-sentence summary
   - `links`: source URL or URLs
   - `tags`: short lowercase labels from the page, module, or topic
   - `timestamp`: `YYYY-MM-DD`

## Formatting Rules

- Do not rewrite files that are already in the target format.
- In direct requirement mode, write new `.md` files under `.issues/` instead of editing unrelated files.
- Treat files missing the full frontmatter set as non-standard and rewrite them.
- Do not invent requirements or add new work items.
- When splitting a direct requirement, preserve the source scope exactly; split for execution clarity, not for expansion.
- Default `status` to `todo` unless the source note clearly indicates otherwise.
- Keep the original request body, only normalizing spacing, punctuation, and markdown readability.
- Keep links exact unless formatting them as a YAML list improves clarity.
