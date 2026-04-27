from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.container import ContentDeps, get_content_deps
from app.modules.auth.api.dependencies import current_user_id
from app.modules.content.api.converters import piece_to_response
from app.modules.content.api.schemas import PiecePageResponse, PieceResponse
from app.modules.content.application.dto import Cursor, PieceFilter
from app.modules.content.application.use_cases.get_published_piece_by_slug import (
    GetPublishedPieceBySlugUseCase,
)
from app.modules.content.application.use_cases.list_published_pieces import (
    ListPublishedPiecesUseCase,
)
from app.modules.content.domain.entities import ListeningBody, Piece
from app.modules.content.domain.value_objects import (
    CefrLevel,
    PieceKind,
    Slug,
    Topic,
)

router = APIRouter(prefix="/api/library", tags=["library"])


async def _attach_url(deps: ContentDeps, piece: Piece) -> str | None:
    if isinstance(piece.body, ListeningBody) and piece.body.audio_ref:
        return await deps.media.url_for(piece.body.audio_ref.storage_key)
    return None


@router.get("", response_model=PiecePageResponse, response_model_by_alias=True)
async def list_library(
    cefr: str | None = Query(None),
    kind: str | None = Query(None),
    topic: str | None = Query(None),
    cursor: str | None = Query(None),
    limit: int = Query(20, ge=1, le=50),
    _user: UUID = Depends(current_user_id),
    deps: ContentDeps = Depends(get_content_deps),
) -> PiecePageResponse:
    uc = ListPublishedPiecesUseCase(deps.pieces)
    f = PieceFilter(
        cefr=CefrLevel(cefr) if cefr else None,
        kind=PieceKind(kind) if kind else None,
        topic=Topic(topic) if topic else None,
    )
    page = await uc.execute(f, Cursor.decode(cursor) if cursor else None, limit)
    items = []
    for p in page.items:
        url = await _attach_url(deps, p)
        items.append(piece_to_response(p, audio_url=url))
    return PiecePageResponse(items=items, next_cursor=page.next_cursor)


@router.get("/{slug}", response_model=PieceResponse, response_model_by_alias=True)
async def get_piece_by_slug(
    slug: str,
    _user: UUID = Depends(current_user_id),
    deps: ContentDeps = Depends(get_content_deps),
) -> PieceResponse:
    uc = GetPublishedPieceBySlugUseCase(deps.pieces)
    piece = await uc.execute(Slug(slug))
    url = await _attach_url(deps, piece)
    return piece_to_response(piece, audio_url=url)
