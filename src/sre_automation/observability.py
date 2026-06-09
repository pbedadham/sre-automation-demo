from __future__ import annotations

import json
import logging
import time
from collections.abc import Iterator
from contextlib import contextmanager


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def event(name: str, **fields: object) -> None:
    payload = {"event": name, **fields}
    logging.getLogger("sre_automation").info(json.dumps(payload, sort_keys=True))


@contextmanager
def timed_metric(name: str, **labels: object) -> Iterator[None]:
    started = time.monotonic()
    try:
        yield
        status = "success"
    except Exception:
        status = "failure"
        raise
    finally:
        duration_ms = int((time.monotonic() - started) * 1000)
        event(
            "metric",
            metric=name,
            duration_ms=duration_ms,
            status=status,
            **labels,
        )
