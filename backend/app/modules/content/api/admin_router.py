from __future__ import annotations

import io
from uuid import UUID

import mutagen
from fastapi import APIRouter, Depends, File, Query, UploadFile, status

from app.container import ContentDeps, get_content_deps
from app.modules.auth.api.dependencies import require_admin
from app.modules.content.api.converters import (
    payload_to_create_input,
    payload_to_partial_input,
    piece_to_response,
)
from app.modules.content.api.schemas import (
    CreatePiecePayload,
    GeneratePiecePayload,
    PiecePageResponse,
    PieceResponse,
    UpdatePiecePayload,
)
from app.modules.content.application.dto import Cursor, GenerationSpec, PieceFilter
from app.modules.content.application.use_cases.archive_piece import ArchivePieceUseCase
from app.modules.content.application.use_cases.create_draft_piece import (
    CreateDraftPieceUseCase,
)
from app.modules.content.application.use_cases.delete_draft_piece import (
    DeleteDraftPieceUseCase,
)
from app.modules.content.application.use_cases.generate_draft_piece import (
    GenerateDraftPieceUseCase,
)
from app.modules.content.application.use_cases.list_admin_pieces import (
    ListAdminPiecesUseCase,
)
from app.modules.content.application.use_cases.publish_piece import PublishPieceUseCase
from app.modules.content.application.use_cases.update_draft_piece import (
    UpdateDraftPieceUseCase,
)
from app.modules.content.application.use_cases.upload_piece_media import (
    UploadPieceMediaUseCase,
)
from app.modules.content.domain.exceptions import PieceNotFound
from app.modules.content.domain.value_objects import (
    CefrLevel,
    PieceKind,
    PieceStatus,
    Topic,
)

router = APIRouter(prefix="/api/admin/content", tags=["admin-content"])


@router.get("", response_model=PiecePageResponse, response_model_by_alias=True)
async def list_admin_pieces(
    status_: str | None = Query(None, alias="status"),
    kind: str | None = Query(None),
    cefr: str | None = Query(None),
    topic: str | None = Query(None),
    cursor: str | None = Query(None),
    limit: int = Query(20, ge=1, le=50),
    _admin: UUID = Depends(require_admin),
    deps: ContentDeps = Depends(get_content_deps),
) -> PiecePageResponse:
    uc = ListAdminPiecesUseCase(deps.pieces)
    f = PieceFilter(
        status=PieceStatus(status_) if status_ else None,
        kind=PieceKind(kind) if kind else None,
        cefr=CefrLevel(cefr) if cefr else None,
        topic=Topic(topic) if topic else None,
    )
    page = await uc.execute(f, Cursor.decode(cursor) if cursor else None, limit)
    items = [piece_to_response(p) for p in page.items]
    return PiecePageResponse(items=items, next_cursor=page.next_cursor)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=PieceResponse,
    response_model_by_alias=True,
)
async def create_draft(
    payload: CreatePiecePayload,
    _admin: UUID = Depends(require_admin),
    deps: ContentDeps = Depends(get_content_deps),
) -> PieceResponse:
    inp = payload_to_create_input(payload)
    piece = await CreateDraftPieceUseCase(deps.pieces).execute(inp)
    return piece_to_response(piece)


@router.get("/{piece_id}", response_model=PieceResponse, response_model_by_alias=True)
async def get_admin_piece(
    piece_id: UUID,
    _admin: UUID = Depends(require_admin),
    deps: ContentDeps = Depends(get_content_deps),
) -> PieceResponse:
    piece = await deps.pieces.get_by_id(piece_id)
    if piece is None:
        raise PieceNotFound(str(piece_id))
    return piece_to_response(piece)


@router.patch("/{piece_id}", response_model=PieceResponse, response_model_by_alias=True)
async def update_draft(
    piece_id: UUID,
    payload: UpdatePiecePayload,
    _admin: UUID = Depends(require_admin),
    deps: ContentDeps = Depends(get_content_deps),
) -> PieceResponse:
    existing = await deps.pieces.get_by_id(piece_id)
    if existing is None:
        raise PieceNotFound(str(piece_id))
    patch = payload_to_partial_input(existing.kind, payload)
    piece = await UpdateDraftPieceUseCase(deps.pieces).execute(piece_id, patch)
    return piece_to_response(piece)


@router.post("/{piece_id}/publish", response_model=PieceResponse, response_model_by_alias=True)
async def publish(
    piece_id: UUID,
    _admin: UUID = Depends(require_admin),
    deps: ContentDeps = Depends(get_content_deps),
) -> PieceResponse:
    piece = await PublishPieceUseCase(deps.pieces).execute(piece_id)
    return piece_to_response(piece)


@router.post("/{piece_id}/archive", response_model=PieceResponse, response_model_by_alias=True)
async def archive(
    piece_id: UUID,
    _admin: UUID = Depends(require_admin),
    deps: ContentDeps = Depends(get_content_deps),
) -> PieceResponse:
    piece = await ArchivePieceUseCase(deps.pieces).execute(piece_id)
    return piece_to_response(piece)


@router.delete("/{piece_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_draft(
    piece_id: UUID,
    _admin: UUID = Depends(require_admin),
    deps: ContentDeps = Depends(get_content_deps),
) -> None:
    uc = DeleteDraftPieceUseCase(deps.pieces, deps.media)
    await uc.execute(piece_id)


@router.post("/{piece_id}/media", response_model=PieceResponse, response_model_by_alias=True)
async def upload_media(
    piece_id: UUID,
    file: UploadFile = File(...),
    _admin: UUID = Depends(require_admin),
    deps: ContentDeps = Depends(get_content_deps),
) -> PieceResponse:
    content = await file.read()
    mime = file.content_type or "application/octet-stream"

    duration: int | None = None
    try:
        meta = mutagen.File(io.BytesIO(content))  # type: ignore[attr-defined]
        if meta is not None and getattr(meta.info, "length", None):
            duration = int(meta.info.length)
    except Exception:  # best-effort metadata extraction
        duration = None

    uc = UploadPieceMediaUseCase(deps.pieces, deps.media)
    piece = await uc.execute(piece_id, content=content, mime_type=mime, duration_seconds=duration)
    return piece_to_response(piece)


@router.post(
    "/generate",
    status_code=status.HTTP_201_CREATED,
    response_model=PieceResponse,
    response_model_by_alias=True,
)
async def generate_draft(
    payload: GeneratePiecePayload,
    admin_id: UUID = Depends(require_admin),
    deps: ContentDeps = Depends(get_content_deps),
) -> PieceResponse:
    spec = GenerationSpec(
        kind=PieceKind(payload.kind),
        cefr=CefrLevel(payload.cefr),
        topic=Topic(payload.topic),
        seed_prompt=payload.seed_prompt,
    )
    uc = GenerateDraftPieceUseCase(deps.pieces, deps.generator, deps.log, deps.rate_limiter)
    piece = await uc.execute(admin_id, spec)
    return piece_to_response(piece)
