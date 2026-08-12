---
name: ocr-excel-luckysheet
description: Integrate or repair a Luckysheet and LuckyExcel browser preview for generated XLSX files, especially when embedded previews have click-coordinate drift, pages rerender while previewing, or fuzzy-matched spreadsheet cells need contextual candidate selection. Use for full-screen read-only Excel previews, stable Luckysheet lifecycle handling, XLSX hidden-sheet metadata, and click-anchored Top-N candidate popups.
---

# OCR Excel Luckysheet

## Overview

Build a stable, read-only XLSX preview around Luckysheet without treating it as a fully compatible Excel renderer. Keep the generated workbook authoritative; use browser-only edits as transient preview decisions unless explicit save-back behavior exists.

Read [references/integration.md](references/integration.md) before implementing. It contains the exact integration contract, coordinate handling, and failure modes.

## Implementation workflow

1. Inspect the current preview lifecycle, host placement, polling/rerender paths, and static-cache versioning before editing.
2. Load `.xlsx` with LuckyExcel, then create Luckysheet only after the full-screen dialog and its host are visible.
3. Keep the Luckysheet host outside list rows or components that rerender during upload polling. Destroy only when the preview closes or changes workbooks.
4. Treat Excel data-validation import as unreliable. For Top-N choices, read workbook metadata from a hidden sheet and render a custom HTML popup on the Luckysheet `cellMousedown` hook.
5. Reproduce the real preview path with an XLSX containing an exceptional cell. Verify click targeting, popup opening, candidate selection, close paths, viewport bounds, and cache refresh.

## Required design constraints

- Use a full-screen native `<dialog>` for interactive previews when inline rendering causes click/focus mismatch.
- Render the candidate popup as a fixed, separate DOM layer. Do not depend on Luckysheet’s native data-validation UI.
- Anchor the popup to the click event’s `clientX`/`clientY`; flip left/up when needed and clamp it to the dialog with a margin.
- Store hidden-sheet cell values as `cell.v?.v ?? cell.v`; LuckyExcel `celldata` values are commonly nested cell objects.
- Display `型号（匹配度）` in choices but write only the model value with `luckysheet.setcellvalue(row, column, value)`.
- Hide auxiliary metadata sheets from the visible sheet tabs before passing data to Luckysheet.

## Verification

Run JavaScript syntax checks and the project test suite. Inspect the built workbook with OpenPyXL if it emits hidden candidate sheets, comments, or data validation. Then test a completed local task in a browser: static checks do not prove Luckysheet click coordinates or popup behavior.
