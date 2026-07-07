---
name: scan-issues
description: "Scan `.issues` markdown task files that currently exist in the working tree, find standard docs whose YAML frontmatter has `status: todo` and type like `dev`, `requirement`, `需求`, `bug`, or `fixbug`, then implement at most 5 of them per run in the current repo and move each picked issue forward after verification. Use when the user wants Codex to work through local `.issues` tasks instead of just listing them, especially in repos that track work as markdown files."
---

# Scan Issues

1. Read the repo root `AGENTS.md` and obey repo-local workflow before touching code.
2. Scan only `.issues/**/*.md` that currently exist in the working tree.
3. Ignore everything outside the current `.issues` filesystem view:
   - do not read git history, deleted blobs, old commits, stash entries, or reflog for issue discovery
   - do not comment on which issue files used to exist
   - do not discuss deleted, missing, or renamed issue files unless the user explicitly asks
4. Treat a file as eligible only when all of these are true:
   - it already has YAML frontmatter
   - frontmatter contains `status`
   - `status` is exactly `todo`
   - `type` is one of `dev`, `requirement`, `需求`, `bug`, `fixbug`, or a clearly equivalent local label
5. If an eligible issue frontmatter contains `markmap`:
   - try to read the referenced markmap file as a supplement to the issue text
   - treat it as a scope-and-boundary aid, not as a replacement for the issue body
   - prefer it for understanding `核心目标`, `需求边界：做什么 (In Scope)`, and `需求边界：不做什么 (Out of Scope)`
   - if the `markmap` path is missing or unreadable, continue with the issue body and report that the markmap supplement was unavailable
6. After finding all eligible issues, sort them by issue file path in ascending lexical order and pick at most the first 5 for the current batch:
   - this 5-item cap is a hard limit for every run of `$scan-issues`
   - never process more than 5 todo issues in one run, even if more are eligible
   - leave the remaining eligible issues untouched for later runs
   - report which eligible issues were deferred because of the batch limit
7. Skip non-standard notes. Do not normalize them here. If most files are non-standard, stop and use `$issues2okf` first.
8. Use one independent subagent per picked issue:
   - start a fresh subagent thread for each issue
   - give the subagent the issue file path, the repo path, any directly referenced screenshots or files, and the referenced `markmap` file when present
   - tell the subagent to read the real code path before editing
   - tell the subagent to make the smallest change that fixes the root cause or delivers the requested slice
   - tell the subagent to reuse existing helpers and patterns before adding new code
9. Have the main agent coordinate, not implement the issue work directly:
   - launch the subagent
   - review the subagent's diff and verification notes
   - apply or refine follow-up edits only if the subagent missed something critical
   - keep issue execution isolated so one issue does not leak assumptions into another
10. Before a new development batch, perform any repo-required backup commit or checkpoint step if `AGENTS.md` asks for one.
11. After each issue:
   - run the smallest real verification the repo supports
   - if the repo has no CLI build/test path, do static verification and report that manual validation is still needed
   - move the issue `status` forward:
     - `review` when code is done but still needs manual/product verification
     - `done` only after the required verification is actually completed
     - keep `todo` if no reliable implementation was made
   - when moving an issue from `todo` to `review`, update frontmatter `links` to include only source code files changed in that round
   - keep any original reference URL or URL list and append changed repo file paths rather than replacing them
   - source code files here means implementation files such as `.uvue`, `.vue`, `.js`, `.ts`, `.uts`, `.css`, `.scss`, `.less`, `.json`, and similar code/config files that were intentionally edited for the task
   - do not append backend API path strings, OpenAPI paths, screenshots, generated assets, icon files, font files, build artifacts, lockfiles, or other non-code byproducts unless the user explicitly asks for them
   - when moving an issue from `todo` to `review`, append this empty template at the end of the body for the next review round, using the next sequential round number:

```md
## Review 第 n 轮

- 未通过原因：
- 开发建议：
```

   - if review later fails and the issue returns to `todo`, fill the latest `Review 第 n 轮` section instead of deleting older requirement text or review history
12. If subagent capability is unavailable in the current harness, stop and report that this skill cannot execute as designed instead of silently falling back to single-agent implementation.
13. Do not silently rewrite issue content, filenames, or frontmatter shape here except for the intentional issue-log updates above: advancing `status`, updating `links`, and appending the next empty review template.
14. Do not perform repository repair or issue inventory reconciliation here:
   - no git-based recovery
   - no recreating issue files from history
   - no placeholder issue files

## Output

- Report which issue files were picked up.
- Report which eligible issues were deferred because they exceeded the per-run limit of 5.
- Report that each issue was assigned to its own subagent.
- For each issue, state the code path changed and the verification performed.
- Call out whether a `markmap` supplement was read for that issue when present, or whether it was unavailable.
- Call out anything skipped because the issue was non-standard, blocked, or needed manual verification.
- Do not mention deleted or missing issue files unless the user explicitly asked about them.
