"""Point d'entrée de l'API QuestBoard (V0 technique).

Valide la boucle minimale : créer une tâche, la terminer, voir XP/or calculés.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from .db import get_session, init_db
from .routers import projects, tasks
from .routers.tasks import compute_stats
from .schemas import Stats


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="QuestBoard API", version="0.1.0", lifespan=lifespan)

# Local-first : le frontend SvelteKit (5173) appelle l'API (8000). En usage
# strictement local, on autorise toutes les origines pour simplifier la V0.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)
app.include_router(projects.router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"service": "QuestBoard API", "status": "ok"}


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/stats", response_model=Stats, tags=["stats"])
def get_stats(session: Session = Depends(get_session)) -> Stats:
    return compute_stats(session)
