from typing import Dict
from fastapi import FastAPI, Body
from uuid import UUID, uuid4

from payment_gateway_api.domain.acquiring_back import AcquiringBankStatus
from payment_gateway_api.domain.currency_lib import CurrencyCode
from payment_gateway_api.dto.payment import ProcessPaymentBody, PaymentResponse


app = FastAPI(title="Payment Gateway API")


@app.get("/")
async def ping() -> Dict[str, str]:
    return {"app": "payment-gateway-api"}


@app.post("/payment")
async def process_payment(
    payload: ProcessPaymentBody
) -> PaymentResponse:
    """
    process a payment request by making a POST request to acquiring bank.
    """
    # 1. the payload should use pydantic model to make sure input data model is correct
    # 2. create an paymend_id
    payment_id = uuid4()
    last_4_card_num = payload.card_number[-4:]
    # 3. create payload object needed to make api call to acquiring bank
    # 4. make api call to acquiring bank and save result to db
    # 5. return response
    return PaymentResponse(
        payment_id=payment_id,
        status=AcquiringBankStatus.AUTHORIZED,
        last_4_card_number=last_4_card_num,
        exp_month=payload.exp_month,
        exp_year=payload.exp_year,
        currency=payload.currency,
        amount=payload.amount
    )


@app.get("/payment")
async def get_payment(
    payment_id: UUID = Body(..., embed=True, include_in_schema=True)
) -> PaymentResponse:
    """
    get previous payment details by payment_id
    """
    # 1. look up id and find the instance
    # 2. return in payment response model
    return PaymentResponse(
        payment_id=payment_id,
        status=AcquiringBankStatus.AUTHORIZED,
        last_4_card_number="9567",
        exp_month=12,
        exp_year=2027,
        currency=CurrencyCode.EUR,
        amount=6666,
    )