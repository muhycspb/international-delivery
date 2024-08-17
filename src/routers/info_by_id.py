from fastapi import APIRouter, Depends
from src.database.database import get_async_session
from src.services.services import get_info_by_id
from src.schemas.schemas import SParcelId

router = APIRouter(
    prefix="/info_by_id",
    tags=["info_by_id"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def info_by_id(parcel_id: SParcelId, session=Depends(get_async_session)):
    info = await get_info_by_id(parcel_id, session)
    return info
