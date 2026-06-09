"""
Modèles ORM SQLAlchemy 2.0 (mapping déclaratif).
Tables mappées 1:1 avec le schéma MySQL fsbm_db.
"""

from __future__ import annotations
from datetime import datetime, date, time
from typing import Optional

from sqlalchemy import (
    String, Integer, BigInteger, SmallInteger, Boolean, Date, DateTime, Time,
    Text, Numeric, ForeignKey, Enum as SQLEnum, JSON,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# ─── DEPARTMENT ───────────────────────────────────────────────────────────────
class Department(Base):
    __tablename__ = "departments"

    id:              Mapped[int] = mapped_column(BigInteger, primary_key=True)
    code:            Mapped[str] = mapped_column(String(20), unique=True)
    name:            Mapped[str] = mapped_column(String(150))
    name_short:      Mapped[Optional[str]] = mapped_column(String(50))
    description:     Mapped[Optional[str]] = mapped_column(Text)
    head_name:       Mapped[Optional[str]] = mapped_column(String(150))
    head_email:      Mapped[Optional[str]] = mapped_column(String(150))
    head_phone:      Mapped[Optional[str]] = mapped_column(String(30))
    office_location: Mapped[Optional[str]] = mapped_column(String(150))
    color_hex:       Mapped[Optional[str]] = mapped_column(String(7))
    logo_url:        Mapped[Optional[str]] = mapped_column(String(255))
    created_at:      Mapped[datetime] = mapped_column(DateTime)
    updated_at:      Mapped[datetime] = mapped_column(DateTime)

    filieres: Mapped[list["Filiere"]] = relationship(back_populates="department")
    professors: Mapped[list["Professor"]] = relationship(back_populates="department")


# ─── FILIERE ──────────────────────────────────────────────────────────────────
class Filiere(Base):
    __tablename__ = "filieres"

    id:             Mapped[int] = mapped_column(BigInteger, primary_key=True)
    code:           Mapped[str] = mapped_column(String(20), unique=True)
    name:           Mapped[str] = mapped_column(String(200))
    type:           Mapped[str] = mapped_column(String(30))
    department_id:  Mapped[int] = mapped_column(BigInteger, ForeignKey("departments.id"))
    coordinator:    Mapped[Optional[str]] = mapped_column(String(150))
    coord_email:    Mapped[Optional[str]] = mapped_column(String(150))
    duration_years: Mapped[int] = mapped_column(SmallInteger)
    capacity:       Mapped[int] = mapped_column(Integer)
    description:    Mapped[Optional[str]] = mapped_column(Text)
    objectives:     Mapped[Optional[str]] = mapped_column(Text)
    careers:        Mapped[Optional[str]] = mapped_column(Text)
    admission:      Mapped[Optional[str]] = mapped_column(Text)
    logo_url:       Mapped[Optional[str]] = mapped_column(String(255))
    is_active:      Mapped[bool] = mapped_column(Boolean)
    created_at:     Mapped[datetime] = mapped_column(DateTime)
    updated_at:     Mapped[datetime] = mapped_column(DateTime)

    department: Mapped["Department"] = relationship(back_populates="filieres")
    modules:    Mapped[list["Module"]] = relationship(back_populates="filiere")
    students:   Mapped[list["Student"]] = relationship(back_populates="filiere")


# ─── MODULE ───────────────────────────────────────────────────────────────────
class Module(Base):
    __tablename__ = "modules"

    id:             Mapped[int] = mapped_column(BigInteger, primary_key=True)
    code:           Mapped[str] = mapped_column(String(30), unique=True)
    name:           Mapped[str] = mapped_column(String(200))
    filiere_id:     Mapped[int] = mapped_column(BigInteger, ForeignKey("filieres.id"))
    semester:       Mapped[int] = mapped_column(SmallInteger)
    credits:        Mapped[int] = mapped_column(SmallInteger)
    coefficient:    Mapped[float] = mapped_column(Numeric(3, 1))
    hours_cours:    Mapped[int] = mapped_column(Integer)
    hours_td:       Mapped[int] = mapped_column(Integer)
    hours_tp:       Mapped[int] = mapped_column(Integer)
    description:    Mapped[Optional[str]] = mapped_column(Text)
    prerequisites:  Mapped[Optional[str]] = mapped_column(Text)
    is_eliminatory: Mapped[bool] = mapped_column(Boolean)
    created_at:     Mapped[datetime] = mapped_column(DateTime)
    updated_at:     Mapped[datetime] = mapped_column(DateTime)

    filiere: Mapped["Filiere"] = relationship(back_populates="modules")


# ─── MODULE_TEACHERS (M:N) ────────────────────────────────────────────────────
class ModuleTeacher(Base):
    __tablename__ = "module_teachers"

    id:           Mapped[int] = mapped_column(BigInteger, primary_key=True)
    module_id:    Mapped[int] = mapped_column(BigInteger, ForeignKey("modules.id"))
    professor_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("professors.id"))
    role:         Mapped[str] = mapped_column(String(20))
    annee_univ:   Mapped[str] = mapped_column(String(9))


