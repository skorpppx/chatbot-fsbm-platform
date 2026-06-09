"""
Routes système : /api/health et /api/stats.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db, get_stats
from app.core.memory import memory
from app.models.schemas import HealthResponse, StatsResponse
from app.routers.chat import get_classifier

router = APIRouter(prefix="/api", tags=["system"])


@router.get("/health", response_model=HealthResponse, summary="Statut du service")
async def health():
    classifier = get_classifier()
    return HealthResponse(
        status="ok",
        nlp_ready=classifier.is_trained,
    )


@router.get("/stats", response_model=StatsResponse, summary="Statistiques globales")
async def stats(db: AsyncSession = Depends(get_db)):
    db_stats = await get_stats(db)
    mem_stats = memory.stats()
    return StatsResponse(
        **db_stats,
        active_sessions=mem_stats["active_sessions"],
    )
