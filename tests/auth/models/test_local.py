import requests
import unittest
from springapi.auth.models.local import (
    request_auth_code, exchange_auth_token)
from unittest import mock


class TestGoogleAuth(unittest.TestCase):

    @mock.patch.object(requests, "get")
    def test_request_auth_code_returns_code(self, mock_get):
        mock_get.return_value.status_code = 200
        response = request_auth_code({"a": "b"})
        self.assertEqual(response, {"success": True})

    @mock.patch.object(requests, "post")
    def test_exchange_auth_token_returns_token(self, mock_post):
        mock_post.return_value.status_code = 200
        response = exchange_auth_token('some_auth_code')
        self.assertEqual(response, {"success": True})
