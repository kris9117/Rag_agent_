import json
import logging
import time
from typing import Any


logger = logging.getLogger("enterprise_it_support")


def log_event(event: str, **fields: Any) -> None:
    """Write a structured JSON log event."""

    payload = {
        "event": event,
        **fields,
    }

    logger.info(json.dumps(payload, default=str))


class Timer:
    """Simple execution timer."""

    def __init__(self) -> None:
        self.start_time = time.perf_counter()

    def elapsed_ms(self) -> float:
        return round(
            (time.perf_counter() - self.start_time) * 1000,
            2,
        )