# ─── PROFESSOR ────────────────────────────────────────────────────────────────
class Professor(Base):
    __tablename__ = "professors"

    id:            Mapped[int] = mapped_column(BigInteger, primary_key=True)
    matricule:     Mapped[str] = mapped_column(String(30), unique=True)
    first_name:    Mapped[str] = mapped_column(String(80))
    last_name:     Mapped[str] = mapped_column(String(80))
    email:         Mapped[str] = mapped_column(String(150), unique=True)
    phone:         Mapped[Optional[str]] = mapped_column(String(30))
    grade:         Mapped[str] = mapped_column(String(20))
    department_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("departments.id"))
    specialty:     Mapped[Optional[str]] = mapped_column(String(200))
    bureau:        Mapped[Optional[str]] = mapped_column(String(50))
    photo_url:     Mapped[Optional[str]] = mapped_column(String(255))
    bio:           Mapped[Optional[str]] = mapped_column(Text)
    created_at:    Mapped[datetime] = mapped_column(DateTime)
    updated_at:    Mapped[datetime] = mapped_column(DateTime)

    department: Mapped["Department"] = relationship(back_populates="professors")


# ─── STUDENT ──────────────────────────────────────────────────────────────────
class Student(Base):
    __tablename__ = "students"

    id:           Mapped[int] = mapped_column(BigInteger, primary_key=True)
    cne:          Mapped[str] = mapped_column(String(20), unique=True)
    apogee:       Mapped[Optional[str]] = mapped_column(String(20), unique=True)
    first_name:   Mapped[str] = mapped_column(String(80))
    last_name:    Mapped[str] = mapped_column(String(80))
    email:        Mapped[str] = mapped_column(String(150), unique=True)
    phone:        Mapped[Optional[str]] = mapped_column(String(30))
    birth_date:   Mapped[Optional[date]] = mapped_column(Date)
    birth_place:  Mapped[Optional[str]] = mapped_column(String(100))
    gender:       Mapped[str] = mapped_column(String(1))
    nationality:  Mapped[Optional[str]] = mapped_column(String(50))
    cin:          Mapped[Optional[str]] = mapped_column(String(20))
    address:      Mapped[Optional[str]] = mapped_column(String(255))
    city:         Mapped[Optional[str]] = mapped_column(String(80))
    filiere_id:   Mapped[int] = mapped_column(BigInteger, ForeignKey("filieres.id"))
    annee_etude:  Mapped[int] = mapped_column(SmallInteger)
    group_name:   Mapped[Optional[str]] = mapped_column(String(20))
    is_boursier:  Mapped[bool] = mapped_column(Boolean)
    statut:       Mapped[str] = mapped_column(String(20))
    photo_url:    Mapped[Optional[str]] = mapped_column(String(255))
    enrolled_at:  Mapped[Optional[date]] = mapped_column(Date)
    created_at:   Mapped[datetime] = mapped_column(DateTime)
    updated_at:   Mapped[datetime] = mapped_column(DateTime)

    filiere: Mapped["Filiere"] = relationship(back_populates="students")


# ─── SCHEDULE ─────────────────────────────────────────────────────────────────
class Schedule(Base):
    __tablename__ = "schedules"

    id:           Mapped[int] = mapped_column(BigInteger, primary_key=True)
    filiere_id:   Mapped[int] = mapped_column(BigInteger, ForeignKey("filieres.id"))
    module_id:    Mapped[int] = mapped_column(BigInteger, ForeignKey("modules.id"))
    professor_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("professors.id"))
    semester:     Mapped[int] = mapped_column(SmallInteger)
    annee_etude:  Mapped[int] = mapped_column(SmallInteger)
    group_name:   Mapped[Optional[str]] = mapped_column(String(20))
    day_of_week:  Mapped[str] = mapped_column(String(15))
    start_time:   Mapped[time] = mapped_column(Time)
    end_time:     Mapped[time] = mapped_column(Time)
    salle:        Mapped[str] = mapped_column(String(50))
    type_seance:  Mapped[str] = mapped_column(String(10))
    annee_univ:   Mapped[str] = mapped_column(String(9))
    created_at:   Mapped[datetime] = mapped_column(DateTime)


