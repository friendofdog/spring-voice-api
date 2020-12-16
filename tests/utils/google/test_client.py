import json
import requests
import unittest

from springapi.utils.google.client import (
    create_auth_request_uri, get_oauth_token, get_authenticated_user_email,
    AuthProviderResponseError)
from unittest import mock


GOOGLE_CREDENTIALS = {
    "web": {
        "client_id": "abc",
        "client_secret": "123"
    }
}


class TestGoogleAuthorization(unittest.TestCase):

    def test_create_auth_request_returns_url_string(self):
        expected_url = "https://accounts.google.com/o/oauth2/v2/auth"
        expected_params = ['access_type', 'client_id', 'redirect_uri',
                           'response_type', 'scope']
        response = create_auth_request_uri(
            "https://example.com", GOOGLE_CREDENTIALS)
        url, param_str = response.split("?")
        params = [s.split("=")[0] for s in param_str.split("&")]
        self.assertEqual(url, expected_url)
        self.assertListEqual(params, expected_params)


@mock.patch.object(requests, "post")
class TestGoogleToken(unittest.TestCase):

    def test_exchange_auth_token_returns_token(self, mock_post):
        expected = mock_post.return_value.content = \
            b'{"access_token": "12345", "expires_in": 5000}'
        response = get_oauth_token(
            {"code": "1234"}, GOOGLE_CREDENTIALS, "https://example.com")
        self.assertEqual(response, json.loads(expected)["access_token"])

    def test_exchange_auth_token_raises_AuthProviderResponseError(
            self, mock_post):
        mock_post.return_value.content = b'{"error": "bad response"}'
        token_url = "https://someoauthprovider.com"
        with self.assertRaises(AuthProviderResponseError) as context:
            get_oauth_token(
                {"code": "1234"}, GOOGLE_CREDENTIALS, "https://example.com",
                token_url)
        self.assertEqual(
            str(context.exception),
            f"Error retrieving token from {token_url}")


@mock.patch.object(requests, "get")
class TestGetAuthenticatedUser(unittest.TestCase):

    def test_get_authenticated_user_email_returns_user_info(self, mock_get):
        expected = mock_get.return_value.content = b'{"email": "foo@bar.com"}'
        response = get_authenticated_user_email("abc123")
        self.assertEqual(response, json.loads(expected)["email"])

    def test_get_authenticated_user_email_raises_AuthProviderResponseError(
            self, mock_get):
        mock_get.return_value.content = b'{"bad_field": "error"}'
        user_url = "https://example.com"
        with self.assertRaises(AuthProviderResponseError) as context:
            get_authenticated_user_email(
                {"access_token": "abc123"}, user_url)
        self.assertEqual(
            str(context.exception),
            f"Error retrieving user info from {user_url}")
