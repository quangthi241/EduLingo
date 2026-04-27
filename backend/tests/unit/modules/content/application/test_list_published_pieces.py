from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.modules.content.application.dto import PieceFilter
from app.modules.content.application.use_cases.list_published_pieces import (
    ListPublishedPiecesUseCase,
)
from app.modules.content.domain.entities import Piece, ReadingBody
from app.modules.content.domain.value_objects import (
    MCQ,
    CefrLevel,
    PieceKind,
    PieceSource,
    PieceStatus,
    ShortAnswerPrompt,
    Slug,
    Topic,
)
from tests.unit.modules.content.application.fakes import FakePieceRepository


def _published(slug: str) -> Piece:
    now = datetime.now(UTC)
    mcq = tuple(MCQ(question=f"Q{i}", choices=["a", "b"], correct_index=0, rationale="r") for i in range(3))
    p = Piece(
        id=uuid4(),
        slug=Slug(slug),
        title=slug,
        cefr=CefrLevel.B1,
        minutes=5,
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
    p.publish()
    return p


@pytest.mark.asyncio
async def test_returns_only_published():
    repo = FakePieceRepository()
    pub = _published("pub-one")
    await repo.save(pub)
    draft = _published("draft-one")
    draft.status = PieceStatus.DRAFT
    draft.published_at = None
    await repo.save(draft)

    uc = ListPublishedPiecesUseCase(repo)
    page = await uc.execute(PieceFilter(), cursor=None, limit=10)
    assert [p.slug.value for p in page.items] == ["pub-one"]


@pytest.mark.asyncio
async def test_forces_status_filter():
    repo = FakePieceRepository()
    await repo.save(_published("one"))
    uc = ListPublishedPiecesUseCase(repo)
    page = await uc.execute(PieceFilter(status=PieceStatus.DRAFT), cursor=None, limit=10)
    assert page.items == []
