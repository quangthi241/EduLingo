import pytest

from app.modules.content.application.dto import PieceFilter
from app.modules.content.application.use_cases.list_admin_pieces import (
    ListAdminPiecesUseCase,
)
from app.modules.content.domain.value_objects import PieceStatus
from tests.unit.modules.content.application.fakes import FakePieceRepository
from tests.unit.modules.content.application.test_list_published_pieces import _published


@pytest.mark.asyncio
async def test_returns_all_statuses_without_filter():
    repo = FakePieceRepository()
    p1 = _published("pub")
    p2 = _published("draft")
    p2.status = PieceStatus.DRAFT
    p2.published_at = None
    await repo.save(p1)
    await repo.save(p2)
    uc = ListAdminPiecesUseCase(repo)
    page = await uc.execute(PieceFilter(), cursor=None, limit=10)
    assert {p.slug.value for p in page.items} == {"pub", "draft"}


@pytest.mark.asyncio
async def test_passes_filter_through():
    repo = FakePieceRepository()
    p1 = _published("pub")
    p2 = _published("draft")
    p2.status = PieceStatus.DRAFT
    p2.published_at = None
    await repo.save(p1)
    await repo.save(p2)
    uc = ListAdminPiecesUseCase(repo)
    page = await uc.execute(PieceFilter(status=PieceStatus.DRAFT), cursor=None, limit=10)
    assert {p.slug.value for p in page.items} == {"draft"}
