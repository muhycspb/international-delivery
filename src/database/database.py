from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from config import settings as s

engine = create_async_engine(f"postgresql+asyncpg://{s.postgres_username}:{s.postgres_password}@"
                             f"{s.postgres_host}:{s.postgres_port}/{s.postgres_database}", echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


def connect_to_redis():
    redis = aioredis.from_url(f"redis://{s.redis_container_name}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


class Base(DeclarativeBase):
    pass


async def get_async_session():
    async with async_session_maker() as session:
        yield session
