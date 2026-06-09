"""
============================================================================
 FSBM Chatbot Service v2 — FastAPI
 Port 5001 — Démarre avec : python -m uvicorn app.main:app --reload --port 5001
============================================================================
"""

from __future__ import annotations
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Forcer UTF-8 sur stdout (Windows cp1252 ne supporte pas les emojis)
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from app.core.config import get_settings
from app.core.web_fetcher import fetcher
from app.llm.llm_service import LLMService
from app.nlp.classifier import IntentClassifier
from app.routers import chat as chat_router_mod
from app.routers.chat import router as chat_router, set_classifier
from app.routers.intents import router as intents_router
from app.routers.llm import router as llm_router, set_llm_service
from app.routers.system import router as system_router


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialise le NLP au démarrage."""
    print("=" * 70)
    print(f"  🤖 FSBM Chatbot Service v2 — Démarrage")
    print(f"  Environnement : {settings.env}")
    print(f"  Port           : {settings.service_port}")
    print("=" * 70)
    classifier = IntentClassifier(
        confidence_threshold=settings.confidence_threshold,
    )
    # Charger depuis cache si disponible, sinon entraîner
    if not classifier.load_model():
        classifier.train()
    set_classifier(classifier)

    # Configurer le web fetcher avec l'URL du academic-service
    fetcher.academic_service_url = settings.academic_service_url.rstrip("/")
    print(f"  Web fetcher configuré : academic-service @ {fetcher.academic_service_url}")

    # Initialiser le LLMService (Groq + HF + fallback TF-IDF)
    llm_svc = LLMService(
        classifier=classifier,
        groq_api_key=settings.groq_api_key,
        hf_api_key=settings.hf_api_key,
        groq_model=settings.groq_model,
        rag_top_k=settings.rag_top_k,
    )
    set_llm_service(llm_svc)
    status = llm_svc.status()
    print(f"  LLM Service : provider primaire = {status['primary']}")
    if status['groq']['available']:
        print(f"    Groq      : OK ({status['groq']['model']})")
    if status['hf']['available']:
        print(f"    HuggingFace : OK ({status['hf']['model']})")
    print(f"    TF-IDF    : OK (fallback toujours dispo)")
    print("=" * 70)
    print(f"  ✅ Service prêt sur http://localhost:{settings.service_port}")
    print(f"  📖 Docs Swagger : http://localhost:{settings.service_port}/docs")
    print(f"  📚 Docs ReDoc   : http://localhost:{settings.service_port}/redoc")
    print("=" * 70)
    yield
    print("[chatbot-service] Arrêt propre.")


app = FastAPI(
    title="FSBM Chatbot Service",
    description=(
        "Service de chatbot intelligent pour la Faculté des Sciences Ben M'Sick.\n\n"
        "**Fonctionnalités :**\n"
        "- NLP TF-IDF + Cosine Similarity (n-grammes)\n"
        "- Mémoire conversationnelle par session\n"
        "- Top-K candidats et suggestions automatiques\n"
        "- Historique persistant en MySQL\n"
        "- Feedbacks utilisateurs\n\n"
        "**Projet de Fin d'Études 2025/2026** — AKRAM, ZAKARIA, NOUHAILA"
    ),
    version="2.0.0",
    lifespan=lifespan,
    contact={"name": "Équipe PFE FSBM", "email": "contact@fsbm.ma"},
    license_info={"name": "Académique"},
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(chat_router)
app.include_router(intents_router)
app.include_router(llm_router)
app.include_router(system_router)


@app.get("/", tags=["root"], summary="Racine du service")
async def root():
    return {
        "service": "FSBM Chatbot Service",
        "version": "2.0.0",
        "status": "online",
        "docs": "/docs",
        "endpoints": {
            "chat":        "POST /api/chat",
            "feedback":    "POST /api/chat/feedback",
            "history":     "GET  /api/chat/history/{session_id}",
            "suggestions": "GET  /api/chat/suggestions",
            "intents":     "GET  /api/intents",
            "health":      "GET  /api/health",
            "stats":       "GET  /api/stats",
        },
    }


# Pour exécuter directement : python app/main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.service_port,
        reload=settings.debug,
    )
