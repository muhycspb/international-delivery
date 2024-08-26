from fastapi import APIRouter, Cookie, Depends, Response

from src.database.database import get_async_session
from src.schemas.schemas import SParcel
from src.services.services import check_cookie, generate_parcel_id
from src.worker.insert_parcel_celery import insert_parcel

router = APIRouter(
    prefix="/register_a_parcel",
    tags=["register_a_parcel"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def register_a_parcel(data: SParcel,
                            response: Response,
                            session_id=Cookie(None),
                            session=Depends(get_async_session)):
    parcel_id = await generate_parcel_id()
    session_id = await check_cookie(response=response,
                                    session_id=session_id,
                                    session=session)
    await insert_parcel(data.__dict__,
                        parcel_id=parcel_id,
                        session_id=session_id)
    return parcel_id
