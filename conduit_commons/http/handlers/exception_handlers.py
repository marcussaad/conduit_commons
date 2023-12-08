from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from conduit_commons.exceptions.validation_exception import ValidationException
from conduit_commons.http.errors import ValidationResponseError, FieldError


async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            ValidationResponseError(
                errors=list(
                    map(lambda error: (FieldError(message=error.get("msg"), field=error.get("loc")[1])), exc.errors())
                )
            )
        ),
    )


async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(exc.error))
