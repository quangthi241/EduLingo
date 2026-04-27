import pytest

from app.modules.content.application.use_cases.get_published_piece_by_slug import (
    GetPublishedPieceBySlugUseCase,
)
from app.modules.content.domain.exceptions import PieceNotFound
from app.modules.content.domain.value_objects import PieceStatus, Slug
from tests.unit.modules.content.application.fakes import FakePieceRepository
from tests.unit.modules.content.application.test_list_published_pieces import _published


@pytest.mark.asyncio
async def test_returns_published():
    repo = FakePieceRepository()
    p = _published("coastlines")
    await repo.save(p)
    uc = GetPublishedPieceBySlugUseCase(repo)
    got = await uc.execute(Slug("coastlines"))
    assert got.id == p.id


@pytest.mark.asyncio
async def test_draft_raises_not_found():
    repo = FakePieceRepository()
    p = _published("draft-only")
    p.status = PieceStatus.DRAFT
    p.published_at = None
    await repo.save(p)
    uc = GetPublishedPieceBySlugUseCase(repo)
    with pytest.raises(PieceNotFound):
        await uc.execute(Slug("draft-only"))


@pytest.mark.asyncio
async def test_missing_raises_not_found():
    repo = FakePieceRepository()
    uc = GetPublishedPieceBySlugUseCase(repo)
    with pytest.raises(PieceNotFound):
        await uc.execute(Slug("nope"))
