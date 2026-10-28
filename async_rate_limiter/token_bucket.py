import time
import asyncio
from typing import Dict

class TokenBucketLimiter:
    """Thread-safe and task-safe async Token Bucket rate limiter."""

    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.buckets: Dict[str, float] = {}
        self.last_refill: Dict[str, float] = {}
        self._lock = asyncio.Lock()

    async def acquire(self, key: str = "default", tokens: float = 1.0) -> bool:
        async with self._lock:
            now = time.time()
            current_tokens = self.buckets.get(key, self.capacity)
            last_time = self.last_refill.get(key, now)

            # Refill tokens
            elapsed = now - last_time
            current_tokens = min(self.capacity, current_tokens + (elapsed * self.refill_rate))
            self.last_refill[key] = now

            if current_tokens >= tokens:
                self.buckets[key] = current_tokens - tokens
                return True
            else:
                self.buckets[key] = current_tokens
                return False
