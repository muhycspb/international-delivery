from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from config import settings as s


async def connect_to_redis() -> None:
    """Подключаемся к Redis"""
    redis = aioredis.from_url(f"redis://{s.redis_container_name}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


print(s.redis_container_name)
