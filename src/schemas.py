from pydantic import BaseModel, Field, model_validator


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
