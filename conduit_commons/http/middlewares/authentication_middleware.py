import logging

from conduit_auth.roles.roles import Roles
from fastapi import HTTPException
from pydantic import parse_obj_as
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from conduit_commons.authentication.auth0_authentication import Auth0Authentication
from conduit_commons.authentication.auth_user import AuthUser
from conduit_commons.authentication.errors import (
    JWKSInvalidJSON,
    NoKeysFoundInJWKS,
    NoKeyMatch,
    MissingValidJWT,
    InvalidJWTToken,
    InvalidJWTAlgorithm,
    ExpiredToken,
    InvalidClaims,
    InvalidToken,
)

log = logging.getLogger(__name__)


class AuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, *args, **kwargs):
        self.domain = kwargs.get("domain", None)

        if self.domain:
            self.auth0_auth = Auth0Authentication(
                jwks_url=f"https://{self.domain}/.well-known/jwks.json",
                issuer=f"https://{self.domain}/",
                audience=f"https://{self.domain}/api/v2/",
            )

            self.user_vault = kwargs.get("user_vault", None)

        super().__init__(app=kwargs.get("app"))

    async def dispatch(self, request: Request, call_next):
        try:
            if request.headers.get("Authorization"):
                user = self.get_current_user(request=request)
                request.state.user = user
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content=e.detail)
        except Exception as e:
            log.error("Error trying to get current user", e)
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=None)

        return await call_next(request)

    def get_current_user(self, request: Request) -> AuthUser:
        authorization_header = request.headers.get("Authorization", None)
        impersonated_user_id_from_header = request.headers.get("Conduit-Impersonate", None)

        if authorization_header:
            try:
                token = authorization_header.replace("Bearer ", "")

                user = self.auth0_auth.validate_token(token)
                auth_user = parse_obj_as(AuthUser, user)

                """
                    If a user id was provided in the Conduit-Impersonate header,
                    we validate that the user who set the header is a system admin,
                    then we set the user in the session as the one who we're impersonating,
                    while marking who is the impersonator.
                """
                if impersonated_user_id_from_header:
                    impersonator = self.user_vault.get_user(auth_user.id())
                    if impersonator.role() == Roles.SystemAdministratorRole:
                        impersonated_user = self.user_vault.get_user(impersonated_user_id_from_header)
                        if impersonated_user:
                            impersonated_user.set_impersonator(impersonator=impersonator)
                            auth_user = impersonated_user
                        else:
                            # Failed to find user to impersonate
                            auth_user = self.user_vault.get_user(auth_user.id())
                    else:
                        # Non SystemAdmin trying to impersonate
                        raise InvalidJWTToken()
                else:
                    auth_user = self.user_vault.get_user(auth_user.id())

                if not auth_user:
                    raise HTTPException(status_code=401, detail="Could not authenticate request")

                return auth_user
            except (
                JWKSInvalidJSON,
                NoKeysFoundInJWKS,
                NoKeyMatch,
                MissingValidJWT,
                InvalidJWTToken,
                InvalidJWTAlgorithm,
            ):
                raise HTTPException(status_code=401, detail="Failed to parse token")
            except (ExpiredToken, InvalidClaims, InvalidToken):
                raise HTTPException(status_code=401, detail="Could not authenticate request")
        else:
            raise HTTPException(status_code=401, detail="Missing authentication")
