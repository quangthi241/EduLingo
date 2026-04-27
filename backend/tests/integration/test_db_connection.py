import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


@pytest.mark.integration
async def test_db_connection_roundtrip(pg_url: str) -> None:
    engine = create_async_engine(pg_url)
    async with engine.connect() as conn:
        r = await conn.execute(text("SELECT 1"))
        assert r.scalar() == 1
    await engine.dispose()
