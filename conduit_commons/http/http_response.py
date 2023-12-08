class Response(object):
    def __init__(self, value=None, error=None):
        self._value = value
        self._error = error

    def is_success(self):
        raise NotImplementedError

    def is_failure(self):
        raise NotImplementedError

    def is_unavailable(self):
        raise NotImplementedError

    def value(self):
        raise NotImplementedError

    def value_or(self):
        raise NotImplementedError

    def failure(self):
        raise NotImplementedError

    def http_response(self):
        raise NotImplementedError


class SuccessResponse(Response):
    def is_success(self):
        return True

    def is_failure(self):
        return False

    def is_unavailable(self):
        return False

    def value(self):
        return self._value

    def value_or(self, default=None):
        return self._value or default

    def failure(self):
        return

    def http_response(self):
        return self.value_or(default=""), 200


class ErrorResponse(Response):
    def is_success(self):
        return False

    def is_failure(self):
        return True

    def is_unavailable(self):
        return False

    def value(self):
        return None

    def value_or(self, default=None):
        return default

    def failure(self):
        return self._error

    def http_response(self):
        return self.failure(), 400


class UnavailableResponse(Response):
    def is_success(self):
        return False

    def is_failure(self):
        return False

    def is_unavailable(self):
        return True

    def value(self):
        return None

    def value_or(self, default=None):
        return default

    def failure(self):
        return self._error

    def http_response(self):
        return self.failure(), 408
