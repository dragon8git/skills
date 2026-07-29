---
name: wxapp-subpackages-inspect
description: Inspect and safely remediate WeChat Mini Program cross-subpackage runtime imports in UniApp X projects. Use when a MiniProgramError says a module is not defined, a page white-screens only on mp-weixin, or when auditing pages.json subPackages for unsafe business-module imports.
---

# WeChat Mini Program Subpackage Inspection

Treat every `pages.json` `subPackages.root` as an independent runtime boundary. A page, component, or API module must not runtime-import a module from another business subpackage.

## Inspect

1. Read the error's `require args` when present. It identifies the missing module and usually the source subpackage.
2. Run the bundled scanner from the app root:

   ```bash
   python3 "$HOME/.codex/skills/wxapp-subpackages-inspect/scripts/scan_subpackage_imports.py" app
   ```

3. Classify results:
   - **High**: a source file under subpackage A imports `@/pages/wbd/<B>/...` and A differs from B.
   - **Review**: a shared component has a runtime business-subpackage import; inspect every page that uses it.
   - Ignore `import type` only when the import is genuinely type-only.
4. Do not treat a stale `unpackage/dist` file as proof that source still has the dependency. It is useful only after a fresh target build.

## Fix

Make the smallest change that preserves API paths, request parameters, cache keys, and permission codes.

- Prefer a main-package public API for genuinely shared contracts.
- If HBuilderX module placement is unstable, place the minimal wrapper in the affected subpackage's already-loaded API module.
- Keep target-page imports inside their own subpackage; do not solve the problem by preloading another business subpackage.
- Copy only the needed type, request wrapper, cache helper, or permission check. Do not move unrelated maintenance UI or business logic.

## Verify

1. Run the scanner again; target subpackages must have no high-risk imports.
2. Compile:

   ```bash
   /Applications/HBuilderX.app/Contents/MacOS/cli launch mp-weixin --project "$(pwd)/app" --compile true --continue-on-error false
   ```

3. In WeChat Developer Tools, cold-start and directly enter each repaired page. Test a rapid route switch if the original fault was probabilistic.

## Report

State the source subpackage, imported subpackage, source file, imported path, severity, and whether it is runtime or type-only. Distinguish verified source findings from device-side validation still required.
