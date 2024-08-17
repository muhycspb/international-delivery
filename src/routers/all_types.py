from fastapi import APIRouter

router = APIRouter(
    prefix="/all_types",
    tags=["all_types"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_root():
    return 'all_types'
#
#
# @router.post("/")
# async def register_a_parcel(data: Parcel, session=Depends(get_async_session)):
#     return data
