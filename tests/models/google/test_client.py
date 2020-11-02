import json
import requests
import unittest
from springapi.models.google.client import (
    create_auth_request, exchange_auth_token, AuthProviderResponseError,
    ValidationError)
from unittest import mock


class TestGoogleAuthorization(unittest.TestCase):

    def test_create_auth_request_returns_url_string(self):
        expected = "https://accounts.google.com/o/oauth2/v2/auth?client_id=" \
                   "abc&redirect_uri=" \
                   "https%3A%2F%2Fexample.comapi%2Fv1%2Fauth-callback&" \
                   "response_type=code&scope=https%3A%2F%2Fwww.googleapis" \
                   ".com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww." \
                   "googleapis.com%2Fauth%2Fuserinfo.profile+"
        redirect_host = "https://example.com"
        response = create_auth_request(redirect_host, {"client_id": "abc"})
        self.assertEqual(response, expected)

    def test_create_auth_request_raises_ValidationError_bad_credentials(self):
        with self.assertRaises(ValidationError) as context:
            create_auth_request("https://example.com", {"bad_key": "123"})
        self.assertEqual(
            str(context.exception), "Bad credentials")


class TestGoogleToken(unittest.TestCase):

    @mock.patch.object(requests, "post")
    def test_exchange_auth_token_returns_token(self, mock_post):
        expected = mock_post.return_value.content = \
            b'{"access_token": "12345", "expires_in": 5000}'
        response = exchange_auth_token(
            "https://example.com",
            {"client_id": "abc", "client_secret": "def"},
            "12345"
        )
        self.assertEqual(response, json.loads(expected))

    @mock.patch.object(requests, "post")
    def test_exchange_auth_token_raises_AuthProviderResponseError(
            self, mock_post):
        mock_post.return_value.content = b'{"error": "bad response"}'
        with self.assertRaises(AuthProviderResponseError) as context:
            exchange_auth_token(
                "https://example.com",
                {"client_id": "abc", "client_secret": "def"},
                "12345"
            )
        self.assertEqual(
            str(context.exception),
            "Error retrieving token from https://oauth2.googleapis.com/token")

    def test_exchange_auth_token_raises_ValidationError_bad_credentials(self):
        with self.assertRaises(ValidationError) as context:
            exchange_auth_token(
                "https://example.com", {"client_id": "abc"}, "12345")
        self.assertEqual(str(context.exception), "Bad credentials")
