import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.content.application.dto import PieceFilter
from app.modules.content.domain.value_objects import PieceStatus, Slug
from app.modules.content.infrastructure.persistence.piece_repository import (
    SqlPieceRepository,
)
from scripts.seed_content import seed

pytestmark = pytest.mark.integration


async def test_seed_is_idempotent(db_session: AsyncSession, tmp_path):
    await seed(session=db_session, media_root=str(tmp_path))
    repo = SqlPieceRepository(db_session)
    page = await repo.list(PieceFilter(), cursor=None, limit=50)
    count1 = len(page.items)
    assert count1 >= 11

    await seed(session=db_session, media_root=str(tmp_path))
    page2 = await repo.list(PieceFilter(), cursor=None, limit=50)
    assert len(page2.items) == count1


async def test_seeded_pieces_include_coastlines(db_session: AsyncSession, tmp_path):
    await seed(session=db_session, media_root=str(tmp_path))
    repo = SqlPieceRepository(db_session)

    p = await repo.get_by_slug(Slug("coastlines"))
    assert p is not None
    assert p.status == PieceStatus.PUBLISHED
