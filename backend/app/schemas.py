"""Schémas d'entrée/sortie de l'API (séparés des modèles de table)."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from .models import TaskDifficulty, TaskPriority, TaskStatus, TaskType


class TaskCreate(BaseModel):
    """Capture rapide : seul le titre est obligatoire.

    Si ``difficulty`` est absent, il est déduit du type (cf. scoring).
    """

    title: str
    description: str = ""
    type: TaskType = TaskType.exploitation
    priority: TaskPriority = TaskPriority.normal
    difficulty: TaskDifficulty | None = None


class TaskRead(BaseModel):
    id: int
    title: str
    description: str
    type: TaskType
    priority: TaskPriority
    difficulty: TaskDifficulty
    status: TaskStatus
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
