import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.database.initial_currency_data import CURRENCIES_FOR_SEEDING
from src.database.models import Currency
from src.schemas import CurrencyCreate

logger = logging.getLogger(__name__)


async def seed_initial_currencies(session: AsyncSession):
    """
    Проверяет, есть ли валюты в таблице Currency.
    Если таблица пуста, заполняет ее данными из initial_currency_data,

    Args:
        session (AsyncSession)
    """
    logger.info("Checking currency availability in the database")
    existing_currencies = await session.execute(select(Currency))

    if existing_currencies.first():
        logger.info("Currencies already exist in the database")
        return

    logger.info(
        "The currency table is empty. Starting to insert the initial currencies"
    )

    currencies_to_add = []

    for currency_data in CURRENCIES_FOR_SEEDING:
        try:
            currency_pydantic = CurrencyCreate(**currency_data)

            currency_orm = Currency.create_obj(currency_pydantic)

            currencies_to_add.append(currency_orm)

        except Exception as e:
            logger.exception(f"Exception while creating pydantic model {e}")
            raise e

    if currencies_to_add:
        try:
            session.add_all(currencies_to_add)
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            logger.exception(f"Integrity error, possibly duplicates {e}")
            raise e
        except Exception as e:
            await session.rollback()
            logger.exception(
                f"Unexpected error when saving currencies to the database {e}"
            )
            raise e
    logger.info("Inserting finished")
