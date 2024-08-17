from fastapi import APIRouter, Cookie, Depends, Response

from src.database.database import get_async_session
from src.schemas.schemas import SParcel
from src.services.services import check_cookie, insert_parcel

router = APIRouter(
    prefix="/register_a_parcel",
    tags=["register_a_parcel"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def register_a_parcel(data: SParcel, response: Response, session_id=Cookie(None),
                            session=Depends(get_async_session)):
    session_id = await check_cookie(response, session_id, session)
    parcel_id = await insert_parcel(data, session_id, session)
    return parcel_id
