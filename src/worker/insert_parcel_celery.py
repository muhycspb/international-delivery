from celery import Celery
from sqlalchemy import insert
from src.database.database import engine
from src.database.models import Parcel
from src.routers.calculate_the_delivery import calculate


rabbitmq_broker = Celery(broker="amqp://user:password@rabbitmq_container:5672/parcels")


@rabbitmq_broker.task
async def insert_parcel(data, parcel_id, session_id):
    """Добавление посылки в БД"""
    try:
        cost_delivery = await calculate(weight=data["parcel_weight"], cost=data["parcel_cost"])
    except Exception:
        cost_delivery = None

    async with engine.begin() as session:
        parcel = insert(Parcel).values(
            parcel_name=data["parcel_name"],
            parcel_weight=data["parcel_weight"],
            parcel_type=data["parcel_type"],
            parcel_cost=data["parcel_cost"],
            parcel_cost_delivery=cost_delivery,
            parcel_id=parcel_id,
            parcel_session_id=session_id,
        )
        await session.execute(parcel)
