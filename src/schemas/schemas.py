from pydantic import BaseModel


class Base(BaseModel):
    pass


class SParcel(Base):
    parcel_name: str
    parcel_weight: float
    parcel_type: str
    parcel_cost: float


class SParcelId(Base):
    parcel_id: str
