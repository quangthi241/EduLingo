from uuid import uuid4

import pytest
from fastapi import Request

from app.modules.auth.api.dependencies import (
    COOKIE_NAME,
    current_user_claims,
    require_admin,
)
from app.shared.errors import PermissionDeniedError


class _FakeTokens:
    def __init__(self, claims):
        self._claims = claims

    def decode(self, raw):
        if raw == "bad":
            raise ValueError("nope")
        return self._claims


def _req(cookie: str | None):
    scope = {"type": "http", "headers": []}
    req = Request(scope)
    req.scope["headers"] = [(b"cookie", f"{COOKIE_NAME}={cookie}".encode())] if cookie else []
    return req


@pytest.mark.asyncio
async def test_current_user_claims_returns_decoded_payload():
    uid = uuid4()
    claims = {"sub": str(uid), "role": "learner"}
    tokens = _FakeTokens(claims)
    out = await current_user_claims(_req("ok"), tokens)  # type: ignore[arg-type]
    assert out == claims


@pytest.mark.asyncio
async def test_current_user_claims_without_cookie_raises():
    tokens = _FakeTokens({"sub": str(uuid4()), "role": "learner"})
    with pytest.raises(PermissionDeniedError):
        await current_user_claims(_req(None), tokens)  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_current_user_claims_invalid_token_raises():
    tokens = _FakeTokens({"sub": str(uuid4()), "role": "learner"})
    with pytest.raises(PermissionDeniedError):
        await current_user_claims(_req("bad"), tokens)  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_require_admin_returns_uuid_when_admin():
    uid = uuid4()
    claims = {"sub": str(uid), "role": "admin"}
    out = await require_admin(claims)
    assert out == uid


@pytest.mark.asyncio
async def test_require_admin_rejects_learner():
    claims = {"sub": str(uuid4()), "role": "learner"}
    with pytest.raises(PermissionDeniedError):
        await require_admin(claims)


@pytest.mark.asyncio
async def test_require_admin_rejects_missing_role():
    claims = {"sub": str(uuid4())}
    with pytest.raises(PermissionDeniedError):
        await require_admin(claims)
