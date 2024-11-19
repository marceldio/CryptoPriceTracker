from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_prices():
    response = client.get("/prices/?ticker=btc_usd")
    assert response.status_code == 200

def test_get_last_price():
    response = client.get("/prices/last/?ticker=eth_usd")
    assert response.status_code == 200
