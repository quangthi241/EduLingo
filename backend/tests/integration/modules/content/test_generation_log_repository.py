from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.infrastructure.persistence.models import UserModel
from app.modules.content.application.dto import GenerationLogEntry
from app.modules.content.infrastructure.persistence.generation_log_repository import (
    SqlGenerationLogRepository,
)
from app.modules.content.infrastructure.persistence.models import (
    ContentGenerationLogModel,
)

pytestmark = pytest.mark.integration


async def test_record_persists_log_row(db_session: AsyncSession):
    user = UserModel(
        id=uuid4(),
        email="admin@example.com",
        password_hash="$argon2id$...",
        role="admin",
    )
    db_session.add(user)
    await db_session.flush()

    repo = SqlGenerationLogRepository(db_session)
    entry = GenerationLogEntry(
        admin_user_id=user.id,
        piece_id=None,
        spec={"kind": "reading", "cefr": "B1", "topic": "travel"},
        model="gemini-2.5-flash",
        prompt_hash="deadbeef",
        usage={"input_tokens": 10, "output_tokens": 5},
        duration_ms=1200,
        status="succeeded",
    )
    await repo.record(entry)

    res = await db_session.execute(select(ContentGenerationLogModel))
    rows = list(res.scalars().all())
    assert len(rows) == 1
    assert rows[0].admin_user_id == user.id
    assert rows[0].prompt_hash == "deadbeef"
    assert rows[0].status == "succeeded"
