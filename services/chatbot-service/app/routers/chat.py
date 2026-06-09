"""
Routes /api/chat — endpoints conversationnels MULTILINGUES.

Nouveautés v3 :
  * Détection automatique de langue (FR/EN/Darija)
  * Réponse dans la langue détectée
  * Recherche web LIVE déclenchée automatiquement sur l'intent `live_news`
"""

from __future__ import annotations
import time
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import (
    get_db, save_conversation, save_feedback, get_session_history
)
from app.core.memory import memory
from app.core.persona import personalize_response, acknowledge_self_intro, detect_gender, detect_name
from app.core.web_fetcher import fetcher, format_news_response
from app.nlp.resolver import resolve as resolve_rules
from app.models.schemas import (
    ChatRequest, ChatResponse, FeedbackRequest, FeedbackResponse,
    HistoryResponse, HistoryMessage, IntentCandidate, NewsItemSchema,
)

router = APIRouter(prefix="/api/chat", tags=["chat"])

_classifier = None


def set_classifier(clf):
    global _classifier
    _classifier = clf


def get_classifier():
    if _classifier is None:
        raise RuntimeError("Classifier non initialisé.")
    return _classifier


# ──────────────────────────────────────────────────────────────────────────────
@router.post("",
             response_model=ChatResponse,
             summary="Envoyer un message au chatbot (multilingue FR/EN/Darija)",
             description=(
                "Le bot détecte automatiquement la langue (Français, Anglais ou Darija "
                "marocaine) et répond dans la même langue. Si la question concerne les "
                "actualités, le bot va chercher en direct sur fsbm.ma + notre base locale."
             ))
