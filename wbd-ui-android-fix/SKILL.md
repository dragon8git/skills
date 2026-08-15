---
name: wbd-ui-android-fix
description: Scan and repair UniApp X Android CSS compatibility issues in WBD .uvue files, including native-element selectors, nth-child/last-child selectors, unsupported keyframe selectors, baseline alignment, percentage max-width, and explicit classes. Use when HBuilderX Android reports uvue CSS compiler errors.
---

# WBD UI Android Fix

## Overview

Use this skill to migrate unsupported CSS patterns in WBD UniApp X source. Keep changes mechanical and visual-only: preserve business logic and existing behavior; do not modify third-party `uni_modules` unless explicitly requested.

## Workflow

1. Inspect the repository graph before searching files, then inventory `.uvue` styles and matching template nodes.
2. Limit the default scope to `app/pages/wbd/**/*.uvue`, `app/components/**/*.uvue`, and `app/windows/**/*.uvue`; exclude `app/uni_modules`, `wxcomponents`, backups, and unrelated demos/API pages.
3. Find unsupported native-element selectors such as:
   - `.parent text`
   - `.parent.active text`
   - `.parent text:first-child`
   - `.parent text:last-child`
   - `.outer .inner text` and `.outer > text`
   - `.photo-thumb image`, `.device-picker-row picker`, `.overview view`
   - `.day-grid .option-chip:nth-child(4n)` and other `:nth-child(...)` layout selectors
   - `.flow-stage:last-child .flow-content` and other `:last-child` layout selectors
4. Add deterministic classes to matching nodes. Merge with existing static/dynamic classes rather than replacing them. Preserve first/last-child semantics with explicit variants.
5. Replace the entire unsupported selector with class selectors. Do not leave native-element descendant selectors in the stylesheet.
6. Replace unsupported properties mechanically:
   - `align-items: baseline` → `align-items: center`.
   - Percentage `max-width` used for value columns → `flex: 1; min-width: 0`, retaining margins and text alignment.
   - Do not replace supported percentage `width`; only target compiler-reported unsupported `max-width` values.
7. Handle animations by wrapping both the animation declaration and keyframes containing `from`, `to`, or percentage selectors in `/* #ifdef WEB || MP */ ... /* #endif */`. Android should skip the animation and its unsupported selectors; WEB/H5 and MP keep the existing animation. Preserve the animation trigger logic outside of platform-specific CSS.
8. Keep the migration scoped to template/style markup. Do not refactor scripts, APIs, routes, or unrelated CSS.

## Naming and safety rules

- Use deterministic, file-local names such as `uvue-text-<parent>` and `uvue-text-<parent>-first/last`; avoid random names.
- When multiple selectors target one node, merge all generated classes and preserve existing semantic/state classes.
- Replace `:nth-child(...)`, `:first-child`, and `:last-child` layout semantics with deterministic template classes such as `day-grid-last` or `flow-stage-last`; derive them from existing loop indexes/data rather than changing business ordering.
- Convert `view`, `image`, and `picker` descendant selectors when they are reported by the Android compiler; use explicit classes on the matching nodes.
- Do not modify third-party `uni_modules` by default; record their errors separately.
- Do not touch `uni_modules` by default because dependency updates may overwrite local fixes.

## Verification

- Run a static scan over the selected scope and confirm zero native-element descendant selectors for the reported tags, no unsupported `:nth-child`/`:first-child`/`:last-child` layout selectors, no `align-items: baseline`, and no percentage `max-width` values.
- Confirm every guarded keyframe has balanced conditional markers and every changed `.uvue` still has balanced template/style blocks.
- Confirm animation declarations referencing guarded keyframes are inside the same platform conditional block; Android must retain only the static base style.
- Run `git diff --check`.
- Run HBuilderX Android compilation with `launch app-android --compile true --continue-on-error false`; distinguish newly introduced compatibility errors from pre-existing CSS/UTS errors.
- Run `launch mp-weixin --compile true --continue-on-error false` to catch shared `.uvue` syntax regressions.
- Report remaining unsupported selectors or property errors separately; do not silently broaden the migration.
