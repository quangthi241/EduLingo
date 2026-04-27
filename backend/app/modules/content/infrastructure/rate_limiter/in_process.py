from __future__ import annotations

import asyncio
import time
from collections import defaultdict, deque

from app.modules.content.application.dto import RateVerdict, RateWindow


class InProcessRateLimiter:
    def __init__(self) -> None:
        self._buckets: dict[str, deque[float]] = defaultdict(deque)
        self._lock = asyncio.Lock()

    async def check_and_increment(self, key: str, window: RateWindow) -> RateVerdict:
        async with self._lock:
            now = time.monotonic()
            horizon = now - window.seconds
            bucket = self._buckets[key]
            while bucket and bucket[0] <= horizon:
                bucket.popleft()
            if len(bucket) >= window.max_hits:
                retry = max(1, int(window.seconds - (now - bucket[0])))
                return RateVerdict(allowed=False, retry_after_seconds=retry)
            bucket.append(now)
            return RateVerdict(allowed=True, retry_after_seconds=0)
