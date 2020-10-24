from springapi.exceptions import AuthorizationError, ValidationError
from tests.helpers import RouteResponseAssertions
from unittest import mock


class TestAuthRoute(RouteResponseAssertions):

    __test__ = False

    def test_auth_route_returns_success(self):
        expected = {"success": True}
        self.assert_post_raises_ok(
            "/api/v1/auth", {"client_id": "123"}, expected)

    def test_auth_route_rejects_invalid_json(self):
        err = ValidationError('Invalid JSON')
        self.assert_post_raises_invalid_body(
            "/api/v1/auth", err.error_response_body())

    @mock.patch('springapi.routes.authorization.get_auth_code')
    def test_auth_route_raises_authorization_error(self, mock_err):
        err = mock_err.side_effect = AuthorizationError('Bad auth')
        self.assert_post_raises_authorization_error(
            "/api/v1/auth", {"foo": "bar"},
            {"error": f"Something went wrong with authorization: {err}"})


@mock.patch('springapi.routes.authorization.exchange_token')
class TestAuthCallbackRoute(RouteResponseAssertions):

    __test__ = False

    def test_auth_callback_route_exchanges_token(self, mock_auth):
        expected = mock_auth.return_value = {"success": True}
        self.assert_get_raises_ok(
            "/api/v1/auth-callback?code=123", expected)

    def test_auth_callback_route_raises_authorization_error(self, mock_err):
        err = mock_err.side_effect = AuthorizationError('Bad token')
        self.assert_get_raises_authorization_error(
            "/api/v1/auth-callback?bad_param=abc", {"foo": "bar"},
            {"error": f"Something went wrong with token exchange: {err}"})
