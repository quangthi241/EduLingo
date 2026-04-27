import pytest

from app.modules.content.application.dto import CreatePieceInput
from app.modules.content.application.use_cases.create_draft_piece import (
    CreateDraftPieceUseCase,
)
from app.modules.content.application.use_cases.upload_piece_media import (
    UploadPieceMediaUseCase,
)
from app.modules.content.domain.entities import ListeningBody
from app.modules.content.domain.exceptions import PieceStateError
from app.modules.content.domain.value_objects import CefrLevel, PieceKind, Topic
from tests.unit.modules.content.application.fakes import (
    FakeMediaStorage,
    FakePieceRepository,
)


def _listening_input() -> CreatePieceInput:
    return CreatePieceInput(
        kind=PieceKind.LISTENING,
        slug="night-radio",
        title="Night Radio",
        cefr=CefrLevel.B1,
        minutes=5,
        topic=Topic.CULTURE,
        body={
            "audio_ref": None,
            "transcript": "a transcript",
            "mcq": [
                {
                    "question": f"Q{i}",
                    "choices": ["a", "b"],
                    "correct_index": 0,
                    "rationale": "r",
                }
                for i in range(3)
            ],
            "short_answer": {"prompt": "p", "grading_notes": "n"},
        },
    )


@pytest.mark.asyncio
async def test_upload_attaches_audio_to_listening():
    repo = FakePieceRepository()
    media = FakeMediaStorage()
    p = await CreateDraftPieceUseCase(repo).execute(_listening_input())
    uc = UploadPieceMediaUseCase(repo, media)
    updated = await uc.execute(
        p.id,
        content=b"\x00\x01bytes",
        mime_type="audio/mpeg",
        duration_seconds=180,
    )
    assert isinstance(updated.body, ListeningBody)
    assert updated.body.audio_ref is not None
    assert updated.body.audio_ref.duration_seconds == 180


@pytest.mark.asyncio
async def test_upload_rejects_non_listening():
    from tests.unit.modules.content.application.test_create_draft_piece import _reading_input

    repo = FakePieceRepository()
    media = FakeMediaStorage()
    p = await CreateDraftPieceUseCase(repo).execute(_reading_input())
    uc = UploadPieceMediaUseCase(repo, media)
    with pytest.raises(PieceStateError):
        await uc.execute(p.id, content=b"x", mime_type="audio/mpeg", duration_seconds=1)
