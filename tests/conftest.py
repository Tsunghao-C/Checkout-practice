import pytest
from fastapi.testclient import TestClient
from payment_gateway_api.app import app
from payment_gateway_api.dto.payment import ProcessPaymentBody


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

@pytest.fixture
def valid_payment_body() -> ProcessPaymentBody:
    return ProcessPaymentBody(
    card_number="2222405343248875",
    exp_month=6,
    exp_year=2028,
    currency="GBP",
    amount=1000,
    cvv="1234"
)
