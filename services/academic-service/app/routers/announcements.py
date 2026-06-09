"""Routes /api/announcements, /api/events, /api/clubs."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import Announcement, Event, Club
from app.schemas.academic import AnnouncementOut, EventOut, ClubOut

router = APIRouter(tags=["announcements"])


@router.get("/api/announcements",
            response_model=list[AnnouncementOut],
            summary="Annonces officielles (récentes en premier)")
async def list_announcements(
    limit: int = Query(20, ge=1, le=100),
    type: str | None = Query(None, description="INFO, URGENT, EXAMEN, EVENT, VACANCE"),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Announcement)
    if type:
        stmt = stmt.where(Announcement.type == type)
    stmt = stmt.order_by(Announcement.is_pinned.desc(), Announcement.published_at.desc()).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/api/events",
            response_model=list[EventOut],
            summary="Événements universitaires à venir")
async def list_events(
    upcoming_only: bool = Query(True),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    from datetime import datetime
    stmt = select(Event)
    if upcoming_only:
        stmt = stmt.where(Event.start_date >= datetime.utcnow())
    stmt = stmt.order_by(Event.start_date).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/api/clubs",
            response_model=list[ClubOut],
            summary="Clubs étudiants actifs")
async def list_clubs(
    category: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Club).where(Club.is_active == True)
    if category:
        stmt = stmt.where(Club.category == category)
    stmt = stmt.order_by(Club.members_count.desc())
    result = await db.execute(stmt)
    return result.scalars().all()
