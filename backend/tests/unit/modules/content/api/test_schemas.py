import pytest
from pydantic import ValidationError

from app.modules.content.api.schemas import (
    CreatePiecePayload,
    PieceResponse,
)


def test_create_piece_payload_reading_parses():
    payload = CreatePiecePayload.model_validate(
        {
            "kind": "reading",
            "slug": "coastlines",
            "title": "Coastlines",
            "cefr": "B1",
            "minutes": 6,
            "topic": "travel",
            "body": {
                "text": "x" * 200,
                "mcq": [
                    {
                        "question": f"Q{i}",
                        "choices": ["a", "b", "c"],
                        "correctIndex": 0,
                        "rationale": "r",
                    }
                    for i in range(3)
                ],
                "shortAnswer": {"prompt": "s", "gradingNotes": "n"},
            },
        }
    )
    assert payload.kind == "reading"
    assert payload.body.mcq[0].correct_index == 0


def test_listening_payload_accepts_null_audio_ref():
    payload = CreatePiecePayload.model_validate(
        {
            "kind": "listening",
            "slug": "night-radio",
            "title": "Night Radio",
            "cefr": "B1",
            "minutes": 5,
            "topic": "culture",
            "body": {
                "audioRef": None,
                "transcript": "t",
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
    assert payload.body.audio_ref is None


def test_piece_response_is_camel_cased_on_serialization():
    from datetime import UTC, datetime
    from uuid import uuid4

    payload = {
        "id": uuid4(),
        "slug": "coastlines",
        "title": "Coastlines",
        "cefr": "B1",
        "minutes": 6,
        "topic": "travel",
        "status": "draft",
        "source": "editorial",
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
        "published_at": None,
        "kind": "reading",
        "body": {
            "kind": "reading",
            "text": "x" * 200,
            "mcq": [
                {"question": "Q", "choices": ["a", "b"], "correct_index": 0, "rationale": "r"}
                for _ in range(3)
            ],
            "short_answer": {"prompt": "p", "grading_notes": "n"},
        },
    }
    resp = PieceResponse.model_validate(payload)
    dumped = resp.model_dump(by_alias=True)
    assert "createdAt" in dumped
    assert "publishedAt" in dumped
    assert dumped["body"]["shortAnswer"] == {"prompt": "p", "gradingNotes": "n"}


def test_create_piece_wrong_body_for_kind_rejected():
    with pytest.raises(ValidationError):
        CreatePiecePayload.model_validate(
            {
                "kind": "reading",
                "slug": "x",
                "title": "t",
                "cefr": "B1",
                "minutes": 5,
                "topic": "travel",
                "body": {
                    "kind": "listening",  # wrong
                    "transcript": "t",
                    "mcq": [],
                    "shortAnswer": {"prompt": "p", "gradingNotes": "n"},
                },
            }
        )
