from config import settings as s
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(f"postgresql+asyncpg://{s.postgres_username}:{s.postgres_password}@"
                             f"{s.postgres_container_name}/{s.postgres_database}", echo=False)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


def connect_to_redis():
    """Подключаемся к Redis"""
    redis = aioredis.from_url(f"redis://{s.redis_container_name}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


class Base(DeclarativeBase):
    pass


async def get_async_session():
    async with async_session_maker() as session:
        yield session


async def create_table() -> None:
    """Создание таблиц в БД"""
    async with engine.connect() as conn:
        tables = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )
        if not tables:
            await conn.run_sync(Base.metadata.create_all)
            await conn.commit()
