"""Calcul du scoring XP / or.

Règles issues de docs/cadrage-projet.md §5 et docs/economie-rpg.md :
- l'XP récompense la complexité (barème par difficulté) ;
- l'or récompense la priorité (barème par priorité) ;
- la difficulté par défaut découle du type seul, corrigeable à la main ;
- le niveau ``major`` (Boss) n'est jamais attribué automatiquement.

Les bonus automatiques et la répartition compagnie/capitaine arriveront avec
le MVP scoring complet ; la V0 se limite au socle XP/or.
"""

from __future__ import annotations

from .models import TaskDifficulty, TaskPriority, TaskType

XP_BY_DIFFICULTY: dict[TaskDifficulty, int] = {
    TaskDifficulty.trivial: 5,
    TaskDifficulty.easy: 10,
    TaskDifficulty.normal: 25,
    TaskDifficulty.hard: 50,
    TaskDifficulty.complex: 80,
    TaskDifficulty.major: 150,
}

GOLD_BY_PRIORITY: dict[TaskPriority, int] = {
    TaskPriority.low: 2,
    TaskPriority.normal: 5,
    TaskPriority.high: 15,
    TaskPriority.critical: 35,
}

# Difficulté par défaut déduite du type (jamais ``major`` automatiquement).
DEFAULT_DIFFICULTY_BY_TYPE: dict[TaskType, TaskDifficulty] = {
    TaskType.followup: TaskDifficulty.easy,
    TaskType.watch: TaskDifficulty.easy,
    TaskType.exploitation: TaskDifficulty.easy,
    TaskType.communication: TaskDifficulty.easy,
    TaskType.interruption: TaskDifficulty.easy,
    TaskType.meeting: TaskDifficulty.normal,
    TaskType.user_ticket: TaskDifficulty.normal,
    TaskType.documentation: TaskDifficulty.normal,
    TaskType.analysis: TaskDifficulty.normal,
    TaskType.improvement: TaskDifficulty.normal,
    TaskType.script: TaskDifficulty.hard,
    TaskType.audit: TaskDifficulty.hard,
    TaskType.change: TaskDifficulty.hard,
    TaskType.incident: TaskDifficulty.hard,
    TaskType.project: TaskDifficulty.complex,
}


def default_difficulty_for_type(task_type: TaskType) -> TaskDifficulty:
    """Difficulté suggérée à partir du type (défaut : ``normal``)."""
    return DEFAULT_DIFFICULTY_BY_TYPE.get(TaskType(task_type), TaskDifficulty.normal)


def xp_for_difficulty(difficulty: TaskDifficulty | str) -> int:
    return XP_BY_DIFFICULTY[TaskDifficulty(difficulty)]


def gold_for_priority(priority: TaskPriority | str) -> int:
    return GOLD_BY_PRIORITY[TaskPriority(priority)]
