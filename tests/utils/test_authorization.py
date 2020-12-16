import unittest
from springapi.utils.authorization import (
    create_api_token, exchange_oauth_token, generate_api_token,
    get_auth_code_uri)
from springapi.exceptions import AuthorizationError, AuthProviderResponseError
from unittest import mock


@mock.patch('springapi.utils.authorization.create_auth_request_uri')
class TestGetAuthorizationCode(unittest.TestCase):

    def test_get_auth_code_uri_returns_success(self, mock_resp):
        expected = mock_resp.return_value = {"success": True}
        response = get_auth_code_uri({"foo": "bar"}, {"client_id": "abc"})

        self.assertEqual(response, expected)


@mock.patch('springapi.utils.authorization.get_oauth_token')
class TestExchangeOAuthToken(unittest.TestCase):

    @mock.patch('springapi.models.email.Email.get_authorized_emails')
    @mock.patch('springapi.utils.authorization.get_authenticated_user_email')
    def test_exchange_oauth_token_returns_success(
            self, mock_user, mock_email, mock_oauth):
        oauth_args = b"abc", {"foo": "bar"}, "http://example.com"
        email = "foo@bar.com"
        mock_user.return_value = email
        mock_email.return_value = [email]
        response = exchange_oauth_token(*oauth_args)

        mock_oauth.assert_called_with(*oauth_args)
        self.assertEqual(response, email)

    @mock.patch('springapi.models.email.Email.get_authorized_emails')
    @mock.patch('springapi.utils.authorization.get_authenticated_user_email')
    def test_exchange_oauth_token_raises_AuthorizationError_on_bad_email(
            self, mock_user, mock_email, mock_oauth):
        user_email = mock_user.return_value = "foo@bar.com"
        mock_email.return_value = ["bar@foo.com"]
        mock_oauth.return_value = "abc123"

        with self.assertRaises(AuthorizationError) as context:
            exchange_oauth_token(b"abc", {"foo": "bar"}, "http://example.com")

        self.assertEqual(
            str(context.exception),
            f"User associated with {user_email} is not authorized")

    def test_exchange_oauth_token_raises_error_on_bad_requst(self, mock_oauth):
        mock_oauth.side_effect = AuthProviderResponseError("no good")

        with self.assertRaises(AuthorizationError) as context:
            exchange_oauth_token(b"abc", {"foo": "bar"}, "http://example.com")

        self.assertEqual(str(context.exception), "no good")


@mock.patch('springapi.utils.authorization.jwt.encode')
class TestGenerateApiToken(unittest.TestCase):

    def test_generate_api_token_returns_token(self, mock_jwt):
        expected = mock_jwt.return_value = b"qwerty"
        token = generate_api_token("foo@bar.com", "keysecret")

        self.assertEqual(expected, token)


@mock.patch('springapi.models.token.Token.create_token')
@mock.patch('springapi.utils.authorization.generate_api_token')
@mock.patch('springapi.utils.authorization.exchange_oauth_token')
class TestCreateApiToken(unittest.TestCase):

    def __init__(self, _):
        super().__init__(_)
        self.args = "auth-code-str", {"client_id": "123"},\
                    "secretkey", "http://example.com"

    def test_create_api_token_returns_api_token(
            self, mock_exch, mock_gen, mock_create):
        mock_exch.return_value = "foo@bar.com"
        expected = mock_gen.return_value = b"qwerty"
        mock_create.return_value = {"abc": "def"}
        response = create_api_token(*self.args)

        self.assertEqual(expected, response)

    def test_create_api_token_raises_error_if_exch_oauth_token_fails(
            self, mock_exch, mock_gen, mock_create):
        err = "OAuth failed somehow"
        mock_exch.side_effect = AuthorizationError(err)

        with self.assertRaises(AuthorizationError) as context:
            create_api_token(*self.args)

        self.assertIsInstance(context.exception, AuthorizationError)
        self.assertEqual(str(context.exception), err)
        self.assertFalse(mock_gen.called)
        self.assertFalse(mock_create.called)

    def test_create_api_token_raises_error_if_generate_api_token_fails(
            self, mock_exch, mock_gen, mock_create):
        err = "Generate API token failed somehow"
        mock_exch.return_value = "foo@bar.com"
        mock_gen.side_effect = ValueError(err)

        with self.assertRaises(ValueError) as context:
            create_api_token(*self.args)

        self.assertIsInstance(context.exception, ValueError)
        self.assertEqual(str(context.exception), err)
        self.assertFalse(mock_create.called)

    def test_create_api_token_raises_AuthorizationError_if_store_token_fails(
            self, mock_exch, mock_gen, mock_create):
        err = "Something invalid"
        mock_exch.return_value = False
        mock_gen.return_value = b"qwerty"
        mock_create.side_effect = AuthorizationError(err)

        with self.assertRaises(AuthorizationError) as context:
            create_api_token(*self.args)

        self.assertIsInstance(context.exception, AuthorizationError)
        self.assertEqual(str(context.exception), err)
