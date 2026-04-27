from datetime import UTC, datetime
from uuid import uuid4

from app.modules.content.api.converters import payload_to_create_input, piece_to_response
from app.modules.content.api.schemas import CreatePiecePayload
from app.modules.content.domain.entities import Piece, ReadingBody
from app.modules.content.domain.value_objects import (
    MCQ,
    CefrLevel,
    PieceKind,
    PieceSource,
    ShortAnswerPrompt,
    Slug,
    Topic,
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
    )


def test_piece_to_response_round_trip_reading():
    p = _reading_piece()
    resp = piece_to_response(p)
    dumped = resp.model_dump(by_alias=True)
    assert dumped["slug"] == "coastlines"
    assert dumped["body"]["kind"] == "reading"
    assert len(dumped["body"]["mcq"]) == 3


def test_payload_to_create_input_maps_body():
    payload = CreatePiecePayload.model_validate(
        {
            "kind": "reading",
            "slug": "x",
            "title": "t",
            "cefr": "B1",
            "minutes": 5,
            "topic": "travel",
            "body": {
                "kind": "reading",
                "text": "x" * 200,
                "mcq": [
                    {
                        "question": f"Q{i}",
                        "choices": ["a", "b"],
                        "correctIndex": 0,
                        "rationale": "r",
                    }
                    for i in range(3)
                ],
                "shortAnswer": {"prompt": "p", "gradingNotes": "n"},
            },
        }
    )
    inp = payload_to_create_input(payload)
    assert inp.slug == "x"
    assert inp.kind == PieceKind.READING
    assert inp.body["text"].startswith("x")
    assert inp.body["mcq"][0]["correct_index"] == 0
    assert inp.body["short_answer"]["prompt"] == "p"
