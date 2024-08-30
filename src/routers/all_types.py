from fastapi import APIRouter, Depends
from sqlalchemy import select

from src.database.database import get_async_session
from src.database.models import ParcelType

router = APIRouter(
    prefix="/all_types",
    tags=["all_types"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def all_types(session=Depends(get_async_session)):
    query = select(ParcelType.id, ParcelType.type_name, )
    result = await session.execute(query)
    result = dict(result.all())
    return result
