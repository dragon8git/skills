---
name: init-project
description: Initialize a new frontend, backend, or full-stack software project with customizable technology choices, sensible defaults, repository hygiene, starter functionality, and end-to-end verification. Use when the user asks to create, scaffold, bootstrap, or initialize an application, especially when they mention frontend/backend directories, framework or database choices, README documentation, gitignore rules, dependency setup, migrations, or a runnable starter.
---

# Init Project

Initialize production-shaped project scaffolds without overbuilding application features.

## Workflow

1. Inspect the target directory, existing files, repository state, local runtimes, and package managers.
2. Preserve existing work. Never overwrite a non-empty target directory or replace unrelated files without understanding them.
3. Determine whether the request needs a frontend, backend, or both.
4. Use user-specified technologies when provided. For unspecified choices, use the defaults in [references/stack-options.md](references/stack-options.md).
5. Ask only about unresolved choices that materially change architecture. Prefer the defaults when the user asks for a standard setup or grants discretion.
6. Verify current scaffold commands and framework integration patterns from local CLI help or official documentation when they may have changed.
7. Generate the framework-native scaffold first, then integrate additional libraries using their supported CLIs.
8. Add a small runnable vertical slice that proves the selected technologies work together.
9. Add root project hygiene and usage documentation.
10. Install dependencies and run all relevant validation before reporting completion.

## Required Project Quality

For every generated project:

- Use separate `frontend/` and `backend/` directories for a full-stack request unless the user specifies another layout.
- Avoid nested Git repositories created by framework scaffolds when initializing inside a larger project.
- Generate lock files for the selected package managers.
- Add `.env.example` files for runtime configuration. Never commit secrets.
- Add or update a root `.gitignore` covering dependencies, build outputs, virtual environments, caches, local databases, and environment files.
- Add or update a root `README.md` with exact install, migration, development, test, and build commands.
- Keep generated code typed, formatted, lintable, and organized according to the selected frameworks.
- Pin Python direct dependencies in `requirements.txt` when pip is selected.
- Add health checks and database migrations when the backend stack supports them.
- Configure frontend-to-backend URL and backend CORS for local development when both sides are generated.

## Default Vertical Slice

When the user requests a runnable starter rather than dependencies only:

- Frontend: render a concise starter page demonstrating the chosen UI and styling systems, with a visible backend health status when a backend exists.
- Backend: expose `GET /health` and a small `Item` CRUD resource with validation, persistence, and not-found behavior.
- Database: default to a local development database and allow switching to the requested production database through `DATABASE_URL`.
- Migration: create and run an initial migration rather than creating tables implicitly at application startup.
- Tests: cover the health endpoint and the complete CRUD lifecycle.

Do not add authentication, Docker, deployment manifests, CI, or domain-specific features unless requested.

## Custom Technology Choices

Accept replacements for any default, including:

- Frontend framework, language, router, styling, component libraries, state management, and package manager.
- Backend language, framework, dependency manager, ORM, migration tool, sync/async database access, and database engines.
- Monorepo layout, test framework, linting, formatting, containers, and deployment targets.

Adapt the scaffold, commands, environment variables, documentation, and tests consistently. Do not install default technologies that the user replaced.

Read [references/stack-options.md](references/stack-options.md) when choosing defaults or mapping common alternatives.

## Validation

Run checks appropriate to the selected stack:

- Frontend dependency install, lint, type check if separate, tests when present, and production build.
- Backend isolated environment creation, dependency install, syntax/import checks, migrations, and tests.
- Confirm generated CLIs resolve from the project environment.
- Remove disposable databases, caches, and test artifacts after verification; keep lock files and environments only when appropriate for the workspace.
- Report the exact checks run and any warning or validation that could not be completed.

If a toolchain failure is environment-specific, diagnose it and try another compatible installed runtime before weakening project requirements.
