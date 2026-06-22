"""Modèles de données SQLModel pour QuestBoard.

V0 technique : seul le modèle ``Task`` est nécessaire pour valider la boucle
« créer → terminer → calculer XP/or ». Les modèles RPG (Company, Adventurer,
Expedition…) viendront avec le MVP Camp (voir docs/cadrage-projet.md §8).
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from enum import Enum

from sqlmodel import Field, SQLModel


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class TaskStatus(str, Enum):
    inbox = "inbox"
    todo = "todo"
    in_progress = "in_progress"
    waiting = "waiting"
    planned = "planned"
    done = "done"
    abandoned = "abandoned"


class TaskType(str, Enum):
    incident = "incident"
    interruption = "interruption"
    exploitation = "exploitation"
    project = "project"
    audit = "audit"
    documentation = "documentation"
    script = "script"
    communication = "communication"
    meeting = "meeting"
    analysis = "analysis"
    followup = "followup"
    watch = "watch"
    improvement = "improvement"
    change = "change"
    user_ticket = "user_ticket"


class TaskPriority(str, Enum):
    low = "low"
    normal = "normal"
    high = "high"
    critical = "critical"


class TaskDifficulty(str, Enum):
    trivial = "trivial"
    easy = "easy"
    normal = "normal"
    hard = "hard"
    complex = "complex"
    major = "major"


class ProjectStatus(str, Enum):
    active = "active"
    archived = "archived"


class Project(SQLModel, table=True):
    """Projet / regroupement de tâches, rangé par domaine (libre)."""

    id: int | None = Field(default=None, primary_key=True)
    name: str
    domain: str = ""
    description: str = ""
    status: ProjectStatus = ProjectStatus.active
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)


class Task(SQLModel, table=True):
    """Tâche du Dashboard.

    Conformément à la décision §4.3 du cadrage, l'or n'est pas stocké sur la
    tâche : il est calculé à la clôture à partir de la priorité et destiné à
    être crédité à la compagnie. Seul ``xp_reward`` est persisté.
    """

    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str = ""
    notes: str = ""
    type: TaskType = TaskType.exploitation
    priority: TaskPriority = TaskPriority.normal
    difficulty: TaskDifficulty = TaskDifficulty.normal
    status: TaskStatus = TaskStatus.todo
    # Dates de pilotage (vue Aujourd'hui / relances). planned_date est simplifié
    # en `date` pour la vue jour ; le créneau horaire viendra avec le calendrier.
    planned_date: date | None = None
    due_date: date | None = None
    followup_date: date | None = None
    project_id: int | None = Field(default=None, foreign_key="project.id")
    xp_reward: int = 0
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)
    completed_at: datetime | None = None
