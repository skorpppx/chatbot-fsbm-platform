"""
Schémas Pydantic v2 pour la validation des requêtes/réponses API.
Documentation OpenAPI auto-générée à partir de ces schémas.
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# ─── REQUEST SCHEMAS ──────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    """Requête envoyée au chatbot."""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "message": "Comment m'inscrire à la FSBM ?",
            "session_id": "session_1234567890_abc",
            "user_id": None,
            "language": None,
        }
    })

    message: str = Field(..., min_length=1, max_length=500, description="Message de l'utilisateur")
    session_id: Optional[str] = Field(default=None, description="ID de session (sera généré si absent)")
    user_id: Optional[int] = Field(default=None, description="ID utilisateur si connecté")
    language: Optional[str] = Field(default=None,
        description="Force la langue de réponse : 'fr', 'en' ou 'darija'. Sinon auto-détection.")


class FeedbackRequest(BaseModel):
    """Feedback sur une réponse du chatbot."""
    conversation_id: int = Field(..., description="ID de la conversation à noter")
    note: int = Field(..., ge=1, le=5, description="Note de 1 à 5")
    is_helpful: Optional[bool] = Field(default=None, description="Réponse utile ?")
    commentaire: Optional[str] = Field(default=None, max_length=500)


# ─── RESPONSE SCHEMAS ─────────────────────────────────────────────────────────

class IntentCandidate(BaseModel):
    """Un intent candidat avec son score."""
    intent: str
    confidence: float
    matched_pattern: Optional[str] = None


class NewsItemSchema(BaseModel):
    title: str
    url: str = ""
    excerpt: str = ""
    date: Optional[str] = None
    image_url: Optional[str] = None
    source: str = "local"
    type: str = "INFO"


class ChatResponse(BaseModel):
    """Réponse du chatbot."""
    response: str = Field(..., description="Texte de réponse à afficher")
    intent: str = Field(..., description="Intent détecté")
    confidence: float = Field(..., description="Score de confiance 0-1")
    conversation_id: int = Field(..., description="ID DB pour feedback ultérieur")
    session_id: str
    language: str = Field(default="fr", description="Langue détectée/utilisée")
    language_confidence: float = Field(default=0.0, description="Confiance de la détection de langue")
    top_candidates: list[IntentCandidate] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list,
                                    description="Questions de relance suggérées")
    news_items: list[NewsItemSchema] = Field(default_factory=list,
        description="Actualités fraîches récupérées (si intent live_news)")
    response_time_ms: int = Field(default=0)


class IntentInfo(BaseModel):
    """Métadonnées d'un intent."""
    tag: str
    category: Optional[str] = None
    icon: Optional[str] = None
    nb_patterns: int
    nb_responses: int
    example: Optional[str] = None


class IntentsListResponse(BaseModel):
    """Liste de tous les intents."""
    total: int
    intents: list[IntentInfo]


class FeedbackResponse(BaseModel):
    success: bool = True
    feedback_id: int
    message: str = "Merci pour votre retour !"


class HistoryMessage(BaseModel):
    sender: str  # "user" | "bot"
    text: str
    intent: Optional[str] = None
    confidence: Optional[float] = None
    timestamp: datetime


class HistoryResponse(BaseModel):
    session_id: str
    total_messages: int
    history: list[HistoryMessage]


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "chatbot-service"
    version: str = "2.0.0"
    nlp_ready: bool
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class StatsResponse(BaseModel):
    total_conversations: int
    conversations_today: int
    top_intents: list[dict]
    average_satisfaction: Optional[float]
    response_rate: float
    active_sessions: int
