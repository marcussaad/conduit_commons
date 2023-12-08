from typing import List

from pydantic import BaseModel


class ServerUnavailableError(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "Server is unavailable"
        super().__init__(msg, *args, **kwargs)


class RequestTimeoutError(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "Request timed out"
        super().__init__(msg, *args, **kwargs)


class RequestNotFoundError(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "Request not found"
        super().__init__(msg, *args, **kwargs)


class FieldError(BaseModel):
    field: str
    message: str


class ResponseError(BaseModel):
    detail: str = None


class ValidationResponseError(ResponseError):
    errors: List[FieldError]
