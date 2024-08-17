from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import settings as s

engine = create_async_engine(f"postgresql+asyncpg://{s.postgres_username}:{s.postgres_password}@"
                             f"{s.postgres_host}:{s.postgres_port}/{s.postgres_database}", echo=False)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_async_session():
    async with async_session_maker() as session:
        yield session
