import logging
from logging.handlers import TimedRotatingFileHandler
import json


def setup_logger():
    log = logging.getLogger()

    for handler in log.handlers[:]:
        log.removeHandler(handler)

    with open("data/config.json", 'r') as f:
        config = json.load(f)
    log.setLevel(config["log_level"])
    formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')

    # Setup console logging
    ch = logging.StreamHandler()  # Console handler
    ch.setFormatter(formatter)
    log.addHandler(ch)

    # Setup daily rotating file logging
    fh = TimedRotatingFileHandler('logs/ai_weather_forecast.log', when="midnight", interval=1, backupCount=7)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    # Silence other loggers to warning level
    logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("multipart.multipart").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore.connection").setLevel(logging.WARNING)
    logging.getLogger("httpcore.http11").setLevel(logging.WARNING)

