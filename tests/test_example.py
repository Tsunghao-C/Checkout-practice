from fastapi.testclient import TestClient
from payment_gateway_api.app import app


def test_example(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"app": "payment-gateway-api"}



def test_post_process_payment_happy_path(client, valid_payment_body):
    
    response = client.post(url="/payment", content=valid_payment_body.json())

    assert response.status_code == 200
    assert response.json().get("last_4_card_number") == "8875"

