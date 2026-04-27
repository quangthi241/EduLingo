from datetime import timedelta
from pathlib import Path

import pytest

from app.modules.content.infrastructure.media.local_disk import LocalDiskMediaStorage


@pytest.mark.asyncio
async def test_put_writes_file_and_returns_ref(tmp_path: Path):
    storage = LocalDiskMediaStorage(root=str(tmp_path))
    ref = await storage.put("a/b/c.mp3", b"\xff\xfe data", "audio/mpeg")
    assert ref.storage_key == "a/b/c.mp3"
    assert ref.mime_type == "audio/mpeg"
    assert (tmp_path / "a" / "b" / "c.mp3").read_bytes() == b"\xff\xfe data"


@pytest.mark.asyncio
async def test_url_for_returns_relative_path(tmp_path: Path):
    storage = LocalDiskMediaStorage(root=str(tmp_path))
    url = await storage.url_for("x.mp3", timedelta(minutes=5))
    assert url == "/media/x.mp3"


@pytest.mark.asyncio
async def test_delete_removes_file(tmp_path: Path):
    storage = LocalDiskMediaStorage(root=str(tmp_path))
    await storage.put("delete-me.mp3", b"bytes", "audio/mpeg")
    assert (tmp_path / "delete-me.mp3").exists()
    await storage.delete("delete-me.mp3")
    assert not (tmp_path / "delete-me.mp3").exists()


@pytest.mark.asyncio
async def test_delete_missing_is_idempotent(tmp_path: Path):
    storage = LocalDiskMediaStorage(root=str(tmp_path))
    await storage.delete("nope.mp3")  # no raise
