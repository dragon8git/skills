---
name: hbuldx-h5-publish
description: Build and validate a UniApp X H5_PRO artifact locally through HBuilderX. Use when a user asks to compile, package, export, or verify the custom H5 release of a UniApp X project, especially when production H5 API requests must remain host-relative. Does not deploy, upload, or modify release versions.
---

# HBuilderX H5 Publish

Create and validate only a local H5 artifact. Do not upload it, deploy it, change `manifest.json`, or infer a hosting target.

## Preflight

1. Treat the repository's `AGENTS.md` as project-specific authority.
2. Inspect `package.json` for `uni-app.scripts.H5-PRO`. Require that its environment selects H5 and its define includes `H5_PRO`; report a blocker if it is absent or mismatched. Do not silently substitute a generic H5 build.
3. Inspect `git status --short` and report pre-existing changes without reverting or overwriting them.
4. State that build success proves only the local artifact. A real `{host}/api/...` request requires a separately authorized deployment and runtime check.

## Build

Use the **computer-use** skill to operate HBuilderX when the HBuilderX CLI cannot select the custom release configuration:

1. Open the `app/` project in HBuilderX.
2. Choose **发行 → 自定义发行 →** the entry backed by `H5-PRO` (the displayed title may be project-specific, for example `消防企业端H5端`).
3. Start the local Web/H5 release. Leave every upload, server, or hosting option disabled unless the user separately authorizes it.
4. Wait for completion and require `app/unpackage/dist/build/web/index.html` to exist and be newer than the build start time.

If the project provides a documented CLI command that selects the exact `H5-PRO` custom release, it may be used instead. Never fall back to an ordinary `publish web` command that ignores `H5-PRO`.

## Validate the artifact

Run checks against `app/unpackage/dist/build/web`, not source text or a stale development output:

1. Confirm `index.html` exists and JavaScript bundle files are present.
2. Count occurrences across bundle JavaScript files of the target API route (when known), `'/api/api/'`, and the old absolute API origin (when applicable). Use a counting command that returns zero explicitly, such as `rg -o ... | wc -l`; do not mistake `rg`'s no-match exit code for a failed validation.
3. For the standard maintenance login case, require:
   - `/api/maintenance/auth/login` occurs in the bundle;
   - `/api/api/maintenance/auth/login` occurs zero times;
   - `https://wbfw.zf-data.com/api/maintenance/auth/login` occurs zero times.
4. If the request concerns a different endpoint or former origin, substitute those exact strings and state them in the result.

An H5 production request should retain its existing `/api/...` path and use an empty request base URL, yielding `{host}/api/...`; do not prepend `/api` to an already `/api`-prefixed endpoint.

## Report

Report the selected custom release, artifact directory, artifact freshness evidence, and each bundle-count result. Separate:

- **Verified:** local H5 artifact and static API-path checks.
- **Not verified:** real request behavior on the deployed host, unless deployment and browser/network verification were explicitly authorized and completed.
