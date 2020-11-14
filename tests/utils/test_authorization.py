import unittest
from springapi.utils.authorization import get_auth_code_uri, exchange_token
from springapi.exceptions import AuthorizationError, AuthProviderResponseError
from unittest import mock


@mock.patch('springapi.utils.authorization.create_auth_request_uri')
class TestAuthorization(unittest.TestCase):

    def test_get_auth_code_uri_returns_success(self, mock_resp):
        expected = mock_resp.return_value = {"success": True}
        response = get_auth_code_uri({"foo": "bar"}, {"client_id": "abc"})

        self.assertEqual(response, expected)


@mock.patch('springapi.utils.authorization.get_oauth_token')
class TestToken(unittest.TestCase):

    @mock.patch('springapi.models.email.Email.get_authorized_emails')
    @mock.patch('springapi.utils.authorization.get_authenticated_user_email')
    def test_exchange_oauth_token_returns_success(
            self, mock_user, mock_email, mock_resp):
        email = "foo@bar.com"
        mock_user.return_value = email
        mock_email.return_value = [email]
        expected = mock_resp.return_value = "abc123"
        response = exchange_token(
            b"abc", {"foo": "bar"}, "http://example.com")

        self.assertEqual(response, expected)

    @mock.patch('springapi.models.email.Email.get_authorized_emails')
    @mock.patch('springapi.utils.authorization.get_authenticated_user_email')
    def test_exchange_oauth_token_raises_ValidationError_on_bad_email(
            self, mock_user, mock_email, mock_resp):
        user_email = mock_user.return_value = "foo@bar.com"
        mock_email.return_value = ["bar@foo.com"]
        mock_resp.return_value = "abc123"

        with self.assertRaises(AuthorizationError) as context:
            exchange_token(b"abc", {"foo": "bar"}, "http://example.com")

        self.assertEqual(
            str(context.exception),
            f"User associated with {user_email} is not authorized")

    def test_exchange_oauth_token_raises_error_on_bad_requst(self, mock_resp):
        mock_resp.side_effect = AuthProviderResponseError("no good")

        with self.assertRaises(AuthorizationError) as context:
            exchange_token(b"abc", {"foo": "bar"}, "http://example.com")

        self.assertEqual(str(context.exception), "no good")
