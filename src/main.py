from fastapi import FastAPI

from src.database.database import connect_to_redis, create_table, insert_types
from src.routers.routers import all_routers

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Выполняется при запуске и закрытии приложения"""
    print("Приложение запущено")
    await connect_to_redis()
    # await create_table()
    # await insert_types()
    yield
    print("Закрытие приложения")


app = FastAPI(lifespan=lifespan)

for router in all_routers:
    app.include_router(router)
