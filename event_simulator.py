import requests
import random
import time
from datetime import datetime, timedelta
import argparse

API_URL = "http://localhost:8000/alerts"
CURRENCIES = ["USD", "EUR", "JPY", "BTC"]


def simulate_events(event_type: str, count: int = 6):
    now = datetime.utcnow()
    events = []
    if event_type == "burst":
        for i in range(count):
            events.append({
                "user_id": "burst_user",
                "amount": 10,
                "currency": "USD",
                "timestamp": (now + timedelta(seconds=i)).isoformat()
            })
    elif event_type == "high-value":
        events.append({
            "user_id": "rich_user",
            "amount": 20000,
            "currency": "USD",
            "timestamp": now.isoformat()
        })
    elif event_type == "unusual-currency":
        events.append({
            "user_id": "fx_user",
            "amount": 10,
            "currency": "BTC",
            "timestamp": now.isoformat()
        })
    else:
        print("Unknown event type")
        return
    resp = requests.post(API_URL, json={"events": events})
    print(f"Status: {resp.status_code}")
    print(resp.json())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate Stripe charge events for ChargeIQ.")
    parser.add_argument("type", choices=["burst", "high-value", "unusual-currency"], help="Type of event to simulate")
    args = parser.parse_args()
    simulate_events(args.type) 