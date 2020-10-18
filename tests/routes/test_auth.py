from tests.helpers import RouteResponseAssertions


class TestAuthRoute(RouteResponseAssertions):

    def test_auth_route_returns_expected_auth_code_scope_user(self):
        code = "123"
        expected = {"code": code}
        self.assert_get_raises_ok(
            f"/api/v1/auth?code={code}", expected)

    def test_auth_route_raises_error(self):
        expected = {"error": "Authorization code not found"}
        self.assert_get_raises_assertion_error(
            "/api/v1/auth?bad_param=abc", expected)
