from datetime import date
import logging
from typing import Sequence

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.database.models import Currency, CurrencyRate

logger = logging.getLogger(__name__)


class Repository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_date_rate(self, search_date: date) -> Sequence[CurrencyRate]:
        query = (
            select(CurrencyRate)
            .options(joinedload(CurrencyRate.currency))
            .filter(CurrencyRate.date == search_date)
        )
        return (await self.session.execute(query)).scalars().all()

    async def get_all_currencies(self) -> Sequence[Currency]:
        return (await self.session.execute(select(Currency))).scalars().all()

    async def add_new_date(self, rates: list[CurrencyRate]):
        try:
            self.session.add_all(rates)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
        except Exception as e:
            logger.exception(f"Unexpected error when saving new rates {e}")
            raise e
