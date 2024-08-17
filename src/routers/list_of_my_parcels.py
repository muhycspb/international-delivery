from fastapi import APIRouter

router = APIRouter(
    prefix="/list_of_my_parcels",
    tags=["list_of_my_parcels"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_root():
    return 'list_of_my_parcels'

#
# @router.post("/")
# async def register_a_parcel(data: Parcel, session=Depends(get_async_session)):
#     return data
