"""
Routes /api/intents — explorer les intentions du chatbot.
"""

from fastapi import APIRouter
from app.models.schemas import IntentsListResponse
from app.routers.chat import get_classifier

router = APIRouter(prefix="/api/intents", tags=["intents"])


@router.get("",
            response_model=IntentsListResponse,
            summary="Lister tous les intents du chatbot")
async def list_intents():
    classifier = get_classifier()
    intents = classifier.get_all_intents()
    return IntentsListResponse(total=len(intents), intents=intents)
