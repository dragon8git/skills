---
name: issues2okf
description: Normalize `.issues` markdown notes into standard TODO docs with YAML frontmatter, readable filenames, and preserved body text. Use when converting requirement, development, or bug notes under `.issues` into repo-standard task documents, or when skipping files that are already in the target format.
---

# Issues to OKF

## Workflow

1. Scan the target `.issues` directory.
2. Leave a file unchanged if it already has the standard TODO shape:
   - YAML frontmatter exists
   - frontmatter includes `status`, `type`, `title`, `description`, `links`, `tags`, `timestamp`
   - body starts after the frontmatter block and is already clean enough to read as a task note
3. For each raw note, rewrite it into:
   - YAML frontmatter with `status`, `type`, `title`, `description`, `links`, `tags`, `timestamp`
   - a body that preserves the original request text with only light formatting cleanup
4. Rename the file to a readable title. Keep numeric prefixes when present, for example `01.md -> 01_省市区接口对接.md`.
5. Infer the smallest correct values from the source note:
   - `status`: `todo`, `doing`, `review`, or `done` (default `todo`)
   - `type`: `dev`, `bug`, or the closest simple category
   - `title`: short human title
   - `description`: one-sentence summary
   - `links`: source URL or URLs
   - `tags`: short lowercase labels from the page, module, or topic
   - `timestamp`: `YYYY-MM-DD`

## Formatting Rules

- Do not rewrite files that are already in the target format.
- Treat files missing the full frontmatter set as non-standard and rewrite them.
- Do not invent requirements or add new work items.
- Default `status` to `todo` unless the source note clearly indicates otherwise.
- Keep the original request body, only normalizing spacing, punctuation, and markdown readability.
- Keep links exact unless formatting them as a YAML list improves clarity.
