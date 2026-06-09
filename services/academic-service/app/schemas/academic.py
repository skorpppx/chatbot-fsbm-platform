"""Schémas Pydantic pour les ressources académiques."""

from __future__ import annotations
from datetime import datetime, date, time
from typing import Optional, Generic, TypeVar
from pydantic import BaseModel, Field, ConfigDict


# ─── PAGINATION GÉNÉRIQUE ─────────────────────────────────────────────────────
T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Réponse paginée standard."""
    items: list[T]
    total: int
    page: int = 1
    page_size: int = 20
    total_pages: int = 1


# ─── DEPARTMENT ───────────────────────────────────────────────────────────────
class DepartmentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    code: str
    name: str
    name_short: Optional[str] = None
    description: Optional[str] = None
    head_name: Optional[str] = None
    head_email: Optional[str] = None
    head_phone: Optional[str] = None
    office_location: Optional[str] = None
    color_hex: Optional[str] = None
    logo_url: Optional[str] = None


class DepartmentOut(DepartmentBase):
    id: int


class DepartmentDetail(DepartmentOut):
    filieres_count: int = 0
    professors_count: int = 0


# ─── FILIERE ──────────────────────────────────────────────────────────────────
class FiliereBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    code: str
    name: str
    type: str
    department_id: int
    coordinator: Optional[str] = None
    coord_email: Optional[str] = None
    duration_years: int
    capacity: int
    description: Optional[str] = None
    objectives: Optional[str] = None
    careers: Optional[str] = None
    admission: Optional[str] = None
    logo_url: Optional[str] = None
    is_active: bool


class FiliereOut(FiliereBase):
    id: int


class FiliereDetail(FiliereOut):
    department_name: Optional[str] = None
    modules_count: int = 0
    students_count: int = 0


# ─── MODULE ───────────────────────────────────────────────────────────────────
class ModuleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    code: str
    name: str
    filiere_id: int
    semester: int
    credits: int
    coefficient: float
    hours_cours: int
    hours_td: int
    hours_tp: int
    description: Optional[str] = None
    prerequisites: Optional[str] = None
    is_eliminatory: bool


class ModuleOut(ModuleBase):
    id: int


class ModuleDetail(ModuleOut):
    filiere_name: Optional[str] = None
    teachers: list[str] = Field(default_factory=list)
    total_hours: int = 0


# ─── PROFESSOR ────────────────────────────────────────────────────────────────
class ProfessorBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    matricule: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    grade: str
    department_id: int
    specialty: Optional[str] = None
    bureau: Optional[str] = None
    photo_url: Optional[str] = None
    bio: Optional[str] = None


class ProfessorOut(ProfessorBase):
    id: int


class ProfessorDetail(ProfessorOut):
    department_name: Optional[str] = None
    full_name: Optional[str] = None


# ─── STUDENT ──────────────────────────────────────────────────────────────────
class StudentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cne: str
    apogee: Optional[str] = None
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    birth_date: Optional[date] = None
    birth_place: Optional[str] = None
    gender: str
    nationality: Optional[str] = None
    cin: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    filiere_id: int
    annee_etude: int
    group_name: Optional[str] = None
    is_boursier: bool
    statut: str
    photo_url: Optional[str] = None
    enrolled_at: Optional[date] = None


class StudentOut(StudentBase):
    id: int


class StudentDetail(StudentOut):
    filiere_name: Optional[str] = None
    department_name: Optional[str] = None
    full_name: Optional[str] = None


# ─── SCHEDULE ─────────────────────────────────────────────────────────────────
class ScheduleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    filiere_id: int
    module_id: int
    professor_id: Optional[int] = None
    semester: int
    annee_etude: int
    group_name: Optional[str] = None
    day_of_week: str
    start_time: time
    end_time: time
    salle: str
    type_seance: str
    annee_univ: str


class ScheduleDetail(ScheduleOut):
    module_name: Optional[str] = None
    module_code: Optional[str] = None
    professor_name: Optional[str] = None


# ─── EXAM ─────────────────────────────────────────────────────────────────────
class ExamOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    module_id: int
    filiere_id: int
    exam_date: date
    start_time: time
    duration_min: int
    salle: str
    session: str
    annee_univ: str
    surveillants: Optional[str] = None
    consignes: Optional[str] = None


class ExamDetail(ExamOut):
    module_name: Optional[str] = None
    module_code: Optional[str] = None


# ─── ANNOUNCEMENTS / EVENTS / CLUBS ───────────────────────────────────────────
class AnnouncementOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    content: str
    type: str
    target_filiere: Optional[int] = None
    target_year: Optional[int] = None
    author: Optional[str] = None
    published_at: datetime
    expires_at: Optional[datetime] = None
    is_pinned: bool
    image_url: Optional[str] = None
    attachment_url: Optional[str] = None


class EventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: Optional[str] = None
    event_type: str
    start_date: datetime
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    organizer: Optional[str] = None
    registration_url: Optional[str] = None
    image_url: Optional[str] = None
    attachment_url: Optional[str] = None


class ClubOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: Optional[str] = None
    category: str
    president: Optional[str] = None
    contact_email: Optional[str] = None
    social_links: Optional[dict] = None
    logo_url: Optional[str] = None
    members_count: int
    is_active: bool
