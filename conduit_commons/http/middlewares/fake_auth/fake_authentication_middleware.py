import logging

from fastapi import HTTPException
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from conduit_commons.http.middlewares.fake_auth import fake_authentication

log = logging.getLogger(__name__)


class FakeAuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            if request.url.path != "/authorization/api/auth/token":
                authorization_header = request.headers.get("Authorization", None)

                if not authorization_header:
                    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="Invalid token")

                token = authorization_header.replace("Bearer ", "")
                if token not in fake_authentication.TOKENS:
                    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="Invalid token")
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content=e.detail)
        except Exception as e:
            log.error("Error trying to get current user", e)
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=None)

        return await call_next(request)
