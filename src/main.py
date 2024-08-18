from fastapi import FastAPI

from src.database.database import connect_to_redis
from src.routers.routers import all_routers
from src.services.services import create_table, insert_types

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Выполняется при запуске и закрытии приложения"""
    print("Приложение запущено")
    connect_to_redis()
    # await create_table()
    # await add_types()
    yield
    print("Закрытие приложения")


app = FastAPI(lifespan=lifespan)

for router in all_routers:
    app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
