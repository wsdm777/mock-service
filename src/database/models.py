from decimal import Decimal
import datetime

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Numeric,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship

from src.schemas import CurrencyCreate, CurrencyRateCreate


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class Currency(Base):
    __tablename__ = "currencies"

    char_code: Mapped[str] = mapped_column(nullable=False)
    num_code: Mapped[str] = mapped_column(nullable=False, unique=True)
    nominal: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    valute_id_prefix: Mapped[str] = mapped_column(nullable=False, unique=True)
    min_rate: Mapped[int] = mapped_column(nullable=False)
    max_rate: Mapped[int] = mapped_column(nullable=False)

    __table_args__ = (CheckConstraint("nominal > 0", name="chk_nominal_positive"),)

    @classmethod
    def create_obj(cls, obj: CurrencyCreate):
        return cls(**obj.model_dump())


class CurrencyRate(Base):
    __tablename__ = "currency_rates"

    date: Mapped[datetime.date] = mapped_column(nullable=False, index=True)
    currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id", ondelete="CASCADE"),
        nullable=False,
    )
    value: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False)

    __table_args__ = (
        UniqueConstraint("date", "currency_id", name="uq_date_currency_id"),
    )

    currency: Mapped["Currency"] = relationship()

    @classmethod
    def create_obj(cls, obj: CurrencyRateCreate):
        return cls(**obj.model_dump())
