import unittest
from springapi.auth.authorization import (
    get_auth_code, exchange_token)
from springapi.exceptions import AuthorizationError, AuthProviderResponseError
from unittest import mock


@mock.patch('springapi.auth.authorization.client_get_auth')
class TestAuthorization(unittest.TestCase):

    def test_get_auth_code_returns_success(self, mock_resp):
        expected = mock_resp.return_value = {"success": True}
        response = get_auth_code({"foo": "bar"})
        self.assertEqual(response, expected)

    def test_get_auth_code_raises_error_on_bad_requst(self, mock_resp):
        mock_resp.side_effect = AuthProviderResponseError("blah")
        with self.assertRaises(AuthorizationError) as context:
            get_auth_code({"foo": "bar"})
        self.assertEqual(str(context.exception), "blah")


@mock.patch('springapi.auth.authorization.client_get_token')
class TestToken(unittest.TestCase):

    def test_exchange_token_returns_success(self, mock_resp):
        expected = mock_resp.return_value = {"success": True}
        response = exchange_token({"foo": "bar"})
        self.assertEqual(response, expected)

    def test_exchange_token_raises_error_on_bad_requst(self, mock_resp):
        mock_resp.side_effect = AuthProviderResponseError("no good")
        with self.assertRaises(AuthorizationError) as context:
            exchange_token({"foo": "bar"})
        self.assertEqual(str(context.exception), "no good")
