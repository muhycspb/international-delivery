import json
import requests
import uuid

from datetime import datetime
from fastapi import Response
from fastapi_cache.decorator import cache
from hashlib import sha256

from src.database.models import Session


@cache(expire=60)
async def get_current_course_usd() -> float:
    """Получение текущего курса доллара в рублях"""
    response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    data = json.loads(response.text)
    return data["Valute"]["USD"]["Value"]


async def insert_session_id(session_id: str, session) -> None:
    """Добавление сессии в БД"""
    session_id = Session(session_id=session_id)
    session.add(session_id)
    await session.commit()


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


async def check_cookie(response: Response, session_id, session):
    """Проверка наличия cookie с идентификатором сессии, если нет - создание нового и запись в БД"""
    if not session_id:
        session_id = await set_cookie(response=response)
        await insert_session_id(session_id=session_id, session=session)
    return session_id
