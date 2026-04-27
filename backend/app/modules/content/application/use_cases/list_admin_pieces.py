from app.modules.content.application.dto import Cursor, PieceFilter, PiecePage
from app.modules.content.application.ports import PieceRepository


class ListAdminPiecesUseCase:
    def __init__(self, pieces: PieceRepository) -> None:
        self._pieces = pieces

    async def execute(self, filter: PieceFilter, cursor: Cursor | None, limit: int) -> PiecePage:
        return await self._pieces.list(filter, cursor, limit)
