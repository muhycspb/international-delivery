from fastapi import APIRouter, Cookie, Depends, Response
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.database.database import get_async_session
from src.database.models import Parcel
from src.services.services import check_cookie

router = APIRouter(
    prefix="/list_of_my_parcels",
    tags=["list_of_my_parcels"],
    responses={404: {"description": "Not found"}},
)


async def get_list_of_my_parcels(session_id, session, page, parcel_type, cost_delivery, page_size: int = 10):
    """Получение информации о посылках по сессии"""
    query = (select(Parcel.parcel_name,
                    Parcel.parcel_weight,
                    Parcel.parcel_type,
                    Parcel.parcel_cost,
                    Parcel.parcel_cost_delivery,
                    )
             .where(Parcel.parcel_session_id == session_id,
                    Parcel.parcel_type == parcel_type,
                    Parcel.parcel_cost_delivery is None if not cost_delivery else not None)
             .offset((page - 1) * page_size).limit(page_size))

    my_parcels = []

    try:
        result = await session.execute(query)
        result = list(result.all())
        for parcel in result:
            parcel = list(parcel)
            if parcel[4] is None:
                parcel[4] = "Не рассчитано"
            my_parcels.append(dict(zip(("название", "вес", "тип посылки", "стоимость", "стоимость доставки"), parcel)))
    except NoResultFound:
        return "Посылок нет"
    return my_parcels


@router.get("/")
async def list_of_my_parcels(response: Response,
                             session_id=Cookie(None),
                             session=Depends(get_async_session),
                             page: int = 1,
                             parcel_type: str = "одежда",
                             cost_delivery: bool = True):
    session_id = await check_cookie(response=response,
                                    session_id=session_id,
                                    session=session)
    result = await get_list_of_my_parcels(session_id=session_id,
                                          session=session,
                                          page=page,
                                          parcel_type=parcel_type,
                                          cost_delivery=cost_delivery)
    return result
