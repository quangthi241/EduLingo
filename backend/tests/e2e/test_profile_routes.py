from collections.abc import AsyncIterator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine

import app.modules.auth.infrastructure.persistence.models
from app.shared.db import Base


@pytest.fixture
async def app(pg_url: str, monkeypatch: pytest.MonkeyPatch) -> AsyncIterator[FastAPI]:
    monkeypatch.setenv("DATABASE_URL", pg_url)
    monkeypatch.setenv("JWT_SECRET", "test-secret-" + "x" * 32)

    import app.shared.db as db_module

    db_module._engine = None
    db_module._sessionmaker = None

    engine = create_async_engine(pg_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

    from app.main import create_app

    yield create_app()

    db_module._engine = None
    db_module._sessionmaker = None


@pytest.mark.e2e
async def test_patch_me_updates_profile(app: FastAPI) -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as c:
        r = await c.post(
            "/api/auth/register",
            json={"email": "p@q.co", "password": "secret123", "displayName": "Initial"},
        )
        assert r.status_code == 200, r.text

        r2 = await c.patch(
            "/api/auth/me",
            json={
                "displayName": "Updated",
                "targetCefr": "B1",
                "goals": ["travel", "work"],
            },
        )
        assert r2.status_code == 200, r2.text
        body = r2.json()
        assert body["displayName"] == "Updated"
        assert body["targetCefr"] == "B1"
        assert body["goals"] == ["travel", "work"]

        r3 = await c.get("/api/auth/me")
        assert r3.status_code == 200
        assert r3.json()["targetCefr"] == "B1"
        assert r3.json()["goals"] == ["travel", "work"]


@pytest.mark.e2e
async def test_patch_me_requires_auth(app: FastAPI) -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as c:
        r = await c.patch(
            "/api/auth/me",
            json={"displayName": "x", "targetCefr": "B1", "goals": []},
        )
        assert r.status_code == 403


@pytest.mark.e2e
async def test_patch_me_rejects_invalid_cefr(app: FastAPI) -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as c:
        await c.post(
            "/api/auth/register",
            json={"email": "bad@c.co", "password": "secret123", "displayName": None},
        )
        r = await c.patch(
            "/api/auth/me",
            json={"displayName": None, "targetCefr": "Z9", "goals": []},
        )
        assert r.status_code == 422
        assert r.json()["title"] == "domain_error"
