from http import HTTPStatus
from typing import Iterator, List

from conduit_auth.roles.roles import Roles
from graphql import ExecutionResult, GraphQLError
from pydantic import parse_obj_as
from strawberry.extensions import SchemaExtension
from strawberry.types.graphql import OperationType
from strawberry.utils.await_maybe import AwaitableOrValue

from conduit_commons.authentication.auth0_authentication import Auth0Authentication
from conduit_commons.authentication.auth_user import AuthUser
from conduit_commons.authentication.errors import (
    UnauthorizedRequest,
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


class MutationErrorHandler(SchemaExtension):
    def on_execute(self) -> AwaitableOrValue[None]:
        yield
        if self.execution_context.operation_type == OperationType.MUTATION:
            if self.execution_context.result.data:
                for (
                    operationName,
                    operationResult,
                ) in self.execution_context.result.data.items():
                    if self.execution_context.context.get("errors", []):
                        operationResult["status"] = HTTPStatus.BAD_REQUEST.value


class UserVaultExtension(SchemaExtension):
    def __init__(self, *args, **kwargs):
        self.user_vault = kwargs.get("user_vault", None)

    def on_operation(self):
        self.execution_context.context["user_vault"] = self.user_vault
        yield


class AuthenticateRequests(SchemaExtension):
    def __init__(self, *args, **kwargs):
        self.domain = kwargs.get("domain", None)
        self.user_vault = kwargs.get("user_vault", None)

    def on_operation(self):
        headers = self.execution_context.context["request"].headers
        authorization_header = headers.get("Authorization", headers.get("X-Authorization", None))
        impersonated_user_id_from_header = self.execution_context.context["request"].headers.get(
            "Conduit-Impersonate", None
        )

        auth0_auth = Auth0Authentication(
            jwks_url=f"https://{self.domain}/.well-known/jwks.json",
            issuer=f"https://{self.domain}/",
            audience=f"https://{self.domain}/api/v2/",
        )

        if authorization_header:
            try:
                token = authorization_header.replace("Bearer ", "")

                user = auth0_auth.validate_token(token)
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
                            self.execution_context.context["user"] = impersonated_user
                        else:
                            # Failed to find user to impersonate
                            self.execution_context.context["user"] = self.user_vault.get_user(auth_user.id())
                    else:
                        # Non SystemAdmin trying to impersonate
                        raise InvalidJWTToken()
                else:
                    self.execution_context.context["user"] = self.user_vault.get_user(auth_user.id())
                yield
            except (
                JWKSInvalidJSON,
                NoKeysFoundInJWKS,
                NoKeyMatch,
                MissingValidJWT,
                InvalidJWTToken,
                InvalidJWTAlgorithm,
            ):
                self.execution_context.result = ExecutionResult(
                    data={"status": 401}, errors=[UnauthorizedRequest("Failed to parse token")]
                )
            except (ExpiredToken, InvalidClaims, InvalidToken):
                self.execution_context.result = ExecutionResult(
                    data={"status": 401}, errors=[UnauthorizedRequest("Could not authenticate request")]
                )
            finally:
                yield
        else:
            self.execution_context.result = ExecutionResult(
                data={"status": 401}, errors=[UnauthorizedRequest("Missing authentication")]
            )
            yield


class CleanerErrors(SchemaExtension):
    error_message: str

    def __init__(self, error_message: str = "Unexpected error.", *args, **kwargs):
        self.error_message = error_message
        super().__init__(*args, **kwargs)

    def clean_error(self, error: GraphQLError) -> GraphQLError:
        return GraphQLError(
            message=error.message or self.error_message,
            nodes=None,
            source=None,
            positions=None,
            path=None,
            original_error=None,
        )

    def on_operation(self) -> Iterator[None]:
        yield
        result = self.execution_context.result
        if result and result.errors:
            processed_errors: List[GraphQLError] = []
            for error in result.errors:
                processed_errors.append(self.clean_error(error))

            result.errors = processed_errors
