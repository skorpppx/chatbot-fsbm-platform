"""
CRUD ADMIN — Départements (logos) + Clubs (vie étudiante).
Protégé par get_current_admin (JWT). PHASE 2.
Préfixe : /api/admin
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.core.security import get_current_admin
from app.db.session import get_db
from app.models import Department, Club
from app.schemas.academic import DepartmentOut, ClubOut
from app.schemas.admin import (
    DepartmentCreate, DepartmentUpdate,
    ClubCreate, ClubUpdate, DeleteResponse,
)

router = APIRouter(prefix="/api/admin", tags=["admin-misc"],
                   dependencies=[Depends(get_current_admin)])


# ─── DÉPARTEMENTS ─────────────────────────────────────────────────────────────
@router.post("/departments", response_model=DepartmentOut, status_code=status.HTTP_201_CREATED)
async def admin_create_department(payload: DepartmentCreate, db: AsyncSession = Depends(get_db)):
    now = datetime.utcnow()
    obj = Department(**payload.model_dump(), created_at=now, updated_at=now)
    db.add(obj)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "Code département déjà utilisé.")
    await db.refresh(obj)
    return obj


@router.put("/departments/{item_id}", response_model=DepartmentOut)
async def admin_update_department(item_id: int, payload: DepartmentUpdate,
                                  db: AsyncSession = Depends(get_db)):
    obj = await db.get(Department, item_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Département introuvable.")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    obj.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/departments/{item_id}", response_model=DeleteResponse)
async def admin_delete_department(item_id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Department, item_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Département introuvable.")
    try:
        await db.delete(obj)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Impossible : des filières/professeurs sont rattachés à ce département.",
        )
    return DeleteResponse(deleted_id=item_id, message="Département supprimé.")


# ─── CLUBS (vie étudiante) ────────────────────────────────────────────────────
@router.get("/clubs", response_model=list[ClubOut])
async def admin_list_clubs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Club).order_by(Club.name))
    return result.scalars().all()


@router.post("/clubs", response_model=ClubOut, status_code=status.HTTP_201_CREATED)
async def admin_create_club(payload: ClubCreate, db: AsyncSession = Depends(get_db)):
    obj = Club(**payload.model_dump(), created_at=datetime.utcnow())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/clubs/{item_id}", response_model=ClubOut)
async def admin_update_club(item_id: int, payload: ClubUpdate,
                            db: AsyncSession = Depends(get_db)):
    obj = await db.get(Club, item_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Club introuvable.")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/clubs/{item_id}", response_model=DeleteResponse)
async def admin_delete_club(item_id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Club, item_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Club introuvable.")
    await db.delete(obj)
    await db.commit()
    return DeleteResponse(deleted_id=item_id, message="Club supprimé.")
