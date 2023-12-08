from conduit_commons.http.errors import ValidationResponseError


class ValidationException(Exception):
    error: ValidationResponseError

    def __init__(self, *args, **kwargs):
        self.error = kwargs.get("error")
