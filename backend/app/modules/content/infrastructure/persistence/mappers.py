from __future__ import annotations

from typing import Any

from app.modules.content.domain.entities import (
    ListeningBody,
    Piece,
    ReadingBody,
    SpeakingBody,
    WritingBody,
)
from app.modules.content.domain.value_objects import (
    DEFAULT_CEFR_RUBRIC,
    MCQ,
    CefrLevel,
    MediaRef,
    PieceKind,
    PieceSource,
    PieceStatus,
    ShortAnswerPrompt,
    Slug,
    Topic,
)
from app.modules.content.infrastructure.persistence.models import (
    ListeningPieceModel,
    PieceModel,
    ReadingPieceModel,
    SpeakingPieceModel,
    WritingPieceModel,
)

KindBodyRow = ReadingPieceModel | ListeningPieceModel | SpeakingPieceModel | WritingPieceModel


def _mcq_to_dict(m: MCQ) -> dict[str, Any]:
    return {
        "question": m.question,
        "choices": list(m.choices),
        "correct_index": m.correct_index,
        "rationale": m.rationale,
    }


def _mcq_from_dict(d: dict[str, Any]) -> MCQ:
    return MCQ(
        question=d["question"],
        choices=d["choices"],
        correct_index=d["correct_index"],
        rationale=d["rationale"],
    )


def _sa_to_dict(s: ShortAnswerPrompt) -> dict[str, Any]:
    return {"prompt": s.prompt, "grading_notes": s.grading_notes}


def _sa_from_dict(d: dict[str, Any]) -> ShortAnswerPrompt:
    return ShortAnswerPrompt(prompt=d["prompt"], grading_notes=d["grading_notes"])


def _rubric_to_dict(r: Any) -> dict[str, Any]:
    return {
        "criteria": [
            {
                "name": c.name,
                "description": c.description,
                "min_score": c.min_score,
                "max_score": c.max_score,
            }
            for c in r.criteria
        ],
    }


def _rubric_from_dict(d: dict[str, Any]) -> Any:
    return DEFAULT_CEFR_RUBRIC


def piece_to_rows(p: Piece) -> tuple[PieceModel, KindBodyRow]:
    meta = PieceModel(
        id=p.id,
        slug=p.slug.value,
        title=p.title,
        cefr=p.cefr.value,
        minutes=p.minutes,
        kind=p.kind.value,
        topic=p.topic.value,
        status=p.status.value,
        source=p.source.value,
        generation_metadata=p.generation_metadata,
        published_at=p.published_at,
        created_at=p.created_at,
        updated_at=p.updated_at,
    )
    body_row: KindBodyRow
    if isinstance(p.body, ReadingBody):
        body_row = ReadingPieceModel(
            piece_id=p.id,
            text=p.body.text,
            mcq=[_mcq_to_dict(m) for m in p.body.mcq],
            short_answer=_sa_to_dict(p.body.short_answer),
        )
    elif isinstance(p.body, ListeningBody):
        a = p.body.audio_ref
        body_row = ListeningPieceModel(
            piece_id=p.id,
            audio_storage_key=a.storage_key if a else None,
            audio_mime=a.mime_type if a else None,
            audio_duration_seconds=a.duration_seconds if a else None,
            transcript=p.body.transcript,
            mcq=[_mcq_to_dict(m) for m in p.body.mcq],
            short_answer=_sa_to_dict(p.body.short_answer),
        )
    elif isinstance(p.body, SpeakingBody):
        a2 = p.body.reference_audio_ref
        body_row = SpeakingPieceModel(
            piece_id=p.id,
            prompt=p.body.prompt,
            reference_audio_storage_key=a2.storage_key if a2 else None,
            reference_audio_mime=a2.mime_type if a2 else None,
            reference_audio_duration_seconds=a2.duration_seconds if a2 else None,
            rubric=_rubric_to_dict(p.body.rubric),
        )
    elif isinstance(p.body, WritingBody):
        body_row = WritingPieceModel(
            piece_id=p.id,
            prompt=p.body.prompt,
            exemplar=p.body.exemplar,
            rubric=_rubric_to_dict(p.body.rubric),
        )
    else:
        raise TypeError(f"unknown body type: {type(p.body)}")
    return meta, body_row


def rows_to_piece(meta: PieceModel, body: KindBodyRow) -> Piece:
    kind = PieceKind(meta.kind)
    if kind is PieceKind.READING:
        assert isinstance(body, ReadingPieceModel)
        domain_body: ReadingBody | ListeningBody | SpeakingBody | WritingBody = ReadingBody(
            text=body.text,
            mcq=tuple(_mcq_from_dict(d) for d in body.mcq),
            short_answer=_sa_from_dict(body.short_answer),
        )
    elif kind is PieceKind.LISTENING:
        assert isinstance(body, ListeningPieceModel)
        audio = (
            MediaRef(
                storage_key=body.audio_storage_key,
                mime_type=body.audio_mime if body.audio_mime is not None else "",
                duration_seconds=body.audio_duration_seconds,
            )
            if body.audio_storage_key
            else None
        )
        domain_body = ListeningBody(
            audio_ref=audio,
            transcript=body.transcript,
            mcq=tuple(_mcq_from_dict(d) for d in body.mcq),
            short_answer=_sa_from_dict(body.short_answer),
        )
    elif kind is PieceKind.SPEAKING:
        assert isinstance(body, SpeakingPieceModel)
        ref_audio = (
            MediaRef(
                storage_key=body.reference_audio_storage_key,
                mime_type=body.reference_audio_mime if body.reference_audio_mime is not None else "",
                duration_seconds=body.reference_audio_duration_seconds,
            )
            if body.reference_audio_storage_key
            else None
        )
        domain_body = SpeakingBody(
            prompt=body.prompt,
            reference_audio_ref=ref_audio,
            rubric=_rubric_from_dict(body.rubric),
        )
    elif kind is PieceKind.WRITING:
        assert isinstance(body, WritingPieceModel)
        domain_body = WritingBody(
            prompt=body.prompt,
            exemplar=body.exemplar,
            rubric=_rubric_from_dict(body.rubric),
        )
    else:
        raise TypeError(f"unknown kind: {kind}")

    return Piece(
        id=meta.id,
        slug=Slug(meta.slug),
        title=meta.title,
        cefr=CefrLevel(meta.cefr),
        minutes=meta.minutes,
        kind=kind,
        topic=Topic(meta.topic),
        source=PieceSource(meta.source),
        body=domain_body,
        created_at=meta.created_at,
        updated_at=meta.updated_at,
        status=PieceStatus(meta.status),
        generation_metadata=meta.generation_metadata,
        published_at=meta.published_at,
    )
