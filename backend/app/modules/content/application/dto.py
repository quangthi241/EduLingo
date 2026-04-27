from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from app.modules.content.domain.entities import Piece
from app.modules.content.domain.value_objects import (
    CefrLevel,
    PieceKind,
    PieceStatus,
    Topic,
)


@dataclass(frozen=True, slots=True)
class PieceFilter:
    status: PieceStatus | None = None
    kind: PieceKind | None = None
    cefr: CefrLevel | None = None
    topic: Topic | None = None


@dataclass(frozen=True, slots=True)
class Cursor:
    created_at: datetime
    id: UUID

    def encode(self) -> str:
        payload = json.dumps({"c": self.created_at.isoformat(), "i": str(self.id)})
        return base64.urlsafe_b64encode(payload.encode()).decode()

    @classmethod
    def decode(cls, raw: str) -> Cursor:
        data = json.loads(base64.urlsafe_b64decode(raw.encode()).decode())
        return cls(created_at=datetime.fromisoformat(data["c"]), id=UUID(data["i"]))


@dataclass(frozen=True, slots=True)
class PiecePage:
    items: list[Piece]
    next_cursor: str | None


@dataclass(frozen=True, slots=True)
class GenerationSpec:
    kind: PieceKind
    cefr: CefrLevel
    topic: Topic
    seed_prompt: str | None = None


@dataclass(frozen=True, slots=True)
class CreatePieceInput:
    kind: PieceKind
    slug: str
    title: str
    cefr: CefrLevel
    minutes: int
    topic: Topic
    body: dict[str, Any]


@dataclass(frozen=True, slots=True)
class PartialPieceInput:
    title: str | None = None
    cefr: CefrLevel | None = None
    minutes: int | None = None
    topic: Topic | None = None
    body: dict[str, Any] | None = None


@dataclass(frozen=True, slots=True)
class RateWindow:
    seconds: int
    max_hits: int


@dataclass(frozen=True, slots=True)
class RateVerdict:
    allowed: bool
    retry_after_seconds: int


@dataclass(frozen=True, slots=True)
class GenerationLogEntry:
    admin_user_id: UUID
    piece_id: UUID | None
    spec: dict[str, object]
    model: str
    prompt_hash: str
    usage: dict[str, object]
    duration_ms: int
    status: str  # "succeeded" | "failed"
    error_reason: str | None = None
