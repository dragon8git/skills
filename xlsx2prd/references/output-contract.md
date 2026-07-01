# Output Contract

## Contents

1. Delivery structure
2. Source analysis
3. PRD standard
4. Epic and Story standard
5. Traceability
6. Quality checks

## 1. Delivery Structure

Use this default structure unless the user specifies another:

```text
OUTPUT_DIR/
├── PRD.md
├── 附录/
│   └── 字段字典.md          # only when field definitions exist
└── todolist/
    ├── README.md
    ├── 01-page-module/
    │   └── Epic1.md         # simple module
    └── 02-complex-module/
        ├── Epic2.md         # entry and Story index
        ├── Story2.1-name.md
        └── Story2.2-name.md
```

Use stable ASCII folder names where practical. File titles and content may follow the source language.

## 2. Source Analysis

Build a private working matrix with these columns:

| Source | Sheet | Row | System | Module | Function | Description | Estimate | Price | Requirement ID | Notes |
|---|---|---:|---|---|---|---|---:|---:|---|---|

Apply merged-cell values downward only to reconstruct hierarchy. Do not propagate function names, descriptions, estimates, or totals unless the workbook structure clearly requires it.

Check:

- number of sheets and used rows;
- numbered and unnumbered functions;
- field counts by layer/category;
- effort and price sums;
- displayed workbook totals versus calculated totals;
- placeholder values such as `--`, `TBD`, zero, or blank;
- contradictions in dimensions, categories, roles, states, and client scope.

Record source discrepancies in the PRD rather than repairing them silently.

## 3. PRD Standard

Include these sections when applicable:

1. Product overview
2. Goals and success outcomes
3. In scope
4. Out of scope
5. Users and roles
6. Core domain objects
7. Core business flows
8. State models
9. Functional requirements grouped by client/module
10. Field and validation principles
11. Non-functional requirements
12. Metrics
13. Acceptance baseline
14. Open product questions
15. Source estimate/quotation notes

### Requirement IDs

Use stable IDs:

- `FR-PC-001` for PC;
- `FR-MP-001` for mini program/mobile;
- `FR-ADM-001` for administration;
- choose another short client code when required.

Do not renumber IDs merely because document wording changes.

### Requirement Content

Each functional requirement should state observable behavior. Add:

- permissions and data scope;
- validation and failure behavior;
- state transition;
- audit/history effect;
- cross-client synchronization;
- acceptance conditions.

Avoid prescribing a technical stack unless the source or user requires one.

### Productization Boundary

Standard operability details may be added directly: loading, empty state, retry, validation, permission enforcement, audit, idempotency, and transaction integrity.

Material business behavior must remain an open question or recommendation: approval policy, deletion meaning, financial formula, matching threshold, retention period, role conflict, and legal/compliance decisions.

## 4. Epic and Story Standard

### `todolist/README.md`

Include:

- module index with links;
- Epic/Story decomposition mode;
- recommended implementation order;
- TODO status convention;
- global definition of done.

### Epic Entry

Include:

- title and associated `FR-*` range;
- goal;
- Story index for complex modules;
- Epic-level integration TODO;
- acceptance criteria;
- open questions.

### Story

Include:

- title and exact associated `FR-*` IDs;
- user story or outcome;
- flat `[ ]` TODO list;
- acceptance criteria;
- open questions when unresolved.

TODO items should be implementation-sized and testable. Cover frontend, backend, data, permissions, state, error handling, audit, and tests where relevant. Avoid vague items such as “complete page” or “optimize experience.”

### Split Heuristic

Split a Story when at least one condition is true:

- more than one distinct user workflow;
- separate state machines or approval paths;
- complex dynamic form or field engine;
- import/export or large asynchronous job;
- graph/tree relationship editing;
- evidence upload, offline draft, or weak-network behavior;
- likely independent development and acceptance ownership.

Do not split solely to make files similar in size.

## 5. Traceability

Maintain this chain:

```text
XLSX sheet/row -> FR-* in PRD -> Epic/Story -> TODO -> acceptance criteria
```

Every source function must map to a requirement. Every PRD requirement must appear in at least one Epic or Story. A Story may cover multiple requirements when they form one workflow.

For ambiguous source rows:

1. preserve the original intent in the functional requirement;
2. add the missing decision under `待产品确认`;
3. add a blocking TODO only if development genuinely cannot proceed without it.

## 6. Quality Checks

Before delivery:

- compare source function count with coverage matrix;
- verify field dictionary count against the workbook;
- recalculate effort and price totals independently;
- scan for unsupported claims presented as facts;
- verify all relative Markdown links;
- verify all `FR-*` IDs are unique and covered;
- verify each complex Epic indexes all Story files;
- count Epic, Story, and TODO items;
- ensure output lives in the user's requested directory.
