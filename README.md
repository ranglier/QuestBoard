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

Backend tests (inside the backend container):

```bash
docker compose run --rm backend sh -c "pip install -e '.[dev]' && pytest"
```

## Data policy

QuestBoard is intended to be local-first. Real professional data, secrets, tokens, credentials and sensitive operational details must not be committed to this repository.

The `data/`, `exports/` and `backups/` folders are intentionally ignored except for their README files.
