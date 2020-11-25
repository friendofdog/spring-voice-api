import json
import unittest

from tests.helpers import make_test_client


class RouteResponseAssertions(unittest.TestCase):

    def assert_expected_code_and_response(
            self, method, path, expected_code, expected_response, body=None,
            credentials=None, config=None, content_type="application/json"):
        request_headers = {}
        request_headers.update(credentials if credentials is not None else {})
        with make_test_client(config) as client:
            call = getattr(client, method)
            if method in ['post', 'put']:
                r = call(path, data=body, headers=request_headers)
            else:
                r = call(path, headers=request_headers)
            self.assertEqual(expected_code, r.status)
            response_body = r.get_json()
            if expected_response is not None:
                self.assertEqual(response_body, expected_response)
            self.assertEqual(
                content_type, r.headers["Content-type"])

    def assert_checks_authentication(self, method, path):
        self.assert_expected_code_and_response(
            method, path, '302 FOUND', None,
            content_type="text/html; charset=utf-8")

        self.assert_expected_code_and_response(
            method, path, '302 FOUND', None,
            credentials={"Authorization": "FOOBAR"},
            content_type="text/html; charset=utf-8")

        self.assert_expected_code_and_response(
            method, path, '302 FOUND', None,
            credentials={"Authorization": "Bearer FOOBAR"},
            content_type="text/html; charset=utf-8")

    def assert_requires_admin_authentication(self, method, path):
        expected_response = {
            "error": "unauthorized",
            "message": "Request requires Authorization header"
        }
        self.assert_expected_code_and_response(
            method, path, '401 UNAUTHORIZED', expected_response)

        expected_response = {
            "error": "bad_request",
            "message": "Requires bearer token"
        }
        self.assert_expected_code_and_response(
            method, path, '400 BAD REQUEST', expected_response,
            credentials={"Authorization": "FOOBAR"})

        expected_response = {
            "error": "forbidden",
            "message": "You are not authorized to perform this action"
        }
        self.assert_expected_code_and_response(
            method, path, '403 FORBIDDEN', expected_response,
            credentials={"Authorization": "Bearer FOOBAR"})

    def assert_get_raises_ok(
            self, path, expected_response=None, credentials=None,
            content_type="application/json"):
        return self.assert_expected_code_and_response(
            'get', path, '200 OK', expected_response, credentials=credentials,
            content_type=content_type)

    def assert_get_returns_redirect(self, path, credentials):
        expected_response = {"status": "Valid token found in request header"}
        return self.assert_expected_code_and_response(
            'get', path, '200 OK', expected_response, credentials=credentials)

    def assert_get_raises_not_found(
            self, path, expected_response=None, credentials=None):
        return self.assert_expected_code_and_response(
            'get', path, '404 NOT FOUND', expected_response,
            credentials=credentials)

    def assert_get_raises_invalid_body(
            self, path, expected_response=None, credentials=None):
        return self.assert_expected_code_and_response(
            'get', path, '400 BAD REQUEST', expected_response,
            credentials=credentials)

    def assert_get_raises_authorization_error(
            self, path, expected_response=None):
        return self.assert_expected_code_and_response(
            'get', path, '400 BAD REQUEST', expected_response)

    def assert_post_raises_ok(
            self, path, body, expected_response=None, credentials=None):
        return self.assert_expected_code_and_response(
            'post', path, '200 OK', expected_response, json.dumps(body),
            credentials=credentials)

    def assert_post_raises_created(
            self, path, body, expected_response=None, credentials=None):
        return self.assert_expected_code_and_response(
            'post', path, '201 CREATED', expected_response, json.dumps(body),
            credentials=credentials)

    def assert_post_raises_invalid_body(
            self, path, expected_response=None, credentials=None):
        invalid_body = b'FOOBAR'
        return self.assert_expected_code_and_response(
            'post', path, '400 BAD REQUEST', expected_response, invalid_body,
            credentials=credentials)

    def assert_post_raises_authorization_error(
            self, path, body, expected_response=None, credentials=None):
        return self.assert_expected_code_and_response(
            'post', path, '400 BAD REQUEST', expected_response,
            json.dumps(body), credentials=credentials)

    def assert_post_raises_already_exists(
            self, path, body, expected_response=None, credentials=None):
        return self.assert_expected_code_and_response(
            'post', path, '409 CONFLICT', expected_response, json.dumps(body),
            credentials=credentials)

    def assert_put_raises_ok(
            self, path, body, expected_response=None, credentials=None):
        return self.assert_expected_code_and_response(
            'put', path, '200 OK', expected_response, json.dumps(body),
            credentials=credentials)

    def assert_put_raises_not_found(
            self, path, body, expected_response=None, credentials=None):
        return self.assert_expected_code_and_response(
            'put', path, '404 NOT FOUND', expected_response, json.dumps(body),
            credentials=credentials)

    def assert_put_raises_invalid_body(
            self, path, expected_response=None, credentials=None):
        invalid_body = b'FOOBAR'
        return self.assert_expected_code_and_response(
            'put', path, '400 BAD REQUEST', expected_response, invalid_body,
            credentials=credentials)
