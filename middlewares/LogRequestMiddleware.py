from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging
import json

logger = logging.getLogger("LogMiddleware")


class LogRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        body = await request.body()
        json_body = None
        if "content-length" in request.headers and int(request.headers["content-length"]) > 0:
            try:
                json_body = json.loads(body.decode())
            except json.JSONDecodeError:
                logger.error("Invalid JSON in request body.")
                json_body = body

        log_request = {
            "method": request.method,
            "url": str(request.url),
            "body": json_body
        }

        logger.debug(log_request)

        response = await call_next(request)
        process_time = (time.time() - start_time)

        log_response = {
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "process_time_s": process_time
        }

        if request.method != "GET":
            logger.info(log_response)
        else:
            logger.debug(log_response)

        return response
