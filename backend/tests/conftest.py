"""Fixtures de test : base SQLite temporaire isolée et client FastAPI.

L'URL de base est fixée avant l'import de l'application pour que l'engine
pointe sur une base jetable et non sur la base de développement.
"""

import os
import tempfile
from pathlib import Path

_DB_PATH = Path(tempfile.gettempdir()) / "questboard_test.db"
os.environ["QUESTBOARD_DATABASE_URL"] = f"sqlite:///{_DB_PATH}"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlmodel import SQLModel  # noqa: E402

from app.db import engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(autouse=True)
def fresh_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
