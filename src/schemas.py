from decimal import Decimal
import logging
from fastapi import HTTPException, status
from pydantic import (
    BaseModel,
    Field,
    computed_field,
    model_validator,
)
from datetime import datetime, date

from pydantic_xml import BaseXmlModel, attr, element

logger = logging.getLogger(__name__)

API_START_DATE = date(1993, 1, 1)


class CurrencyCreate(BaseModel):
    char_code: str
    num_code: str
    nominal: int = Field(gt=0)
    name: str
    valute_id_prefix: str
    min_rate: int = Field(gt=0)
    max_rate: int = Field(gt=0)

    @model_validator(mode="after")
    def check_min_max_rates(self) -> "CurrencyCreate":
        if self.min_rate >= self.max_rate:
            raise ValueError("max_rate must be greater than min_rate")
        return self


class SearchParams(BaseModel):
    date_req: str | None = Field(None, description="Дата запроса в формате DD/MM/YYYY")
    simulate_error: bool = Field(
        False, description="Если True, возвращает HTTP 500 ошибку"
    )

    @computed_field
    @property
    def parsed_date(self) -> date:
        if self.date_req is None:
            return date.today()
        else:
            try:
                parsed_date = datetime.strptime(self.date_req, "%d/%m/%Y").date()
                if not (API_START_DATE <= parsed_date <= date.today()):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Запрошенная дата ({self.date_req}) выходит за пределы доступного диапазона API.",
                    )
                return parsed_date
            except ValueError:
                logger.warning(f"Wrong search data {self.date_req}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Неверный формат даты для date_req. Используйте DD/MM/YYYY.",
                )


class CurrencyRateCreate(BaseModel):
    date: date
    currency_id: int
    value: Decimal


class CurrencyXml(BaseXmlModel, tag="Valute"):
    valute_id: str = attr(name="ID")
    num_code: str = element(tag="NumCode")
    char_code: str = element(tag="CharCode")
    nominal: int = element(tag="Nominal")
    name: str = element(tag="Name")
    value: str = element(tag="Value")
    vunit_rate: str = element(tag="VunitRate")


class ValCursXml(BaseXmlModel, tag="ValCurs"):
    date_str: str = attr(name="Date")
    name: str = attr(name="name")
    valutes: list[CurrencyXml] = element(tag="Valute")
