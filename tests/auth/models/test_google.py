import requests
import unittest
from springapi.auth.models.google import (
    request_auth_code, exchange_token, GoogleResponseError)
from unittest import mock


@mock.patch.object(requests, "get")
class TestGoogleAuthorization(unittest.TestCase):

    def test_request_auth_code_returns_code(self, mock_get):
        mock_get.return_value.status_code = 200
        response = request_auth_code({"a": "b"})
        self.assertEqual(response, {"success": True})

    def test_request_auth_code_raises_error_on_bad_response(self, mock_get):
        mock_get.return_value.status_code = 400

        with self.assertRaises(GoogleResponseError) as context:
            request_auth_code({"a": "b"})
        self.assertEqual(
            str(context.exception),
            "Error retrieving auth code from "
            "https://accounts.google.com/o/oauth2/v2/auth")


@mock.patch.object(requests, "post")
class TestGoogleToken(unittest.TestCase):

    def test_exchange_token_returns_token(self, mock_post):
        mock_post.return_value.status_code = 200
        response = exchange_token('some_auth_code')
        self.assertEqual(response, {"success": True})

    def test_exchange_token_raises_error_on_bad_response(self, mock_post):
        mock_post.return_value.status_code = 400

        with self.assertRaises(GoogleResponseError) as context:
            exchange_token('some_auth_code')
        self.assertEqual(
            str(context.exception),
            "Error retrieving token from https://oauth2.googleapis.com/token")
