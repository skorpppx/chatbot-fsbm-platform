"""Routes /api/exams — examens."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import Exam, Module

router = APIRouter(prefix="/api/exams", tags=["exams"])


@router.get("",
            summary="Calendrier des examens (filtré)")
async def get_exams(
    filiere_id: int | None = Query(None),
    session: str = Query("NORMALE_S2", description="NORMALE_S1, NORMALE_S2, RATTRAPAGE"),
    annee_univ: str = Query("2025-2026"),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Exam, Module.name.label("module_name"), Module.code.label("module_code"),
               Module.semester.label("semester"))
        .join(Module, Module.id == Exam.module_id)
        .where(Exam.session == session)
        .where(Exam.annee_univ == annee_univ)
    )
    if filiere_id:
        stmt = stmt.where(Exam.filiere_id == filiere_id)
    stmt = stmt.order_by(Exam.exam_date, Exam.start_time)
    result = await db.execute(stmt)
    rows = result.all()
    exams = []
    for ex, mod_name, mod_code, semester in rows:
        exams.append({
            "id": ex.id,
            "module_code": mod_code,
            "module_name": mod_name,
            "semester": semester,
            "exam_date": ex.exam_date.isoformat(),
            "start_time": ex.start_time.strftime("%H:%M"),
            "duration_min": ex.duration_min,
            "salle": ex.salle,
            "session": ex.session,
            "surveillants": ex.surveillants,
            "consignes": ex.consignes,
        })
    return {
        "filiere_id": filiere_id,
        "session": session,
        "annee_univ": annee_univ,
        "total_exams": len(exams),
        "exams": exams,
    }