# ─── EXAM ─────────────────────────────────────────────────────────────────────
class Exam(Base):
    __tablename__ = "exams"

    id:            Mapped[int] = mapped_column(BigInteger, primary_key=True)
    module_id:     Mapped[int] = mapped_column(BigInteger, ForeignKey("modules.id"))
    filiere_id:    Mapped[int] = mapped_column(BigInteger, ForeignKey("filieres.id"))
    exam_date:     Mapped[date] = mapped_column(Date)
    start_time:    Mapped[time] = mapped_column(Time)
    duration_min:  Mapped[int] = mapped_column(Integer)
    salle:         Mapped[str] = mapped_column(String(100))
    session:       Mapped[str] = mapped_column(String(20))
    annee_univ:    Mapped[str] = mapped_column(String(9))
    surveillants:  Mapped[Optional[str]] = mapped_column(Text)
    consignes:     Mapped[Optional[str]] = mapped_column(Text)
    created_at:    Mapped[datetime] = mapped_column(DateTime)


# ─── GRADE ────────────────────────────────────────────────────────────────────
class Grade(Base):
    __tablename__ = "grades"

    id:           Mapped[int] = mapped_column(BigInteger, primary_key=True)
    student_id:   Mapped[int] = mapped_column(BigInteger, ForeignKey("students.id"))
    module_id:    Mapped[int] = mapped_column(BigInteger, ForeignKey("modules.id"))
    note_cc:      Mapped[Optional[float]] = mapped_column(Numeric(4, 2))
    note_examen:  Mapped[Optional[float]] = mapped_column(Numeric(4, 2))
    note_finale:  Mapped[Optional[float]] = mapped_column(Numeric(4, 2))
    session:      Mapped[str] = mapped_column(String(20))
    annee_univ:   Mapped[str] = mapped_column(String(9))
    is_validated: Mapped[Optional[bool]] = mapped_column(Boolean)
    mention:      Mapped[Optional[str]] = mapped_column(String(20))
    created_at:   Mapped[datetime] = mapped_column(DateTime)
    updated_at:   Mapped[datetime] = mapped_column(DateTime)


# ─── FAQ ──────────────────────────────────────────────────────────────────────
class FaqCategory(Base):
    __tablename__ = "faq_categories"
    id:            Mapped[int] = mapped_column(BigInteger, primary_key=True)
    code:          Mapped[str] = mapped_column(String(50), unique=True)
    name:          Mapped[str] = mapped_column(String(150))
    description:   Mapped[Optional[str]] = mapped_column(Text)
    icon:          Mapped[Optional[str]] = mapped_column(String(20))
    color_hex:     Mapped[Optional[str]] = mapped_column(String(7))
    display_order: Mapped[int] = mapped_column(Integer)
    is_active:     Mapped[bool] = mapped_column(Boolean)


class FaqItem(Base):
    __tablename__ = "faq_items"
    id:            Mapped[int] = mapped_column(BigInteger, primary_key=True)
    category_id:   Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("faq_categories.id"))
    intent_tag:    Mapped[str] = mapped_column(String(80))
    question:      Mapped[str] = mapped_column(Text)
    answer:        Mapped[str] = mapped_column(Text)
    keywords:      Mapped[Optional[str]] = mapped_column(Text)
    related_url:   Mapped[Optional[str]] = mapped_column(String(255))
    consultations: Mapped[int] = mapped_column(Integer)
    is_active:     Mapped[bool] = mapped_column(Boolean)
    created_at:    Mapped[datetime] = mapped_column(DateTime)
    updated_at:    Mapped[datetime] = mapped_column(DateTime)


