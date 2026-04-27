from app.modules.content.application.ports import PieceRepository
from app.modules.content.domain.entities import Piece
from app.modules.content.domain.exceptions import PieceNotFound
from app.modules.content.domain.value_objects import PieceStatus, Slug


class GetPublishedPieceBySlugUseCase:
    def __init__(self, pieces: PieceRepository) -> None:
        self._pieces = pieces

    async def execute(self, slug: Slug) -> Piece:
        p = await self._pieces.get_by_slug(slug)
        if p is None or p.status != PieceStatus.PUBLISHED:
            raise PieceNotFound(slug.value)
        return p
