---
name: xlsx2prd
description: Convert Excel requirement, feature, quotation, scope, or field-list workbooks (.xlsx) into a traceable PRD.md and implementation-ready page-module todolist with Epic/Story Markdown files. Use when Codex must interpret spreadsheet requirements, preserve source scope and estimates, extract field dictionaries, identify ambiguities, define product flows and acceptance criteria, or split a PRD into frontend-like page folders and developer TODO checklists.
---

# XLSX to PRD

Turn spreadsheet rows into a product baseline and a development work breakdown without silently inventing business decisions.

## Workflow

1. Locate the input `.xlsx` files and the requested output directory.
2. Use the Spreadsheets skill when available. Inspect workbook sheets, used ranges, merged cells, formulas, and visible values.
3. Run the bundled extractor for an auditable source snapshot:

```bash
python3 scripts/extract_xlsx.py INPUT.xlsx --output-dir WORK_DIR/source
```

4. Read `source/workbook.json` and `source/inventory.md`. Identify:
   - systems or clients such as PC, mobile, mini program, and admin;
   - modules, pages, functions, descriptions, estimates, prices, and totals;
   - field-list sheets, enumerations, formulas, notes, exclusions, and open questions;
   - hierarchy conveyed by merged or blank continuation cells.
5. Create a source coverage matrix before drafting. Assign stable requirement IDs such as `FR-PC-001` or `FR-MP-101`.
6. Draft `PRD.md`, then derive the implementation TODO from that PRD. Do not independently reinterpret the spreadsheet a second time.
7. Split TODO files by page module. Keep simple modules in one `EpicN.md`; split only complex modules into `StoryN.M-description.md`.
8. Run:

```bash
python3 scripts/validate_delivery.py OUTPUT_DIR
```

9. Repair broken links, missing requirement coverage, duplicate IDs, or missing indexes before delivery.

Read [references/output-contract.md](references/output-contract.md) before writing deliverables. It defines the required PRD sections, decomposition rules, TODO quality bar, traceability, and handling of uncertainty.

## Interpretation Rules

- Preserve source facts, names, quantities, estimates, prices, formulas, and exclusions.
- Separate **source requirement**, **product clarification**, and **implementation recommendation**.
- Put unresolved business choices under `待产品确认`; never present them as approved behavior.
- State discrepancies explicitly, including missing numbering, subtotal mismatches, `--`, zero estimates, duplicate fields, or conflicting terminology.
- Normalize language for clarity while retaining a trace back to the source row or assigned `FR-*` ID.
- Treat quote effort and price as source metadata, not as a confirmed schedule or contract.
- Infer standard error, empty, loading, permission, audit, idempotency, and validation requirements when needed for implementability; label substantial scope additions as recommendations.

## Decomposition Rules

- Organize folders by user-visible page or cohesive module, not database table or backend service.
- Use one Epic as the module entry and index every Story from it.
- Keep a module as Epic-only when its work can be understood and accepted as one cohesive page.
- Split Stories when a module has multiple independently testable workflows, substantial state transitions, complex forms, import/export, approval, relationship editing, or cross-client behavior.
- Keep shared platform work in a dedicated foundation Epic only when it supports multiple pages.
- Make every Story independently developable and testable.

## Completion Criteria

- Produce `PRD.md`, `todolist/README.md`, page-module Epic/Story files, and a field dictionary when the workbook contains field definitions.
- Cover every source function with at least one `FR-*` requirement and one TODO location.
- Include acceptance criteria and open questions.
- Keep all Markdown relative links valid.
- Report workbook counts, requirement counts, Epic/Story counts, TODO count, and any unresolved source discrepancy.
