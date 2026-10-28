import pytest
import asyncio
from async_rate_limiter import TokenBucketLimiter, SlidingWindowLimiter, rate_limit, RateLimitExceeded

def test_token_bucket():
    async def run():
        limiter = TokenBucketLimiter(capacity=3, refill_rate=1.0)
        assert await limiter.acquire("user_1", 1.0) is True
        assert await limiter.acquire("user_1", 1.0) is True
        assert await limiter.acquire("user_1", 1.0) is True
        # Exhausted
        assert await limiter.acquire("user_1", 1.0) is False

    asyncio.run(run())

def test_sliding_window():
    async def run():
        limiter = SlidingWindowLimiter(max_requests=2, window_seconds=1.0)
        assert await limiter.acquire("ip_1") is True
        assert await limiter.acquire("ip_1") is True
        assert await limiter.acquire("ip_1") is False

    asyncio.run(run())

def test_decorator_rate_limit():
    async def run():
        @rate_limit(max_requests=2, window_seconds=1.0)
        async def fetch_profile():
            return "ok"

        assert await fetch_profile() == "ok"
        assert await fetch_profile() == "ok"
        with pytest.raises(RateLimitExceeded):
            await fetch_profile()

    asyncio.run(run())
