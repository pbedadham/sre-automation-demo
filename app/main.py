from __future__ import annotations

import os
import time

from fastapi import FastAPI, Response

STARTED_AT = time.time()
APP_VERSION = os.getenv("APP_VERSION", "local")
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

app = FastAPI(title="Orders API", version=APP_VERSION)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "environment": ENVIRONMENT, "version": APP_VERSION}


@app.get("/ready")
def ready() -> dict[str, object]:
    return {
        "ready": True,
        "uptime_seconds": round(time.time() - STARTED_AT, 2),
    }


@app.get("/metrics")
def metrics() -> Response:
    body = "\n".join(
        [
            "# HELP orders_api_up Service availability.",
            "# TYPE orders_api_up gauge",
            "orders_api_up 1",
            "# HELP orders_api_uptime_seconds Service uptime.",
            "# TYPE orders_api_uptime_seconds gauge",
            f"orders_api_uptime_seconds {round(time.time() - STARTED_AT, 2)}",
            "",
        ]
    )
    return Response(content=body, media_type="text/plain")


@app.get("/orders/{order_id}")
def get_order(order_id: str) -> dict[str, object]:
    return {
        "order_id": order_id,
        "status": "processing",
        "items": [
            {"sku": "demo-widget", "quantity": 1},
        ],
    }
