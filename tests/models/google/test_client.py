import requests
import unittest
from springapi.models.google.client import (
    create_auth_request, exchange_auth_token, AuthProviderResponseError)
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

    def test_create_auth_request_raises_KeyError_on_bad_credentials(self):
        with self.assertRaises(AuthProviderResponseError) as context:
            create_auth_request("https://example.com", {"bad_key": "123"})
        self.assertEqual(
            str(context.exception), "Bad credentials")


@mock.patch.object(requests, "post")
class TestGoogleToken(unittest.TestCase):

    def test_exchange_auth_token_returns_token(self, mock_post):
        mock_post.return_value.status_code = 200
        response = exchange_auth_token('some_auth_code')
        self.assertEqual(response, {"success": True})

    def test_exchange_auth_token_raises_err_on_bad_response(self, mock_post):
        mock_post.return_value.status_code = 400

        with self.assertRaises(AuthProviderResponseError) as context:
            exchange_auth_token('some_auth_code')
        self.assertEqual(
            str(context.exception),
            "Error retrieving token from https://oauth2.googleapis.com/token")
