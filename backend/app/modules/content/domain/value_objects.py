from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum

from app.modules.content.domain.exceptions import MCQInvalid, RubricInvalid, SlugInvalid

_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True, slots=True)
class Slug:
    value: str

    def __init__(self, raw: str) -> None:
        trimmed = (raw or "").strip()
        if not (2 <= len(trimmed) <= 64) or not _SLUG_RE.fullmatch(trimmed):
            raise SlugInvalid(f"invalid slug: {raw!r}")
        object.__setattr__(self, "value", trimmed)


class CefrLevel(StrEnum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"


class PieceKind(StrEnum):
    READING = "reading"
    LISTENING = "listening"
    SPEAKING = "speaking"
    WRITING = "writing"


class Topic(StrEnum):
    TRAVEL = "travel"
    BUSINESS = "business"
    DAILY_LIFE = "daily-life"
    ACADEMIC = "academic"
    CULTURE = "culture"
    SCIENCE = "science"


class PieceStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class PieceSource(StrEnum):
    EDITORIAL = "editorial"
    LLM_GENERATED = "llm_generated"


@dataclass(frozen=True, slots=True)
class MCQ:
    question: str
    choices: tuple[str, ...]
    correct_index: int
    rationale: str

    def __init__(
        self,
        question: str,
        choices: list[str] | tuple[str, ...],
        correct_index: int,
        rationale: str,
    ) -> None:
        if not question.strip():
            raise MCQInvalid("question must be non-empty")
        choices_t = tuple(choices)
        if not (2 <= len(choices_t) <= 5):
            raise MCQInvalid("MCQ must have 2..5 choices")
        if not (0 <= correct_index < len(choices_t)):
            raise MCQInvalid("correct_index out of range")
        if any(not c.strip() for c in choices_t):
            raise MCQInvalid("choices must be non-empty")
        object.__setattr__(self, "question", question)
        object.__setattr__(self, "choices", choices_t)
        object.__setattr__(self, "correct_index", correct_index)
        object.__setattr__(self, "rationale", rationale)


@dataclass(frozen=True, slots=True)
class ShortAnswerPrompt:
    prompt: str
    grading_notes: str

    def __post_init__(self) -> None:
        if not self.prompt.strip():
            raise ValueError("prompt must be non-empty")
        if not self.grading_notes.strip():
            raise ValueError("grading_notes must be non-empty")


@dataclass(frozen=True, slots=True)
class RubricCriterion:
    name: str
    description: str
    min_score: int
    max_score: int

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise RubricInvalid("criterion name required")
        if self.min_score != 1 or self.max_score != 5:
            raise RubricInvalid("rubric criteria are fixed 1..5")


@dataclass(frozen=True, slots=True)
class CefrRubric:
    criteria: tuple[RubricCriterion, ...]

    def __post_init__(self) -> None:
        if not self.criteria:
            raise RubricInvalid("rubric must have criteria")


@dataclass(frozen=True, slots=True)
class MediaRef:
    storage_key: str
    mime_type: str
    duration_seconds: int | None

    def __post_init__(self) -> None:
        if not self.storage_key.strip():
            raise ValueError("storage_key required")
        if not self.mime_type.strip():
            raise ValueError("mime_type required")
        if self.duration_seconds is not None and self.duration_seconds < 0:
            raise ValueError("duration_seconds must be >= 0")


DEFAULT_CEFR_RUBRIC = CefrRubric(
    criteria=(
        RubricCriterion(
            name="Task achievement",
            description="Addresses the prompt fully and relevantly.",
            min_score=1,
            max_score=5,
        ),
        RubricCriterion(
            name="Coherence",
            description="Ideas are organised and signposted clearly.",
            min_score=1,
            max_score=5,
        ),
        RubricCriterion(
            name="Range",
            description="Uses varied grammar and vocabulary appropriate to level.",
            min_score=1,
            max_score=5,
        ),
        RubricCriterion(
            name="Accuracy",
            description="Grammar, spelling, and pronunciation are accurate.",
            min_score=1,
            max_score=5,
        ),
    ),
)
