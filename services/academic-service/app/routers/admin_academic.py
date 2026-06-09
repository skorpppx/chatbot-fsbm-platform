"""
CRUD ADMIN — Filières, Modules, Professeurs.
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
from app.models import Filiere, Module, Professor
from app.schemas.academic import FiliereOut, ModuleOut, ProfessorOut
from app.schemas.admin import (
    FiliereCreate, FiliereUpdate,
    ModuleCreate, ModuleUpdate,
    ProfessorCreate, ProfessorUpdate,
    DeleteResponse,
)

router = APIRouter(prefix="/api/admin", tags=["admin-academic"],
                   dependencies=[Depends(get_current_admin)])


async def _commit_or_409(db: AsyncSession, msg: str):
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, msg)


# ─── FILIÈRES ─────────────────────────────────────────────────────────────────
@router.post("/filieres", response_model=FiliereOut, status_code=status.HTTP_201_CREATED)
async def admin_create_filiere(payload: FiliereCreate, db: AsyncSession = Depends(get_db)):
    now = datetime.utcnow()
    obj = Filiere(**payload.model_dump(), created_at=now, updated_at=now)
    db.add(obj)
    await _commit_or_409(db, "Code filière déjà utilisé.")
    await db.refresh(obj)
    return obj


@router.put("/filieres/{item_id}", response_model=FiliereOut)
async def admin_update_filiere(item_id: int, payload: FiliereUpdate,
                               db: AsyncSession = Depends(get_db)):
    obj = await db.get(Filiere, item_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Filière introuvable.")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    obj.updated_at = datetime.utcnow()
    await _commit_or_409(db, "Code filière déjà utilisé.")
    await db.refresh(obj)
    return obj


@router.delete("/filieres/{item_id}", response_model=DeleteResponse)
async def admin_delete_filiere(item_id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Filiere, item_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Filière introuvable.")
    try:
        await db.delete(obj)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Impossible : des étudiants/modules sont rattachés à cette filière.",
        )
    return DeleteResponse(deleted_id=item_id, message="Filière supprimée.")


# ─── MODULES ──────────────────────────────────────────────────────────────────
@router.post("/modules", response_model=ModuleOut, status_code=status.HTTP_201_CREATED)
async def admin_create_module(payload: ModuleCreate, db: AsyncSession = Depends(get_db)):
    now = datetime.utcnow()
    obj = Module(**payload.model_dump(), created_at=now, updated_at=now)
    db.add(obj)
    await _commit_or_409(db, "Code module déjà utilisé.")
    await db.refresh(obj)
    return obj


@router.put("/modules/{item_id}", response_model=ModuleOut)
async def admin_update_module(item_id: int, payload: ModuleUpdate,
                              db: AsyncSession = Depends(get_db)):
    obj = await db.get(Module, item_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Module introuvable.")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    obj.updated_at = datetime.utcnow()
    await _commit_or_409(db, "Code module déjà utilisé.")
    await db.refresh(obj)
    return obj


@router.delete("/modules/{item_id}", response_model=DeleteResponse)
async def admin_delete_module(item_id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Module, item_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Module introuvable.")
    await db.delete(obj)
    await db.commit()
    return DeleteResponse(deleted_id=item_id, message="Module supprimé.")


# ─── PROFESSEURS ──────────────────────────────────────────────────────────────
@router.post("/professors", response_model=ProfessorOut, status_code=status.HTTP_201_CREATED)
async def admin_create_professor(payload: ProfessorCreate, db: AsyncSession = Depends(get_db)):
    now = datetime.utcnow()
    obj = Professor(**payload.model_dump(), created_at=now, updated_at=now)
    db.add(obj)
    await _commit_or_409(db, "Matricule ou email déjà utilisé.")
    await db.refresh(obj)
    return obj


@router.put("/professors/{item_id}", response_model=ProfessorOut)
async def admin_update_professor(item_id: int, payload: ProfessorUpdate,
                                 db: AsyncSession = Depends(get_db)):
    obj = await db.get(Professor, item_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Professeur introuvable.")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    obj.updated_at = datetime.utcnow()
    await _commit_or_409(db, "Matricule ou email déjà utilisé.")
    await db.refresh(obj)
    return obj


@router.delete("/professors/{item_id}", response_model=DeleteResponse)
async def admin_delete_professor(item_id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Professor, item_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Professeur introuvable.")
    await db.delete(obj)
    await db.commit()
    return DeleteResponse(deleted_id=item_id, message="Professeur supprimé.")
