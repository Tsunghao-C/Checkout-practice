from pydantic import BaseModel, Field, validator, root_validator
from datetime import datetime

from payment_gateway_api.domain.currency_lib import CurrencyCode


class ProcessPaymentBody(BaseModel):
    card_number: str = Field(..., max_length=19, min_length=14)
    exp_month: int = Field(..., ge=1, le=12)
    exp_year: int = Field(..., ge=2000)  # Just ensure it's a reasonable year
    currency: CurrencyCode
    # ammount: int
    # cvv: str

    @validator("card_number")
    def card_number_must_be_numbers(cls, v):
        if v.isdigit():
            return v
        else:
            raise ValueError("card_number must between 14 - 19 chars long and only digits allowed")
    
    @root_validator
    def month_year_must_be_in_future(cls, values):
        exp_month = values.get('exp_month')
        exp_year = values.get('exp_year')
        
        if exp_month is not None and exp_year is not None:
            now = datetime.now()
            current_year = now.year
            current_month = now.month
            
            # Check if the expiration date is in the past
            if exp_year < current_year or (exp_year == current_year and exp_month < current_month):
                raise ValueError(f"expiration month-year {exp_month}-{exp_year} is not in the future")
        
        return values
    
    @validator("currency", pre=True)
    def capitalize_currency(cls, v):
        return v.upper()


# Test with valid future date
try:
    valid_model = ProcessPaymentBody(
        card_number="123456789012345",
        exp_month=12,
        exp_year=2025,
        currency="Gbp"
    )
    print("Valid model: ", valid_model)
    card_last_4 = valid_model.card_number[-4:]
    print("last four: ", card_last_4)
except ValueError as e:
    print("Validation error:", e)

# Test with invalid currency
try:
    valid_model = ProcessPaymentBody(
        card_number="123456789012345",
        exp_month=12,
        exp_year=2025,
        currency="GBY"
    )
    print("Valid model: ", valid_model)
except ValueError as e:
    print("Validation error:", e)

# # Test with past date
# try:
#     invalid_model = ProcessPaymentBody(
#         card_number="123456789012345",
#         exp_month=1,
#         exp_year=2020,
#     )
#     print("Invalid model: ", invalid_model)
# except ValueError as e:
#     print("Validation error:", e)

# # Test with current month (should fail if we're past the current month)
# try:
#     current_date = datetime.now()
#     current_model = ProcessPaymentBody(
#         card_number="123456789012345",
#         exp_month=current_date.month,
#         exp_year=current_date.year,
#     )
#     print("Current month model: ", current_model)
# except ValueError as e:
#     print("Validation error:", e)

# # Test with future month in current year
# try:
#     current_date = datetime.now()
#     future_month = current_date.month + 1 if current_date.month < 12 else 1
#     future_year = current_date.year if current_date.month < 12 else current_date.year + 1
#     future_model = ProcessPaymentBody(
#         card_number="123456789012345",
#         exp_month=future_month,
#         exp_year=future_year,
#     )
#     print("Future month model: ", future_model)
# except ValueError as e:
#     print("Validation error:", e)
