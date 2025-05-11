from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import logging
from detector import detect_anomalies, maybe_send_slack_alert, send_slack_alert
from schemas import Charge, Alert

app = FastAPI(title="Stripe Anomaly Detector")
logger = logging.getLogger("chargeiq")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

class AlertsRequest(BaseModel):
    events: List[Charge]

@app.post("/alerts", response_model=List[Alert])
def post_alerts(req: AlertsRequest):
    alerts = detect_anomalies(req.events)
    if send_slack_alert is None:
        logger.warning("[chargeiq] Pro plugin not installed: Slack alerting is disabled.")
    maybe_send_slack_alert(alerts)
    return alerts 