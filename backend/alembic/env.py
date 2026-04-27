import asyncio
import importlib
import pkgutil
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

import app.modules
from alembic import context
from app.shared.config import get_settings
from app.shared.db import Base

# Autoload every module's ORM models so Base.metadata is complete.
for m in pkgutil.walk_packages(app.modules.__path__, prefix="app.modules."):
    if m.name.endswith(".infrastructure.persistence.models"):
        importlib.import_module(m.name)

config = context.config
config.set_main_option("sqlalchemy.url", get_settings().database_url)
if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _run_migrations(conn: Connection) -> None:
    context.configure(connection=conn, target_metadata=target_metadata, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()


async def _run_async_migrations() -> None:
    cfg = config.get_section(config.config_ini_section, {})
    engine = async_engine_from_config(cfg, prefix="sqlalchemy.", poolclass=pool.NullPool, future=True)
    async with engine.connect() as conn:
        await conn.run_sync(_run_migrations)
    await engine.dispose()


if context.is_offline_mode():
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()
else:
    asyncio.run(_run_async_migrations())
