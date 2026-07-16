---
name: scan-issues
description: "Scan `.issues` markdown task files that currently exist in the working tree, find standard docs whose YAML frontmatter has `status: todo` and type like `dev`, `requirement`, `需求`, `bug`, or `fixbug`, then implement them and move each picked issue forward after verification. Parallel mode processes at most 5 by default; serial dependency mode processes all eligible todo issues by default. An explicit quantity limit in the user's prompt overrides either default. Use when the user wants Codex to work through local `.issues` tasks instead of just listing them, especially in repos that track work as markdown files."
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
6. After finding all eligible issues, sort them by issue file path in ascending lexical order. Determine the selected-batch limit from the user's current description before selecting issues:
   - first recognize explicit positive-integer quantity limits, including `size=5`, `length=10`, `最多做 10 个`, and equivalent clear wording such as `最多处理 10 个` or `最多开发 10 个`; accept whitespace around `=` and match `size` / `length` case-insensitively
   - an explicit quantity limit overrides the mode default: select at most that many eligible todo issues in either parallel or serial dependency mode
   - if multiple explicit quantity limits conflict, do not guess which one applies; stop and ask the user to clarify the intended maximum
   - if no explicit quantity limit is present, parallel mode defaults to at most 5 eligible todo issues, while serial dependency mode has no batch limit and selects all eligible todo issues
   - leave issues beyond an applicable limit untouched for later runs and report which ones were deferred because of that limit
7. Skip non-standard notes. Do not normalize them here. If most files are non-standard, stop and use `$issues2okf` first.
8. Choose the execution mode from the user's current description before launching workers:
   - default to **parallel mode**.
   - enter **serial dependency mode** when the description contains any of these case-insensitive triggers: `deps`, `依赖`, `串行`, `逐个`, `one`, or `slow`. Treat English triggers as whole words, so unrelated words such as `someone` do not trigger serial mode.
   - explicit user instructions about execution order override these defaults.
9. In serial dependency mode, discover dependencies across all eligible todo issues before selecting the batch:
   - read frontmatter dependency fields such as `depends_on`, `dependencies`, or `deps`, and explicit body references to another issue's exact path, filename, title, or stated prerequisite.
   - treat an issue as dependent only when the text establishes a real prerequisite: another issue must land first because it creates, changes, or unlocks an API, data model, shared component, configuration, migration, or named deliverable it consumes.
   - do not infer a dependency merely because issues share a module, page, tag, or broad topic. When the evidence is unclear, report no dependency rather than guessing.
   - order confirmed dependencies before their dependents. If a dependency is an eligible todo issue, include its prerequisite before its dependent while staying within the applicable selected-batch limit; defer dependents whose required prerequisite cannot be included in this batch.
   - if no dependency can be confirmed, execute the selected issues one by one in ascending lexical issue-path order.
   - if a cycle or contradictory dependency is confirmed, do not parallelize the affected issues; execute the affected issues in ascending lexical issue-path order and report the cycle as a caveat.
10. In parallel mode, select the first eligible issues in ascending lexical issue-path order up to the applicable selected-batch limit and launch their workers concurrently:
   - use dependency discovery only to avoid an unsafe race: run confirmed prerequisite/dependent pairs as ordered waves, while continuing to run unrelated issues in parallel.
   - do not silently change to fully serial execution unless the user supplied a serial trigger or explicit ordering instruction.
11. Use one independent subagent per picked issue:
   - start a fresh subagent thread for each issue
   - give the subagent the issue file path, the repo path, any directly referenced screenshots or files, and the referenced `markmap` file when present
   - tell the subagent to read the real code path before editing
   - tell the subagent to make the smallest change that fixes the root cause or delivers the requested slice
   - tell the subagent to reuse existing helpers and patterns before adding new code
   - in serial dependency mode, start the next subagent only after the preceding issue has completed its development and required verification.
   - in parallel mode, start all independent selected issue workers concurrently, up to the applicable selected-batch limit; start each ordered wave only after its prerequisites complete.
12. Have the main agent coordinate, not implement the issue work directly:
   - launch the subagent
   - review the subagent's diff and verification notes
   - apply or refine follow-up edits only if the subagent missed something critical
   - keep issue execution isolated so one issue does not leak assumptions into another
13. Before a new development batch, perform any repo-required backup commit or checkpoint step if `AGENTS.md` asks for one.
14. Default verification boundary:
   - unless the user explicitly requests browser-level testing, do not open a browser, run Playwright, take screenshots, or perform browser interaction checks
   - prefer script-level verification such as builds, compiles, targeted automated tests, lint, type checks, or static checks supported by the repo
   - treat browser and hands-on product validation as the user's responsibility by default; report any remaining manual verification need without attempting it
15. After each issue:
   - run the smallest applicable script-level verification the repo supports
   - if the repo has no CLI build/test path, do static verification and report that manual validation is still needed
   - if code or issue-relevant files were changed for the issue, append one new development log block to the end of the issue body before appending any next review template
   - the development log must be append-only; never overwrite or rewrite older development logs
   - use the next sequential round number and this exact structure:

```md
## Dev Summary 第 n 轮

- 开发纪要：
```

   - fill the block with concise factual content from the current round only
   - write the block like a developer reporting work results to a lead: concise, concrete, outcome-first, and easy for the next coding agent to continue from
   - `开发纪要` is required and should summarize what was actually delivered this round, what key implementation decisions were made, which files or modules were touched when that context matters, and any follow-up hints, caveats, manual verification notes, review context, dependency notes, or handoff information that the next agent should not rediscover
   - do not pad the summary with generic process language; record only information that materially helps later review or follow-up development
   - if no reliable implementation was made, do not fabricate a development log; instead keep `status: todo` and report the block was not appended
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
   - when a later round resumes work on the same issue, append a new `Dev Summary 第 n 轮` block for that round instead of editing prior summary blocks
16. If subagent capability is unavailable in the current harness, stop and report that this skill cannot execute as designed instead of silently falling back to single-agent implementation.
17. Do not silently rewrite issue content, filenames, or frontmatter shape here except for the intentional issue-log updates above: advancing `status`, updating `links`, appending a new `Dev Summary 第 n 轮` block, and appending the next empty review template.
18. Do not perform repository repair or issue inventory reconciliation here:
   - no git-based recovery
   - no recreating issue files from history
   - no placeholder issue files

## Output

- Report which issue files were picked up.
- Report the applicable selected-batch limit: the explicit quantity instruction when present; otherwise the parallel default of 5 or that serial mode selected all eligible todo issues.
- Report which eligible issues were deferred because they exceeded an applicable selected-batch limit.
- Report the selected execution mode and the trigger that selected it when serial dependency mode was used.
- In serial dependency mode, report confirmed dependency edges, lexical fallback order when no dependency was confirmed, and any dependency-related deferral or cycle.
- In parallel mode, report the concurrent worker groups and any ordered dependency waves used to avoid a confirmed race.
- Report that each issue was assigned to its own subagent.
- For each issue, state the code path changed and the verification performed.
- For each issue, state whether a new `Dev Summary 第 n 轮` block was appended.
- State that browser-level testing was skipped unless the user explicitly requested it, and identify any remaining manual verification responsibility.
- Call out whether a `markmap` supplement was read for that issue when present, or whether it was unavailable.
- Call out anything skipped because the issue was non-standard, blocked, or needed manual verification.
- Do not mention deleted or missing issue files unless the user explicitly asked about them.
