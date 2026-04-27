from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID

from app.modules.auth.domain.value_objects import Email, HashedPassword


class Role(StrEnum):
    LEARNER = "learner"
    ADMIN = "admin"


@dataclass(slots=True)
class User:
    id: UUID | None
    email: Email
    password: HashedPassword
    role: Role = Role.LEARNER
    display_name: str | None = None
    target_cefr: str | None = None
    goals: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
