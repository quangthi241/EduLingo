from uuid import uuid4

import pytest

from app.modules.content.application.dto import GenerationSpec
from app.modules.content.application.use_cases.generate_draft_piece import (
    GenerateDraftPieceUseCase,
)
from app.modules.content.domain.exceptions import (
    GenerationFailed,
    RateLimitExceeded,
)
from app.modules.content.domain.value_objects import (
    CefrLevel,
    PieceKind,
    PieceStatus,
    Topic,
)
from tests.unit.modules.content.application.fakes import (
    FakeContentGenerator,
    FakeGenerationLogRepository,
    FakePieceRepository,
    FakeRateLimiter,
)


def _spec() -> GenerationSpec:
    return GenerationSpec(
        kind=PieceKind.READING,
        cefr=CefrLevel.B1,
        topic=Topic.SCIENCE,
        seed_prompt=None,
    )


@pytest.mark.asyncio
async def test_happy_path_persists_draft_and_logs_success():
    repo = FakePieceRepository()
    gen = FakeContentGenerator()
    log = FakeGenerationLogRepository()
    limiter = FakeRateLimiter()
    uc = GenerateDraftPieceUseCase(repo, gen, log, limiter)
    admin_id = uuid4()
    piece = await uc.execute(admin_id, _spec())

    assert piece.status == PieceStatus.DRAFT
    assert piece.source.value == "llm_generated"
    assert piece.generation_metadata is not None
    persisted = await repo.get_by_id(piece.id)
    assert persisted is not None
    assert len(log.entries) == 1
    assert log.entries[0].status == "succeeded"


@pytest.mark.asyncio
async def test_rate_limit_blocks_and_does_not_log():
    repo = FakePieceRepository()
    gen = FakeContentGenerator()
    log = FakeGenerationLogRepository()
    limiter = FakeRateLimiter(allow=False, retry_after=42)
    uc = GenerateDraftPieceUseCase(repo, gen, log, limiter)
    with pytest.raises(RateLimitExceeded) as exc:
        await uc.execute(uuid4(), _spec())
    assert exc.value.retry_after_seconds == 42
    assert log.entries == []
    assert gen.calls == []


@pytest.mark.asyncio
async def test_generator_failure_logs_failed():
    repo = FakePieceRepository()
    gen = FakeContentGenerator(fail=True)
    log = FakeGenerationLogRepository()
    limiter = FakeRateLimiter()
    uc = GenerateDraftPieceUseCase(repo, gen, log, limiter)
    with pytest.raises(GenerationFailed):
        await uc.execute(uuid4(), _spec())
    assert len(log.entries) == 1
    assert log.entries[0].status == "failed"
