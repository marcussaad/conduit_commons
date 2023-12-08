from unittest import TestCase
from conduit_commons.http.errors import (
    ServerUnavailableError,
    RequestNotFoundError,
    RequestTimeoutError,
)


class ErrorsTestCase(TestCase):
    def test_server_unavailable_error(self):
        with self.assertRaises(ServerUnavailableError, msg="Server is unavailable"):
            raise ServerUnavailableError

    def test_request_timeout_error(self):
        with self.assertRaises(RequestTimeoutError, msg="Request timed out"):
            raise RequestTimeoutError

    def test_request_not_found_error(self):
        with self.assertRaises(RequestNotFoundError, msg="Request not found"):
            raise RequestNotFoundError
