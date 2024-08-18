from fastapi import APIRouter, Depends, Response, Cookie
from sqlalchemy import select

from src.database.database import get_async_session
from src.services.services import check_cookie
from src.database.models import Parcel
from src.schemas.schemas import SParcelId

router = APIRouter(
    prefix="/info_by_id",
    tags=["info_by_id"],
    responses={404: {"description": "Not found"}},
)


async def get_info_by_id(parcel_id: SParcelId, session_id, session):
    """Получение информации о посылке по идентификатору посылки"""
    query = (select(Parcel.parcel_name,
                    Parcel.parcel_weight,
                    Parcel.parcel_type,
                    Parcel.parcel_cost,
                    Parcel.parcel_cost_delivery,
                    )
             .where(Parcel.parcel_id == parcel_id.parcel_id and Parcel.parcel_session_id == session_id))

    try:
        result = await session.execute(query)
        result = list(result.one())
        if result[4] is None:
            result[4] = "Не рассчитано"
        result = dict(zip(("название", "вес", "тип посылки", "стоимость", "стоимость доставки"), result))
    except Exception as e:
        print(e)
        result = "Посылка не найдена"
    return result


@router.post("/")
async def info_by_id(parcel_id: SParcelId, response: Response, session_id=Cookie(None),
                     session=Depends(get_async_session)):
    session_id = await check_cookie(response=response, session_id=session_id, session=session)
    info = await get_info_by_id(parcel_id=parcel_id, session_id=session_id, session=session)
    return info
