"""Schémas Pydantic — Avis étudiants / Reviews (PHASE 2)."""

from __future__ import annotations
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict, field_validator

TargetType = Literal["AI_ASSISTANT", "MODULE", "PROFESSOR", "FILIERE", "FACULTE", "GENERAL"]
ReviewStatus = Literal["PENDING", "APPROVED", "HIDDEN"]


# ─── CRÉATION (public) ────────────────────────────────────────────────────────
class ReviewCreate(BaseModel):
    target_type: TargetType = "GENERAL"
    target_id: Optional[int] = None
    target_label: Optional[str] = Field(None, max_length=200)
    rating: Optional[int] = Field(None, ge=1, le=5)
    title: Optional[str] = Field(None, max_length=200)
    comment: str = Field(..., min_length=3, max_length=2000)
    author_name: Optional[str] = Field(None, max_length=120)
    author_email: Optional[str] = Field(None, max_length=150)
    author_filiere: Optional[str] = Field(None, max_length=120)

    @field_validator("rating")
    @classmethod
    def rating_required_for_ai(cls, v, info):
        # La note étoilée est obligatoire pour l'assistant IA
        if info.data.get("target_type") == "AI_ASSISTANT" and v is None:
            raise ValueError("Une note (1 à 5) est obligatoire pour l'assistant IA.")
        return v


# ─── SORTIE (publique : sans email/ip) ────────────────────────────────────────
class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    target_type: str
    target_id: Optional[int] = None
    target_label: Optional[str] = None
    rating: Optional[int] = None
    title: Optional[str] = None
    comment: str
    author_name: Optional[str] = None
    author_filiere: Optional[str] = None
    is_pinned: bool = False
    admin_response: Optional[str] = None
    created_at: datetime


# ─── SORTIE (admin : champs complets) ─────────────────────────────────────────
class ReviewAdminOut(ReviewOut):
    author_email: Optional[str] = None
    status: str
    ip_address: Optional[str] = None
    updated_at: datetime


# ─── MODÉRATION (admin) ───────────────────────────────────────────────────────
class ReviewModerate(BaseModel):
    status: Optional[ReviewStatus] = None
    is_pinned: Optional[bool] = None
    admin_response: Optional[str] = Field(None, max_length=2000)


# ─── STATISTIQUES (note moyenne assistant IA, etc.) ───────────────────────────
class RatingBucket(BaseModel):
    stars: int
    count: int


class ReviewStats(BaseModel):
    ai_average: float = 0.0
    ai_count: int = 0
    total_reviews: int = 0
    distribution: list[RatingBucket] = Field(default_factory=list)
