from datetime import UTC, datetime
from uuid import uuid4

from app.modules.content.domain.entities import ListeningBody, Piece, ReadingBody
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
from app.modules.content.infrastructure.persistence.mappers import (
    piece_to_rows,
    rows_to_piece,
)
from app.modules.content.infrastructure.persistence.models import (
    ListeningPieceModel,
    PieceModel,
    ReadingPieceModel,
)


def _reading_piece() -> Piece:
    now = datetime.now(UTC)
    mcq = tuple(MCQ(question=f"Q{i}", choices=["a", "b"], correct_index=0, rationale="r") for i in range(3))
    return Piece(
        id=uuid4(),
        slug=Slug("coastlines"),
        title="Coastlines",
        cefr=CefrLevel.B1,
        minutes=6,
        kind=PieceKind.READING,
        topic=Topic.TRAVEL,
        source=PieceSource.EDITORIAL,
        body=ReadingBody(
            text="x" * 200,
            mcq=mcq,
            short_answer=ShortAnswerPrompt(prompt="p", grading_notes="n"),
        ),
        created_at=now,
        updated_at=now,
        status=PieceStatus.DRAFT,
    )


def test_reading_piece_round_trip():
    p = _reading_piece()
    meta, body = piece_to_rows(p)
    assert isinstance(meta, PieceModel)
    assert isinstance(body, ReadingPieceModel)
    assert meta.slug == "coastlines"
    assert meta.kind == "reading"
    assert len(body.mcq) == 3

    back = rows_to_piece(meta, body)
    assert back.slug == p.slug
    assert back.body.text == p.body.text
    assert back.body.mcq[0].question == "Q0"


def test_listening_piece_with_audio_round_trip():
    now = datetime.now(UTC)
    mcq = tuple(MCQ(question=f"Q{i}", choices=["a", "b"], correct_index=0, rationale="r") for i in range(3))
    audio = MediaRef(storage_key="k.mp3", mime_type="audio/mpeg", duration_seconds=180)
    p = Piece(
        id=uuid4(),
        slug=Slug("night-radio"),
        title="Night Radio",
        cefr=CefrLevel.B1,
        minutes=5,
        kind=PieceKind.LISTENING,
        topic=Topic.CULTURE,
        source=PieceSource.EDITORIAL,
        body=ListeningBody(
            audio_ref=audio,
            transcript="t",
            mcq=mcq,
            short_answer=ShortAnswerPrompt(prompt="p", grading_notes="n"),
        ),
        created_at=now,
        updated_at=now,
    )
    meta, body = piece_to_rows(p)
    assert isinstance(body, ListeningPieceModel)
    assert body.audio_storage_key == "k.mp3"
    back = rows_to_piece(meta, body)
    assert back.body.audio_ref.storage_key == "k.mp3"
    assert back.body.audio_ref.duration_seconds == 180
