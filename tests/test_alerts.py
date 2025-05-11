from fastapi.testclient import TestClient
from main import app
from schemas import Charge
from datetime import datetime, timedelta
import pytest

client = TestClient(app)

def test_high_value_charge():
    now = datetime.utcnow()
    events = [
        {"user_id": "u1", "amount": 20000, "currency": "USD", "timestamp": now.isoformat()}
    ]
    resp = client.post("/alerts", json={"events": events})
    assert resp.status_code == 200
    alerts = resp.json()
    assert any("High value charge" in a["reason"] for a in alerts)

def test_many_charges_in_minute():
    now = datetime.utcnow()
    events = [
        {"user_id": "u2", "amount": 10, "currency": "USD", "timestamp": (now + timedelta(seconds=i)).isoformat()} for i in range(6)
    ]
    resp = client.post("/alerts", json={"events": events})
    assert resp.status_code == 200
    alerts = resp.json()
    assert any("More than 5 charges" in a["reason"] for a in alerts)

def test_unusual_currency():
    now = datetime.utcnow()
    events = [
        {"user_id": "u3", "amount": 10, "currency": "JPY", "timestamp": now.isoformat()}
    ]
    resp = client.post("/alerts", json={"events": events})
    assert resp.status_code == 200
    alerts = resp.json()
    assert any("Unusual currency" in a["reason"] for a in alerts) 