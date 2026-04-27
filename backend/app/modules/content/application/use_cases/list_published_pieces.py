from dataclasses import replace

from app.modules.content.application.dto import Cursor, PieceFilter, PiecePage
from app.modules.content.application.ports import PieceRepository
from app.modules.content.domain.value_objects import PieceStatus


class ListPublishedPiecesUseCase:
    def __init__(self, pieces: PieceRepository) -> None:
        self._pieces = pieces

    async def execute(self, filter: PieceFilter, cursor: Cursor | None, limit: int) -> PiecePage:
        if filter.status is not None and filter.status != PieceStatus.PUBLISHED:
            return PiecePage(items=[], next_cursor=None)
        forced = replace(filter, status=PieceStatus.PUBLISHED)
        return await self._pieces.list(forced, cursor, limit)
