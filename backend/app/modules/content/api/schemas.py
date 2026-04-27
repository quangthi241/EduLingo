from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel


class _Base(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class MCQSchema(_Base):
    question: str
    choices: list[str]
    correct_index: int
    rationale: str


class ShortAnswerSchema(_Base):
    prompt: str
    grading_notes: str


class MediaRefSchema(_Base):
    storage_key: str
    mime_type: str
    duration_seconds: int | None = None


class ReadingBodySchema(_Base):
    kind: Literal["reading"] = "reading"
    text: str
    mcq: list[MCQSchema]
    short_answer: ShortAnswerSchema


class ListeningBodySchema(_Base):
    kind: Literal["listening"] = "listening"
    audio_ref: MediaRefSchema | None = None
    audio_url: str | None = None
    transcript: str
    mcq: list[MCQSchema]
    short_answer: ShortAnswerSchema


class RubricCriterionSchema(_Base):
    name: str
    description: str
    min_score: int
    max_score: int


class RubricSchema(_Base):
    criteria: list[RubricCriterionSchema]


class SpeakingBodySchema(_Base):
    kind: Literal["speaking"] = "speaking"
    prompt: str
    reference_audio_ref: MediaRefSchema | None = None
    reference_audio_url: str | None = None
    rubric: RubricSchema


class WritingBodySchema(_Base):
    kind: Literal["writing"] = "writing"
    prompt: str
    exemplar: str | None = None
    rubric: RubricSchema


BodySchema = Annotated[
    ReadingBodySchema | ListeningBodySchema | SpeakingBodySchema | WritingBodySchema,
    Field(discriminator="kind"),
]


class PieceResponse(_Base):
    id: UUID
    slug: str
    title: str
    cefr: str
    minutes: int
    kind: str
    topic: str
    status: str
    source: str
    created_at: datetime
    updated_at: datetime
    published_at: datetime | None = None
    body: BodySchema


class PiecePageResponse(_Base):
    items: list[PieceResponse]
    next_cursor: str | None = None


class CreatePiecePayload(_Base):
    kind: Literal["reading", "listening", "speaking", "writing"]
    slug: str
    title: str
    cefr: str
    minutes: int
    topic: str
    body: BodySchema

    @model_validator(mode="before")
    @classmethod
    def _inject_kind_into_body(cls, data: object) -> object:
        if isinstance(data, dict):
            kind = data.get("kind")
            body = data.get("body")
            if kind and isinstance(body, dict) and "kind" not in body:
                data = {**data, "body": {**body, "kind": kind}}
        return data

    def model_post_init(self, __ctx: object) -> None:
        if self.body.kind != self.kind:
            raise ValueError(f"body.kind={self.body.kind} does not match kind={self.kind}")


class UpdatePiecePayload(_Base):
    title: str | None = None
    cefr: str | None = None
    minutes: int | None = None
    topic: str | None = None
    body: BodySchema | None = None


class GeneratePiecePayload(_Base):
    kind: Literal["reading", "listening", "speaking", "writing"]
    cefr: str
    topic: str
    seed_prompt: str | None = None
