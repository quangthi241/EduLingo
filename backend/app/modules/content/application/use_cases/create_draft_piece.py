from datetime import UTC, datetime
from uuid import uuid4

from app.modules.content.application.body_builder import build_body
from app.modules.content.application.dto import CreatePieceInput
from app.modules.content.application.ports import PieceRepository
from app.modules.content.domain.entities import Piece
from app.modules.content.domain.exceptions import SlugAlreadyExists
from app.modules.content.domain.value_objects import PieceSource, Slug


class CreateDraftPieceUseCase:
    def __init__(self, pieces: PieceRepository) -> None:
        self._pieces = pieces

    async def execute(self, inp: CreatePieceInput) -> Piece:
        slug = Slug(inp.slug)
        if await self._pieces.get_by_slug(slug) is not None:
            raise SlugAlreadyExists(inp.slug)
        now = datetime.now(UTC)
        piece = Piece(
            id=uuid4(),
            slug=slug,
            title=inp.title,
            cefr=inp.cefr,
            minutes=inp.minutes,
            kind=inp.kind,
            topic=inp.topic,
            source=PieceSource.EDITORIAL,
            body=build_body(inp.kind, inp.body),
            created_at=now,
            updated_at=now,
        )
        await self._pieces.save(piece)
        return piece
