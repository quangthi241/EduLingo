from collections.abc import AsyncIterator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import app.modules.auth.infrastructure.persistence.models  # noqa: F401
from app.modules.auth.domain.entities import Role, User
from app.modules.auth.domain.value_objects import Email, HashedPassword
from app.modules.auth.infrastructure.persistence.repository import SqlUserRepository
from app.shared.db import Base


@pytest.fixture
async def session(pg_url: str) -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(pg_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    sm = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with sm() as s:
        yield s
    await engine.dispose()


@pytest.mark.integration
async def test_repository_round_trip(session: AsyncSession) -> None:
    repo = SqlUserRepository(session)
    bcrypt_hash = "$2b$12$" + "x" * 53
    saved = await repo.add(
        User(
            id=None,
            email=Email("a@b.co"),
            password=HashedPassword(bcrypt_hash),
            role=Role.LEARNER,
        )
    )
    await session.commit()
    got = await repo.get_by_email(Email("a@b.co"))
    assert got is not None
    assert got.id == saved.id
    assert got.email.value == "a@b.co"
