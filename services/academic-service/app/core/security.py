"""
Sécurité — Hachage bcrypt + JWT (PHASE 2).

On utilise la librairie `bcrypt` DIRECTEMENT (pas passlib) car
bcrypt 5.x casse la détection de version interne de passlib 1.7.x.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.db.session import get_db
from app.models import User

settings = get_settings()

# Schéma Bearer (Swagger affichera un cadenas "Authorize")
bearer_scheme = HTTPBearer(auto_error=False)


# ─── MOTS DE PASSE ────────────────────────────────────────────────────────────
def hash_password(plain: str) -> str:
    """Hache un mot de passe en clair avec bcrypt (cost 12)."""
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Vérifie un mot de passe en clair contre son hash bcrypt."""
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except (ValueError, TypeError):
        return False


# ─── JWT ──────────────────────────────────────────────────────────────────────
def create_access_token(user: User) -> str:
    """Génère un JWT signé contenant l'identité de l'utilisateur."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.jwt_expire_minutes)).timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    """Décode et vérifie un JWT. Lève 401 si invalide/expiré."""
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token invalide ou expiré : {exc}",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ─── DÉPENDANCES FASTAPI ──────────────────────────────────────────────────────
async def get_current_user(
    creds: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Récupère l'utilisateur courant à partir du Bearer token."""
    if creds is None or not creds.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification requise (Bearer token manquant).",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_token(creds.credentials)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token sans identifiant utilisateur.")

    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    if user is None or not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Utilisateur introuvable ou désactivé.")
    return user


async def get_current_admin(user: User = Depends(get_current_user)) -> User:
    """Autorise uniquement les rôles ADMIN (ou SCOLARITE)."""
    if user.role not in ("ADMIN", "SCOLARITE"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé à l'administration.",
        )
    return user
