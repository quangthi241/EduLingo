import pytest

from app.modules.content.application.use_cases.archive_piece import ArchivePieceUseCase
from app.modules.content.application.use_cases.create_draft_piece import (
    CreateDraftPieceUseCase,
)
from app.modules.content.application.use_cases.delete_draft_piece import (
    DeleteDraftPieceUseCase,
)
from app.modules.content.application.use_cases.publish_piece import PublishPieceUseCase
from app.modules.content.domain.exceptions import PieceNotFound, PieceStateError
from app.modules.content.domain.value_objects import PieceStatus
from tests.unit.modules.content.application.fakes import FakePieceRepository
from tests.unit.modules.content.application.test_create_draft_piece import _reading_input


@pytest.mark.asyncio
async def test_publish_transitions_and_persists():
    repo = FakePieceRepository()
    p = await CreateDraftPieceUseCase(repo).execute(_reading_input())
    uc = PublishPieceUseCase(repo)
    published = await uc.execute(p.id)
    assert published.status == PieceStatus.PUBLISHED
    reloaded = await repo.get_by_id(p.id)
    assert reloaded.status == PieceStatus.PUBLISHED


@pytest.mark.asyncio
async def test_publish_missing_raises():
    repo = FakePieceRepository()
    from uuid import uuid4

    with pytest.raises(PieceNotFound):
        await PublishPieceUseCase(repo).execute(uuid4())


@pytest.mark.asyncio
async def test_archive_requires_published():
    repo = FakePieceRepository()
    p = await CreateDraftPieceUseCase(repo).execute(_reading_input())
    with pytest.raises(PieceStateError):
        await ArchivePieceUseCase(repo).execute(p.id)


@pytest.mark.asyncio
async def test_archive_flows():
    repo = FakePieceRepository()
    p = await CreateDraftPieceUseCase(repo).execute(_reading_input())
    await PublishPieceUseCase(repo).execute(p.id)
    archived = await ArchivePieceUseCase(repo).execute(p.id)
    assert archived.status == PieceStatus.ARCHIVED


@pytest.mark.asyncio
async def test_delete_only_drafts():
    repo = FakePieceRepository()
    p = await CreateDraftPieceUseCase(repo).execute(_reading_input())
    await DeleteDraftPieceUseCase(repo).execute(p.id)
    assert await repo.get_by_id(p.id) is None


@pytest.mark.asyncio
async def test_delete_published_rejected():
    repo = FakePieceRepository()
    p = await CreateDraftPieceUseCase(repo).execute(_reading_input())
    await PublishPieceUseCase(repo).execute(p.id)
    with pytest.raises(PieceStateError):
        await DeleteDraftPieceUseCase(repo).execute(p.id)
