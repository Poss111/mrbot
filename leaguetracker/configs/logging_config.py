import logging
import structlog
from structlog.contextvars import merge_contextvars
import os

from leaguetracker.configs.environment_variables import EnvVariables

def setup_logging():
    """Setup logging configuration"""
    log_level = os.getenv(EnvVariables.LOG_LEVEL.name, "INFO")
    log_level = logging.INFO
    match log_level:    
        case "DEBUG":
            log_level = logging.DEBUG
        case "INFO":
            log_level = logging.INFO
        case "WARNING" | "WARN":
            log_level = logging.WARNING
        case "ERROR":
            log_level = logging.ERROR
        case "CRITICAL":
            log_level = logging.CRITICAL
        case "":
            log_level = logging.INFO
            
    logging_format = os.getenv(EnvVariables.LOGGING_FORMAT.name, "text")
            
    print(f"Setting log level to {log_level} with {logging_format} format")
    

    if logging_format == "json":
        print("Using JSON logging format")
        structlog.configure(
            processors=[
                structlog.stdlib.add_log_level,
                structlog.processors.TimeStamper(),
                structlog.processors.JSONRenderer()
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.make_filtering_bound_logger(log_level)
        )
    else:
        structlog.configure(
            processors=[
                merge_contextvars,
                structlog.stdlib.add_log_level,
                structlog.processors.TimeStamper(),
                structlog.processors.KeyValueRenderer(key_order=["command", "event", "id"]),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.make_filtering_bound_logger(log_level)
        )
    