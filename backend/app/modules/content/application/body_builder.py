from __future__ import annotations

from typing import Any

from app.modules.content.domain.entities import (
    ListeningBody,
    ReadingBody,
    SpeakingBody,
    WritingBody,
)
from app.modules.content.domain.value_objects import (
    DEFAULT_CEFR_RUBRIC,
    MCQ,
    MediaRef,
    PieceKind,
    ShortAnswerPrompt,
)


def _mcqs(raw: list[Any]) -> tuple[MCQ, ...]:
    return tuple(
        MCQ(
            question=d["question"],
            choices=d["choices"],
            correct_index=d["correct_index"],
            rationale=d["rationale"],
        )
        for d in raw
    )


def _sa(d: Any) -> ShortAnswerPrompt:
    return ShortAnswerPrompt(prompt=d["prompt"], grading_notes=d["grading_notes"])


def _audio(d: Any) -> MediaRef | None:
    if not d:
        return None
    return MediaRef(
        storage_key=d["storage_key"],
        mime_type=d["mime_type"],
        duration_seconds=d.get("duration_seconds"),
    )


def build_body(
    kind: PieceKind, payload: dict[str, Any]
) -> ReadingBody | ListeningBody | SpeakingBody | WritingBody:
    if kind is PieceKind.READING:
        return ReadingBody(
            text=payload["text"],
            mcq=_mcqs(payload["mcq"]),
            short_answer=_sa(payload["short_answer"]),
        )
    if kind is PieceKind.LISTENING:
        return ListeningBody(
            audio_ref=_audio(payload.get("audio_ref")),
            transcript=payload["transcript"],
            mcq=_mcqs(payload["mcq"]),
            short_answer=_sa(payload["short_answer"]),
        )
    if kind is PieceKind.SPEAKING:
        return SpeakingBody(
            prompt=payload["prompt"],
            reference_audio_ref=_audio(payload.get("reference_audio_ref")),
            rubric=DEFAULT_CEFR_RUBRIC,
        )
    if kind is PieceKind.WRITING:
        return WritingBody(
            prompt=payload["prompt"],
            exemplar=payload.get("exemplar"),
            rubric=DEFAULT_CEFR_RUBRIC,
        )
    raise ValueError(f"unknown kind: {kind}")
