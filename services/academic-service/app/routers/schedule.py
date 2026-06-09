"""Routes /api/schedule — emplois du temps."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import Schedule, Module, Professor

router = APIRouter(prefix="/api/schedule", tags=["schedule"])


@router.get("",
            summary="Emploi du temps (filtré)")
async def get_schedule(
    filiere_id: int = Query(...),
    semester: int = Query(..., ge=1, le=6),
    annee_etude: int | None = Query(None, ge=1, le=5),
    group_name: str | None = Query(None),
    annee_univ: str = Query("2025-2026"),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(
            Schedule,
            Module.name.label("module_name"),
            Module.code.label("module_code"),
            Professor.first_name.label("prof_first"),
            Professor.last_name.label("prof_last"),
        )
        .join(Module, Module.id == Schedule.module_id)
        .join(Professor, Professor.id == Schedule.professor_id, isouter=True)
        .where(Schedule.filiere_id == filiere_id)
        .where(Schedule.semester == semester)
        .where(Schedule.annee_univ == annee_univ)
    )
    if annee_etude:
        stmt = stmt.where(Schedule.annee_etude == annee_etude)
    if group_name:
        stmt = stmt.where(Schedule.group_name == group_name)

    order = {"LUNDI":1,"MARDI":2,"MERCREDI":3,"JEUDI":4,"VENDREDI":5,"SAMEDI":6}
    result = await db.execute(stmt)
    rows = result.all()
    sessions = []
    for sched, mod_name, mod_code, prof_first, prof_last in rows:
        sessions.append({
            "id": sched.id,
            "day": sched.day_of_week,
            "day_order": order.get(sched.day_of_week, 7),
            "start_time": sched.start_time.strftime("%H:%M"),
            "end_time": sched.end_time.strftime("%H:%M"),
            "module_code": mod_code,
            "module_name": mod_name,
            "professor": f"{prof_first} {prof_last}" if prof_first else None,
            "salle": sched.salle,
            "type_seance": sched.type_seance,
            "group_name": sched.group_name,
        })
    sessions.sort(key=lambda s: (s["day_order"], s["start_time"]))

    return {
        "filiere_id": filiere_id,
        "semester": semester,
        "annee_etude": annee_etude,
        "group_name": group_name,
        "annee_univ": annee_univ,
        "total_sessions": len(sessions),
        "sessions": sessions,
    }
