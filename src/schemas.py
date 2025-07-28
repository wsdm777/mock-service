from decimal import Decimal
import logging
from pydantic import BaseModel, Field, PrivateAttr, field_validator, model_validator
from datetime import datetime, date

logger = logging.getLogger(__name__)


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
    _parsed_date: date = PrivateAttr()

    @field_validator("date_req")
    @classmethod
    def parse_date(cls, search_data: str | None) -> str | None:
        if search_data is None:
            cls._parsed_date = datetime.now().date()
            return search_data
        else:
            try:
                cls._parsed_date = datetime.strptime(search_data, "%d/%m/%Y").date()
                return search_data
            except ValueError:
                logger.warning(f"Wrong search data {search_data}")
                raise ValueError("wrong date format for date_req. Use DD/MM/YYYY.")


class CurrencyRateCreate(BaseModel):
    date: date
    currency_id: int
    value: Decimal
