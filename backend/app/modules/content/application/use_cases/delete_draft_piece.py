from uuid import UUID

from app.modules.content.application.ports import MediaStorage, PieceRepository
from app.modules.content.domain.entities import ListeningBody
from app.modules.content.domain.exceptions import PieceNotFound, PieceStateError
from app.modules.content.domain.value_objects import PieceStatus


class DeleteDraftPieceUseCase:
    def __init__(self, pieces: PieceRepository, media: MediaStorage | None = None) -> None:
        self._pieces = pieces
        self._media = media

    async def execute(self, id: UUID) -> None:
        p = await self._pieces.get_by_id(id)
        if p is None:
            raise PieceNotFound(str(id))
        if p.status != PieceStatus.DRAFT:
            raise PieceStateError("only drafts can be deleted")
        if self._media and isinstance(p.body, ListeningBody) and p.body.audio_ref:
            await self._media.delete(p.body.audio_ref.storage_key)
        await self._pieces.delete(id)
