from __future__ import annotations

from typing import Any

from app.modules.content.api.schemas import (
    BodySchema,
    CreatePiecePayload,
    ListeningBodySchema,
    MCQSchema,
    MediaRefSchema,
    PieceResponse,
    ReadingBodySchema,
    RubricCriterionSchema,
    RubricSchema,
    ShortAnswerSchema,
    SpeakingBodySchema,
    UpdatePiecePayload,
    WritingBodySchema,
)
from app.modules.content.application.dto import CreatePieceInput, PartialPieceInput
from app.modules.content.domain.entities import (
    ListeningBody,
    Piece,
    ReadingBody,
    SpeakingBody,
    WritingBody,
)
from app.modules.content.domain.value_objects import (
    CefrLevel,
    CefrRubric,
    MediaRef,
    PieceKind,
    Topic,
)


def _body_dict_from_payload(kind: PieceKind, body: BodySchema) -> dict[str, Any]:
    if isinstance(body, ReadingBodySchema):
        return {
            "text": body.text,
            "mcq": [
                {
                    "question": m.question,
                    "choices": m.choices,
                    "correct_index": m.correct_index,
                    "rationale": m.rationale,
                }
                for m in body.mcq
            ],
            "short_answer": {
                "prompt": body.short_answer.prompt,
                "grading_notes": body.short_answer.grading_notes,
            },
        }
    if isinstance(body, ListeningBodySchema):
        return {
            "audio_ref": (
                {
                    "storage_key": body.audio_ref.storage_key,
                    "mime_type": body.audio_ref.mime_type,
                    "duration_seconds": body.audio_ref.duration_seconds,
                }
                if body.audio_ref
                else None
            ),
            "transcript": body.transcript,
            "mcq": [
                {
                    "question": m.question,
                    "choices": m.choices,
                    "correct_index": m.correct_index,
                    "rationale": m.rationale,
                }
                for m in body.mcq
            ],
            "short_answer": {
                "prompt": body.short_answer.prompt,
                "grading_notes": body.short_answer.grading_notes,
            },
        }
    if isinstance(body, SpeakingBodySchema):
        return {
            "prompt": body.prompt,
            "reference_audio_ref": (
                {
                    "storage_key": body.reference_audio_ref.storage_key,
                    "mime_type": body.reference_audio_ref.mime_type,
                    "duration_seconds": body.reference_audio_ref.duration_seconds,
                }
                if body.reference_audio_ref
                else None
            ),
        }
    if isinstance(body, WritingBodySchema):
        return {"prompt": body.prompt, "exemplar": body.exemplar}
    raise ValueError(f"unknown body type: {type(body)}")


def payload_to_create_input(payload: CreatePiecePayload) -> CreatePieceInput:
    kind = PieceKind(payload.kind)
    return CreatePieceInput(
        kind=kind,
        slug=payload.slug,
        title=payload.title,
        cefr=CefrLevel(payload.cefr),
        minutes=payload.minutes,
        topic=Topic(payload.topic),
        body=_body_dict_from_payload(kind, payload.body),
    )


def payload_to_partial_input(kind: PieceKind, patch: UpdatePiecePayload) -> PartialPieceInput:
    return PartialPieceInput(
        title=patch.title,
        cefr=CefrLevel(patch.cefr) if patch.cefr else None,
        minutes=patch.minutes,
        topic=Topic(patch.topic) if patch.topic else None,
        body=_body_dict_from_payload(kind, patch.body) if patch.body else None,
    )


def _media_ref_schema(ref: MediaRef | None, url: str | None) -> MediaRefSchema | None:
    if ref is None:
        return None
    return MediaRefSchema(
        storage_key=ref.storage_key,
        mime_type=ref.mime_type,
        duration_seconds=ref.duration_seconds,
    )


def _rubric_schema(rubric: CefrRubric) -> RubricSchema:
    return RubricSchema(
        criteria=[
            RubricCriterionSchema(
                name=c.name,
                description=c.description,
                min_score=c.min_score,
                max_score=c.max_score,
            )
            for c in rubric.criteria
        ]
    )


def _mcqs(mcq: tuple[Any, ...]) -> list[MCQSchema]:
    return [
        MCQSchema(
            question=m.question,
            choices=list(m.choices),
            correct_index=m.correct_index,
            rationale=m.rationale,
        )
        for m in mcq
    ]


def piece_to_response(piece: Piece, *, audio_url: str | None = None) -> PieceResponse:
    if isinstance(piece.body, ReadingBody):
        body: BodySchema = ReadingBodySchema(
            text=piece.body.text,
            mcq=_mcqs(piece.body.mcq),
            short_answer=ShortAnswerSchema(
                prompt=piece.body.short_answer.prompt,
                grading_notes=piece.body.short_answer.grading_notes,
            ),
        )
    elif isinstance(piece.body, ListeningBody):
        body = ListeningBodySchema(
            audio_ref=_media_ref_schema(piece.body.audio_ref, None),
            audio_url=audio_url,
            transcript=piece.body.transcript,
            mcq=_mcqs(piece.body.mcq),
            short_answer=ShortAnswerSchema(
                prompt=piece.body.short_answer.prompt,
                grading_notes=piece.body.short_answer.grading_notes,
            ),
        )
    elif isinstance(piece.body, SpeakingBody):
        body = SpeakingBodySchema(
            prompt=piece.body.prompt,
            reference_audio_ref=_media_ref_schema(piece.body.reference_audio_ref, None),
            reference_audio_url=audio_url,
            rubric=_rubric_schema(piece.body.rubric),
        )
    elif isinstance(piece.body, WritingBody):
        body = WritingBodySchema(
            prompt=piece.body.prompt,
            exemplar=piece.body.exemplar,
            rubric=_rubric_schema(piece.body.rubric),
        )
    else:
        raise TypeError(f"unknown body: {type(piece.body)}")

    return PieceResponse(
        id=piece.id,
        slug=piece.slug.value,
        title=piece.title,
        cefr=piece.cefr.value,
        minutes=piece.minutes,
        kind=piece.kind.value,
        topic=piece.topic.value,
        status=piece.status.value,
        source=piece.source.value,
        created_at=piece.created_at,
        updated_at=piece.updated_at,
        published_at=piece.published_at,
        body=body,
    )
