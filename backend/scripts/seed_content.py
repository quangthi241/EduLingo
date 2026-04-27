from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import yaml

import app.shared.db as db_module
from app.modules.content.application.body_builder import build_body
from app.modules.content.domain.entities import Piece
from app.modules.content.domain.value_objects import (
    CefrLevel,
    PieceKind,
    PieceSource,
    Slug,
    Topic,
)
from app.modules.content.infrastructure.media.local_disk import LocalDiskMediaStorage
from app.modules.content.infrastructure.persistence.piece_repository import (
    SqlPieceRepository,
)
from app.shared.config import get_settings
from app.shared.db import get_engine

SEEDS_DIR = Path(__file__).resolve().parent.parent / "seeds" / "content"
YAML_PATH = SEEDS_DIR / "pieces.yaml"
AUDIO_DIR = SEEDS_DIR / "audio"


async def _upload_audio(media: LocalDiskMediaStorage, slug: str, file_name: str):
    src = AUDIO_DIR / file_name
    if not src.exists():
        return None
    content = src.read_bytes()
    return await media.put(f"seeds/{slug}/{file_name}", content, "audio/mpeg")


def _body_dict(entry: dict) -> dict:
    body = dict(entry["body"])
    if entry["kind"] == "reading":
        return {
            "text": body["text"].strip(),
            "mcq": [
                {
                    "question": m["question"],
                    "choices": m["choices"],
                    "correct_index": m["correct_index"],
                    "rationale": m.get("rationale", ""),
                }
                for m in body["mcq"]
            ],
            "short_answer": {
                "prompt": body["short_answer"]["prompt"],
                "grading_notes": body["short_answer"]["grading_notes"],
            },
        }
    if entry["kind"] == "listening":
        return {
            "audio_ref": None,
            "transcript": body["transcript"].strip(),
            "mcq": [
                {
                    "question": m["question"],
                    "choices": m["choices"],
                    "correct_index": m["correct_index"],
                    "rationale": m.get("rationale", ""),
                }
                for m in body["mcq"]
            ],
            "short_answer": {
                "prompt": body["short_answer"]["prompt"],
                "grading_notes": body["short_answer"]["grading_notes"],
            },
        }
    if entry["kind"] == "speaking":
        return {"prompt": body["prompt"].strip(), "reference_audio_ref": None}
    if entry["kind"] == "writing":
        return {"prompt": body["prompt"].strip(), "exemplar": body.get("exemplar")}
    raise ValueError(f"unknown kind: {entry['kind']}")


async def seed(session=None, media_root: str | None = None) -> None:
    settings = get_settings()
    owns_session = session is None
    if owns_session:
        get_engine()
        assert db_module._sessionmaker is not None
        session = db_module._sessionmaker()

    media = LocalDiskMediaStorage(root=media_root or settings.media_root)
    repo = SqlPieceRepository(session)

    entries = yaml.safe_load(YAML_PATH.read_text())

    try:
        for entry in entries:
            slug = Slug(entry["slug"])
            existing = await repo.get_by_slug(slug)
            if existing:
                continue

            kind = PieceKind(entry["kind"])
            body_payload = _body_dict(entry)

            audio_name = entry.get("audio")
            if kind is PieceKind.LISTENING and audio_name and audio_name != "null":
                ref = await _upload_audio(media, entry["slug"], audio_name)
                if ref:
                    body_payload["audio_ref"] = {
                        "storage_key": ref.storage_key,
                        "mime_type": ref.mime_type,
                        "duration_seconds": ref.duration_seconds,
                    }

            body = build_body(kind, body_payload)
            now = datetime.now(UTC)
            piece = Piece(
                id=uuid4(),
                slug=slug,
                title=entry["title"],
                cefr=CefrLevel(entry["cefr"]),
                minutes=entry["minutes"],
                kind=kind,
                topic=Topic(entry["topic"]),
                source=PieceSource.EDITORIAL,
                body=body,
                created_at=now,
                updated_at=now,
            )

            is_draft_listening = kind is PieceKind.LISTENING and body_payload.get("audio_ref") is None
            if not is_draft_listening:
                piece.publish()

            await repo.save(piece)

        if owns_session:
            await session.commit()
    finally:
        if owns_session:
            await session.close()


if __name__ == "__main__":
    asyncio.run(seed())
