from springapi.exceptions import AuthorizationError
from tests.helpers import RouteResponseAssertions
from unittest import mock


class TestAuthRoute(RouteResponseAssertions):

    def test_auth_route_returns_success(self):
        self.assert_get_returns_redirect("/api/v1/auth")

    @mock.patch('springapi.routes.authorization.get_auth_code_uri')
    def test_auth_route_raises_authorization_error(self, mock_err):
        err = mock_err.side_effect = AuthorizationError('Bad auth')
        self.assert_get_raises_authorization_error(
            "/api/v1/auth",
            {"error": f"Something went wrong with authorization: {err}"})


@mock.patch('springapi.routes.authorization.exchange_token')
class TestAuthCallbackRoute(RouteResponseAssertions):

    def test_auth_callback_route_exchanges_token(self, mock_auth):
        expected = mock_auth.return_value = {"success": True}
        self.assert_post_raises_ok(
            "/api/v1/auth-callback?code=123", expected)

    def test_auth_callback_route_raises_authorization_error(self, mock_err):
        pass
        err = mock_err.side_effect = AuthorizationError('Bad token')
        self.assert_post_raises_authorization_error(
            "/api/v1/auth-callback?bad_param=abc",
            {"error": f"Something went wrong with token exchange: {err}"})
