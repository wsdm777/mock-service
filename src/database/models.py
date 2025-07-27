from decimal import Decimal
from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Numeric,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
import datetime


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class Currency(Base):
    __tablename__ = "currencies"

    char_code: Mapped[str] = mapped_column(nullable=False)
    num_code: Mapped[int] = mapped_column(nullable=False, unique=True)
    nominal: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    valute_id_prefix: Mapped[str] = mapped_column(nullable=False, unique=True)
    min_date: Mapped[datetime.date] = mapped_column(nullable=False)
    max_date: Mapped[datetime.date] = mapped_column()

    __table_args__ = (CheckConstraint("nominal > 0", name="chk_nominal_positive"),)


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
