import pytest

from app.modules.content.domain.exceptions import (
    GenerationFailed,
    RateLimitExceeded,
)


def test_generation_failed_with_defaults():
    e = GenerationFailed("llm timeout")
    assert e.reason == "llm timeout"
    assert e.details == []
    assert str(e) == "llm timeout"


def test_generation_failed_with_details():
    e = GenerationFailed("bad draft", ["missing question", "too short"])
    assert e.reason == "bad draft"
    assert e.details == ["missing question", "too short"]


def test_generation_failed_none_details_becomes_empty_list():
    e = GenerationFailed("x", None)
    assert e.details == []


def test_rate_limit_exceeded_stores_retry_after():
    e = RateLimitExceeded(60)
    assert e.retry_after_seconds == 60
    assert "60s" in str(e)


def test_rate_limit_exceeded_accepts_zero():
    e = RateLimitExceeded(0)
    assert e.retry_after_seconds == 0


@pytest.mark.parametrize("bad", [-1, "30", 1.5, None])
def test_rate_limit_exceeded_rejects_non_int(bad):
    with pytest.raises(ValueError):
        RateLimitExceeded(bad)  # type: ignore[arg-type]
