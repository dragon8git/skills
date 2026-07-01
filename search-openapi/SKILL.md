---
name: search-openapi
description: Search and slice a local OpenAPI JSON spec, especially api.openai.json, by exact API path, path prefix, or light fuzzy matching. Use when Codex needs one endpoint or an API family without loading the whole spec, such as requests like "show /api/subject/company/search", "find all /api/subject/company/ endpoints", or "inspect the local OpenAPI doc first".
---

# Search OpenAPI

Use the bundled script at `scripts/openapi-doc.mjs` to inspect a local OpenAPI JSON file with minimal context.

## Quick Start

1. Find the spec file.
   Prefer a user-named file. Otherwise prefer repo-root `api.openai.json`. If needed, search with `rg --files . | rg 'api\\.openai\\.json$|openapi.*\\.json$'`.
2. Prefer `show` over `search`.
3. Prefer an exact path query over fuzzy text.
4. Keep JSON compressed by default. Add `--pretty` only when human readability matters.

## Commands

Run the bundled script directly:

```bash
node /Users/lee/.codex/skills/search-openapi/scripts/openapi-doc.mjs show /api/subject/company/search --file /abs/path/api.openai.json
node /Users/lee/.codex/skills/search-openapi/scripts/openapi-doc.mjs show /api/subject/company/ --file /abs/path/api.openai.json
node /Users/lee/.codex/skills/search-openapi/scripts/openapi-doc.mjs show company --file /abs/path/api.openai.json --limit 10
```

If the workspace already has a compatible local `bin/openapi-doc.mjs`, you may use that instead of the bundled script.

## Output Rules

- `show <exact-path>` returns one object.
- `show <path-prefix>` returns an array of full endpoint objects.
- `show <fuzzy-query>` returns an array of full endpoint objects.
- `search <query>` is compatibility-only and returns summary objects.
- `inferredEntity` is heuristic. Treat it as a hint, not schema truth.

## Working Rules

- For agent-to-agent work, pass exact path or path prefix whenever possible.
- When the user asks about one endpoint, return only that endpoint's object or a concise summary of its fields.
- When the user asks about an API family, use a path prefix query first; only fall back to fuzzy matching if there is no stable prefix.
- If no result is found, report the command and the miss instead of guessing fields.
