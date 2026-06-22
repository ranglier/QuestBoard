"""Schémas d'entrée/sortie de l'API (séparés des modèles de table)."""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel

from .models import TaskDifficulty, TaskPriority, TaskStatus, TaskType


class TaskCreate(BaseModel):
    """Capture rapide : seul le titre est obligatoire.

    Si ``difficulty`` est absent, il est déduit du type (cf. scoring).
    """

    title: str
    description: str = ""
    notes: str = ""
    type: TaskType = TaskType.exploitation
    priority: TaskPriority = TaskPriority.normal
    difficulty: TaskDifficulty | None = None
    status: TaskStatus = TaskStatus.todo
    planned_date: date | None = None
    due_date: date | None = None
    followup_date: date | None = None


class TaskUpdate(BaseModel):
    """Mise à jour partielle d'une tâche (transitions de statut, dates, notes).

    La clôture passe par ``POST /tasks/{id}/complete`` (calcul XP/or) : ce schéma
    n'accepte pas le passage au statut ``done``.
    """

    title: str | None = None
    description: str | None = None
    notes: str | None = None
    type: TaskType | None = None
    priority: TaskPriority | None = None
    difficulty: TaskDifficulty | None = None
    status: TaskStatus | None = None
    planned_date: date | None = None
    due_date: date | None = None
    followup_date: date | None = None


class TaskRead(BaseModel):
    id: int
    title: str
    description: str
    notes: str
    type: TaskType
    priority: TaskPriority
    difficulty: TaskDifficulty
    status: TaskStatus
    planned_date: date | None
    due_date: date | None
    followup_date: date | None
    xp_reward: int
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None

    model_config = {"from_attributes": True}


class CompletionResult(BaseModel):
    """Résultat d'une clôture : XP et or gagnés sur cette tâche."""

    task: TaskRead
    xp_gained: int
    gold_gained: int


class Stats(BaseModel):
    """Totaux dérivés des tâches terminées (V0 : pas encore de Company)."""

    total_xp: int
    total_gold: int
    completed_tasks: int
