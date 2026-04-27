"""Test env bootstrap + shared fixtures."""

import os
from collections.abc import Iterator

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("JWT_SECRET", "test-secret-32-chars-minimum-test-secret")
os.environ.setdefault("JWT_ALG", "HS256")
os.environ.setdefault("JWT_TTL_MIN", "10080")
os.environ.setdefault("CORS_ORIGINS", "http://localhost:3000")

import pytest
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def pg_url() -> Iterator[str]:
    """Shared postgres testcontainer for integration + e2e tests."""
    with PostgresContainer("postgres:16-alpine") as pg:
        yield pg.get_connection_url().replace("psycopg2", "asyncpg")
