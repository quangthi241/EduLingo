from __future__ import annotations

from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.content.application.dto import GenerationLogEntry
from app.modules.content.infrastructure.persistence.models import (
    ContentGenerationLogModel,
)


class SqlGenerationLogRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def record(self, entry: GenerationLogEntry) -> None:
        row = ContentGenerationLogModel(
            id=uuid4(),
            admin_user_id=entry.admin_user_id,
            piece_id=entry.piece_id,
            spec=entry.spec,
            model=entry.model,
            prompt_hash=entry.prompt_hash,
            usage=entry.usage,
            duration_ms=entry.duration_ms,
            status=entry.status,
            error_reason=entry.error_reason,
        )
        self._s.add(row)
        await self._s.flush()
