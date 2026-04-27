from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.modules.content.domain.entities import ListeningBody, Piece, ReadingBody
from app.modules.content.domain.exceptions import PieceStateError
from app.modules.content.domain.value_objects import (
    MCQ,
    CefrLevel,
    MediaRef,
    PieceKind,
    PieceSource,
    PieceStatus,
    ShortAnswerPrompt,
    Slug,
    Topic,
)


def _reading_body() -> ReadingBody:
    mcq = tuple(MCQ(question=f"Q{i}", choices=["a", "b"], correct_index=0, rationale="r") for i in range(3))
    return ReadingBody(text="x" * 200, mcq=mcq, short_answer=ShortAnswerPrompt(prompt="p", grading_notes="n"))


def test_piece_construction_defaults_draft():
    now = datetime.now(UTC)
    p = Piece(
        id=uuid4(),
        slug=Slug("coastlines"),
        title="Coastlines",
        cefr=CefrLevel.B1,
        minutes=6,
        kind=PieceKind.READING,
        topic=Topic.TRAVEL,
        source=PieceSource.EDITORIAL,
        body=_reading_body(),
        created_at=now,
        updated_at=now,
    )
    assert p.status == PieceStatus.DRAFT
    assert p.published_at is None
    assert p.generation_metadata is None


def test_piece_rejects_minutes_out_of_range():
    now = datetime.now(UTC)
    with pytest.raises(ValueError):
        Piece(
            id=uuid4(),
            slug=Slug("xx"),
            title="t",
            cefr=CefrLevel.B1,
            minutes=0,
            kind=PieceKind.READING,
            topic=Topic.TRAVEL,
            source=PieceSource.EDITORIAL,
            body=_reading_body(),
            created_at=now,
            updated_at=now,
        )


def test_piece_llm_source_requires_generation_metadata():
    now = datetime.now(UTC)
    with pytest.raises(ValueError):
        Piece(
            id=uuid4(),
            slug=Slug("llm"),
            title="t",
            cefr=CefrLevel.B1,
            minutes=5,
            kind=PieceKind.READING,
            topic=Topic.TRAVEL,
            source=PieceSource.LLM_GENERATED,
            body=_reading_body(),
            created_at=now,
            updated_at=now,
        )


def _listening_body(audio: MediaRef | None) -> ListeningBody:
    mcq = tuple(MCQ(question=f"Q{i}", choices=["a", "b"], correct_index=0, rationale="r") for i in range(3))
    return ListeningBody(
        audio_ref=audio,
        transcript="t",
        mcq=mcq,
        short_answer=ShortAnswerPrompt(prompt="p", grading_notes="n"),
    )


def _piece(body, kind=PieceKind.READING, status=PieceStatus.DRAFT) -> Piece:
    now = datetime.now(UTC)
    return Piece(
        id=uuid4(),
        slug=Slug("xx"),
        title="t",
        cefr=CefrLevel.B1,
        minutes=5,
        kind=kind,
        topic=Topic.TRAVEL,
        source=PieceSource.EDITORIAL,
        body=body,
        created_at=now,
        updated_at=now,
        status=status,
    )


def test_publish_draft_reading_transitions():
    p = _piece(_reading_body())
    p.publish()
    assert p.status == PieceStatus.PUBLISHED
    assert p.published_at is not None


def test_publish_rejects_non_draft():
    p = _piece(_reading_body(), status=PieceStatus.PUBLISHED)
    with pytest.raises(PieceStateError):
        p.publish()


def test_publish_listening_without_audio_rejected():
    p = _piece(_listening_body(None), kind=PieceKind.LISTENING)
    with pytest.raises(PieceStateError):
        p.publish()


def test_publish_listening_with_audio_ok():
    audio = MediaRef(storage_key="k", mime_type="audio/mpeg", duration_seconds=60)
    p = _piece(_listening_body(audio), kind=PieceKind.LISTENING)
    p.publish()
    assert p.status == PieceStatus.PUBLISHED


def test_archive_requires_published():
    p = _piece(_reading_body())
    with pytest.raises(PieceStateError):
        p.archive()


def test_archive_from_published_ok():
    p = _piece(_reading_body())
    p.publish()
    p.archive()
    assert p.status == PieceStatus.ARCHIVED
