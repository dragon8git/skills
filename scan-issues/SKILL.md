---
name: scan-issues
description: "Scan existing `.issues` markdown task files in the current working tree, find standard docs whose YAML frontmatter has `status: todo` and type like `dev`, `requirement`, `需求`, `bug`, or `fixbug`, then implement them one by one in the current repo and move each issue forward after verification. Use when the user wants Codex to work through local `.issues` tasks instead of just listing them, especially in repos that track work as markdown files, and only the files that currently exist should be considered."
---

# Scan Issues

1. Read the repo root `AGENTS.md` and obey repo-local workflow before touching code.
2. Scan only `.issues/**/*.md` that currently exist in the working tree.
3. Treat the current filesystem state as the only source of truth for issue discovery:
   - do not read git history, deleted blobs, old commits, stash entries, or reflog to discover issue files
   - do not recreate, restore, checkout, or regenerate missing `.issues` files unless the user explicitly asks for recovery
   - if an issue document was deleted from `.issues`, treat it as intentionally absent and out of scope for this skill
4. Treat a file as eligible only when all of these are true:
   - it already has YAML frontmatter
   - frontmatter contains `status`
   - `status` is exactly `todo`
   - `type` is one of `dev`, `requirement`, `需求`, `bug`, `fixbug`, or a clearly equivalent local label
5. Skip non-standard notes. Do not normalize them here. If most files are non-standard, stop and use `$issues2okf` first.
6. Use one independent subagent per eligible issue:
   - start a fresh subagent thread for each issue
   - give the subagent only the issue file path, the repo path, and any directly referenced screenshots or files
   - tell the subagent to read the real code path before editing
   - tell the subagent to make the smallest change that fixes the root cause or delivers the requested slice
   - tell the subagent to reuse existing helpers and patterns before adding new code
7. Have the main agent coordinate, not implement the issue work directly:
   - launch the subagent
   - review the subagent's diff and verification notes
   - apply or refine follow-up edits only if the subagent missed something critical
   - keep issue execution isolated so one issue does not leak assumptions into another
8. Before a new development batch, perform any repo-required backup commit or checkpoint step if `AGENTS.md` asks for one.
9. After each issue:
   - run the smallest real verification the repo supports
   - if the repo has no CLI build/test path, do static verification and report that manual validation is still needed
   - move the issue `status` forward:
     - `review` when code is done but still needs manual/product verification
     - `done` only after the required verification is actually completed
     - keep `todo` if no reliable implementation was made
   - when moving an issue from `todo` to `review`, update frontmatter `links` to include the files changed in that round; keep any original reference URL or URL list and append changed repo file paths rather than replacing them
   - when moving an issue from `todo` to `review`, append this empty template at the end of the body for the next review round, using the next sequential round number:

```md
## Review 第 n 轮

- 未通过原因：
- 开发建议：
```

   - if review later fails and the issue returns to `todo`, fill the latest `Review 第 n 轮` section instead of deleting older requirement text or review history
10. If subagent capability is unavailable in the current harness, stop and report that this skill cannot execute as designed instead of silently falling back to single-agent implementation.
11. Do not silently rewrite issue content, filenames, or frontmatter shape here except for the intentional issue-log updates above: advancing `status`, updating `links`, and appending the next empty review template.
12. Do not perform repository repair or issue inventory reconciliation here:
   - no git-based recovery
   - no recreating deleted issue files from history
   - no adding placeholder issue files to match prior scans or prior runs

## Output

- Report which issue files were picked up.
- Report that each issue was assigned to its own subagent.
- For each issue, state the code path changed and the verification performed.
- Call out anything skipped because the issue was non-standard, blocked, or needed manual verification.
