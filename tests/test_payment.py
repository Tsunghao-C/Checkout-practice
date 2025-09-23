import pytest

class TestProcessPaymentEndpoint:
    def test_happy_path(self, client, valid_payment_body):
        response = client.post("/payment", content=valid_payment_body.json())
        assert response.status_code == 200
        assert response.json().get("last_4_card_number") == "8875"

    @pytest.mark.parametrize(
        "amount,status",
        [
            (0, 422),
            (-10, 422),
            (10_000_000_000, 200),
        ],
    )
    def test_amount_validation(self, client, valid_payment_body, amount, status):
        body = valid_payment_body.copy(update={"amount": amount})
        resp = client.post("/payment", content=body.json())
        assert resp.status_code == status
