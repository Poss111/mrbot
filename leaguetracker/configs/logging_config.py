import structlog
from structlog.contextvars import merge_contextvars
import os

def setup_logging():
    """Setup logging configuration"""
    if os.getenv("LOGGING_FORMAT") == "json":
        print("Using JSON logging format")
        structlog.configure(
            processors=[
                structlog.stdlib.add_log_level,
                structlog.processors.TimeStamper(),
                structlog.processors.JSONRenderer()
            ]
        )
    else:
        structlog.configure(
            processors=[
                merge_contextvars,
                structlog.processors.KeyValueRenderer(key_order=["event"]),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
        )
    