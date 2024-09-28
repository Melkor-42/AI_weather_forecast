import logging
from logging.handlers import TimedRotatingFileHandler
import json
import os


def setup_logger():
    """Set up the general logger configuration."""
    log = logging.getLogger()  # Gets the root logger

    # If the logger has handlers, clear them to avoid duplication
    for handler in log.handlers[:]:
        log.removeHandler(handler)

    log.setLevel("DEBUG")  # Set the minimum log level you want
    formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')

    # Setup console logging
    ch = logging.StreamHandler()  # Console handler
    ch.setFormatter(formatter)
    log.addHandler(ch)

    # Setup daily rotating file logging
    # The log filename is "scraper.log" and at midnight, it rotates to create a new log file.
    # Old logs are date-stamped, e.g., scraper.log.2023-10-09, scraper.log.2023-10-08, etc.
    # fh = TimedRotatingFileHandler('logs/tasman_logs.log', when="midnight", interval=1, backupCount=7) # `backupCount` keeps the last 7 log files. Adjust as needed.
    # fh.setFormatter(formatter)
    # log.addHandler(fh)

    # Silence other loggers to warning level
    logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("multipart.multipart").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore.connection").setLevel(logging.WARNING)
    logging.getLogger("httpcore.http11").setLevel(logging.WARNING)

