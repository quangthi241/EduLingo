from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.db import Base


class PieceModel(Base):
    __tablename__ = "pieces"
    __table_args__ = (
        CheckConstraint("cefr IN ('A1','A2','B1','B2','C1')", name="pieces_cefr_chk"),
        CheckConstraint("minutes BETWEEN 1 AND 60", name="pieces_minutes_chk"),
        CheckConstraint(
            "kind IN ('reading','listening','speaking','writing')",
            name="pieces_kind_chk",
        ),
        CheckConstraint("status IN ('draft','published','archived')", name="pieces_status_chk"),
        CheckConstraint("source IN ('editorial','llm_generated')", name="pieces_source_chk"),
        Index("pieces_library_idx", "status", "kind", "cefr", "topic"),
        Index("pieces_created_at_idx", "created_at", "id"),
    )

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    cefr: Mapped[str] = mapped_column(String(2), nullable=False)
    minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    kind: Mapped[str] = mapped_column(String(16), nullable=False)
    topic: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="draft")
    source: Mapped[str] = mapped_column(String(16), nullable=False)
    generation_metadata: Mapped[dict[str, object] | None] = mapped_column(JSONB, nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )


class ReadingPieceModel(Base):
    __tablename__ = "reading_pieces"

    piece_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("pieces.id", ondelete="CASCADE"),
        primary_key=True,
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    mcq: Mapped[list[dict[str, object]]] = mapped_column(JSONB, nullable=False)
    short_answer: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)


class ListeningPieceModel(Base):
    __tablename__ = "listening_pieces"

    piece_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("pieces.id", ondelete="CASCADE"),
        primary_key=True,
    )
    audio_storage_key: Mapped[str | None] = mapped_column(String(512), nullable=True)
    audio_mime: Mapped[str | None] = mapped_column(String(64), nullable=True)
    audio_duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    transcript: Mapped[str] = mapped_column(Text, nullable=False)
    mcq: Mapped[list[dict[str, object]]] = mapped_column(JSONB, nullable=False)
    short_answer: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)


class SpeakingPieceModel(Base):
    __tablename__ = "speaking_pieces"

    piece_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("pieces.id", ondelete="CASCADE"),
        primary_key=True,
    )
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    reference_audio_storage_key: Mapped[str | None] = mapped_column(String(512), nullable=True)
    reference_audio_mime: Mapped[str | None] = mapped_column(String(64), nullable=True)
    reference_audio_duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rubric: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)


class WritingPieceModel(Base):
    __tablename__ = "writing_pieces"

    piece_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("pieces.id", ondelete="CASCADE"),
        primary_key=True,
    )
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    exemplar: Mapped[str | None] = mapped_column(Text, nullable=True)
    rubric: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)


class ContentGenerationLogModel(Base):
    __tablename__ = "content_generation_log"
    __table_args__ = (CheckConstraint("status IN ('succeeded','failed')", name="cg_log_status_chk"),)

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    admin_user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    piece_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("pieces.id", ondelete="SET NULL"),
        nullable=True,
    )
    spec: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    model: Mapped[str] = mapped_column(String(64), nullable=False)
    prompt_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    usage: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    duration_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    error_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
