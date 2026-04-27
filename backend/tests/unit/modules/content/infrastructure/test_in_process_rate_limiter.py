import asyncio

import pytest

from app.modules.content.application.dto import RateWindow
from app.modules.content.infrastructure.rate_limiter.in_process import (
    InProcessRateLimiter,
)


@pytest.mark.asyncio
async def test_allows_up_to_limit():
    limiter = InProcessRateLimiter()
    w = RateWindow(seconds=60, max_hits=3)
    for _ in range(3):
        v = await limiter.check_and_increment("k", w)
        assert v.allowed
    v = await limiter.check_and_increment("k", w)
    assert not v.allowed
    assert v.retry_after_seconds > 0


@pytest.mark.asyncio
async def test_window_eviction_reallows_after_expiry():
    limiter = InProcessRateLimiter()
    w = RateWindow(seconds=1, max_hits=1)
    v1 = await limiter.check_and_increment("k2", w)
    assert v1.allowed
    v2 = await limiter.check_and_increment("k2", w)
    assert not v2.allowed
    await asyncio.sleep(1.1)
    v3 = await limiter.check_and_increment("k2", w)
    assert v3.allowed


@pytest.mark.asyncio
async def test_separate_keys_independent():
    limiter = InProcessRateLimiter()
    w = RateWindow(seconds=60, max_hits=1)
    assert (await limiter.check_and_increment("a", w)).allowed
    assert (await limiter.check_and_increment("b", w)).allowed
    assert not (await limiter.check_and_increment("a", w)).allowed
