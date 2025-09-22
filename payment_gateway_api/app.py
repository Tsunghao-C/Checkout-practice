from typing import Dict
from fastapi import FastAPI, HTTPException
from uuid import uuid4, UUID

import requests
import logging

from payment_gateway_api.domain.acquiring_bank import AcquiringBankStatus
from payment_gateway_api.domain.currency_lib import CurrencyCode
from payment_gateway_api.dto.payment import ProcessPaymentBody, PaymentResponse, PaymentRequest, CheckPaymentBody


ACQUIRING_BANK_URL = "http://localhost:8080"
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
    # 3. create payload object needed to make api call to acquiring bank
    month_str = f"0{payload.exp_month}" if payload.exp_month < 10 else str(payload.exp_month)
    expiry_date = f"{month_str}/{payload.exp_year}"
    request_payload = PaymentRequest(
        card_number=payload.card_number,
        expiry_date=expiry_date,
        currency=payload.currency,
        amount=payload.amount,
        cvv=payload.cvv,
    )
    # 4. make api call to acquiring bank
    response = requests.post(url=f"{ACQUIRING_BANK_URL}/payments", data=request_payload.json())
    if response.status_code != 200:
        logging.error("Fail to request to acquiring bank %i, %s", response.status_code, response.json())
    status = AcquiringBankStatus.AUTHORIZED if response.json().get("authorized") else AcquiringBankStatus.DECLINED
    last_4_card_num = payload.card_number[-4:]
    # 5. save the result to db
    # 5. return response
    return PaymentResponse(
        payment_id=payment_id,
        status=status,
        last_4_card_number=last_4_card_num,
        exp_month=payload.exp_month,
        exp_year=payload.exp_year,
        currency=payload.currency,
        amount=payload.amount
    )


mock_db = {
    UUID("2f480028-92b4-4e77-862c-ab156378b82d"): PaymentResponse(
        payment_id=UUID("2f480028-92b4-4e77-862c-ab156378b82d"),
        status="Authorized",
        last_4_card_number="9487",
        exp_month=6,
        exp_year=2028,
        currency="GBP",
        amount=1000,
    ),
    UUID("e0009aa8-d7c8-44bd-8ede-638dfc4d41bc"): PaymentResponse(
        payment_id=UUID("e0009aa8-d7c8-44bd-8ede-638dfc4d41bc"),
        status="Declined",
        last_4_card_number="3423",
        exp_month=9,
        exp_year=2028,
        currency="USD",
        amount=44,
    )
}


@app.get("/payment")
async def get_payment(
    payload: CheckPaymentBody
) -> PaymentResponse:
    """
    get previous payment details by payment_id
    """
    # 1. look up id and find the instance
    if payload.payment_id not in mock_db.keys():
        logging.error(f"payment_id {payload.payment_id} do not exist")
        raise HTTPException(status_code=404, detail=f"payment_id {payload.payment_id} not found")
    # 2. return in payment response model
    return mock_db[payload.payment_id]
