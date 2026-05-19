"""Structured logging setup with optional trace context."""

import logging
import sys

import structlog


class TraceIdProcessor:
    def __call__(self, _logger: object, _name: str, event_dict: dict[str, object]) -> dict[str, object]:
        event_dict.setdefault("trace_id", "unknown")
        return event_dict


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(stream=sys.stdout, level=getattr(logging, level.upper(), logging.INFO))
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            TraceIdProcessor(),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.PrintLoggerFactory(),
    )
