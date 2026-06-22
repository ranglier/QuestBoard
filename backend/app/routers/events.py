"""Endpoints calendrier local : événements (vue semaine)."""

from __future__ import annotations

from datetime import date as date_type
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from ..db import get_session
from ..models import CalendarEvent
from ..schemas import EventCreate, EventRead, EventUpdate

router = APIRouter(prefix="/events", tags=["events"])


@router.post("", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(payload: EventCreate, session: Session = Depends(get_session)) -> CalendarEvent:
    event = CalendarEvent(**payload.model_dump())
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@router.get("", response_model=list[EventRead])
def list_events(
    start: date_type | None = Query(default=None),
    end: date_type | None = Query(default=None),
    session: Session = Depends(get_session),
) -> list[CalendarEvent]:
    query = select(CalendarEvent)
    if start is not None:
        query = query.where(CalendarEvent.event_date >= start)
    if end is not None:
        query = query.where(CalendarEvent.event_date <= end)
    return list(
        session.exec(query.order_by(CalendarEvent.event_date, CalendarEvent.start_time)).all()
    )


@router.patch("/{event_id}", response_model=EventRead)
def update_event(
    event_id: int, payload: EventUpdate, session: Session = Depends(get_session)
) -> CalendarEvent:
    event = session.get(CalendarEvent, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Événement introuvable")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(event, field, value)
    event.updated_at = datetime.now(timezone.utc)
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, session: Session = Depends(get_session)) -> None:
    event = session.get(CalendarEvent, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Événement introuvable")
    session.delete(event)
    session.commit()
