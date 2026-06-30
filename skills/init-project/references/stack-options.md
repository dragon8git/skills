# Stack Options

## Default Full-Stack Selection

Use these choices when the user does not override them:

| Area | Default |
| --- | --- |
| Frontend | Next.js with React and TypeScript |
| Routing | Next.js App Router with `src/` layout |
| Styling | Tailwind CSS |
| UI | Ant Design and shadcn/ui |
| Frontend package manager | pnpm |
| Backend | Python 3.13+ with FastAPI |
| Python dependencies | pip and `requirements.txt` |
| ORM | SQLAlchemy 2 synchronous ORM |
| Migrations | Alembic |
| Local database | SQLite |
| Production database option | PostgreSQL through `DATABASE_URL` |
| PostgreSQL driver | psycopg 3 |
| Backend tests | pytest and framework test client |

Use current stable compatible versions resolved by the official scaffold and package
managers. Pin direct Python dependencies after confirming runtime compatibility.

## Default Layout

```text
project-root/
├── frontend/
│   ├── src/app/
│   ├── src/components/ui/
│   ├── .env.example
│   ├── package.json
│   └── pnpm-lock.yaml
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routers/
│   │   └── schemas/
│   ├── alembic/
│   ├── tests/
│   ├── .env.example
│   ├── alembic.ini
│   └── requirements.txt
├── .gitignore
└── README.md
```

## Common Alternatives

Map user choices directly and remove superseded defaults:

| User choice | Adaptation |
| --- | --- |
| JavaScript | Do not generate TypeScript-only configuration or types |
| npm, Yarn, Bun | Use that manager and its lock file instead of pnpm |
| Vue, Nuxt, Vite React, SvelteKit | Use the framework's official scaffold and conventions |
| Material UI, Chakra UI, Mantine | Install only requested UI libraries |
| Django, Flask, Litestar | Use that framework's native structure and tests |
| Poetry, uv, Pipenv | Use its manifest, lock file, environment, and commands instead of `requirements.txt` |
| Async SQLAlchemy | Use `AsyncSession` plus async database drivers consistently |
| PostgreSQL only | Make PostgreSQL the default and do not imply SQLite compatibility |
| MySQL or another database | Use a compatible driver, URL, migration setup, and test strategy |
| No example CRUD | Generate only the minimum health/startup surface requested |

When a combination is incompatible, explain the conflict and choose the nearest
compatible implementation only after obtaining user intent.
