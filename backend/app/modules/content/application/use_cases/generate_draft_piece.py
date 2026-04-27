from __future__ import annotations

import hashlib
import json
import time
from typing import Any
from uuid import UUID

from app.modules.content.application.dto import (
    GenerationLogEntry,
    GenerationSpec,
    RateWindow,
)
from app.modules.content.application.ports import (
    ContentGenerator,
    GenerationLogRepository,
    PieceRepository,
    RateLimiter,
)
from app.modules.content.domain.entities import Piece
from app.modules.content.domain.exceptions import (
    GenerationFailed,
    RateLimitExceeded,
)

_MINUTE_WINDOW = RateWindow(seconds=60, max_hits=10)
_DAY_WINDOW = RateWindow(seconds=86400, max_hits=200)


class GenerateDraftPieceUseCase:
    def __init__(
        self,
        pieces: PieceRepository,
        generator: ContentGenerator,
        log: GenerationLogRepository,
        limiter: RateLimiter,
    ) -> None:
        self._pieces = pieces
        self._generator = generator
        self._log = log
        self._limiter = limiter

    async def execute(self, admin_user_id: UUID, spec: GenerationSpec) -> Piece:
        minute_key = f"content_gen:{admin_user_id}:minute"
        day_key = f"content_gen:{admin_user_id}:day"
        m = await self._limiter.check_and_increment(minute_key, _MINUTE_WINDOW)
        if not m.allowed:
            raise RateLimitExceeded(m.retry_after_seconds)
        d = await self._limiter.check_and_increment(day_key, _DAY_WINDOW)
        if not d.allowed:
            raise RateLimitExceeded(d.retry_after_seconds)

        spec_dict: dict[str, object] = {
            "kind": spec.kind.value,
            "cefr": spec.cefr.value,
            "topic": spec.topic.value,
            "seed_prompt": spec.seed_prompt,
        }
        prompt_hash = hashlib.sha256(json.dumps(spec_dict, sort_keys=True).encode()).hexdigest()
        start = time.monotonic()

        try:
            piece = await self._generator.generate_draft(spec)
        except GenerationFailed as e:
            await self._log.record(
                GenerationLogEntry(
                    admin_user_id=admin_user_id,
                    piece_id=None,
                    spec=spec_dict,
                    model="unknown",
                    prompt_hash=prompt_hash,
                    usage={},
                    duration_ms=int((time.monotonic() - start) * 1000),
                    status="failed",
                    error_reason=e.reason,
                )
            )
            raise

        await self._pieces.save(piece)
        raw_metadata = piece.generation_metadata or {}
        metadata: dict[str, Any] = dict(raw_metadata)
        await self._log.record(
            GenerationLogEntry(
                admin_user_id=admin_user_id,
                piece_id=piece.id,
                spec=spec_dict,
                model=str(metadata.get("model", "unknown")),
                prompt_hash=prompt_hash,
                usage=dict(metadata.get("usage") or {}),
                duration_ms=int((time.monotonic() - start) * 1000),
                status="succeeded",
            )
        )
        return piece