async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db)):
    classifier = get_classifier()
    start = time.perf_counter()

    session_id = req.session_id or f"sess_{uuid.uuid4().hex}"
    user_id = req.user_id

    ctx = memory.get_or_create(session_id, user_id)

    # ─── Détection genre/nom AVANT la prédiction ────────────────────────────
    new_gender = detect_gender(req.message)
    new_name   = detect_name(req.message)
    if new_gender and "gender" not in ctx.user_context:
        ctx.user_context["gender"] = new_gender
    if new_name and "name" not in ctx.user_context:
        ctx.user_context["name"] = new_name
    user_gender = ctx.user_context.get("gender")
    user_name   = ctx.user_context.get("name")

    # Prédiction NLP avec langue (forcée ou auto-détectée)
    try:
        result = classifier.predict(
            req.message,
            top_k=5,
            forced_language=req.language,  # None = auto
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erreur NLP : {exc}")

    detected_lang = result.get("language", "fr")
    lang_conf     = result.get("language_confidence", 0.0)
    response_text = result["response"]
    news_items    = []

    # ─── Résolveur haute-précision (règles + base de connaissances réelle) ──
    # Corrige les mé-routages du classifieur TF-IDF et répond aux questions
    # factuelles non couvertes par un intent (doyen, nombre de professeurs,
    # responsable d'une filière, domaines de recherche...), dans les 3 langues.
    # Ne s'applique que si le TF-IDF n'est pas déjà très confiant.
    rule_applied = False
    try:
        rule_hit = resolve_rules(
            req.message, detected_lang, classifier,
            tfidf_conf=result.get("confidence", 0.0),
            tfidf_intent=result.get("intent", ""),
        )
    except Exception:
        rule_hit = None
    if rule_hit:
        response_text = rule_hit["response"]
        result["intent"] = rule_hit["intent"]
        result["confidence"] = rule_hit["confidence"]
        result["trigger_web_fetch"] = False
        rule_applied = True

    # ─── Cas spécial : utilisateur révèle son genre/nom → réponse perso ─────
    # On reconnaît si l'intent est "identite_genre" OU si on vient de détecter
    # un genre/nom et que la confiance est basse (sinon l'intent prend le dessus)
    just_revealed = (new_gender is not None) or (new_name is not None)
    if not rule_applied and (result["intent"] == "identite_genre"
                             or (just_revealed and result["confidence"] < 0.40)):
        response_text = acknowledge_self_intro(
            gender=new_gender or user_gender,
            name=new_name or user_name,
            lang=detected_lang,
        )

    # ─── DECLENCHEMENT WEB FETCH (intent live_news) ─────────────────────────
    if result.get("trigger_web_fetch"):
        try:
            news_data = await fetcher.get_news(source="all", limit=6)
            formatted = format_news_response(news_data, lang=detected_lang)
            response_text = response_text + "\n\n" + formatted
            news_items = [NewsItemSchema(**i) for i in news_data["items"]]
        except Exception as exc:
            response_text += f"\n\n⚠️ (Recherche web indisponible : {str(exc)[:80]})"

    # ─── Personnaliser : substituer placeholders {voc}, {khoya_khti}, etc. ─
    response_text = personalize_response(
        response_text,
        gender=user_gender,
        name=user_name,
        lang=detected_lang,
    )

    response_time_ms = int((time.perf_counter() - start) * 1000)

    # Persistance MySQL (tolérant aux erreurs)
    try:
        conv_id = await save_conversation(
            db,
            session_id=session_id,
            user_message=req.message,
            bot_response=response_text,
            intent=result["intent"],
            confidence=result["confidence"],
            response_time_ms=response_time_ms,
            user_id=user_id,
        )
    except Exception:
        conv_id = 0

    memory.add_turn(
        session_id=session_id,
        user_message=req.message,
        bot_response=response_text,
        intent=result["intent"],
        confidence=result["confidence"],
        user_id=user_id,
    )

    # Suggestions contextuelles dans la même langue
    try:
        suggestions_data = classifier.get_suggestions(
            req.message, k=4, forced_language=detected_lang
        )
        suggestions = [
            s["example_question"]
            for s in suggestions_data
            if s["intent"] != result["intent"]
        ][:3]
    except Exception:
        suggestions = []

    top_candidates = [IntentCandidate(**c) for c in result.get("top_candidates", [])[:3]]

    return ChatResponse(
        response=response_text,
        intent=result["intent"],
        confidence=result["confidence"],
        conversation_id=conv_id,
        session_id=session_id,
        language=detected_lang,
        language_confidence=lang_conf,
        top_candidates=top_candidates,
        suggestions=suggestions,
        news_items=news_items,
        response_time_ms=response_time_ms,
    )


# ──────────────────────────────────────────────────────────────────────────────
@router.post("/feedback",
             response_model=FeedbackResponse,
             summary="Soumettre un feedback sur une réponse")
async def feedback(req: FeedbackRequest, db: AsyncSession = Depends(get_db)):
    if req.conversation_id <= 0:
        raise HTTPException(400, "conversation_id invalide")
    fb_id = await save_feedback(
        db,
        conversation_id=req.conversation_id,
        note=req.note,
        is_helpful=req.is_helpful,
        commentaire=req.commentaire,
    )
    return FeedbackResponse(success=True, feedback_id=fb_id)


# ──────────────────────────────────────────────────────────────────────────────
@router.get("/history/{session_id}",
            response_model=HistoryResponse,
            summary="Récupérer l'historique d'une session")
async def history(session_id: str, db: AsyncSession = Depends(get_db)):
    rows = await get_session_history(db, session_id)
    messages: list[HistoryMessage] = []
    for r in rows:
        messages.append(HistoryMessage(
            sender="user",
            text=r["user_message"],
            timestamp=r["created_at"],
        ))
        messages.append(HistoryMessage(
            sender="bot",
            text=r["bot_response"],
            intent=r["intent_detected"],
            confidence=float(r["confidence"] or 0),
            timestamp=r["created_at"],
        ))
    return HistoryResponse(
        session_id=session_id,
        total_messages=len(messages),
        history=messages,
    )


# ──────────────────────────────────────────────────────────────────────────────
@router.get("/suggestions",
            summary="Suggestions de questions pour démarrer (par langue)")
async def suggestions(lang: str = "fr", limit: int = 6):
    """Retourne des exemples de questions pour démarrer, dans la langue choisie."""
    classifier = get_classifier()
    all_intents = classifier.get_all_intents(lang=lang)
    selected = [it for it in all_intents if it.get("example")][:limit]
    return {
        "language": lang,
        "total": len(selected),
        "suggestions": [
            {
                "intent": it["tag"],
                "icon": it.get("icon"),
                "category": it.get("category"),
                "question": it["example"],
            }
            for it in selected
        ]
    }


# ──────────────────────────────────────────────────────────────────────────────
@router.get("/news",
            summary="Récupérer les actualités FSBM en direct (multi-sources)")
async def get_live_news(source: str = "all", limit: int = 8, lang: str = "fr"):
    """
    Récupère les actualités FSBM depuis :
      * notre base academic-service (annonces + événements)
      * fsbm.ma/news (best effort - site est une SPA JS)
      * Lien direct vers la page Facebook officielle
    """
    data = await fetcher.get_news(source=source, limit=limit)
    data["formatted_text"] = format_news_response(data, lang=lang)
    return data
