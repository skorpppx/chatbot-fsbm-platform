"""
CRUD ADMIN — Annonces, Événements, FAQ.
Toutes les routes sont protégées par get_current_admin (JWT). PHASE 2.
Préfixe : /api/admin
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_admin
from app.db.session import get_db
from app.models import User, Announcement, Event, FaqItem
from app.schemas.academic import AnnouncementOut, EventOut
from app.schemas.admin import (
    AnnouncementCreate, AnnouncementUpdate,
    EventCreate, EventUpdate,
    FaqItemCreate, FaqItemUpdate, FaqItemOut,
    DeleteResponse,
)

router = APIRouter(prefix="/api/admin", tags=["admin-content"],
                   dependencies=[Depends(get_current_admin)])


# ─── ANNONCES ─────────────────────────────────────────────────────────────────
@router.get("/announcements", response_model=list[AnnouncementOut])
async def admin_list_announcements(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Announcement).order_by(desc(Announcement.published_at)))
    return result.scalars().all()


@router.post("/announcements", response_model=AnnouncementOut,
             status_code=status.HTTP_201_CREATED)
async def admin_create_announcement(payload: AnnouncementCreate,
                                    db: AsyncSession = Depends(get_db)):
    now = datetime.utcnow()
    obj = Announcement(**payload.model_dump(), published_at=now, created_at=now)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/announcements/{item_id}", response_model=AnnouncementOut)
async def admin_update_announcement(item_id: int, payload: AnnouncementUpdate,
                                    db: AsyncSession = Depends(get_db)):
    obj = await db.get(Announcement, item_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Annonce introuvable.")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/announcements/{item_id}", response_model=DeleteResponse)
async def admin_delete_announcement(item_id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Announcement, item_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Annonce introuvable.")
    await db.delete(obj)
    await db.commit()
    return DeleteResponse(deleted_id=item_id, message="Annonce supprimée.")


# ─── ÉVÉNEMENTS ───────────────────────────────────────────────────────────────
@router.get("/events", response_model=list[EventOut])
async def admin_list_events(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event).order_by(desc(Event.start_date)))
    return result.scalars().all()


@router.post("/events", response_model=EventOut, status_code=status.HTTP_201_CREATED)
async def admin_create_event(payload: EventCreate, db: AsyncSession = Depends(get_db)):
    obj = Event(**payload.model_dump(), created_at=datetime.utcnow())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/events/{item_id}", response_model=EventOut)
async def admin_update_event(item_id: int, payload: EventUpdate,
                             db: AsyncSession = Depends(get_db)):
    obj = await db.get(Event, item_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Événement introuvable.")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/events/{item_id}", response_model=DeleteResponse)
async def admin_delete_event(item_id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Event, item_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Événement introuvable.")
    await db.delete(obj)
    await db.commit()
    return DeleteResponse(deleted_id=item_id, message="Événement supprimé.")


# ─── FAQ ──────────────────────────────────────────────────────────────────────
@router.get("/faq", response_model=list[FaqItemOut])
async def admin_list_faq(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FaqItem).order_by(FaqItem.intent_tag))
    return result.scalars().all()


@router.post("/faq", response_model=FaqItemOut, status_code=status.HTTP_201_CREATED)
async def admin_create_faq(payload: FaqItemCreate, db: AsyncSession = Depends(get_db)):
    now = datetime.utcnow()
    obj = FaqItem(**payload.model_dump(), consultations=0,
                  created_at=now, updated_at=now)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/faq/{item_id}", response_model=FaqItemOut)
async def admin_update_faq(item_id: int, payload: FaqItemUpdate,
                           db: AsyncSession = Depends(get_db)):
    obj = await db.get(FaqItem, item_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "FAQ introuvable.")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    obj.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/faq/{item_id}", response_model=DeleteResponse)
async def admin_delete_faq(item_id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(FaqItem, item_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "FAQ introuvable.")
    await db.delete(obj)
    await db.commit()
    return DeleteResponse(deleted_id=item_id, message="FAQ supprimée.")
