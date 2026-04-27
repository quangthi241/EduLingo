import pytest

from app.modules.content.application.dto import PartialPieceInput
from app.modules.content.application.use_cases.create_draft_piece import (
    CreateDraftPieceUseCase,
)
from app.modules.content.application.use_cases.update_draft_piece import (
    UpdateDraftPieceUseCase,
)
from app.modules.content.domain.exceptions import PieceStateError
from app.modules.content.domain.value_objects import CefrLevel
from tests.unit.modules.content.application.fakes import FakePieceRepository
from tests.unit.modules.content.application.test_create_draft_piece import _reading_input


@pytest.mark.asyncio
async def test_updates_draft_title_and_cefr():
    repo = FakePieceRepository()
    created = await CreateDraftPieceUseCase(repo).execute(_reading_input())
    uc = UpdateDraftPieceUseCase(repo)
    updated = await uc.execute(created.id, PartialPieceInput(title="New Title", cefr=CefrLevel.B2))
    assert updated.title == "New Title"
    assert updated.cefr == CefrLevel.B2


@pytest.mark.asyncio
async def test_cannot_update_published():
    repo = FakePieceRepository()
    created = await CreateDraftPieceUseCase(repo).execute(_reading_input())
    created.publish()
    await repo.save(created)
    uc = UpdateDraftPieceUseCase(repo)
    with pytest.raises(PieceStateError):
        await uc.execute(created.id, PartialPieceInput(title="x"))
