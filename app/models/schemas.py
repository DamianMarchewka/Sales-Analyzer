from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import date

class SalesInput(BaseModel):
    date: date
    product: str = Field(min_length=1)
    quantity: int = Field(gt=0)
    price: float = Field(ge=0)

    @field_validator("product")
    def strip_product(cls, v):
        return v.strip()
    
    @model_validator(mode="after")
    def check_if_date_not_future(self):
        today = date.today()
        if self.date > today:
            raise ValueError("error date form the future!")
        return self

