from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from app.modules.content.domain.exceptions import MCQInvalid, PieceStateError
from app.modules.content.domain.value_objects import (
    MCQ,
    CefrLevel,
    CefrRubric,
    MediaRef,
    PieceKind,
    PieceSource,
    PieceStatus,
    ShortAnswerPrompt,
    Slug,
    Topic,
)


def _validate_mcq_count(mcq: tuple[MCQ, ...]) -> None:
    if not (3 <= len(mcq) <= 5):
        raise MCQInvalid("must have 3..5 MCQs")


@dataclass(frozen=True, slots=True)
class ReadingBody:
    text: str
    mcq: tuple[MCQ, ...]
    short_answer: ShortAnswerPrompt

    def __post_init__(self) -> None:
        if not (100 <= len(self.text) <= 4000):
            raise ValueError("reading text must be 100..4000 chars")
        _validate_mcq_count(self.mcq)


@dataclass(frozen=True, slots=True)
class ListeningBody:
    audio_ref: MediaRef | None
    transcript: str
    mcq: tuple[MCQ, ...]
    short_answer: ShortAnswerPrompt

    def __post_init__(self) -> None:
        if not self.transcript.strip():
            raise ValueError("transcript required")
        _validate_mcq_count(self.mcq)


@dataclass(frozen=True, slots=True)
class SpeakingBody:
    prompt: str
    reference_audio_ref: MediaRef | None
    rubric: CefrRubric

    def __post_init__(self) -> None:
        if not self.prompt.strip():
            raise ValueError("speaking prompt required")


@dataclass(frozen=True, slots=True)
class WritingBody:
    prompt: str
    exemplar: str | None
    rubric: CefrRubric

    def __post_init__(self) -> None:
        if not self.prompt.strip():
            raise ValueError("writing prompt required")


PieceBody = ReadingBody | ListeningBody | SpeakingBody | WritingBody

_REQUIRED_GEN_KEYS = {"model", "prompt_hash", "generated_at"}


@dataclass(slots=True)
class Piece:
    id: UUID
    slug: Slug
    title: str
    cefr: CefrLevel
    minutes: int
    kind: PieceKind
    topic: Topic
    source: PieceSource
    body: PieceBody
    created_at: datetime
    updated_at: datetime
    status: PieceStatus = PieceStatus.DRAFT
    generation_metadata: dict[str, object] | None = None
    published_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.title.strip() or len(self.title) > 120:
            raise ValueError("title must be 1..120 chars")
        if not (1 <= self.minutes <= 60):
            raise ValueError("minutes must be 1..60")
        if not self._body_matches_kind():
            raise ValueError(f"body type does not match kind={self.kind}")
        if self.source == PieceSource.LLM_GENERATED and (
            not self.generation_metadata or not _REQUIRED_GEN_KEYS.issubset(self.generation_metadata.keys())
        ):
            raise ValueError(
                f"llm_generated pieces require generation_metadata with {sorted(_REQUIRED_GEN_KEYS)}"
            )

    def _body_matches_kind(self) -> bool:
        return {
            PieceKind.READING: isinstance(self.body, ReadingBody),
            PieceKind.LISTENING: isinstance(self.body, ListeningBody),
            PieceKind.SPEAKING: isinstance(self.body, SpeakingBody),
            PieceKind.WRITING: isinstance(self.body, WritingBody),
        }[self.kind]

    def publish(self) -> None:
        if self.status != PieceStatus.DRAFT:
            raise PieceStateError(f"cannot publish from status={self.status}")
        if isinstance(self.body, ListeningBody) and self.body.audio_ref is None:
            raise PieceStateError("listening piece requires audio before publish")
        now = datetime.now(UTC)
        self.status = PieceStatus.PUBLISHED
        self.published_at = now
        self.updated_at = now

    def archive(self) -> None:
        if self.status != PieceStatus.PUBLISHED:
            raise PieceStateError(f"cannot archive from status={self.status}")
        self.status = PieceStatus.ARCHIVED
        self.updated_at = datetime.now(UTC)

    def attach_audio(self, media: MediaRef) -> None:
        if not isinstance(self.body, ListeningBody):
            raise PieceStateError("only listening pieces have audio")
        self.body = ListeningBody(
            audio_ref=media,
            transcript=self.body.transcript,
            mcq=self.body.mcq,
            short_answer=self.body.short_answer,
        )
        self.updated_at = datetime.now(UTC)
