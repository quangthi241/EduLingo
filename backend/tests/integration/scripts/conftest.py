from collections.abc import AsyncIterator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Register ORM models so Base.metadata.create_all picks them up.
import app.modules.auth.infrastructure.persistence.models
import app.modules.content.infrastructure.persistence.models  # noqa: F401
from app.shared.db import Base


@pytest.fixture
async def db_session(pg_url: str, monkeypatch: pytest.MonkeyPatch) -> AsyncIterator[AsyncSession]:
    monkeypatch.setenv("DATABASE_URL", pg_url)

    # Reset db module globals so get_engine() picks up the test pg_url.
    import app.shared.db as db_module

    db_module._engine = None
    db_module._sessionmaker = None

    engine = create_async_engine(pg_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

    # Now yield a fresh session bound to a fresh engine.
    test_engine = create_async_engine(pg_url)
    Sessionmaker = async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)
    async with Sessionmaker() as s:
        yield s
    await test_engine.dispose()

    # Cleanup: reset module globals so subsequent tests get a clean lazy init.
    db_module._engine = None
    db_module._sessionmaker = None
