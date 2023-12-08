import logging

from conduit_commons.http.http_response import (
    SuccessResponse,
    ErrorResponse,
    UnavailableResponse,
)
from conduit_commons.http.errors import (
    ServerUnavailableError,
    RequestTimeoutError,
    RequestNotFoundError,
)

REQUESTS_LOGGER = logging.getLogger("Commons - Do Request")


def do_request(fn):
    if not callable(fn):
        raise TypeError("fn is not callable")
    try:
        return SuccessResponse(value=fn())

    except ServerUnavailableError as unavailable:
        REQUESTS_LOGGER.error(unavailable.msg)
        return UnavailableResponse(error=unavailable.msg)

    except RequestTimeoutError as timeout:
        REQUESTS_LOGGER.error(timeout.msg)
        return UnavailableResponse(error=timeout.msg)

    except RequestNotFoundError as not_found:
        REQUESTS_LOGGER.error(not_found.msg)
        return ErrorResponse(error=not_found.msg)

    except Exception as e:
        REQUESTS_LOGGER.error(e)
        return ErrorResponse(error="Bad request")
