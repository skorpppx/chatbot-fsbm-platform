"""Routes d'authentification — /api/auth (PHASE 2)."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import (
    verify_password, create_access_token, get_current_user,
)
from app.db.session import get_db
from app.models import User
from app.schemas.auth import LoginRequest, TokenResponse, UserOut

router = APIRouter(prefix="/api/auth", tags=["auth"])
settings = get_settings()


@router.post("/login", response_model=TokenResponse, summary="Connexion (email + mot de passe)")
async def login(creds: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == creds.email))
    user = result.scalar_one_or_none()

    if user is None or not verify_password(creds.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect.",
        )
    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Compte désactivé.")

    user.last_login = datetime.utcnow()
    await db.commit()
    await db.refresh(user)

    token = create_access_token(user)
    return TokenResponse(
        access_token=token,
        expires_in=settings.jwt_expire_minutes * 60,
        user=UserOut.model_validate(user),
    )


@router.get("/me", response_model=UserOut, summary="Profil de l'utilisateur connecté")
async def me(current: User = Depends(get_current_user)):
    return UserOut.model_validate(current)
