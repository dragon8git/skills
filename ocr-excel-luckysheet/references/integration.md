# Luckysheet integration reference

## Dependencies

Load Luckysheet plugin CSS/JS, Luckysheet, and LuckyExcel in that order. Pin versions. Do not assume LuckyExcel round-trips all XLSX features; test each feature used by the product.

```html
<script src=".../luckysheet.umd.js"></script>
<script src=".../luckyexcel.umd.js"></script>
```

Convert the downloaded blob into a `File`, then call `LuckyExcel.transformExcelToLucky(file, callback)`.

## Lifecycle

Use one dedicated full-screen dialog host such as `#luckysheet-host`. A polling result-list must never contain this host: replacing `innerHTML` or destroying/recreating the host during polling leads to coordinate drift and lost focus.

```js
luckysheet.create({
  container: host.id,
  data: workbook.sheets.filter((sheet) => sheet.name !== '_metadata'),
  showtoolbar: false,
  showinfobar: false,
  sheetFormulaBar: false,
  showstatisticBar: false,
  hook: { cellMousedown: (cell, position, sheet, event) => openCandidates(position, sheet, event) },
});
```

Destroy with `luckysheet.destroy()` only when closing the preview or switching workbooks. Clear stale async results if a user closes before conversion completes.

## XLSX candidate metadata

For fuzzy matches, create a hidden worksheet with one row per candidate:

| Sheet | Cell | OCR value | Candidate | Score |
| --- | --- | --- | --- | --- |
| 转换结果 | A2 | PLF060-1O | PLF060-10 | 0.8889 |

Excel may separately use native data validation and cell comments. In Luckysheet, extract the hidden sheet from `workbook.sheets` before rendering visible tabs. LuckyExcel cells are shaped as `{ r, c, v: { v, m, ... } }`; use `cell.v?.v ?? cell.v`.

Create an index keyed as `${sheetName}!${cellAddress}`. Convert Luckysheet's zero-based `(r, c)` to an A1 address before lookup.

## Candidate popup

Use a real HTML popup, not Luckysheet data validation. Its buttons should display `value（score%）`; on click call `luckysheet.setcellvalue(row, column, value)` and dismiss the popup.

Position after clearing `hidden`, so `getBoundingClientRect()` reports its final size:

```js
const left = x + gap + width <= dialog.right - margin ? x + gap : x - width - gap;
const top = y + gap + height <= dialog.bottom - margin ? y + gap : y - height - gap;
popup.style.left = `${clamp(left, dialog.left + margin, dialog.right - width - margin)}px`;
popup.style.top = `${clamp(top, dialog.top + margin, dialog.bottom - height - margin)}px`;
```

Use fixed positioning and a z-index above Luckysheet. Close it on a non-candidate cell, explicit close, preview close, and workbook reset.

## Failure triage

- Wrong cell receives focus: move to full-screen dialog; confirm the host is not inside rerendered content; then test a real completed workbook.
- No candidate popup: inspect the parsed hidden sheet; verify nested `cell.v.v`; compare the generated index key with the clicked `sheet.name!A1` key.
- Popup unreachable: ensure no mobile media rule sets it to `display: none`; keep it outside clipping overflow; use `position: fixed`.
- New JavaScript not running: increment the app's static asset version and hard-refresh.

## Completion checklist

- Open and close with button, Escape, and a second preview.
- Click ordinary cells and exceptional cells near all viewport edges.
- Choose each type of candidate and confirm only the value is written.
- Verify auxiliary sheets remain absent from visible tabs.
- Run project tests, JS syntax checks, and a browser test on a real generated file.
