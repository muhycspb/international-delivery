from fastapi import APIRouter, Depends
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound

from src.database.database import get_async_session
from src.database.models import Parcel
from src.services.services import get_current_course_usd

router = APIRouter(
    prefix="/calculate_the_delivery",
    tags=["calculate_the_delivery"],
    responses={404: {"description": "Not found"}},
)


async def calculate(weight: float, cost: float) -> float:
    """Вычисление стоимости доставки посылки
    (вес в кг * 0.5 + стоимость содержимого в долларах * 0.01) * курс доллара к рублю"""
    current_course_usd = await get_current_course_usd()
    if current_course_usd:
        result = round((weight * 0.5 + cost * 0.01) * current_course_usd, 2)
    else:
        result = None
    return result


async def update_cost(list_of_nullable, session):
    for el_id in list_of_nullable:
        cost = calculate(weight=el_id[1], cost=el_id[2])
        query = update(Parcel).where(Parcel.id == el_id[0]).values(parcel_cost_delivery=cost)
        await session.execute(query)
        await session.commit()


async def get_all_nullable(session) -> list:
    query = (select(Parcel.id, Parcel.parcel_weight, Parcel.parcel_cost)
             .where(Parcel.parcel_cost_delivery.is_(None)))
    try:
        result = await session.execute(query)
        result = result.all()
    except NoResultFound:
        result = []
    return result


@router.get("/")
async def calculate_the_delivery(session=Depends(get_async_session)):
    list_of_nullable = await get_all_nullable(session)
    await update_cost(list_of_nullable=list_of_nullable, session=session)
    return "стоимость доставки рассчитана для всех посылок"
