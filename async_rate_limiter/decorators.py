import asyncio
from functools import wraps
from typing import Callable
from .sliding_window import SlidingWindowLimiter

class RateLimitExceeded(Exception):
    """Raised when rate limit quota is exceeded."""
    pass

def rate_limit(max_requests: int = 100, window_seconds: float = 60.0, key_func: Callable = None):
    """Decorator to rate-limit async endpoints or functions."""
    limiter = SlidingWindowLimiter(max_requests, window_seconds)

    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            key = key_func(*args, **kwargs) if key_func else "global"
            allowed = await limiter.acquire(key)
            if not allowed:
                raise RateLimitExceeded(f"Rate limit exceeded: {max_requests} requests per {window_seconds}s")
            return await func(*args, **kwargs)
        return async_wrapper
    return decorator
