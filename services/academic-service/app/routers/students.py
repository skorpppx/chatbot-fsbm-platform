"""Routes /api/students — gestion des étudiants (admin/scolarité)."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import Student, Filiere, Department
from app.schemas.academic import StudentOut, StudentDetail, PaginatedResponse

router = APIRouter(prefix="/api/students", tags=["students"])


@router.get("",
            response_model=PaginatedResponse[StudentOut],
            summary="Lister les étudiants (paginé, filtré)")
async def list_students(
    filiere_id: int | None = Query(None),
    annee_etude: int | None = Query(None, ge=1, le=5),
    statut: str | None = Query(None, description="ACTIF, SUSPENDU, DIPLOME, ABANDON"),
    is_boursier: bool | None = Query(None),
    search: str | None = Query(None, description="Nom, prénom, CNE, email"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Student)
    count_stmt = select(func.count(Student.id))

    if filiere_id:
        stmt = stmt.where(Student.filiere_id == filiere_id)
        count_stmt = count_stmt.where(Student.filiere_id == filiere_id)
    if annee_etude:
        stmt = stmt.where(Student.annee_etude == annee_etude)
        count_stmt = count_stmt.where(Student.annee_etude == annee_etude)
    if statut:
        stmt = stmt.where(Student.statut == statut)
        count_stmt = count_stmt.where(Student.statut == statut)
    if is_boursier is not None:
        stmt = stmt.where(Student.is_boursier == is_boursier)
        count_stmt = count_stmt.where(Student.is_boursier == is_boursier)
    if search:
        like = f"%{search}%"
        cond = or_(
            Student.first_name.like(like),
            Student.last_name.like(like),
            Student.cne.like(like),
            Student.email.like(like),
        )
        stmt = stmt.where(cond)
        count_stmt = count_stmt.where(cond)

    total = await db.scalar(count_stmt) or 0
    stmt = stmt.order_by(Student.last_name, Student.first_name)
    stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(stmt)
    items = result.scalars().all()

    return PaginatedResponse[StudentOut](
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/{student_id}",
            response_model=StudentDetail,
            summary="Détail d'un étudiant")
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    student = await db.get(Student, student_id)
    if not student:
        raise HTTPException(404, f"Étudiant {student_id} non trouvé")
    fil = await db.get(Filiere, student.filiere_id)
    dept = await db.get(Department, fil.department_id) if fil else None
    return StudentDetail(
        **{c.name: getattr(student, c.name) for c in student.__table__.columns},
        filiere_name=fil.name if fil else None,
        department_name=dept.name if dept else None,
        full_name=f"{student.first_name} {student.last_name}",
    )


@router.get("/cne/{cne}",
            response_model=StudentDetail,
            summary="Récupérer un étudiant par CNE")
async def get_student_by_cne(cne: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.cne == cne))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(404, f"Étudiant avec CNE {cne} non trouvé")
    return await get_student(student.id, db)


@router.get("/stats/by-filiere",
            summary="Statistiques d'effectifs par filière")
async def stats_by_filiere(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            Filiere.code, Filiere.name, Filiere.type,
            func.count(Student.id).label("nb_students"),
            func.sum(func.cast(Student.is_boursier, type_=func.cast(0, type_=func.cast(0).type))).label("nb_boursiers"),
        )
        .join(Student, Student.filiere_id == Filiere.id, isouter=True)
        .group_by(Filiere.id)
        .order_by(Filiere.type, Filiere.name)
    )
    return [
        {"code": r[0], "name": r[1], "type": r[2], "nb_students": r[3]}
        for r in result.all()
    ]
