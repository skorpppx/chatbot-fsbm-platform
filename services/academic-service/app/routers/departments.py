"""Routes /api/departments — départements de la FSBM."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import Department, Filiere, Professor
from app.schemas.academic import DepartmentOut, DepartmentDetail, PaginatedResponse

router = APIRouter(prefix="/api/departments", tags=["departments"])


@router.get("",
            response_model=list[DepartmentOut],
            summary="Lister tous les départements")
async def list_departments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Department).order_by(Department.id))
    return result.scalars().all()


@router.get("/{dept_id}",
            response_model=DepartmentDetail,
            summary="Détail d'un département")
async def get_department(dept_id: int, db: AsyncSession = Depends(get_db)):
    dept = await db.get(Department, dept_id)
    if not dept:
        raise HTTPException(404, f"Département {dept_id} non trouvé")

    fil_count = await db.scalar(
        select(func.count(Filiere.id)).where(Filiere.department_id == dept_id)
    )
    prof_count = await db.scalar(
        select(func.count(Professor.id)).where(Professor.department_id == dept_id)
    )

    return DepartmentDetail(
        **{c.name: getattr(dept, c.name) for c in dept.__table__.columns},
        filieres_count=fil_count or 0,
        professors_count=prof_count or 0,
    )


@router.get("/{dept_id}/filieres",
            summary="Filières d'un département")
async def department_filieres(dept_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Filiere).where(Filiere.department_id == dept_id).order_by(Filiere.name)
    )
    filieres = result.scalars().all()
    return {
        "department_id": dept_id,
        "total": len(filieres),
        "filieres": [
            {
                "id": f.id, "code": f.code, "name": f.name, "type": f.type,
                "capacity": f.capacity, "duration_years": f.duration_years,
            }
            for f in filieres
        ]
    }


@router.get("/{dept_id}/professors",
            summary="Professeurs d'un département")
async def department_professors(dept_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Professor).where(Professor.department_id == dept_id)
        .order_by(Professor.last_name, Professor.first_name)
    )
    profs = result.scalars().all()
    return {
        "department_id": dept_id,
        "total": len(profs),
        "professors": [
            {
                "id": p.id, "matricule": p.matricule,
                "full_name": f"{p.first_name} {p.last_name}",
                "email": p.email, "grade": p.grade, "specialty": p.specialty,
                "bureau": p.bureau,
            }
            for p in profs
        ]
    }
