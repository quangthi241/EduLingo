import pytest

from app.modules.content.domain.exceptions import MCQInvalid, RubricInvalid, SlugInvalid
from app.modules.content.domain.value_objects import (
    DEFAULT_CEFR_RUBRIC,
    MCQ,
    CefrLevel,
    CefrRubric,
    MediaRef,
    PieceKind,
    PieceSource,
    PieceStatus,
    RubricCriterion,
    ShortAnswerPrompt,
    Slug,
    Topic,
)


def test_slug_accepts_lower_kebab():
    assert Slug("night-radio").value == "night-radio"


@pytest.mark.parametrize("bad", ["", " ", "a", "A1-hello", "café", "has space", "-leading", "trailing-"])
def test_slug_rejects_invalid(bad):
    with pytest.raises(SlugInvalid):
        Slug(bad)


def test_slug_trims_whitespace():
    assert Slug("  coastlines  ").value == "coastlines"


@pytest.mark.parametrize("level", ["A1", "A2", "B1", "B2", "C1"])
def test_cefr_accepts(level):
    assert CefrLevel(level).value == level


@pytest.mark.parametrize("bad", ["", "C2", "a1", "B3"])
def test_cefr_rejects(bad):
    with pytest.raises(ValueError):
        CefrLevel(bad)


@pytest.mark.parametrize("kind", ["reading", "listening", "speaking", "writing"])
def test_piece_kind(kind):
    assert PieceKind(kind).value == kind


@pytest.mark.parametrize(
    "topic",
    ["travel", "business", "daily-life", "academic", "culture", "science"],
)
def test_topic_accepts(topic):
    assert Topic(topic).value == topic


def test_topic_rejects_unknown():
    with pytest.raises(ValueError):
        Topic("politics")


def test_piece_status_values():
    assert {s.value for s in PieceStatus} == {"draft", "published", "archived"}


def test_piece_source_values():
    assert {s.value for s in PieceSource} == {"editorial", "llm_generated"}


def test_mcq_valid():
    q = MCQ(
        question="What is X?",
        choices=["a", "b", "c"],
        correct_index=1,
        rationale="because b",
    )
    assert q.correct_index == 1


def test_mcq_rejects_index_out_of_range():
    with pytest.raises(MCQInvalid):
        MCQ(question="Q", choices=["a", "b"], correct_index=2, rationale="r")


@pytest.mark.parametrize("choices", [["a"], ["a", "b", "c", "d", "e", "f"]])
def test_mcq_rejects_bad_choice_count(choices):
    with pytest.raises(MCQInvalid):
        MCQ(question="Q", choices=choices, correct_index=0, rationale="r")


def test_mcq_rejects_empty_question():
    with pytest.raises(MCQInvalid):
        MCQ(question="", choices=["a", "b"], correct_index=0, rationale="r")


def test_short_answer_prompt_valid():
    sa = ShortAnswerPrompt(prompt="Summarize", grading_notes="Look for X")
    assert sa.prompt == "Summarize"


def test_short_answer_prompt_rejects_empty():
    with pytest.raises(ValueError):
        ShortAnswerPrompt(prompt="", grading_notes="n")


def test_default_cefr_rubric_has_four_criteria():
    assert len(DEFAULT_CEFR_RUBRIC.criteria) == 4
    names = [c.name for c in DEFAULT_CEFR_RUBRIC.criteria]
    assert names == ["Task achievement", "Coherence", "Range", "Accuracy"]


def test_rubric_criterion_rejects_bad_score_range():
    with pytest.raises(RubricInvalid):
        RubricCriterion(name="X", description="d", min_score=0, max_score=5)


def test_rubric_rejects_empty_criteria():
    with pytest.raises(RubricInvalid):
        CefrRubric(criteria=())


def test_media_ref_minimal():
    m = MediaRef(storage_key="pieces/x/audio.mp3", mime_type="audio/mpeg", duration_seconds=None)
    assert m.storage_key == "pieces/x/audio.mp3"


def test_media_ref_rejects_empty_key():
    with pytest.raises(ValueError):
        MediaRef(storage_key="", mime_type="audio/mpeg", duration_seconds=None)


def test_media_ref_rejects_empty_mime():
    with pytest.raises(ValueError):
        MediaRef(storage_key="k", mime_type="", duration_seconds=None)


def test_media_ref_rejects_negative_duration():
    with pytest.raises(ValueError):
        MediaRef(storage_key="k", mime_type="audio/mpeg", duration_seconds=-1)
