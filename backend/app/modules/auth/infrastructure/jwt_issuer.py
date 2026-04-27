from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

import jwt


class JwtIssuer:
    def __init__(self, secret: str, alg: str, ttl_minutes: int) -> None:
        self._secret = secret
        self._alg = alg
        self._ttl = ttl_minutes

    def issue(self, user_id: UUID, role: str) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": str(user_id),
            "role": role,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=self._ttl)).timestamp()),
        }
        return jwt.encode(payload, self._secret, algorithm=self._alg)

    def decode(self, token: str) -> dict[str, Any]:
        return jwt.decode(token, self._secret, algorithms=[self._alg])
