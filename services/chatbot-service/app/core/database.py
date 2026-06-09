"""
Accès base de données MySQL pour le chatbot-service.
Utilise SQLAlchemy 2.0 async + aiomysql.
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import text

from .config import get_settings


settings = get_settings()
engine = create_async_engine(settings.database_url, echo=False, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncSession:
    """Dépendance FastAPI pour injecter une session DB."""
    async with SessionLocal() as session:
        yield session


# ─── REQUÊTES BRUTES (pour rester simple sans définir les modèles ORM) ────────

async def save_conversation(
    db: AsyncSession,
    session_id: str,
    user_message: str,
    bot_response: str,
    intent: str,
    confidence: float,
    response_time_ms: int = 0,
    user_id: Optional[int] = None,
) -> int:
    """Insère une conversation et retourne son ID."""
    result = await db.execute(text("""
        INSERT INTO conversations
        (session_id, user_id, user_message, bot_response, intent_detected,
         confidence, response_time_ms, created_at)
        VALUES (:session_id, :user_id, :user_message, :bot_response, :intent,
                :confidence, :rt, :created_at)
    """), {
        "session_id": session_id,
        "user_id": user_id,
        "user_message": user_message,
        "bot_response": bot_response,
        "intent": intent,
        "confidence": confidence,
        "rt": response_time_ms,
        "created_at": datetime.utcnow(),
    })
    await db.commit()
    return result.lastrowid  # type: ignore


async def save_feedback(
    db: AsyncSession,
    conversation_id: int,
    note: int,
    is_helpful: Optional[bool] = None,
    commentaire: Optional[str] = None,
) -> int:
    """Enregistre un feedback et retourne son ID."""
    result = await db.execute(text("""
        INSERT INTO feedbacks (conversation_id, note, is_helpful, commentaire, created_at)
        VALUES (:conv_id, :note, :is_helpful, :commentaire, :created_at)
    """), {
        "conv_id": conversation_id,
        "note": note,
        "is_helpful": is_helpful,
        "commentaire": commentaire,
        "created_at": datetime.utcnow(),
    })
    await db.commit()
    return result.lastrowid  # type: ignore


async def get_session_history(db: AsyncSession, session_id: str, limit: int = 50) -> list[dict]:
    """Récupère l'historique d'une session de conversation."""
    result = await db.execute(text("""
        SELECT id, user_message, bot_response, intent_detected, confidence, created_at
        FROM conversations
        WHERE session_id = :session_id
        ORDER BY created_at ASC
        LIMIT :limit
    """), {"session_id": session_id, "limit": limit})
    rows = result.mappings().all()
    return [dict(r) for r in rows]


async def get_stats(db: AsyncSession) -> dict:
    """Calcule les statistiques globales du chatbot."""
    total = (await db.execute(text("SELECT COUNT(*) AS c FROM conversations"))).scalar()
    today = (await db.execute(text(
        "SELECT COUNT(*) AS c FROM conversations WHERE DATE(created_at) = CURDATE()"
    ))).scalar()

    top_intents_rows = (await db.execute(text("""
        SELECT intent_detected AS intent, COUNT(*) AS count
        FROM conversations
        WHERE intent_detected != 'default'
        GROUP BY intent_detected
        ORDER BY count DESC
        LIMIT 5
    """))).mappings().all()

    avg_note = (await db.execute(text("SELECT AVG(note) AS m FROM feedbacks"))).scalar()

    rates = (await db.execute(text("""
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN intent_detected != 'default' THEN 1 ELSE 0 END) AS resolved
        FROM conversations
    """))).mappings().first()
    total_ = rates["total"] if rates else 0
    resolved_ = rates["resolved"] if rates else 0
    rate = (resolved_ / total_ * 100) if total_ else 0.0

    return {
        "total_conversations": total or 0,
        "conversations_today": today or 0,
        "top_intents": [dict(r) for r in top_intents_rows],
        "average_satisfaction": round(float(avg_note), 2) if avg_note is not None else None,
        "response_rate": round(rate, 1),
    }
