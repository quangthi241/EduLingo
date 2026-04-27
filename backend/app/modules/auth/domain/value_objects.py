from __future__ import annotations

import re
from dataclasses import dataclass

from app.modules.auth.domain.exceptions import InvalidEmail, WeakPassword

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True, slots=True)
class Email:
    value: str

    def __init__(self, raw: str) -> None:
        normalized = raw.strip().lower()
        if not _EMAIL_RE.match(normalized):
            raise InvalidEmail(f"invalid email: {raw!r}")
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True, slots=True)
class HashedPassword:
    value: str

    def __init__(self, raw: str) -> None:
        if not raw.startswith(("$2a$", "$2b$", "$2y$")):
            raise WeakPassword("password must be bcrypt-hashed")
        object.__setattr__(self, "value", raw)
