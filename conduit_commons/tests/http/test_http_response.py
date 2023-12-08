from unittest import TestCase

from conduit_commons.http.http_response import (
    Response,
    ErrorResponse,
    SuccessResponse,
    UnavailableResponse,
)


class ResponseTestCase(TestCase):
    def setUp(self):
        self.request = Response()

    def test_init(self):
        self.assertEqual(self.request._value, None)
        self.assertEqual(self.request._error, None)

    def test_is_success(self):
        with self.assertRaises(NotImplementedError):
            self.request.is_success()

    def test_is_failure(self):
        with self.assertRaises(NotImplementedError):
            self.request.is_failure()

    def test_is_unavailable(self):
        with self.assertRaises(NotImplementedError):
            self.request.is_unavailable()

    def test_value_or(self):
        with self.assertRaises(NotImplementedError):
            self.request.value_or()

    def test_value(self):
        with self.assertRaises(NotImplementedError):
            self.request.value()

    def test_failure(self):
        with self.assertRaises(NotImplementedError):
            self.request.failure()

    def test_http_response(self):
        with self.assertRaises(NotImplementedError):
            self.request.http_response()


class SuccessResponseTestCase(TestCase):
    def setUp(self):
        self.request = SuccessResponse(value=True)

    def test_init(self):
        self.assertEqual(self.request._value, True)
        self.assertEqual(self.request._error, None)

    def test_is_success(self):
        self.assertTrue(self.request.is_success())

    def test_is_failure(self):
        self.assertFalse(self.request.is_failure())

    def test_is_unavailable(self):
        self.assertFalse(self.request.is_unavailable())

    def test_value_or(self):
        self.assertEqual(self.request.value_or(default=False), True)
        self.assertEqual(SuccessResponse().value_or(default=False), False)

    def test_value(self):
        self.assertEqual(self.request.value(), True)
        self.assertEqual(SuccessResponse().value(), None)

    def test_http_response(self):
        self.assertEqual(self.request.http_response(), (True, 200))
        self.assertEqual(SuccessResponse().http_response(), ("", 200))

    def test_failure(self):
        self.assertEqual(self.request.failure(), None)


class ErrorResponseTestCase(TestCase):
    def setUp(self):
        self.request = ErrorResponse(error="foo")

    def test_init(self):
        self.assertEqual(self.request._value, None)
        self.assertEqual(self.request._error, "foo")

    def test_is_success(self):
        self.assertFalse(self.request.is_success())

    def test_is_failure(self):
        self.assertTrue(self.request.is_failure())

    def test_is_unavailable(self):
        self.assertFalse(self.request.is_unavailable())

    def test_value_or(self):
        self.assertEqual(self.request.value_or(default=False), False)
        self.assertEqual(ErrorResponse().value_or(default=False), False)

    def test_value(self):
        self.assertEqual(self.request.value(), None)
        self.assertEqual(ErrorResponse().value(), None)

    def test_http_response(self):
        self.assertEqual(self.request.http_response(), ("foo", 400))
        self.assertEqual(ErrorResponse().http_response(), (None, 400))

    def test_failure(self):
        self.assertEqual(self.request.failure(), "foo")


class UnavailableResponseTestCase(TestCase):
    def setUp(self):
        self.request = UnavailableResponse(error="foo")

    def test_init(self):
        self.assertEqual(self.request._value, None)
        self.assertEqual(self.request._error, "foo")

    def test_is_success(self):
        self.assertFalse(self.request.is_success())

    def test_is_failure(self):
        self.assertFalse(self.request.is_failure())

    def test_is_unavailable(self):
        self.assertTrue(self.request.is_unavailable())

    def test_value_or(self):
        self.assertEqual(self.request.value_or(default=False), False)
        self.assertEqual(UnavailableResponse().value_or(default=False), False)

    def test_value(self):
        self.assertEqual(self.request.value(), None)
        self.assertEqual(UnavailableResponse().value(), None)

    def test_http_response(self):
        self.assertEqual(self.request.http_response(), ("foo", 408))
        self.assertEqual(UnavailableResponse().http_response(), (None, 408))

    def test_failure(self):
        self.assertEqual(self.request.failure(), "foo")
