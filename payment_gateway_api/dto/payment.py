from pydantic import BaseModel, Field, validator, root_validator
from datetime import datetime
from uuid import UUID, uuid4

from payment_gateway_api.domain.currency_lib import CurrencyCode
from payment_gateway_api.domain.acquiring_bank import AcquiringBankStatus


class ProcessPaymentBody(BaseModel):
    # Model 1 Process payment payload
    """
    card_number: str (14 - 19 chars, only numeric)
    exp_month: int (between 1 - 12)
    exp_year: int (month + year must be in the future)
    currency: str (must be 3 chars, all upper case)
    amount: str
    cvv: str (3 - 4 chars, only numeric)
    """
    card_number: str = Field(..., max_length=19, min_length=14)
    exp_month: int = Field(..., ge=1, le=12)
    exp_year: int = Field(..., ge=datetime.now().year)
    currency: CurrencyCode = Field()
    amount: int = Field(..., gt=0, description="Amount in minor currency unit (e.g., USD: $1.00 = 100, JPY: ¥1 = 1)")
    cvv: str = Field(..., min_length=3, max_length=4)

    @validator("card_number")
    def card_number_must_be_numbers(cls, v):
        if not v.isdigit():
            raise ValueError("card_number must between 14 - 19 chars long and only digits allowed")
        return v

    @root_validator()
    def month_year_must_be_in_future(cls, values):
        month, year = values.get("exp_month"), values.get("exp_year")
        if year < datetime.now().year or (year == datetime.now().year and month < datetime.now().month):
            raise ValueError(f"expiration {month}-{year} is not in the future")
        return values

    @validator("currency", pre=True)
    def uppercase_currency(cls, v):
        return v.upper()

    @validator("cvv")
    def cvv_must_be_numbers(cls, v):
        if not v.isdigit():
            raise ValueError("cvv must be 3 - 4 chars long and only digits allowed")
        return v
    

class PaymentRequest(BaseModel):
    """
    """
    card_number: str = Field(..., max_length=19, min_length=14)
    expiry_date: str = Field()
    currency: CurrencyCode = Field()
    amount: int = Field()
    cvv: str = Field(..., min_length=3, max_length=4)

class PaymentResponse(BaseModel):
    """
    payment_id: uuid
    status: Authorized, Declined
    last_4_card_number: str
    exp_month: int
    exp_year: int
    currency: str
    amount: int
    """
    payment_id: UUID = Field()
    status: AcquiringBankStatus = Field()
    last_4_card_number: str
    exp_month: int
    exp_year: int
    currency: CurrencyCode
    amount: int


class CheckPaymentBody(BaseModel):
    payment_id: UUID = Field()