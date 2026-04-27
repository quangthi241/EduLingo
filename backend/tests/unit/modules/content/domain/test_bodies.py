import pytest

from app.modules.content.domain.entities import ListeningBody, ReadingBody, SpeakingBody, WritingBody
from app.modules.content.domain.exceptions import MCQInvalid
from app.modules.content.domain.value_objects import DEFAULT_CEFR_RUBRIC, MCQ, MediaRef, ShortAnswerPrompt


def _mcq(i: int = 0) -> MCQ:
    return MCQ(question=f"Q{i}", choices=["a", "b", "c"], correct_index=0, rationale="r")


def _sa() -> ShortAnswerPrompt:
    return ShortAnswerPrompt(prompt="p", grading_notes="n")


def test_reading_body_valid():
    body = ReadingBody(
        text="hello" * 30,
        mcq=(_mcq(1), _mcq(2), _mcq(3)),
        short_answer=_sa(),
    )
    assert len(body.mcq) == 3


@pytest.mark.parametrize("n", [2, 6])
def test_reading_body_rejects_wrong_mcq_count(n):
    with pytest.raises(MCQInvalid):
        ReadingBody(
            text="hello" * 30,
            mcq=tuple(_mcq(i) for i in range(n)),
            short_answer=_sa(),
        )


def test_reading_body_rejects_short_text():
    with pytest.raises(ValueError):
        ReadingBody(text="short", mcq=(_mcq(1), _mcq(2), _mcq(3)), short_answer=_sa())


def test_reading_body_rejects_long_text():
    with pytest.raises(ValueError):
        ReadingBody(
            text="x" * 5000,
            mcq=(_mcq(1), _mcq(2), _mcq(3)),
            short_answer=_sa(),
        )


def test_listening_body_audio_optional_on_draft():
    body = ListeningBody(
        audio_ref=None,
        transcript="hi there",
        mcq=(_mcq(1), _mcq(2), _mcq(3)),
        short_answer=_sa(),
    )
    assert body.audio_ref is None


def test_listening_body_with_audio():
    body = ListeningBody(
        audio_ref=MediaRef(storage_key="k", mime_type="audio/mpeg", duration_seconds=120),
        transcript="t",
        mcq=(_mcq(1), _mcq(2), _mcq(3)),
        short_answer=_sa(),
    )
    assert body.audio_ref.duration_seconds == 120


def test_listening_body_rejects_empty_transcript():
    with pytest.raises(ValueError):
        ListeningBody(
            audio_ref=None,
            transcript="",
            mcq=(_mcq(1), _mcq(2), _mcq(3)),
            short_answer=_sa(),
        )


def test_speaking_body_valid():
    body = SpeakingBody(
        prompt="Describe your weekend.",
        reference_audio_ref=None,
        rubric=DEFAULT_CEFR_RUBRIC,
    )
    assert body.prompt.startswith("Describe")


def test_speaking_body_rejects_empty_prompt():
    with pytest.raises(ValueError):
        SpeakingBody(prompt="", reference_audio_ref=None, rubric=DEFAULT_CEFR_RUBRIC)


def test_writing_body_valid_without_exemplar():
    body = WritingBody(prompt="Write a letter.", exemplar=None, rubric=DEFAULT_CEFR_RUBRIC)
    assert body.exemplar is None


def test_writing_body_rejects_empty_prompt():
    with pytest.raises(ValueError):
        WritingBody(prompt="  ", exemplar=None, rubric=DEFAULT_CEFR_RUBRIC)
