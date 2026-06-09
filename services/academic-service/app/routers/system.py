"""Routes système — /api/health, /api/overview."""

from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import (
    Department, Filiere, Module, Professor, Student, Event,
    Announcement, Club,
)

router = APIRouter(prefix="/api", tags=["system"])


@router.get("/health", summary="Statut du service")
async def health():
    return {
        "status": "ok",
        "service": "academic-service",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    }


# Chiffres OFFICIELS REELS de la FSBM (source : site institutionnel fsbm.ma, juin 2026)
# Affiches comme indicateurs d'echelle de la faculte sur le tableau de bord.
OFFICIEL = {
    "departments": 6,
    "filieres": 30,        # 18 licences + 12 masters
    "professors": 239,
    "students": 11994,
    "laboratoires": 12,
    "entreprises_partenaires": 160,
    "licences": 18,
    "masters": 12,
    "doctorats": 4,
}

DOYEN = "Pr. Abdeslam EL BOUARI"
DOYEN_MESSAGE = (
    "La Faculte des Sciences Ben M'Sick (FSBM) est un etablissement ouvert et inclusif, fier de "
    "former chaque annee des milliers d'etudiants marocains et internationaux. Portee par une "
    "vision d'excellence, d'innovation et de responsabilite sociale, la FSBM s'engage a offrir un "
    "enseignement de qualite, a stimuler une recherche scientifique ambitieuse et a promouvoir une "
    "gouvernance moderne et participative. Au coeur de notre projet, nos etudiants, nos chercheurs "
    "et l'ensemble de notre personnel administratif sont pleinement impliques pour faire de la "
    "Faculte un pole de savoir rayonnant, au service du developpement durable de notre societe. "
    "Ensemble, construisons une FSBM plus forte, plus innovante et plus ouverte sur l'avenir."
)


@router.get("/overview", summary="Vue d'ensemble (compteurs reels FSBM)")
async def overview(db: AsyncSession = Depends(get_db)):
    """Tableau de bord : chiffres officiels reels de la FSBM (fsbm.ma) pour les
    indicateurs d'echelle, et compteurs en base pour les contenus geres."""
    module_count = await db.scalar(select(func.count(Module.id))) or 0
    event_count  = await db.scalar(select(func.count(Event.id))) or 0
    ann_count    = await db.scalar(select(func.count(Announcement.id))) or 0
    club_count   = await db.scalar(select(func.count(Club.id))) or 0

    return {
        "departments":   OFFICIEL["departments"],
        "filieres":      OFFICIEL["filieres"],
        "modules":       module_count,
        "professors":    OFFICIEL["professors"],
        "students":      OFFICIEL["students"],
        "events":        event_count,
        "announcements": ann_count,
        "clubs":         club_count,
        "laboratoires":  OFFICIEL["laboratoires"],
        "entreprises_partenaires": OFFICIEL["entreprises_partenaires"],
        "filieres_by_type": {
            "LICENCE": OFFICIEL["licences"],
            "MASTER":  OFFICIEL["masters"],
            "DOCTORAT": OFFICIEL["doctorats"],
        },
        "doyen": DOYEN,
        "doyen_message": DOYEN_MESSAGE,
        "source": "Donnees officielles fsbm.ma",
    }
