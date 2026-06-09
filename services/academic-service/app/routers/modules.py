"""Routes /api/modules."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import Module, Filiere, Professor, ModuleTeacher
from app.schemas.academic import ModuleOut, ModuleDetail

router = APIRouter(prefix="/api/modules", tags=["modules"])


@router.get("",
            response_model=list[ModuleOut],
            summary="Lister les modules (filtres : filière, semestre, recherche)")
async def list_modules(
    filiere_id: int | None = Query(None),
    semester: int | None = Query(None, ge=1, le=6),
    search: str | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Module)
    if filiere_id:
        stmt = stmt.where(Module.filiere_id == filiere_id)
    if semester:
        stmt = stmt.where(Module.semester == semester)
    if search:
        like = f"%{search}%"
        stmt = stmt.where(or_(Module.name.like(like), Module.code.like(like)))
    stmt = stmt.order_by(Module.semester, Module.code).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{module_id}",
            response_model=ModuleDetail,
            summary="Détail d'un module avec ses enseignants")
async def get_module(module_id: int, db: AsyncSession = Depends(get_db)):
    mod = await db.get(Module, module_id)
    if not mod:
        raise HTTPException(404, f"Module {module_id} non trouvé")
    fil = await db.get(Filiere, mod.filiere_id)

    # Enseignants
    teachers_q = await db.execute(
        select(Professor.first_name, Professor.last_name, ModuleTeacher.role)
        .join(ModuleTeacher, ModuleTeacher.professor_id == Professor.id)
        .where(ModuleTeacher.module_id == module_id)
    )
    teachers = [f"{r[0]} {r[1]} ({r[2]})" for r in teachers_q.all()]

    return ModuleDetail(
        **{c.name: getattr(mod, c.name) for c in mod.__table__.columns},
        filiere_name=fil.name if fil else None,
        teachers=teachers,
        total_hours=mod.hours_cours + mod.hours_td + mod.hours_tp,
    )


@router.get("/code/{code}",
            response_model=ModuleDetail,
            summary="Récupérer un module par son code")
async def get_module_by_code(code: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Module).where(Module.code == code))
    mod = result.scalar_one_or_none()
    if not mod:
        raise HTTPException(404, f"Module de code '{code}' non trouvé")
    return await get_module(mod.id, db)
