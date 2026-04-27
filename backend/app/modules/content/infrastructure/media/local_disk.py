from __future__ import annotations

import asyncio
from datetime import timedelta
from pathlib import Path

from app.modules.content.domain.value_objects import MediaRef


class LocalDiskMediaStorage:
    def __init__(self, root: str) -> None:
        self._root = Path(root)
        self._root.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        return self._root / key

    async def put(self, key: str, content: bytes, mime_type: str) -> MediaRef:
        def _write() -> None:
            path = self._path(key)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)

        await asyncio.to_thread(_write)
        duration = None
        try:
            import mutagen  # noqa: PLC0415

            meta = await asyncio.to_thread(mutagen.File, str(self._path(key)))  # type: ignore[attr-defined]
            if meta is not None and getattr(meta.info, "length", None):
                duration = int(meta.info.length)
        except Exception:
            duration = None
        return MediaRef(storage_key=key, mime_type=mime_type, duration_seconds=duration)

    async def url_for(
        self, key: str, expires_in: timedelta = timedelta(hours=1)
    ) -> str:
        return f"/media/{key}"

    async def delete(self, key: str) -> None:
        def _unlink() -> None:
            p = self._path(key)
            if p.exists():
                p.unlink()

        await asyncio.to_thread(_unlink)
