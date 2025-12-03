# app/auth/redis.py
"""Async Redis helpers used for token blacklisting.

The legacy ``aioredis`` package does not support Python 3.12+, so we
prefer the maintained ``redis`` asyncio client. Import failures surface a
clear error message to aid local test environments where Redis support
is optional.
"""

from __future__ import annotations

from typing import Optional

from app.core.config import get_settings

try:
    from redis import asyncio as redis_async
except Exception as exc:  # pragma: no cover - import guard
    redis_async = None
    _import_error: Optional[Exception] = exc
else:  # pragma: no cover - simple attribute assignment
    _import_error = None

settings = get_settings()


class RedisNotConfigured(RuntimeError):
    """Raised when Redis support is unavailable at runtime."""


async def get_redis():
    """Return a cached Redis client or raise if Redis is unavailable."""
    if redis_async is None:
        raise RedisNotConfigured(
            "Redis asyncio client is unavailable. Install the 'redis' package or "
            "configure REDIS_URL appropriately."
        ) from _import_error

    if not hasattr(get_redis, "_client"):
        # ``from_url`` returns an async-aware client; caching avoids reconnects.
        get_redis._client = redis_async.from_url(
            settings.REDIS_URL or "redis://localhost"
        )
    return get_redis._client


async def add_to_blacklist(jti: str, exp: int):
    """Add a token's JTI to the blacklist."""
    redis = await get_redis()
    await redis.set(f"blacklist:{jti}", "1", ex=exp)


async def is_blacklisted(jti: str) -> bool:
    """Return True if a token's JTI is blacklisted."""
    redis = await get_redis()
    return bool(await redis.exists(f"blacklist:{jti}"))