from sqlalchemy.orm import Mapped, mapped_column
from src.database.database import Base


class Session(Base):
    __tablename__ = "session"
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[str]


class Parcel(Base):
    __tablename__ = "parcel"
    id: Mapped[int] = mapped_column(primary_key=True)
    parcel_name: Mapped[str]
    parcel_weight: Mapped[float]
    parcel_type: Mapped[str]
    parcel_cost: Mapped[float]
    parcel_cost_delivery: Mapped[float] = mapped_column(nullable=True)
    parcel_id: Mapped[str]
    parcel_session_id: Mapped[str]


class ParcelType(Base):
    __tablename__ = "parcel_type"
    id: Mapped[int] = mapped_column(primary_key=True)
    type_name: Mapped[str]
