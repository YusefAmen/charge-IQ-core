from typing import List
from collections import defaultdict
from schemas import Charge, Alert
from datetime import timedelta

UNUSUAL_CURRENCIES = {"USD", "EUR"}

# Try to import pro plugin
try:
    from pro.alert_plugins import send_slack_alert
except ImportError:
    send_slack_alert = None

def detect_anomalies(events: List[Charge]) -> List[Alert]:
    alerts = []
    # Rule 1: > $10,000 charge
    for event in events:
        if event.amount > 10000:
            alerts.append(Alert(user_id=event.user_id, reason="High value charge", charge=event))
        if event.currency not in UNUSUAL_CURRENCIES:
            alerts.append(Alert(user_id=event.user_id, reason=f"Unusual currency: {event.currency}", charge=event))
    # Rule 2: > 5 charges in a minute
    user_events = defaultdict(list)
    for event in events:
        user_events[event.user_id].append(event)
    for user_id, charges in user_events.items():
        charges_sorted = sorted(charges, key=lambda c: c.timestamp)
        for i in range(len(charges_sorted)):
            window = [c for c in charges_sorted if 0 <= (c.timestamp - charges_sorted[i].timestamp).total_seconds() <= 60]
            if len(window) > 5:
                alerts.append(Alert(user_id=user_id, reason="More than 5 charges in a minute", related_charges=window))
                break
    return alerts

def maybe_send_slack_alert(alerts: List[Alert]):
    if send_slack_alert:
        send_slack_alert(alerts) 