from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
import logging

logger = logging.getLogger("RequestControlMiddleware")


class RequestControlMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        #Restrict to only certain HTTP methods
        if request.method not in ["GET", "POST"]:
            logger.warning("Method Not Allowed")
            return Response(content="Method Not Allowed", status_code=405)

        response = await call_next(request)
        return response
