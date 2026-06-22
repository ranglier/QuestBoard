"""Endpoints projets : création, liste, détail (avec tâches), mise à jour."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..db import get_session
from ..models import Project, ProjectStatus, Task
from ..schemas import ProjectCreate, ProjectDetail, ProjectRead, ProjectUpdate, TaskRead

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, session: Session = Depends(get_session)) -> Project:
    project = Project(name=payload.name, domain=payload.domain, description=payload.description)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.get("", response_model=list[ProjectRead])
def list_projects(
    include_archived: bool = False, session: Session = Depends(get_session)
) -> list[Project]:
    query = select(Project)
    if not include_archived:
        query = query.where(Project.status == ProjectStatus.active)
    return list(session.exec(query.order_by(Project.created_at.desc())).all())


@router.get("/{project_id}", response_model=ProjectDetail)
def get_project(project_id: int, session: Session = Depends(get_session)) -> ProjectDetail:
    project = session.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Projet introuvable")
    tasks = session.exec(
        select(Task).where(Task.project_id == project_id).order_by(Task.created_at.desc())
    ).all()
    detail = ProjectDetail.model_validate(project)
    detail.tasks = [TaskRead.model_validate(t) for t in tasks]
    return detail


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int, payload: ProjectUpdate, session: Session = Depends(get_session)
) -> Project:
    project = session.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Projet introuvable")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    project.updated_at = datetime.now(timezone.utc)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project
