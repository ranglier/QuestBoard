"""Connexion SQLite et gestion de session.

L'URL est lue depuis ``QUESTBOARD_DATABASE_URL`` (cf. .env.example / compose).
Par défaut, une base locale ``questboard.db`` est créée dans le dossier courant
pour permettre un lancement hors Docker.
"""

from __future__ import annotations

import os
from collections.abc import Iterator

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.environ.get("QUESTBOARD_DATABASE_URL", "sqlite:///./questboard.db")

# check_same_thread=False : nécessaire pour SQLite servi par plusieurs threads
# (uvicorn). Sans incidence en local-first mono-utilisateur.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def init_db() -> None:
    """Crée les tables manquantes (V0 : pas de migrations Alembic)."""
    # Import nécessaire pour enregistrer les modèles auprès de SQLModel.
    from . import models  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
