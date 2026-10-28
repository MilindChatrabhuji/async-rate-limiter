# Async Rate Limiter ⏱️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![FastAPI Ready](https://img.shields.io/badge/FastAPI-Compatible-009688.svg)](https://fastapi.tiangolo.com/)

A high-performance, asynchronous rate limiting library for Python, FastAPI, and ASGI applications. Implements **Token Bucket** and **Sliding Window Log** algorithms with thread-safe and coroutine-safe in-memory stores.

---

## 🚀 Quickstart

### 1. Token Bucket Limiter

```python
import asyncio
from async_rate_limiter import TokenBucketLimiter

# 10 burst capacity, refills 2 tokens per second
limiter = TokenBucketLimiter(capacity=10, refill_rate=2.0)

async def handle_user_request(user_id: str):
    if await limiter.acquire(user_id):
        return {"status": "success"}
    return {"status": "rate_limited"}, 429
```

### 2. Endpoint Decorator

```python
from async_rate_limiter import rate_limit, RateLimitExceeded

# Max 5 calls per 10 seconds per IP
@rate_limit(max_requests=5, window_seconds=10.0)
async def sensitive_external_api():
    return {"data": "verified"}
```

---

## 🧪 Testing

```bash
python -m pytest tests
```

---

## 📄 License
MIT License. Created by [Milind Chatrabhuji](https://github.com/MilindChatrabhuji).
