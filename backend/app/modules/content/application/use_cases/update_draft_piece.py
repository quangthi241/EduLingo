from datetime import UTC, datetime
from uuid import UUID

from app.modules.content.application.body_builder import build_body
from app.modules.content.application.dto import PartialPieceInput
from app.modules.content.application.ports import PieceRepository
from app.modules.content.domain.entities import Piece
from app.modules.content.domain.exceptions import PieceNotFound, PieceStateError
from app.modules.content.domain.value_objects import PieceStatus


class UpdateDraftPieceUseCase:
    def __init__(self, pieces: PieceRepository) -> None:
        self._pieces = pieces

    async def execute(self, id: UUID, patch: PartialPieceInput) -> Piece:
        p = await self._pieces.get_by_id(id)
        if p is None:
            raise PieceNotFound(str(id))
        if p.status != PieceStatus.DRAFT:
            raise PieceStateError("only drafts can be updated")
        if patch.title is not None:
            p.title = patch.title
        if patch.cefr is not None:
            p.cefr = patch.cefr
        if patch.minutes is not None:
            p.minutes = patch.minutes
        if patch.topic is not None:
            p.topic = patch.topic
        if patch.body is not None:
            p.body = build_body(p.kind, patch.body)
        p.updated_at = datetime.now(UTC)
        await self._pieces.save(p)
        return p
