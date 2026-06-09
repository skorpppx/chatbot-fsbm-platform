"""Routes /api/professors."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import Professor, Department
from app.schemas.academic import ProfessorOut, ProfessorDetail, PaginatedResponse

router = APIRouter(prefix="/api/professors", tags=["professors"])


@router.get("",
            response_model=PaginatedResponse[ProfessorOut],
            summary="Lister les professeurs (paginé)")
async def list_professors(
    department_id: int | None = Query(None),
    grade: str | None = Query(None, description="PA, PH, PES, VACATAIRE, EMERITE"),
    search: str | None = Query(None, description="Recherche par nom/prénom/spécialité"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Professor)
    count_stmt = select(func.count(Professor.id))

    if department_id:
        stmt = stmt.where(Professor.department_id == department_id)
        count_stmt = count_stmt.where(Professor.department_id == department_id)
    if grade:
        stmt = stmt.where(Professor.grade == grade)
        count_stmt = count_stmt.where(Professor.grade == grade)
    if search:
        like = f"%{search}%"
        cond = or_(
            Professor.first_name.like(like),
            Professor.last_name.like(like),
            Professor.specialty.like(like),
        )
        stmt = stmt.where(cond)
        count_stmt = count_stmt.where(cond)

    total = await db.scalar(count_stmt) or 0
    stmt = stmt.order_by(Professor.last_name, Professor.first_name)
    stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(stmt)
    items = result.scalars().all()

    return PaginatedResponse[ProfessorOut](
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/{prof_id}",
            response_model=ProfessorDetail,
            summary="Détail d'un professeur")
async def get_professor(prof_id: int, db: AsyncSession = Depends(get_db)):
    prof = await db.get(Professor, prof_id)
    if not prof:
        raise HTTPException(404, f"Professeur {prof_id} non trouvé")
    dept = await db.get(Department, prof.department_id)
    return ProfessorDetail(
        **{c.name: getattr(prof, c.name) for c in prof.__table__.columns},
        department_name=dept.name if dept else None,
        full_name=f"{prof.first_name} {prof.last_name}",
    )
