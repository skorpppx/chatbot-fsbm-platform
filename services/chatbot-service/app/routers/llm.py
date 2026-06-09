"""
Routes /api/llm/* — endpoints LLM avec RAG et fallback automatique.

Endpoints :
    POST /api/llm/chat       Generation LLM avec RAG (Groq + fallback)
    GET  /api/llm/status     Etat des fournisseurs (Groq/HF dispo ?)
    GET  /api/llm/models     Liste des modeles disponibles
"""

from __future__ import annotations
import time
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field, ConfigDict

from app.core.database import get_db, save_conversation
from app.core.memory import memory
from app.core.persona import detect_gender, detect_name
from app.nlp.resolver import resolve as resolve_rules

router = APIRouter(prefix="/api/llm", tags=["llm"])


# ─── Schemas ─────────────────────────────────────────────────────────────────
class LLMChatRequest(BaseModel):
    """Requete LLM."""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "message": "Quelles sont les conditions pour le master IADS ?",
            "session_id": "sess_abc",
            "language": None,
            "temperature": 0.6,
        }
    })

    message: str = Field(..., min_length=1, max_length=500)
    session_id: str | None = None
    user_id: int | None = None
    language: str | None = Field(default=None, description="fr|en|darija ou None=auto")
    temperature: float = Field(default=0.6, ge=0.0, le=1.5)


class ContextSchema(BaseModel):
    tag: str
    score: float
    category: str
    icon: str = ""
    patterns: list[str] = []
    reference_response: str = ""


class LLMChatResponse(BaseModel):
    response: str
    provider: str        # groq | hf | tfidf
    model: str
    intent_detected: str
    confidence: float
    language: str
    contexts_used: list[ContextSchema]
    conversation_id: int
    session_id: str
    history_length: int
    latency_ms: int
    tokens_used: int = 0
    error: str | None = None


# ─── Injection du service ────────────────────────────────────────────────────
_llm_service = None


def set_llm_service(svc):
    global _llm_service
    _llm_service = svc


def get_llm_service():
    if _llm_service is None:
        raise RuntimeError("LLMService non initialise")
    return _llm_service


# ─── Endpoint principal ──────────────────────────────────────────────────────
@router.post("/chat",
             response_model=LLMChatResponse,
             summary="Chat avec LLaMA 3 + RAG (FSBM Knowledge)",
             description=(
                "Pipeline complet :\n"
                "1. Detection langue (FR/EN/Darija)\n"
                "2. RAG : recupere top-3 contextes pertinents du dataset FAQ\n"
                "3. Construit le prompt avec systeme + contexte + historique\n"
                "4. Appelle Groq (LLaMA 3.3 70B) — fallback HF — fallback TF-IDF\n"
                "5. Reponse contextuelle, sans hallucination"
             ))
async def llm_chat(req: LLMChatRequest, db: AsyncSession = Depends(get_db)):
    svc = get_llm_service()
    session_id = req.session_id or f"sess_{uuid.uuid4().hex}"

    # Memoire conversationnelle
    ctx = memory.get_or_create(session_id, req.user_id)

    # Detection genre/nom
    g = detect_gender(req.message)
    n = detect_name(req.message)
    if g and "gender" not in ctx.user_context:
        ctx.user_context["gender"] = g
    if n and "name" not in ctx.user_context:
        ctx.user_context["name"] = n
    user_gender = ctx.user_context.get("gender")
    user_name = ctx.user_context.get("name")

    # Construire l'historique au format chat
    history = []
    for turn in ctx.history:
        history.append({"role": "user", "content": turn.user_message})
        history.append({"role": "assistant", "content": turn.bot_response})

    # Generation LLM avec RAG
    try:
        result = svc.generate(
            message=req.message,
            history=history,
            forced_language=req.language,
            gender=user_gender,
            name=user_name,
            temperature=req.temperature,
        )
    except Exception as exc:
        raise HTTPException(500, f"LLM generation error: {exc}")

    # ─── Robustesse hors-ligne : si on est retombe sur le TF-IDF (Groq/HF
    # indisponibles), on applique le resolveur a base de regles pour garantir
    # une reponse factuelle correcte (doyen, profs, responsable, recherche...).
    if result.provider == "tfidf":
        try:
            hit = resolve_rules(
                req.message, result.language, svc.classifier,
                tfidf_conf=result.confidence, tfidf_intent=result.intent_detected,
            )
            if hit:
                result.content = hit["response"]
                result.intent_detected = hit["intent"]
                result.confidence = hit["confidence"]
        except Exception:
            pass

    # Persistance MySQL
    try:
        conv_id = await save_conversation(
            db,
            session_id=session_id,
            user_message=req.message,
            bot_response=result.content,
            intent=result.intent_detected,
            confidence=result.confidence,
            response_time_ms=result.latency_ms,
            user_id=req.user_id,
        )
    except Exception:
        conv_id = 0

    # Memoire conversationnelle
    memory.add_turn(
        session_id=session_id,
        user_message=req.message,
        bot_response=result.content,
        intent=result.intent_detected,
        confidence=result.confidence,
        user_id=req.user_id,
    )

    return LLMChatResponse(
        response=result.content,
        provider=result.provider,
        model=result.model,
        intent_detected=result.intent_detected,
        confidence=result.confidence,
        language=result.language,
        contexts_used=[ContextSchema(**c) for c in result.contexts_used],
        conversation_id=conv_id,
        session_id=session_id,
        history_length=result.history_length,
        latency_ms=result.latency_ms,
        tokens_used=result.tokens_used,
        error=result.error,
    )


@router.get("/status",
            summary="Etat des fournisseurs LLM")
async def llm_status():
    svc = get_llm_service()
    return svc.status()


@router.get("/models",
            summary="Liste des modeles disponibles")
async def llm_models():
    from app.llm.groq_client import GROQ_MODELS
    from app.llm.hf_client import HF_MODELS
    return {
        "groq": GROQ_MODELS,
        "huggingface": HF_MODELS,
    }
