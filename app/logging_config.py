"""Structured JSON logging configuration."""

import json
import logging

from app.config import settings


class JSONFormatter(logging.Formatter):
    """Formats log records as single-line JSON for structured log ingestion."""

    def format(self, record: logging.LogRecord) -> str:
        return json.dumps({
            "time": self.formatTime(record),
            "level": record.levelname,
            "feature": getattr(record, "feature", "core"),
            "repo": getattr(record, "repo", "unknown"),
            "message": record.getMessage(),
        })


def setup_logging() -> None:
    """Configure root logger with JSON formatter."""
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())

    root = logging.getLogger()
    root.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    root.handlers = [handler]
