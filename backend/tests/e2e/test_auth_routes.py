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

    # Reset the shared db module globals so get_engine() picks up the new URL.
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
async def test_register_login_me_cycle(app: FastAPI) -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as c:
        r = await c.post(
            "/api/auth/register",
            json={"email": "a@b.co", "password": "secret123", "displayName": "A"},
        )
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["email"] == "a@b.co"

        r2 = await c.get("/api/auth/me")
        assert r2.status_code == 200, r2.text
        assert r2.json()["email"] == "a@b.co"

        r3 = await c.post("/api/auth/logout")
        assert r3.status_code == 200

        r4 = await c.get("/api/auth/me")
        assert r4.status_code == 403


@pytest.mark.e2e
async def test_login_with_wrong_password_returns_404_problem(app: FastAPI) -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as c:
        await c.post(
            "/api/auth/register",
            json={"email": "x@y.co", "password": "rightpass", "displayName": None},
        )
        await c.post("/api/auth/logout")
        r = await c.post(
            "/api/auth/login",
            json={"email": "x@y.co", "password": "wrongpass"},
        )
        assert r.status_code == 404
        assert r.json()["title"] == "not_found"
