from datetime import date
from decimal import Decimal
import random
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import CurrencyRate
from src.schemas import CurrencyRateCreate
from src.repository import Repository
from src.database.database import get_async_session


class Service:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.repository = Repository(session)

    async def create_random_rate(self, new_date: date):
        currencies = await self.repository.get_all_currencies()

        new_currency_list: list[CurrencyRate] = []

        for currency in currencies:
            rate = random.uniform(currency.min_rate, currency.max_rate)
            value = Decimal(f"{rate:.4f}")

            new_currency_list.append(
                CurrencyRate.create_obj(
                    CurrencyRateCreate(
                        date=new_date, currency_id=currency.id, value=value
                    )
                )
            )

        await self.repository.add_new_date(new_currency_list)

    async def get_date_rate(self, search_date: date):
        currencies = await self.repository.get_date_rate(search_date)
        if not currencies:
            await self.create_random_rate(search_date)
            currencies = await self.repository.get_date_rate(search_date)
        return currencies
