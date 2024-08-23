from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.database.database import connect_to_redis, create_table
from src.routers.routers import all_routers


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Выполняется при запуске и закрытии приложения"""
    print("Приложение запущено")
    connect_to_redis()
    await create_table()
    yield
    print("Закрытие приложения")


app = FastAPI(lifespan=lifespan)

for router in all_routers:
    app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
