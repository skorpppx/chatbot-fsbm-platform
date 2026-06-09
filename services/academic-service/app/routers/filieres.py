"""Routes /api/filieres — filières (licences, masters, doctorat)."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import Filiere, Department, Module, Student
from app.schemas.academic import FiliereOut, FiliereDetail

router = APIRouter(prefix="/api/filieres", tags=["filieres"])


@router.get("",
            response_model=list[FiliereOut],
            summary="Lister les filières (filtres : type, département)")
async def list_filieres(
    type: str | None = Query(None, description="LICENCE, LICENCE_PRO, MASTER, MASTER_RECHERCHE, DOCTORAT"),
    department_id: int | None = Query(None),
    is_active: bool = Query(True),
    search: str | None = Query(None, description="Recherche par nom ou code"),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Filiere)
    if type:
        stmt = stmt.where(Filiere.type == type)
    if department_id:
        stmt = stmt.where(Filiere.department_id == department_id)
    if is_active is not None:
        stmt = stmt.where(Filiere.is_active == is_active)
    if search:
        like = f"%{search}%"
        stmt = stmt.where(or_(Filiere.name.like(like), Filiere.code.like(like)))
    stmt = stmt.order_by(Filiere.type, Filiere.name)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{filiere_id}",
            response_model=FiliereDetail,
            summary="Détail d'une filière")
async def get_filiere(filiere_id: int, db: AsyncSession = Depends(get_db)):
    fil = await db.get(Filiere, filiere_id)
    if not fil:
        raise HTTPException(404, f"Filière {filiere_id} non trouvée")
    dept = await db.get(Department, fil.department_id)
    mod_count = await db.scalar(select(func.count(Module.id)).where(Module.filiere_id == filiere_id))
    stu_count = await db.scalar(select(func.count(Student.id)).where(Student.filiere_id == filiere_id))
    return FiliereDetail(
        **{c.name: getattr(fil, c.name) for c in fil.__table__.columns},
        department_name=dept.name if dept else None,
        modules_count=mod_count or 0,
        students_count=stu_count or 0,
    )


@router.get("/code/{code}",
            response_model=FiliereDetail,
            summary="Récupérer une filière par son code (ex: SMI, DI, IADS)")
async def get_filiere_by_code(code: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Filiere).where(Filiere.code == code.upper()))
    fil = result.scalar_one_or_none()
    if not fil:
        raise HTTPException(404, f"Filière de code '{code}' non trouvée")
    dept = await db.get(Department, fil.department_id)
    mod_count = await db.scalar(select(func.count(Module.id)).where(Module.filiere_id == fil.id))
    stu_count = await db.scalar(select(func.count(Student.id)).where(Student.filiere_id == fil.id))
    return FiliereDetail(
        **{c.name: getattr(fil, c.name) for c in fil.__table__.columns},
        department_name=dept.name if dept else None,
        modules_count=mod_count or 0,
        students_count=stu_count or 0,
    )


@router.get("/{filiere_id}/modules",
            summary="Modules d'une filière (groupés par semestre)")
async def filiere_modules(
    filiere_id: int,
    semester: int | None = Query(None, ge=1, le=6),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Module).where(Module.filiere_id == filiere_id)
    if semester:
        stmt = stmt.where(Module.semester == semester)
    stmt = stmt.order_by(Module.semester, Module.code)
    result = await db.execute(stmt)
    modules = result.scalars().all()
    grouped: dict[int, list[dict]] = {}
    for m in modules:
        grouped.setdefault(m.semester, []).append({
            "id": m.id, "code": m.code, "name": m.name,
            "credits": m.credits, "coefficient": float(m.coefficient),
            "hours_cours": m.hours_cours, "hours_td": m.hours_td, "hours_tp": m.hours_tp,
            "is_eliminatory": m.is_eliminatory,
        })
    return {
        "filiere_id": filiere_id,
        "total_modules": len(modules),
        "by_semester": [{"semester": s, "modules": grouped[s]} for s in sorted(grouped.keys())],
    }
