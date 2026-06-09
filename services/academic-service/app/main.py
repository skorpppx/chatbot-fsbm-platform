"""
============================================================================
 FSBM Academic Service — FastAPI
 Port 5002 — Démarrage : python -m uvicorn app.main:app --reload --port 5002
============================================================================
"""

import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Forcer UTF-8 sur stdout (Windows cp1252 ne supporte pas les emojis)
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from app.core.config import get_settings
from app.routers.departments  import router as departments_router
from app.routers.filieres     import router as filieres_router
from app.routers.modules      import router as modules_router
from app.routers.professors   import router as professors_router
from app.routers.students     import router as students_router
from app.routers.schedule     import router as schedule_router
from app.routers.exams        import router as exams_router
from app.routers.announcements import router as announcements_router
from app.routers.system       import router as system_router
# ─── PHASE 2 ──────────────────────────────────────────────────────────────────
from app.routers.auth           import router as auth_router
from app.routers.reviews        import public as reviews_public_router
from app.routers.reviews        import admin  as reviews_admin_router
from app.routers.admin_content  import router as admin_content_router
from app.routers.admin_academic import router as admin_academic_router
from app.routers.admin_misc     import router as admin_misc_router
from app.routers.admin_upload   import router as admin_upload_router


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=" * 70)
    print(f"  🎓 FSBM Academic Service — Démarrage")
    print(f"  Port : {settings.service_port}")
    print(f"  DB   : {settings.db_name}@{settings.db_host}:{settings.db_port}")
    print("=" * 70)
    print(f"  ✅ Prêt : http://localhost:{settings.service_port}")
    print(f"  📖 Docs : http://localhost:{settings.service_port}/docs")
    print("=" * 70)
    yield
    print("[academic-service] Arrêt propre.")


app = FastAPI(
    title="FSBM Academic Service",
    description=(
        "Référentiel académique de la Faculté des Sciences Ben M'Sick.\n\n"
        "**Ressources gérées :**\n"
        "- Départements (5)\n"
        "- Filières (7 licences + 18 masters)\n"
        "- Modules (100+ matières détaillées)\n"
        "- Professeurs (~107 enseignants)\n"
        "- Étudiants (~3000 fiches réalistes)\n"
        "- Emplois du temps\n"
        "- Examens (sessions normale et rattrapage)\n"
        "- Annonces, événements, clubs\n\n"
        "**Projet de Fin d'Études 2025/2026**"
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(departments_router)
app.include_router(filieres_router)
app.include_router(modules_router)
app.include_router(professors_router)
app.include_router(students_router)
app.include_router(schedule_router)
app.include_router(exams_router)
app.include_router(announcements_router)
app.include_router(system_router)
# ─── PHASE 2 : auth, avis, espace admin ───────────────────────────────────────
app.include_router(auth_router)
app.include_router(reviews_public_router)
app.include_router(reviews_admin_router)
app.include_router(admin_content_router)
app.include_router(admin_academic_router)
app.include_router(admin_misc_router)
app.include_router(admin_upload_router)

# Fichiers uploadés (photos, logos, PDF) servis en statique sur /uploads
os.makedirs(settings.upload_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")


@app.get("/", tags=["root"])
async def root():
    return {
        "service": "FSBM Academic Service",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs",
        "endpoints": {
            "departments":   "/api/departments",
            "filieres":      "/api/filieres",
            "modules":       "/api/modules",
            "professors":    "/api/professors",
            "students":      "/api/students",
            "schedule":      "/api/schedule",
            "exams":         "/api/exams",
            "announcements": "/api/announcements",
            "events":        "/api/events",
            "clubs":         "/api/clubs",
            "overview":      "/api/overview",
            "health":        "/api/health",
            "auth":          "/api/auth/login",
            "reviews":       "/api/reviews",
            "admin":         "/api/admin/*",
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.service_port, reload=settings.debug)
