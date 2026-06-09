"""Schémas Pydantic — Création / mise à jour côté ADMIN (PHASE 2)."""

from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# ─── ANNONCES ─────────────────────────────────────────────────────────────────
class AnnouncementCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    content: str = Field(..., min_length=2)
    type: str = Field("INFO", description="INFO/URGENT/EXAMEN/EVENT/VACANCE")
    target_filiere: Optional[int] = None
    target_year: Optional[int] = None
    author: Optional[str] = Field("Administration FSBM", max_length=150)
    expires_at: Optional[datetime] = None
    is_pinned: bool = False
    image_url: Optional[str] = Field(None, max_length=255)
    attachment_url: Optional[str] = Field(None, max_length=255)


class AnnouncementUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None
    type: Optional[str] = None
    target_filiere: Optional[int] = None
    target_year: Optional[int] = None
    author: Optional[str] = Field(None, max_length=150)
    expires_at: Optional[datetime] = None
    is_pinned: Optional[bool] = None
    image_url: Optional[str] = Field(None, max_length=255)
    attachment_url: Optional[str] = Field(None, max_length=255)


# ─── ÉVÉNEMENTS ───────────────────────────────────────────────────────────────
class EventCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    event_type: str = Field("AUTRE", description="CONFERENCE/HACKATHON/PORTES_OUVERTES/GALA/FORUM/AUTRE")
    start_date: datetime
    end_date: Optional[datetime] = None
    location: Optional[str] = Field(None, max_length=200)
    organizer: Optional[str] = Field(None, max_length=150)
    registration_url: Optional[str] = Field(None, max_length=255)
    image_url: Optional[str] = Field(None, max_length=255)
    attachment_url: Optional[str] = Field(None, max_length=255)


class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    event_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = Field(None, max_length=200)
    organizer: Optional[str] = Field(None, max_length=150)
    registration_url: Optional[str] = Field(None, max_length=255)
    image_url: Optional[str] = Field(None, max_length=255)
    attachment_url: Optional[str] = Field(None, max_length=255)


# ─── FILIÈRES ─────────────────────────────────────────────────────────────────
class FiliereCreate(BaseModel):
    code: str = Field(..., max_length=20)
    name: str = Field(..., max_length=200)
    type: str = Field(..., description="LICENCE/LICENCE_PRO/MASTER/MASTER_RECHERCHE/DOCTORAT")
    department_id: int
    coordinator: Optional[str] = Field(None, max_length=150)
    coord_email: Optional[str] = Field(None, max_length=150)
    duration_years: int = 3
    capacity: int = 100
    description: Optional[str] = None
    objectives: Optional[str] = None
    careers: Optional[str] = None
    admission: Optional[str] = None
    logo_url: Optional[str] = Field(None, max_length=255)
    is_active: bool = True


class FiliereUpdate(BaseModel):
    code: Optional[str] = Field(None, max_length=20)
    name: Optional[str] = Field(None, max_length=200)
    type: Optional[str] = None
    department_id: Optional[int] = None
    coordinator: Optional[str] = Field(None, max_length=150)
    coord_email: Optional[str] = Field(None, max_length=150)
    duration_years: Optional[int] = None
    capacity: Optional[int] = None
    description: Optional[str] = None
    objectives: Optional[str] = None
    careers: Optional[str] = None
    admission: Optional[str] = None
    logo_url: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None


# ─── MODULES ──────────────────────────────────────────────────────────────────
class ModuleCreate(BaseModel):
    code: str = Field(..., max_length=30)
    name: str = Field(..., max_length=200)
    filiere_id: int
    semester: int = Field(1, ge=1, le=6)
    credits: int = 4
    coefficient: float = 1.0
    hours_cours: int = 24
    hours_td: int = 18
    hours_tp: int = 12
    description: Optional[str] = None
    prerequisites: Optional[str] = None
    is_eliminatory: bool = False


class ModuleUpdate(BaseModel):
    code: Optional[str] = Field(None, max_length=30)
    name: Optional[str] = Field(None, max_length=200)
    filiere_id: Optional[int] = None
    semester: Optional[int] = Field(None, ge=1, le=6)
    credits: Optional[int] = None
    coefficient: Optional[float] = None
    hours_cours: Optional[int] = None
    hours_td: Optional[int] = None
    hours_tp: Optional[int] = None
    description: Optional[str] = None
    prerequisites: Optional[str] = None
    is_eliminatory: Optional[bool] = None


