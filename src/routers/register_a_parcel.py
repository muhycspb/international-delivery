from fastapi import APIRouter, Cookie, Depends, Response

from src.database.database import get_async_session
from src.database.models import Parcel
from src.schemas.schemas import SParcel
from src.services.services import check_cookie, generate_parcel_id

router = APIRouter(
    prefix="/register_a_parcel",
    tags=["register_a_parcel"],
    responses={404: {"description": "Not found"}},
)


async def insert_parcel(data, parcel_id, session_id, session):
    """Добавление посылки в БД"""
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


@router.post("/")
async def register_a_parcel(data: SParcel,
                            response: Response,
                            session_id=Cookie(None),
                            session=Depends(get_async_session)):
    parcel_id = await generate_parcel_id()
    session_id = await check_cookie(response=response,
                                    session_id=session_id,
                                    session=session)
    await insert_parcel(data=data,
                        parcel_id=parcel_id,
                        session_id=session_id,
                        session=session)
    return parcel_id
