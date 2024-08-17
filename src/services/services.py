import uuid
import requests
import json
from datetime import datetime
from fastapi import Response
from fastapi_cache.decorator import cache
from hashlib import sha256
from sqlalchemy import select, inspect

from src.database.database import Base, engine, async_session_maker
from src.database.models import Parcel, Session, ParcelType
from src.schemas.schemas import SParcel, SParcelId


@cache(expire=60)
async def get_current_course_usd() -> float:
    """Получение текущего курса доллара в рублях"""
    response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    data = json.loads(response.text)
    return data["Valute"]["USD"]["Value"]


async def get_info_by_id(parcel_id: SParcelId, session):
    """Получение информации о посылке по идентификатору посылки"""
    query = (
        select(Parcel.parcel_name,
               Parcel.parcel_weight,
               Parcel.parcel_type,
               Parcel.parcel_cost,
               Parcel.parcel_cost_delivery, )
        .where(Parcel.parcel_id == parcel_id.parcel_id)
    )

    try:
        result = await session.execute(query)
        result = dict(zip(("название", "вес", "тип посылки", "стоимость", "стоимость доставки"), result.one()))
    except Exception:
        result = "Посылка не найдена"
    return result


async def calculate_the_delivery():
    """Вычисление стоимости доставки посылки"""
    current_course_usd = await get_current_course_usd()
    return current_course_usd


async def create_table() -> None:
    """Создание таблиц в БД"""
    async with engine.begin() as conn:
        tables = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )
        if not tables:
            await conn.run_sync(Base.metadata.create_all)


async def insert_types():
    """Добавление типов посылок в БД"""
    async with async_session_maker() as session:
        for type_name in ("одежда", "электроника", "разное"):
            type_name = ParcelType(type_name=type_name)
            session.add(type_name)
        await session.commit()


async def insert_session_id(session_id: str, session) -> None:
    """Добавление сессии в БД"""
    session_id = Session(session_id=session_id)
    session.add(session_id)
    await session.commit()


async def insert_parcel(data: SParcel, session_id, session) -> str:
    """Добавление посылки в БД"""
    parcel_id = await generate_parcel_id()
    parcel = Parcel(
        parcel_name=data.parcel_name,
        parcel_weight=data.parcel_weight,
        parcel_type=data.parcel_type,
        parcel_cost=data.parcel_cost,
        parcel_id=parcel_id,
        parcel_session_id=session_id,
    )
    session.add(parcel)
    await session.commit()
    return parcel_id


async def generate_parcel_id():
    """Генерация идентификатора посылки"""
    parcel_id = sha256(
        f"{datetime.now()}".encode()).hexdigest()
    return parcel_id[0:8]


async def generate_session_id() -> str:
    """Генерация идентификатора сессии"""
    return uuid.uuid4().hex


async def set_cookie(response: Response):
    """Установка cookie с идентификатором сессии"""
    session_id = await generate_session_id()
    response.set_cookie(key="session_id", value=session_id)
    return session_id


async def check_cookie(response: Response, session_id: str, session) -> str:
    """Проверка наличия cookie с идентификатором сессии, если нет - создание нового и запись в БД"""
    if not session_id:
        session_id = await set_cookie(response)
        await insert_session_id(session_id, session)
    return session_id
