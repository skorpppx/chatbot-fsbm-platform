"""
Upload de fichiers ADMIN — /api/admin/upload (PHASE 2).
Accepte images (photos profs, logos, images annonces/events) + PDF.
Stocke dans settings.upload_dir et renvoie une URL absolue servie en statique.
"""

import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.core.config import get_settings
from app.core.security import get_current_admin

settings = get_settings()

ALLOWED = {
    # images
    ".jpg": "image", ".jpeg": "image", ".png": "image", ".gif": "image",
    ".webp": "image", ".svg": "image", ".bmp": "image",
    # documents
    ".pdf": "pdf",
}

router = APIRouter(prefix="/api/admin", tags=["admin-upload"],
                   dependencies=[Depends(get_current_admin)])


@router.post("/upload", summary="Uploader une image ou un PDF (admin)")
async def upload_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Type non autorisé ({ext}). Autorisés : {', '.join(sorted(ALLOWED))}",
        )

    content = await file.read()
    max_bytes = settings.max_upload_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            f"Fichier trop volumineux (max {settings.max_upload_mb} Mo).",
        )

    os.makedirs(settings.upload_dir, exist_ok=True)
    safe_name = f"{uuid.uuid4().hex}{ext}"
    dest = os.path.join(settings.upload_dir, safe_name)
    with open(dest, "wb") as f:
        f.write(content)

    return {
        "url": f"{settings.public_base_url}/uploads/{safe_name}",
        "filename": safe_name,
        "original_name": file.filename,
        "kind": ALLOWED[ext],
        "size": len(content),
    }
