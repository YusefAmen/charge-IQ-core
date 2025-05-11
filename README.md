[![Build Status](https://github.com/your-org/charge-IQ-core/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/charge-IQ-core/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

🚀 **Want alerting + dashboards? [Get Pro](https://chargeiq.com)**

A FastAPI microservice and Python module for detecting anomalies in Stripe charge events. Use as a standalone API (sidecar) or import as a Python module. Pro plugin support for advanced alert delivery.

## 1. Overview
- Detects high-value, rapid, or unusual-currency Stripe charges
- Use cases: fraud alerting, audit trail, sidecar integration in microservices

## 2. Installation
```sh
git clone <your-repo-url>
cd charge-IQ-core
pip install -r requirements.txt
cp .env.example .env
```

## 3. Running the API
- **Local:**
  ```sh
  uvicorn main:app --reload
  ```
- **Docker:**
  ```sh
  docker build -t stripe-anomaly-detector .
  docker run -p 8000:8000 stripe-anomaly-detector
  ```

## 4. API Reference
### POST /alerts
- Accepts a list of Stripe charge events (JSON)
- Each event: `user_id`, `amount`, `currency`, `timestamp`

**Example request:**
```sh
curl -X POST http://localhost:8000/alerts \
  -H 'Content-Type: application/json' \
  -d '{"events": [
    {"user_id": "u1", "amount": 20000, "currency": "USD", "timestamp": "2024-05-10T12:00:00Z"},
    {"user_id": "u2", "amount": 10, "currency": "JPY", "timestamp": "2024-05-10T12:01:00Z"}
  ]}'
```

**Example response:**
```json
[
  {"user_id": "u1", "reason": "High value charge", "charge": {"user_id": "u1", "amount": 20000, "currency": "USD", "timestamp": "2024-05-10T12:00:00Z"}, "related_charges": null},
  {"user_id": "u2", "reason": "Unusual currency: JPY", "charge": {"user_id": "u2", "amount": 10, "currency": "JPY", "timestamp": "2024-05-10T12:01:00Z"}, "related_charges": null}
]
```

## 5. Extending with Plugins
- Pro features: advanced alert delivery (e.g., Slack)
- If `pro/alert_plugins.py` is present, `send_slack_alert(alerts)` will be called automatically
- If not, plugin is skipped silently (with a warning in logs)

**Example code:**
```python
try:
    from pro.alert_plugins import send_slack_alert
except ImportError:
    send_slack_alert = None
if send_slack_alert:
    send_slack_alert(alerts)
```

## 6. Using as a Sidecar (Kubernetes)
- Minimal deployment YAML:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app-with-anomaly-detector
spec:
  containers:
    - name: my-app
      image: my-app:latest
    - name: anomaly-detector
      image: your-dockerhub/stripe-anomaly-detector:latest
      ports:
        - containerPort: 8000
```
- Curl from another service in the same pod:
  ```sh
  curl -X POST http://localhost:8000/alerts -d '{...}'
  ```
- Healthcheck: `GET /healthz`

## 7. Using as a Python Module
```python
from detector import detect_anomalies
from schemas import Charge

alerts = detect_anomalies([
    Charge(user_id="u1", amount=20000, currency="USD", timestamp="2024-05-10T12:00:00Z")
])
```

## 8. License
- MIT License
- Pro features require a commercial license