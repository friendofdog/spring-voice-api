import json
import requests
import unittest

from springapi.models.google.client import (
    create_auth_request, exchange_auth_token, get_authenticated_user,
    AuthProviderResponseError, ValidationError)
from unittest import mock


GOOGLE_CREDENTIALS = {
    "web": {
        "client_id": "abc",
        "client_secret": "123"
    }
}


class TestGoogleAuthorization(unittest.TestCase):

    def test_create_auth_request_returns_url_string(self):
        expected = "https://accounts.google.com/o/oauth2/v2/auth?access_type" \
                   "=offline&client_id=abc&redirect_uri=https%3A%2F%2Fexampl" \
                   "e.comapi%2Fv1%2Fauth-callback&response_type=code&scope=h" \
                   "ttps%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+" \
                   "https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profi" \
                   "le+"
        response = create_auth_request(
            "https://example.com", GOOGLE_CREDENTIALS)
        self.assertEqual(response, expected)

    def test_create_auth_request_raises_ValidationError_bad_credentials(self):
        with self.assertRaises(ValidationError) as context:
            create_auth_request("https://example.com", {"bad_key": "123"})
        self.assertEqual(
            str(context.exception), "Bad credentials")


@mock.patch.object(requests, "post")
class TestGoogleToken(unittest.TestCase):

    def test_exchange_auth_token_returns_token(self, mock_post):
        expected = mock_post.return_value.content = \
            b'{"access_token": "12345", "expires_in": 5000}'
        response = exchange_auth_token(
            {"code": "1234"}, GOOGLE_CREDENTIALS, "https://example.com")
        self.assertEqual(response, json.loads(expected)["access_token"])

    def test_exchange_auth_token_raises_AuthProviderResponseError(
            self, mock_post):
        mock_post.return_value.content = b'{"error": "bad response"}'
        token_url = "https://someoauthprovider.com"
        with self.assertRaises(AuthProviderResponseError) as context:
            exchange_auth_token(
                {"code": "1234"}, GOOGLE_CREDENTIALS, "https://example.com",
                token_url)
        self.assertEqual(
            str(context.exception),
            f"Error retrieving token from {token_url}")

    def test_exchange_auth_token_raises_ValidationError_bad_credentials(
            self, mock_post):
        mock_post.return_value.content = b'{"error": "bad response"}'
        with self.assertRaises(ValidationError) as context:
            exchange_auth_token(
                "https://example.com", {"web": {"bad": "creds"}}, "12345")
        self.assertEqual(str(context.exception), "Bad credentials")


@mock.patch.object(requests, "get")
class TestGetAuthenticatedUser(unittest.TestCase):

    def test_get_authenticated_user_returns_user_info(self, mock_get):
        expected = mock_get.return_value.content = b'{"email": "a@b"}'
        response = get_authenticated_user("abc123")
        self.assertEqual(response, json.loads(expected))

    def test_get_authenticated_user_raises_AuthProviderResponseError(
            self, mock_get):
        mock_get.return_value.content = b'{"bad_field": "error"}'
        user_url = "https://example.com"
        with self.assertRaises(AuthProviderResponseError) as context:
            get_authenticated_user(
                {"access_token": "abc123"}, user_url)
        self.assertEqual(
            str(context.exception),
            f"Error retrieving user info from {user_url}")
