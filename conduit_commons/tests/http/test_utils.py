from unittest import TestCase
from unittest.mock import patch

from conduit_commons.http.errors import (
    ServerUnavailableError,
    RequestTimeoutError,
    RequestNotFoundError,
)
from conduit_commons.http.utils import do_request


class UtilsTestCase(TestCase):
    def raise_(self, exc):
        raise exc

    def test_do_request_not_callable(self):
        with self.assertRaises(TypeError, msg="fn is not callable"):
            do_request(None)

    def test_do_request_success_response(self):
        response = do_request(lambda: True)
        self.assertTrue(response.is_success())
        self.assertEqual(response.value(), True)
        self.assertEqual(response.value_or(default=None), True)
        self.assertEqual(response.http_response(), (True, 200))
        self.assertEqual(response.failure(), None)

    @patch("conduit_commons.http.utils.REQUESTS_LOGGER")
    def test_do_request_unavailable_response(self, mocked_logger):
        response = do_request(lambda: self.raise_(ServerUnavailableError))
        self.assertTrue(response.is_unavailable())
        self.assertEqual(response.value(), None)
        self.assertEqual(response.value_or(), None)
        self.assertEqual(response.http_response(), ("Server is unavailable", 408))
        self.assertEqual(response.failure(), "Server is unavailable")
        mocked_logger.error.assert_called_once()

    @patch("conduit_commons.http.utils.REQUESTS_LOGGER")
    def test_do_request_timeout_response(self, mocked_logger):
        response = do_request(lambda: self.raise_(RequestTimeoutError))
        self.assertTrue(response.is_unavailable())
        self.assertEqual(response.value(), None)
        self.assertEqual(response.value_or(), None)
        self.assertEqual(response.http_response(), ("Request timed out", 408))
        self.assertEqual(response.failure(), "Request timed out")
        mocked_logger.error.assert_called_once()

    @patch("conduit_commons.http.utils.REQUESTS_LOGGER")
    def test_do_request_not_found_response(self, mocked_logger):
        response = do_request(lambda: self.raise_(RequestNotFoundError))
        self.assertTrue(response.is_failure())
        self.assertEqual(response.value(), None)
        self.assertEqual(response.value_or(), None)
        self.assertEqual(response.http_response(), ("Request not found", 400))
        self.assertEqual(response.failure(), "Request not found")
        mocked_logger.error.assert_called_once()
