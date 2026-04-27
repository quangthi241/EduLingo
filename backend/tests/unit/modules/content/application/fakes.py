from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from app.modules.content.application.dto import (
    Cursor,
    GenerationLogEntry,
    GenerationSpec,
    PieceFilter,
    PiecePage,
    RateVerdict,
    RateWindow,
)
from app.modules.content.domain.entities import Piece, ReadingBody
from app.modules.content.domain.exceptions import GenerationFailed
from app.modules.content.domain.value_objects import (
    MCQ,
    MediaRef,
    PieceSource,
    PieceStatus,
    ShortAnswerPrompt,
    Slug,
)


class FakePieceRepository:
    def __init__(self) -> None:
        self._by_id: dict[UUID, Piece] = {}

    async def get_by_id(self, id: UUID) -> Piece | None:
        return self._by_id.get(id)

    async def get_by_slug(self, slug: Slug) -> Piece | None:
        for p in self._by_id.values():
            if p.slug == slug:
                return p
        return None

    async def list(self, filter: PieceFilter, cursor: Cursor | None, limit: int) -> PiecePage:
        items = sorted(
            self._by_id.values(),
            key=lambda p: (p.created_at, p.id),
            reverse=True,
        )
        if filter.status:
            items = [p for p in items if p.status == filter.status]
        if filter.kind:
            items = [p for p in items if p.kind == filter.kind]
        if filter.cefr:
            items = [p for p in items if p.cefr == filter.cefr]
        if filter.topic:
            items = [p for p in items if p.topic == filter.topic]
        return PiecePage(items=items[:limit], next_cursor=None)

    async def save(self, piece: Piece) -> None:
        self._by_id[piece.id] = piece

    async def delete(self, id: UUID) -> None:
        self._by_id.pop(id, None)


class FakeMediaStorage:
    def __init__(self) -> None:
        self.store: dict[str, tuple[bytes, str]] = {}

    async def put(self, key: str, content: bytes, mime_type: str) -> MediaRef:
        self.store[key] = (content, mime_type)
        return MediaRef(storage_key=key, mime_type=mime_type, duration_seconds=None)

    async def url_for(self, key: str, expires_in: timedelta = timedelta(hours=1)) -> str:
        return f"https://fake/{key}"

    async def delete(self, key: str) -> None:
        self.store.pop(key, None)


class FakeContentGenerator:
    def __init__(self, *, fail: bool = False) -> None:
        self.fail = fail
        self.calls: list[GenerationSpec] = []

    async def generate_draft(self, spec: GenerationSpec) -> Piece:
        self.calls.append(spec)
        if self.fail:
            raise GenerationFailed("invalid_output", ["missing mcq"])
        now = datetime.now(UTC)
        mcq = tuple(
            MCQ(question=f"Q{i}", choices=["a", "b"], correct_index=0, rationale="r") for i in range(3)
        )
        return Piece(
            id=uuid4(),
            slug=Slug(f"gen-{uuid4().hex[:6]}"),
            title="Generated",
            cefr=spec.cefr,
            minutes=5,
            kind=spec.kind,
            topic=spec.topic,
            source=PieceSource.LLM_GENERATED,
            body=ReadingBody(
                text="x" * 200,
                mcq=mcq,
                short_answer=ShortAnswerPrompt(prompt="p", grading_notes="n"),
            ),
            created_at=now,
            updated_at=now,
            status=PieceStatus.DRAFT,
            generation_metadata={
                "model": "fake",
                "prompt_hash": "abc",
                "generated_at": now.isoformat(),
            },
        )


class FakeGenerationLogRepository:
    def __init__(self) -> None:
        self.entries: list[GenerationLogEntry] = []

    async def record(self, entry: GenerationLogEntry) -> None:
        self.entries.append(entry)


class FakeRateLimiter:
    def __init__(self, *, allow: bool = True, retry_after: int = 0) -> None:
        self.allow = allow
        self.retry_after = retry_after
        self.keys: list[str] = []

    async def check_and_increment(self, key: str, window: RateWindow) -> RateVerdict:
        self.keys.append(key)
        return RateVerdict(allowed=self.allow, retry_after_seconds=self.retry_after)
