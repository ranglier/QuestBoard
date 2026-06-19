"""Endpoints tâches : création, liste, clôture, statistiques (V0)."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..db import get_session
from ..models import Task, TaskStatus
from ..schemas import CompletionResult, Stats, TaskCreate, TaskRead
from ..scoring import default_difficulty_for_type, gold_for_priority, xp_for_difficulty

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, session: Session = Depends(get_session)) -> Task:
    difficulty = payload.difficulty or default_difficulty_for_type(payload.type)
    task = Task(
        title=payload.title,
        description=payload.description,
        type=payload.type,
        priority=payload.priority,
        difficulty=difficulty,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("", response_model=list[TaskRead])
def list_tasks(session: Session = Depends(get_session)) -> list[Task]:
    return list(session.exec(select(Task).order_by(Task.created_at.desc())).all())


@router.post("/{task_id}/complete", response_model=CompletionResult)
def complete_task(task_id: int, session: Session = Depends(get_session)) -> CompletionResult:
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Tâche introuvable")
    if task.status == TaskStatus.done:
        raise HTTPException(status_code=409, detail="Tâche déjà terminée")

    xp = xp_for_difficulty(task.difficulty)
    gold = gold_for_priority(task.priority)

    task.status = TaskStatus.done
    task.xp_reward = xp
    task.completed_at = datetime.now(timezone.utc)
    task.updated_at = task.completed_at
    session.add(task)
    session.commit()
    session.refresh(task)

    return CompletionResult(task=TaskRead.model_validate(task), xp_gained=xp, gold_gained=gold)


def compute_stats(session: Session) -> Stats:
    done = list(session.exec(select(Task).where(Task.status == TaskStatus.done)).all())
    total_xp = sum(t.xp_reward for t in done)
    total_gold = sum(gold_for_priority(t.priority) for t in done)
    return Stats(total_xp=total_xp, total_gold=total_gold, completed_tasks=len(done))
