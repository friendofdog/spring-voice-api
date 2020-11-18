from flask import Response

from springapi.exceptions import AuthorizationError
from tests.helpers import RouteResponseAssertions
from unittest import mock


class TestAuthRoute(RouteResponseAssertions):

    @mock.patch('springapi.routes.authorization.get_auth_code_uri')
    def test_auth_route_returns_redirect(self, mock_auth):
        mock_auth.return_value = "http://example.com"
        self.assert_get_returns_redirect("/api/v1/auth")


@mock.patch('springapi.routes.authorization.create_api_token')
class TestAuthCallbackRoute(RouteResponseAssertions):

    def test_auth_callback_route_includes_token_in_response_header(
            self, mock_auth):
        response = Response()
        response.headers["token"] = "def456"
        expected = mock_auth.return_value = response
        self.assert_get_raises_ok(
            "/api/v1/auth-callback?code=abc123",
            content_type="text/html; charset=utf-8",
            credentials={"token": expected.headers.get("token")})

    def test_auth_callback_route_raises_authorization_error(self, mock_err):
        pass
        err = mock_err.side_effect = AuthorizationError('Bad token')
        self.assert_get_raises_authorization_error(
            "/api/v1/auth-callback?bad_param=abc",
            {"error": f"Something went wrong with token exchange: {err}"})
