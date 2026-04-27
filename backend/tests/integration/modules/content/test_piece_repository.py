from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.content.application.dto import Cursor, PieceFilter
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
from app.modules.content.infrastructure.persistence.piece_repository import (
    SqlPieceRepository,
)

pytestmark = pytest.mark.integration


def _reading(slug: str, status: PieceStatus = PieceStatus.DRAFT) -> Piece:
    now = datetime.now(UTC)
    mcq = tuple(MCQ(question=f"Q{i}", choices=["a", "b"], correct_index=0, rationale="r") for i in range(3))
    return Piece(
        id=uuid4(),
        slug=Slug(slug),
        title=slug.title(),
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
        status=status,
    )


async def test_save_then_get_by_slug(db_session: AsyncSession):
    repo = SqlPieceRepository(db_session)
    p = _reading("coastlines")
    await repo.save(p)
    got = await repo.get_by_slug(Slug("coastlines"))
    assert got is not None
    assert got.id == p.id


async def test_save_update_is_idempotent(db_session: AsyncSession):
    repo = SqlPieceRepository(db_session)
    p = _reading("update-me")
    await repo.save(p)
    p.title = "Updated Title"
    await repo.save(p)
    got = await repo.get_by_id(p.id)
    assert got.title == "Updated Title"


async def test_list_with_filters_and_cursor(db_session: AsyncSession):
    repo = SqlPieceRepository(db_session)
    for n in ["alpha", "beta", "gamma", "delta", "epsilon"]:
        await repo.save(_reading(n, status=PieceStatus.PUBLISHED))

    page1 = await repo.list(PieceFilter(status=PieceStatus.PUBLISHED), cursor=None, limit=2)
    assert len(page1.items) == 2
    assert page1.next_cursor is not None

    page2 = await repo.list(
        PieceFilter(status=PieceStatus.PUBLISHED),
        cursor=Cursor.decode(page1.next_cursor),
        limit=2,
    )
    assert len(page2.items) == 2
    assert {i.slug.value for i in page1.items}.isdisjoint({i.slug.value for i in page2.items})


async def test_delete(db_session: AsyncSession):
    repo = SqlPieceRepository(db_session)
    p = _reading("to-delete")
    await repo.save(p)
    await repo.delete(p.id)
    assert await repo.get_by_id(p.id) is None
