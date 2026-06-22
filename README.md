# QuestBoard

QuestBoard is a local-first work dashboard with an idle RPG layer powered by completed tasks.

The project is designed as a personal productivity tool: the **Dashboard** helps track work tasks, planning, projects, notes and follow-ups, while the **Camp** provides a short break experience through a lightweight expedition-based RPG.

## Project status

QuestBoard is currently in the **framing and early prototyping** phase.

The current goal is to build a first local MVP that validates the core loop:

> Capture a task → track it → complete it → earn XP / gold / provisions → launch an expedition → collect a short narrative report and rewards.

## Planned architecture

- **Frontend**: SvelteKit
- **Backend**: FastAPI
- **Database**: SQLite
- **Deployment**: local-first with Docker Compose
- **Game loop**: lightweight idle RPG with one expedition active in the MVP

## Repository layout

```text
.
├── backend/        # FastAPI application
├── frontend/       # SvelteKit application
├── docs/           # Product framing, MVP and textual mockups
├── data/           # Local runtime data, ignored by Git
├── exports/        # Generated exports, ignored by Git
├── backups/        # Local backups, ignored by Git
└── scripts/        # Utility scripts
```

## Documentation

Start here:

- [Project framing](docs/cadrage-projet.md)
- [MVP scope](docs/fiche-mvp.md)
- [Textual mockups](docs/maquettes-textuelles.md)

## Local development

The repository is prepared for Docker Compose from the beginning.

```bash
docker compose up --build
```

> **Windows note:** Docker Desktop needs a backend engine. If `docker compose up`
> reports the daemon is unreachable, enable WSL2 first (`wsl --install`, requires
> admin rights and a reboot), then start Docker Desktop. If neither WSL2 nor
> Hyper-V is available, use the native run described below.

Expected local services:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Backend healthcheck: http://localhost:8000/health

### V0 task loop

The technical V0 validates the core stack end to end: create a task, complete
it, and see the computed XP/gold. From the frontend at http://localhost:5173 you
can capture a task, then click **Terminer** to credit XP (from difficulty) and
gold (from priority), per the scoring rules in `docs/cadrage-projet.md` §5.

API surface (V0):

- `POST /tasks` — create a task (only `title` is required)
- `GET /tasks` — list tasks
- `POST /tasks/{id}/complete` — complete a task, returns XP/gold gained
- `GET /stats` — aggregated XP/gold over completed tasks

Backend tests:

```bash
cd backend
pip install -e ".[dev]"
pytest
```

### Run without Docker (local toolchains)

On a machine without Docker (or while WSL2 is being set up), QuestBoard can run
natively. This expects **portable toolchains** under `.tools/` (git-ignored,
no admin rights required):

- `.tools/Python312/python.exe` — Python 3.12 with backend deps installed via
  `python -m pip install -e "backend[dev]"`
- `.tools/node/` — a portable Node.js (e.g. v22) extracted there

Then launch both servers from PowerShell:

```powershell
pwsh -File scripts\dev-local.ps1
```

This starts uvicorn (http://127.0.0.1:8000) and Vite (http://127.0.0.1:5173).

> **Proxy note:** a corporate proxy may intercept `localhost`. If the browser
> cannot reach the API, add `127.0.0.1` and `localhost` to the proxy exceptions
> (`NO_PROXY`).

## Data policy

QuestBoard is intended to be local-first. Real professional data, secrets, tokens, credentials and sensitive operational details must not be committed to this repository.

The `data/`, `exports/` and `backups/` folders are intentionally ignored except for their README files.
