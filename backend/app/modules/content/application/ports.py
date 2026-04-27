from __future__ import annotations

from datetime import timedelta
from typing import Protocol
from uuid import UUID

from app.modules.content.application.dto import (
    Cursor,
    GenerationLogEntry,
    GenerationSpec,
    PieceFilter,
    PiecePage,
    RateVerdict,
    RateWindow,
)
from app.modules.content.domain.entities import Piece
from app.modules.content.domain.value_objects import MediaRef, Slug


class PieceRepository(Protocol):
    async def get_by_slug(self, slug: Slug) -> Piece | None: ...
    async def get_by_id(self, id: UUID) -> Piece | None: ...
    async def list(self, filter: PieceFilter, cursor: Cursor | None, limit: int) -> PiecePage: ...
    async def save(self, piece: Piece) -> None: ...
    async def delete(self, id: UUID) -> None: ...


class MediaStorage(Protocol):
    async def put(self, key: str, content: bytes, mime_type: str) -> MediaRef: ...
    async def url_for(self, key: str, expires_in: timedelta = timedelta(hours=1)) -> str: ...
    async def delete(self, key: str) -> None: ...


class ContentGenerator(Protocol):
    async def generate_draft(self, spec: GenerationSpec) -> Piece: ...


class GenerationLogRepository(Protocol):
    async def record(self, entry: GenerationLogEntry) -> None: ...


class RateLimiter(Protocol):
    async def check_and_increment(self, key: str, window: RateWindow) -> RateVerdict: ...
