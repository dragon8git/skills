---
name: scan-issues
description: "Scan `.issues` markdown task files, find standard docs whose YAML frontmatter has `status: todo` and type like `dev`, `requirement`, `需求`, `bug`, or `fixbug`, then implement them one by one in the current repo and move each issue forward after verification. Use when the user wants Codex to work through local `.issues` tasks instead of just listing them, especially in repos that track work as markdown files."
---

# Scan Issues

1. Read the repo root `AGENTS.md` and obey repo-local workflow before touching code.
2. Scan only `.issues/**/*.md`.
3. Treat a file as eligible only when all of these are true:
   - it already has YAML frontmatter
   - frontmatter contains `status`
   - `status` is exactly `todo`
   - `type` is one of `dev`, `requirement`, `需求`, `bug`, `fixbug`, or a clearly equivalent local label
4. Skip non-standard notes. Do not normalize them here. If most files are non-standard, stop and use `$issues2okf` first.
5. Use one independent subagent per eligible issue:
   - start a fresh subagent thread for each issue
   - give the subagent only the issue file path, the repo path, and any directly referenced screenshots or files
   - tell the subagent to read the real code path before editing
   - tell the subagent to make the smallest change that fixes the root cause or delivers the requested slice
   - tell the subagent to reuse existing helpers and patterns before adding new code
6. Have the main agent coordinate, not implement the issue work directly:
   - launch the subagent
   - review the subagent's diff and verification notes
   - apply or refine follow-up edits only if the subagent missed something critical
   - keep issue execution isolated so one issue does not leak assumptions into another
7. Before a new development batch, perform any repo-required backup commit or checkpoint step if `AGENTS.md` asks for one.
8. After each issue:
   - run the smallest real verification the repo supports
   - if the repo has no CLI build/test path, do static verification and report that manual validation is still needed
   - move the issue `status` forward:
     - `review` when code is done but still needs manual/product verification
     - `done` only after the required verification is actually completed
     - keep `todo` if no reliable implementation was made
9. If subagent capability is unavailable in the current harness, stop and report that this skill cannot execute as designed instead of silently falling back to single-agent implementation.
10. Do not silently rewrite issue content, filenames, or frontmatter shape here except for the `status` field you intentionally advance.

## Output

- Report which issue files were picked up.
- Report that each issue was assigned to its own subagent.
- For each issue, state the code path changed and the verification performed.
- Call out anything skipped because the issue was non-standard, blocked, or needed manual verification.
