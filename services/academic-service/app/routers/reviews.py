"""
Routes Avis étudiants — /api/reviews (public) + /api/admin/reviews (modération).
PHASE 2.
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import get_current_admin
from app.db.session import get_db
from app.models import User, Review
from app.schemas.reviews import (
    ReviewCreate, ReviewOut, ReviewAdminOut, ReviewModerate,
    ReviewStats, RatingBucket,
)

settings = get_settings()

# ══════════════════════════════════════════════════════════════════════════════
#  PUBLIC
# ══════════════════════════════════════════════════════════════════════════════
public = APIRouter(prefix="/api/reviews", tags=["reviews"])


@public.post("", response_model=ReviewOut, status_code=status.HTTP_201_CREATED,
             summary="Déposer un avis (public)")
async def create_review(payload: ReviewCreate, request: Request,
                        db: AsyncSession = Depends(get_db)):
    status_value = "APPROVED" if settings.reviews_auto_approve else "PENDING"
    now = datetime.utcnow()
    review = Review(
        target_type=payload.target_type,
        target_id=payload.target_id,
        target_label=payload.target_label,
        rating=payload.rating,
        title=payload.title,
        comment=payload.comment.strip(),
        author_name=(payload.author_name or "Anonyme").strip(),
        author_email=payload.author_email,
        author_filiere=payload.author_filiere,
        status=status_value,
        is_pinned=False,
        admin_response=None,
        ip_address=request.client.host if request.client else None,
        created_at=now,
        updated_at=now,
    )
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return ReviewOut.model_validate(review)


@public.get("", response_model=list[ReviewOut],
            summary="Lister les avis approuvés")
async def list_reviews(
    target_type: str | None = Query(None, description="AI_ASSISTANT/MODULE/PROFESSOR/FILIERE/FACULTE/GENERAL"),
    target_id: int | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Review).where(Review.status == "APPROVED")
    if target_type:
        stmt = stmt.where(Review.target_type == target_type)
    if target_id is not None:
        stmt = stmt.where(Review.target_id == target_id)
    stmt = stmt.order_by(desc(Review.is_pinned), desc(Review.created_at)).limit(limit)
    result = await db.execute(stmt)
    return [ReviewOut.model_validate(r) for r in result.scalars().all()]


@public.get("/stats", response_model=ReviewStats,
            summary="Statistiques (note moyenne assistant IA)")
async def review_stats(db: AsyncSession = Depends(get_db)):
    # Moyenne + nombre pour l'assistant IA (avis approuvés)
    ai_stmt = select(
        func.avg(Review.rating), func.count(Review.id)
    ).where(
        Review.target_type == "AI_ASSISTANT",
        Review.status == "APPROVED",
        Review.rating.isnot(None),
    )
    ai_avg, ai_count = (await db.execute(ai_stmt)).one()

    total = (await db.execute(
        select(func.count(Review.id)).where(Review.status == "APPROVED")
    )).scalar_one()

    # Distribution des étoiles pour l'assistant IA
    dist_stmt = (
        select(Review.rating, func.count(Review.id))
        .where(
            Review.target_type == "AI_ASSISTANT",
            Review.status == "APPROVED",
            Review.rating.isnot(None),
        )
        .group_by(Review.rating)
    )
    dist_rows = (await db.execute(dist_stmt)).all()
    by_star = {int(stars): int(count) for stars, count in dist_rows}
    distribution = [RatingBucket(stars=s, count=by_star.get(s, 0)) for s in range(5, 0, -1)]

    return ReviewStats(
        ai_average=round(float(ai_avg), 2) if ai_avg is not None else 0.0,
        ai_count=int(ai_count or 0),
        total_reviews=int(total or 0),
        distribution=distribution,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN (modération)
# ══════════════════════════════════════════════════════════════════════════════
admin = APIRouter(prefix="/api/admin/reviews", tags=["admin-reviews"])


@admin.get("", response_model=list[ReviewAdminOut],
           summary="Lister tous les avis (admin)")
async def admin_list_reviews(
    status_filter: str | None = Query(None, alias="status",
                                      description="PENDING/APPROVED/HIDDEN"),
    limit: int = Query(200, ge=1, le=500),
    _: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Review)
    if status_filter:
        stmt = stmt.where(Review.status == status_filter)
    stmt = stmt.order_by(desc(Review.created_at)).limit(limit)
    result = await db.execute(stmt)
    return [ReviewAdminOut.model_validate(r) for r in result.scalars().all()]


@admin.patch("/{review_id}", response_model=ReviewAdminOut,
             summary="Modérer un avis (statut / épingler / réponse)")
async def admin_moderate_review(
    review_id: int, payload: ReviewModerate,
    _: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    review = await db.get(Review, review_id)
    if review is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Avis introuvable.")

    if payload.status is not None:
        review.status = payload.status
    if payload.is_pinned is not None:
        review.is_pinned = payload.is_pinned
    if payload.admin_response is not None:
        review.admin_response = payload.admin_response
    review.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(review)
    return ReviewAdminOut.model_validate(review)


@admin.delete("/{review_id}", summary="Supprimer définitivement un avis")
async def admin_delete_review(
    review_id: int,
    _: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    review = await db.get(Review, review_id)
    if review is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Avis introuvable.")
    await db.delete(review)
    await db.commit()
    return {"success": True, "deleted_id": review_id}