# ─── PROFESSEURS ──────────────────────────────────────────────────────────────
class ProfessorCreate(BaseModel):
    matricule: str = Field(..., max_length=30)
    first_name: str = Field(..., max_length=80)
    last_name: str = Field(..., max_length=80)
    email: str = Field(..., max_length=150)
    phone: Optional[str] = Field(None, max_length=30)
    grade: str = Field("PA", description="PA/PH/PES/VACATAIRE/EMERITE")
    department_id: int
    specialty: Optional[str] = Field(None, max_length=200)
    bureau: Optional[str] = Field(None, max_length=50)
    photo_url: Optional[str] = Field(None, max_length=255)
    bio: Optional[str] = None


class ProfessorUpdate(BaseModel):
    matricule: Optional[str] = Field(None, max_length=30)
    first_name: Optional[str] = Field(None, max_length=80)
    last_name: Optional[str] = Field(None, max_length=80)
    email: Optional[str] = Field(None, max_length=150)
    phone: Optional[str] = Field(None, max_length=30)
    grade: Optional[str] = None
    department_id: Optional[int] = None
    specialty: Optional[str] = Field(None, max_length=200)
    bureau: Optional[str] = Field(None, max_length=50)
    photo_url: Optional[str] = Field(None, max_length=255)
    bio: Optional[str] = None


# ─── FAQ ──────────────────────────────────────────────────────────────────────
class FaqItemCreate(BaseModel):
    intent_tag: str = Field(..., max_length=80)
    question: str = Field(..., min_length=3)
    answer: str = Field(..., min_length=3)
    category_id: Optional[int] = None
    keywords: Optional[str] = None
    related_url: Optional[str] = Field(None, max_length=255)
    is_active: bool = True


class FaqItemUpdate(BaseModel):
    intent_tag: Optional[str] = Field(None, max_length=80)
    question: Optional[str] = None
    answer: Optional[str] = None
    category_id: Optional[int] = None
    keywords: Optional[str] = None
    related_url: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None


class FaqItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    intent_tag: str
    question: str
    answer: str
    category_id: Optional[int] = None
    keywords: Optional[str] = None
    related_url: Optional[str] = None
    consultations: int = 0
    is_active: bool = True


# ─── DÉPARTEMENTS ─────────────────────────────────────────────────────────────
class DepartmentCreate(BaseModel):
    code: str = Field(..., max_length=20)
    name: str = Field(..., max_length=150)
    name_short: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    head_name: Optional[str] = Field(None, max_length=150)
    head_email: Optional[str] = Field(None, max_length=150)
    head_phone: Optional[str] = Field(None, max_length=30)
    office_location: Optional[str] = Field(None, max_length=150)
    color_hex: Optional[str] = Field(None, max_length=7)
    logo_url: Optional[str] = Field(None, max_length=255)


class DepartmentUpdate(BaseModel):
    code: Optional[str] = Field(None, max_length=20)
    name: Optional[str] = Field(None, max_length=150)
    name_short: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    head_name: Optional[str] = Field(None, max_length=150)
    head_email: Optional[str] = Field(None, max_length=150)
    head_phone: Optional[str] = Field(None, max_length=30)
    office_location: Optional[str] = Field(None, max_length=150)
    color_hex: Optional[str] = Field(None, max_length=7)
    logo_url: Optional[str] = Field(None, max_length=255)


# ─── CLUBS (vie étudiante) ────────────────────────────────────────────────────
class ClubCreate(BaseModel):
    name: str = Field(..., max_length=150)
    description: Optional[str] = None
    category: str = Field("TECHNIQUE", description="SCIENTIFIQUE/CULTUREL/SPORTIF/HUMANITAIRE/TECHNIQUE")
    president: Optional[str] = Field(None, max_length=150)
    contact_email: Optional[str] = Field(None, max_length=150)
    social_links: Optional[dict] = None
    logo_url: Optional[str] = Field(None, max_length=255)
    members_count: int = 0
    is_active: bool = True


class ClubUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=150)
    description: Optional[str] = None
    category: Optional[str] = None
    president: Optional[str] = Field(None, max_length=150)
    contact_email: Optional[str] = Field(None, max_length=150)
    social_links: Optional[dict] = None
    logo_url: Optional[str] = Field(None, max_length=255)
    members_count: Optional[int] = None
    is_active: Optional[bool] = None


# ─── RÉPONSE GÉNÉRIQUE ────────────────────────────────────────────────────────
class DeleteResponse(BaseModel):
    success: bool = True
    deleted_id: int
    message: str = "Supprimé avec succès."
