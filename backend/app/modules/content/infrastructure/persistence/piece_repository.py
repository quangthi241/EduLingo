from __future__ import annotations

from typing import cast
from uuid import UUID

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.content.application.dto import Cursor, PieceFilter, PiecePage
from app.modules.content.domain.entities import Piece
from app.modules.content.domain.value_objects import PieceKind, Slug
from app.modules.content.infrastructure.persistence.mappers import (
    piece_to_rows,
    rows_to_piece,
)
from app.modules.content.infrastructure.persistence.models import (
    ListeningPieceModel,
    PieceModel,
    ReadingPieceModel,
    SpeakingPieceModel,
    WritingPieceModel,
)

_BODY_MODEL_BY_KIND = {
    PieceKind.READING: ReadingPieceModel,
    PieceKind.LISTENING: ListeningPieceModel,
    PieceKind.SPEAKING: SpeakingPieceModel,
    PieceKind.WRITING: WritingPieceModel,
}


class SqlPieceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def _load_body(
        self, meta: PieceModel
    ) -> ReadingPieceModel | ListeningPieceModel | SpeakingPieceModel | WritingPieceModel:
        model = _BODY_MODEL_BY_KIND[PieceKind(meta.kind)]
        result = await self._s.get(model, meta.id)
        assert result is not None, f"body row missing for piece {meta.id}"
        return cast(
            ReadingPieceModel | ListeningPieceModel | SpeakingPieceModel | WritingPieceModel,
            result,
        )

    async def get_by_id(self, id: UUID) -> Piece | None:
        meta = await self._s.get(PieceModel, id)
        if not meta:
            return None
        body = await self._load_body(meta)
        return rows_to_piece(meta, body)

    async def get_by_slug(self, slug: Slug) -> Piece | None:
        res = await self._s.execute(select(PieceModel).where(PieceModel.slug == slug.value))
        meta = res.scalar_one_or_none()
        if not meta:
            return None
        body = await self._load_body(meta)
        return rows_to_piece(meta, body)

    async def list(self, filter: PieceFilter, cursor: Cursor | None, limit: int) -> PiecePage:
        q = select(PieceModel)
        if filter.status:
            q = q.where(PieceModel.status == filter.status.value)
        if filter.kind:
            q = q.where(PieceModel.kind == filter.kind.value)
        if filter.cefr:
            q = q.where(PieceModel.cefr == filter.cefr.value)
        if filter.topic:
            q = q.where(PieceModel.topic == filter.topic.value)
        if cursor:
            q = q.where(
                or_(
                    PieceModel.created_at < cursor.created_at,
                    and_(
                        PieceModel.created_at == cursor.created_at,
                        PieceModel.id < cursor.id,
                    ),
                )
            )
        q = q.order_by(PieceModel.created_at.desc(), PieceModel.id.desc()).limit(limit + 1)
        res = await self._s.execute(q)
        rows = list(res.scalars().all())
        has_more = len(rows) > limit
        rows = rows[:limit]
        items = []
        for m in rows:
            body = await self._load_body(m)
            items.append(rows_to_piece(m, body))
        next_cursor = (
            Cursor(created_at=rows[-1].created_at, id=rows[-1].id).encode() if has_more and rows else None
        )
        return PiecePage(items=items, next_cursor=next_cursor)

    async def save(self, piece: Piece) -> None:
        meta, body = piece_to_rows(piece)
        existing = await self._s.get(PieceModel, meta.id)
        if existing is None:
            self._s.add(meta)
            await self._s.flush()  # ensure pieces row exists before FK child insert
            self._s.add(body)
        else:
            for col in (
                "slug",
                "title",
                "cefr",
                "minutes",
                "kind",
                "topic",
                "status",
                "source",
                "generation_metadata",
                "published_at",
                "updated_at",
            ):
                setattr(existing, col, getattr(meta, col))
            body_model = _BODY_MODEL_BY_KIND[PieceKind(meta.kind)]
            existing_body = await self._s.get(body_model, meta.id)
            if existing_body is None:
                self._s.add(body)
            else:
                for col, val in body.__dict__.items():
                    if col.startswith("_"):
                        continue
                    setattr(existing_body, col, val)
        await self._s.flush()

    async def delete(self, id: UUID) -> None:
        meta = await self._s.get(PieceModel, id)
        if meta:
            await self._s.delete(meta)
            await self._s.flush()
