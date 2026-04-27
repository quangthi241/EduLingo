from datetime import UTC, datetime
from uuid import UUID

from app.modules.content.application.ports import MediaStorage, PieceRepository
from app.modules.content.domain.entities import ListeningBody, Piece
from app.modules.content.domain.exceptions import PieceNotFound, PieceStateError
from app.modules.content.domain.value_objects import MediaRef


class UploadPieceMediaUseCase:
    def __init__(self, pieces: PieceRepository, media: MediaStorage) -> None:
        self._pieces = pieces
        self._media = media

    async def execute(
        self,
        id: UUID,
        *,
        content: bytes,
        mime_type: str,
        duration_seconds: int | None,
    ) -> Piece:
        p = await self._pieces.get_by_id(id)
        if p is None:
            raise PieceNotFound(str(id))
        if not isinstance(p.body, ListeningBody):
            raise PieceStateError("media upload only supported on listening pieces")

        key = f"pieces/{p.id}/audio-{datetime.now(UTC).strftime('%Y%m%dT%H%M%S')}"
        ref = await self._media.put(key, content, mime_type)
        ref = MediaRef(
            storage_key=ref.storage_key,
            mime_type=ref.mime_type,
            duration_seconds=duration_seconds if duration_seconds is not None else ref.duration_seconds,
        )
        p.attach_audio(ref)
        await self._pieces.save(p)
        return p