# ─── ANNOUNCEMENTS / EVENTS / CLUBS ───────────────────────────────────────────
class Announcement(Base):
    __tablename__ = "announcements"
    id:             Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title:          Mapped[str] = mapped_column(String(255))
    content:        Mapped[str] = mapped_column(Text)
    type:           Mapped[str] = mapped_column(String(20))
    target_filiere: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("filieres.id"))
    target_year:    Mapped[Optional[int]] = mapped_column(SmallInteger)
    author:         Mapped[Optional[str]] = mapped_column(String(150))
    published_at:   Mapped[datetime] = mapped_column(DateTime)
    expires_at:     Mapped[Optional[datetime]] = mapped_column(DateTime)
    is_pinned:      Mapped[bool] = mapped_column(Boolean)
    image_url:      Mapped[Optional[str]] = mapped_column(String(255))
    attachment_url: Mapped[Optional[str]] = mapped_column(String(255))
    created_at:     Mapped[datetime] = mapped_column(DateTime)


class Event(Base):
    __tablename__ = "events"
    id:               Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title:            Mapped[str] = mapped_column(String(255))
    description:      Mapped[Optional[str]] = mapped_column(Text)
    event_type:       Mapped[str] = mapped_column(String(30))
    start_date:       Mapped[datetime] = mapped_column(DateTime)
    end_date:         Mapped[Optional[datetime]] = mapped_column(DateTime)
    location:         Mapped[Optional[str]] = mapped_column(String(200))
    organizer:        Mapped[Optional[str]] = mapped_column(String(150))
    registration_url: Mapped[Optional[str]] = mapped_column(String(255))
    image_url:        Mapped[Optional[str]] = mapped_column(String(255))
    attachment_url:   Mapped[Optional[str]] = mapped_column(String(255))
    created_at:       Mapped[datetime] = mapped_column(DateTime)


class Club(Base):
    __tablename__ = "clubs"
    id:            Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name:          Mapped[str] = mapped_column(String(150))
    description:   Mapped[Optional[str]] = mapped_column(Text)
    category:      Mapped[str] = mapped_column(String(20))
    president:     Mapped[Optional[str]] = mapped_column(String(150))
    contact_email: Mapped[Optional[str]] = mapped_column(String(150))
    social_links:  Mapped[Optional[dict]] = mapped_column(JSON)
    logo_url:      Mapped[Optional[str]] = mapped_column(String(255))
    members_count: Mapped[int] = mapped_column(Integer)
    is_active:     Mapped[bool] = mapped_column(Boolean)
    created_at:    Mapped[datetime] = mapped_column(DateTime)


# ─── USER (auth JWT — PHASE 2) ────────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"

    id:            Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email:         Mapped[str] = mapped_column(String(150), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role:          Mapped[str] = mapped_column(String(20))   # STUDENT/PROFESSOR/SCOLARITE/ADMIN
    student_id:    Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("students.id"))
    professor_id:  Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("professors.id"))
    is_active:     Mapped[bool] = mapped_column(Boolean)
    last_login:    Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at:    Mapped[datetime] = mapped_column(DateTime)
    updated_at:    Mapped[datetime] = mapped_column(DateTime)


# ─── REVIEW (avis étudiants — PHASE 2) ────────────────────────────────────────
class Review(Base):
    __tablename__ = "reviews"

    id:             Mapped[int] = mapped_column(BigInteger, primary_key=True)
    target_type:    Mapped[str] = mapped_column(String(20))   # AI_ASSISTANT/MODULE/PROFESSOR/FILIERE/FACULTE/GENERAL
    target_id:      Mapped[Optional[int]] = mapped_column(BigInteger)
    target_label:   Mapped[Optional[str]] = mapped_column(String(200))
    rating:         Mapped[Optional[int]] = mapped_column(SmallInteger)   # 1..5
    title:          Mapped[Optional[str]] = mapped_column(String(200))
    comment:        Mapped[str] = mapped_column(Text)
    author_name:    Mapped[Optional[str]] = mapped_column(String(120))
    author_email:   Mapped[Optional[str]] = mapped_column(String(150))
    author_filiere: Mapped[Optional[str]] = mapped_column(String(120))
    status:         Mapped[str] = mapped_column(String(15))   # PENDING/APPROVED/HIDDEN
    is_pinned:      Mapped[bool] = mapped_column(Boolean)
    admin_response: Mapped[Optional[str]] = mapped_column(Text)
    ip_address:     Mapped[Optional[str]] = mapped_column(String(45))
    created_at:     Mapped[datetime] = mapped_column(DateTime)
    updated_at:     Mapped[datetime] = mapped_column(DateTime)
