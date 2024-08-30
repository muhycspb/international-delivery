from src.routers.all_types import router as router_all_types
from src.routers.calculate_the_delivery import router as router_calculate_the_delivery
from src.routers.info_by_id import router as router_info_by_id
from src.routers.list_of_my_parcels import router as router_list_of_my_parcels
from src.routers.register_a_parcel import router as router_register_a_parcel

all_routers = [router_all_types,
               router_calculate_the_delivery,
               router_info_by_id,
               router_list_of_my_parcels,
               router_register_a_parcel]
