from uuid import UUID

from app.modules.content.application.ports import PieceRepository
from app.modules.content.domain.entities import Piece
from app.modules.content.domain.exceptions import PieceNotFound


class PublishPieceUseCase:
    def __init__(self, pieces: PieceRepository) -> None:
        self._pieces = pieces

    async def execute(self, id: UUID) -> Piece:
        p = await self._pieces.get_by_id(id)
        if p is None:
            raise PieceNotFound(str(id))
        p.publish()
        await self._pieces.save(p)
        return p
