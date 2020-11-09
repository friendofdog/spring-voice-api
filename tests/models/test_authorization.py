import unittest
from springapi.models.authorization import (
    get_auth_code_uri, exchange_oauth_token)
from springapi.exceptions import AuthorizationError, AuthProviderResponseError
from unittest import mock


@mock.patch('springapi.models.authorization.client_get_auth')
class TestAuthorization(unittest.TestCase):

    def test_get_auth_code_uri_returns_success(self, mock_resp):
        expected = mock_resp.return_value = {"success": True}
        response = get_auth_code_uri({"foo": "bar"}, {"client_id": "abc"})
        self.assertEqual(response, expected)

    def test_get_auth_code_uri_raises_error_on_bad_requst(self, mock_resp):
        mock_resp.side_effect = AuthProviderResponseError("blah")
        with self.assertRaises(AuthorizationError) as context:
            get_auth_code_uri({"foo": "bar"}, {"client_id": "abc"})
        self.assertEqual(str(context.exception), "blah")


@mock.patch('springapi.models.authorization.client_get_token')
class TestToken(unittest.TestCase):

    @mock.patch('springapi.models.email.Email.get_authorized_emails')
    @mock.patch('springapi.models.authorization.client_get_user')
    def test_exchange_oauth_token_returns_success(
            self, mock_user, mock_email, mock_resp):
        email = "foo@bar.com"
        mock_user.return_value = {"email": email}
        mock_email.return_value = [email]
        expected = mock_resp.return_value = "abc123"
        response = exchange_oauth_token(
            b"abc", {"foo": "bar"}, "http://example.com")
        self.assertEqual(response, expected)

    @mock.patch('springapi.models.email.Email.get_authorized_emails')
    @mock.patch('springapi.models.authorization.client_get_user')
    def test_exchange_oauth_token_raises_ValidationError_on_bad_email(
            self, mock_user, mock_email, mock_resp):
        user = mock_user.return_value = {"email": "foo@bar.com"}
        mock_email.return_value = ["bar@foo.com"]
        mock_resp.return_value = "abc123"
        with self.assertRaises(AuthorizationError) as context:
            exchange_oauth_token(b"abc", {"foo": "bar"}, "http://example.com")
        self.assertEqual(
            str(context.exception),
            f"User associated with {user['email']} is not authorized")

    def test_exchange_oauth_token_raises_error_on_bad_requst(self, mock_resp):
        mock_resp.side_effect = AuthProviderResponseError("no good")
        with self.assertRaises(AuthorizationError) as context:
            exchange_oauth_token(b"abc", {"foo": "bar"}, "http://example.com")
        self.assertEqual(str(context.exception), "no good")
