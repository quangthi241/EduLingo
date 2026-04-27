from collections.abc import AsyncIterator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import update
from sqlalchemy.ext.asyncio import create_async_engine

# Register ORM models so create_all picks them up.
import app.modules.auth.infrastructure.persistence.models
import app.modules.content.infrastructure.persistence.models
from app.modules.auth.infrastructure.persistence.models import UserModel
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


@pytest.fixture
async def db_session(app):
    import app.shared.db as db_module

    # `app` fixture has already triggered engine init via create_app → get_settings → etc.
    # But _sessionmaker is lazy-initialized on first get_engine() call; we must force it.
    db_module.get_engine()
    assert db_module._sessionmaker is not None
    async with db_module._sessionmaker() as s:
        yield s


@pytest.fixture
async def http_client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
async def learner_cookie(http_client: AsyncClient) -> dict[str, str]:
    r = await http_client.post(
        "/api/auth/register",
        json={"email": "learner@test.local", "password": "ValidPass!234"},
    )
    assert r.status_code in (200, 201)
    return {k: v for k, v in r.cookies.items()}


@pytest.fixture
async def admin_cookie(http_client, db_session):
    r = await http_client.post(
        "/api/auth/register",
        json={"email": "admin@test.local", "password": "ValidPass!234"},
    )
    assert r.status_code in (200, 201)
    await db_session.execute(
        update(UserModel).where(UserModel.email == "admin@test.local").values(role="admin")
    )
    await db_session.commit()
    login = await http_client.post(
        "/api/auth/login",
        json={"email": "admin@test.local", "password": "ValidPass!234"},
    )
    assert login.status_code == 200
    return {k: v for k, v in login.cookies.items()}


def _reading_body_json() -> dict:
    return {
        "kind": "reading",
        "text": "x" * 200,
        "mcq": [
            {
                "question": f"Q{i}",
                "choices": ["a", "b"],
                "correctIndex": 0,
                "rationale": "r",
            }
            for i in range(3)
        ],
        "shortAnswer": {"prompt": "p", "gradingNotes": "n"},
    }


@pytest.fixture
async def seed_published_piece(http_client, admin_cookie):
    async def _seed(slug: str = "coastlines", title: str = "Coastlines"):
        create = await http_client.post(
            "/api/admin/content",
            json={
                "kind": "reading",
                "slug": slug,
                "title": title,
                "cefr": "B1",
                "minutes": 6,
                "topic": "travel",
                "body": _reading_body_json(),
            },
            cookies=admin_cookie,
        )
        assert create.status_code == 201, create.text
        piece = create.json()
        pub = await http_client.post(f"/api/admin/content/{piece['id']}/publish", cookies=admin_cookie)
        assert pub.status_code == 200, pub.text
        return pub.json()

    return _seed


@pytest.fixture
async def seed_draft_piece(http_client, admin_cookie):
    async def _seed(slug: str = "draft"):
        r = await http_client.post(
            "/api/admin/content",
            json={
                "kind": "reading",
                "slug": slug,
                "title": slug,
                "cefr": "B1",
                "minutes": 6,
                "topic": "travel",
                "body": _reading_body_json(),
            },
            cookies=admin_cookie,
        )
        assert r.status_code == 201, r.text
        return r.json()

    return _seed
