import time
import asyncio
from typing import Dict, List

class SlidingWindowLimiter:
    """Sliding Window log rate limiter enforcing requests per window."""

    def __init__(self, max_requests: int, window_seconds: float):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.logs: Dict[str, List[float]] = {}
        self._lock = asyncio.Lock()

    async def acquire(self, key: str = "default") -> bool:
        async with self._lock:
            now = time.time()
            cutoff = now - self.window_seconds

            timestamps = self.logs.get(key, [])
            valid_timestamps = [t for t in timestamps if t > cutoff]

            if len(valid_timestamps) < self.max_requests:
                valid_timestamps.append(now)
                self.logs[key] = valid_timestamps
                return True
            else:
                self.logs[key] = valid_timestamps
                return False
