import pytest

from app.modules.content.application.dto import CreatePieceInput
from app.modules.content.application.use_cases.create_draft_piece import (
    CreateDraftPieceUseCase,
)
from app.modules.content.domain.exceptions import SlugAlreadyExists
from app.modules.content.domain.value_objects import (
    CefrLevel,
    PieceKind,
    PieceStatus,
    Slug,
    Topic,
)
from tests.unit.modules.content.application.fakes import FakePieceRepository


def _reading_input(slug: str = "coastlines") -> CreatePieceInput:
    return CreatePieceInput(
        kind=PieceKind.READING,
        slug=slug,
        title="Coastlines",
        cefr=CefrLevel.B1,
        minutes=6,
        topic=Topic.TRAVEL,
        body={
            "text": "x" * 300,
            "mcq": [
                {
                    "question": f"Q{i}",
                    "choices": ["a", "b", "c"],
                    "correct_index": 0,
                    "rationale": "r",
                }
                for i in range(3)
            ],
            "short_answer": {"prompt": "Summarize", "grading_notes": "n"},
        },
    )


@pytest.mark.asyncio
async def test_creates_draft_with_editorial_source():
    repo = FakePieceRepository()
    uc = CreateDraftPieceUseCase(repo)
    p = await uc.execute(_reading_input())
    assert p.status == PieceStatus.DRAFT
    assert p.source.value == "editorial"
    assert p.slug == Slug("coastlines")


@pytest.mark.asyncio
async def test_rejects_duplicate_slug():
    repo = FakePieceRepository()
    uc = CreateDraftPieceUseCase(repo)
    await uc.execute(_reading_input())
    with pytest.raises(SlugAlreadyExists):
        await uc.execute(_reading_input())
