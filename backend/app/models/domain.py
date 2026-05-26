import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, Numeric, text, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from app.core.db import Base
from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint, CheckConstraint, UUID, Integer, Numeric, Boolean, text, Index
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Index

class Profile(Base):
    __tablename__ = "profiles"

    # Definimos el ID como UUID vinculado al usuario
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    display_name: Mapped[Optional[str]] = mapped_column(String(255))
    weight_kg: Mapped[Optional[float]] = mapped_column(Numeric(5, 2))
    
    # NUEVOS CAMPOS: Altura y Foto de perfil
    height_cm: Mapped[Optional[int]] = mapped_column(Integer)
    avatar_url: Mapped[Optional[str]] = mapped_column(String)
    
    goal: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Timestamps básicos para control
    created_at: Mapped[datetime] = mapped_column(server_default=text("now()"))
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=text("now()"))
    
    # Relación con las sesiones (Si se borra el perfil, se borran sus carreras)
    sessions = relationship("Session", back_populates="profile", cascade="all, delete-orphan")

class Session(Base):
    __tablename__ = "sessions"
    
    # Identificadores
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE")
    )
    
    # Datos deportivos de la carrera
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    distance_meters: Mapped[int] = mapped_column(Integer)
    duration_seconds: Mapped[int] = mapped_column(Integer)
    calories: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(server_default=text("now()"))
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=text("now()"))
    sport: Mapped[str] = mapped_column(String(50), server_default="running")

    # Relación inversa con el perfil
    profile = relationship("Profile", back_populates="sessions")


class Follow(Base):
    __tablename__ = "follows"

    follower_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), primary_key=True)
    followed_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("follower_id", "followed_id", name="uix_follower_followed"),
        CheckConstraint("follower_id != followed_id", name="chk_no_self_follow")
    )


class Activity(Base):
    __tablename__ = "activities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False) # Ej: 'session_completed', 'challenge_joined'
    payload = Column(JSONB, nullable=False, server_default='{}')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relación para poder acceder a los datos del perfil que generó la actividad
    user = relationship("Profile", backref="activities")

    # Índice explícito descendente para optimizar las consultas del feed
    __table_args__ = (
        Index('ix_activities_created_at_desc', created_at.desc()),
    )

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    reward_points = Column(Integer, default=0)
    image_url = Column(String, nullable=True) # <--- AÑADIDO AQUÍ
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class ChallengeParticipant(Base):
    __tablename__ = "challenge_participants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    challenge_id = Column(UUID(as_uuid=True), ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, default=0)
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        # Unicidad: un usuario no puede unirse dos veces al mismo reto
        UniqueConstraint("challenge_id", "profile_id", name="uix_participant_challenge_profile"),
    )

# Añadir al final de app/models/domain.py

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    
    type = Column(String, nullable=False)  # Ej: 'new_follower', 'challenge_won', 'system'
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    
    is_read = Column(Boolean, default=False, nullable=False)
    
    # Metadatos extra (ej: ID del reto, ID del seguidor)
    data = Column(JSONB, nullable=False, server_default='{}')
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relación con el perfil
    user = relationship("Profile", backref="notifications")

    __table_args__ = (
        Index('ix_notifications_user_id_created_at', user_id, created_at.desc()),
    )

class Presence(Base):
    __tablename__ = "presence"

    # user_id es Clave Primaria y Foránea a la vez
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("profiles.id", ondelete="CASCADE"), 
        primary_key=True
    )
    
    # status: 'training' o 'idle'
    status = Column(String, nullable=False, server_default="idle")
    
    # session_id: se vincula a la sesión activa si está entrenando
    session_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("sessions.id", ondelete="SET NULL"), 
        nullable=True
    )
    
    # Timestamp con actualización automática
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )

    # Relación uno-a-uno: un perfil tiene una presencia
    user = relationship("Profile", backref=backref("presence", uselist=False))