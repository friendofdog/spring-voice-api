import contextlib
import json
import unittest
from mockfirestore import MockFirestore  # type: ignore
from springapi.app import create_app, create_config
from springapi.config_helpers import AUTH, CLIENT_ID, TOKEN, encode_json_uri
from springapi.exceptions import (
    EntryNotFound, CollectionNotFound, ValidationError, EntryAlreadyExists)
from springapi.models.submission import Submission
from springapi.models.token import Token


class ModelAssertions(unittest.TestCase):

    @contextlib.contextmanager
    def _assert_expected_exception_and_error(
            self, expected_exception, expected_err=None):
        with self.assertRaises(expected_exception) as context:
            yield

        if expected_err is not None:
            self.assertEqual(
                context.exception.error_response_body(),
                expected_err)


class TokenResponseAssertions(ModelAssertions):

    def assert_get_tokens_returns_all_valid_tokens(self, expected):
        expected_tokens = [expected[k] for k in expected]
        response = Token.get_tokens()
        tokens = [r.to_json() for r in response]
        self.assertListEqual(tokens, expected_tokens)

    def assert_get_tokens_raises_CollectionNotFound(self):
        with self._assert_expected_exception_and_error(
                CollectionNotFound,
                {'error': 'Collection tokens not found'}):
            Token.get_tokens()

    def assert_create_token_raises_validation_error(self, data):
        exception = ValidationError
        with self._assert_expected_exception_and_error(exception):
            Token.create_token(data)

    def assert_create_token_raises_already_exists(self, entry_id, data):
        exception = EntryAlreadyExists
        err = {'error': f'{entry_id} already exists in tokens'}
        with self._assert_expected_exception_and_error(exception, err):
            Token.create_token(data)

    def assert_create_token_returns_success(self, data):
        result = Token.create_token(data)
        expected = Token.from_json(data)
        self.assertEqual(expected, result)


class SubmissionResponseAssertions(ModelAssertions):

    def assert_missing_fields_get_default_values(self, data, expected):
        submission = Submission.from_json(data)
        self.assertEqual(submission.to_json(), expected)

    def assert_get_submissions_raises_not_found(self):
        with self._assert_expected_exception_and_error(
                CollectionNotFound,
                {'error': 'Collection submissions not found'}):
            Submission.get_submissions()

    def assert_get_submissions_returns_all_submissions(self, expected_resp):
        result = Submission.get_submissions()
        self.assertEqual(result, expected_resp)

    def assert_get_single_submission_raises_not_found(self, entry_id):
        exception = EntryNotFound
        err = {'error': f'{entry_id} was not found in submissions'}
        with self._assert_expected_exception_and_error(exception, err):
            Submission.get_submission(entry_id)

    def assert_get_single_submission_returns_single(
            self, expected_resp, entry_id):
        self.assertEqual(expected_resp, Submission.get_submission(entry_id))

    def assert_create_submission_raises_validation_error(self, data):
        exception = ValidationError
        with self._assert_expected_exception_and_error(exception):
            Submission.create_submission(data)

    def assert_create_submission_raises_already_exists(self, entry_id, data):
        exception = EntryAlreadyExists
        err = {'error': f'{entry_id} already exists in submissions'}
        with self._assert_expected_exception_and_error(exception, err):
            Submission.create_submission(data)

    def assert_create_submission_returns_success(self, data):
        result = Submission.create_submission(data)
        expected = Submission.from_json(data)
        self.assertEqual(expected, result)

    def assert_update_submission_raises_not_found(self, entry_id, data):
        exception = EntryNotFound
        err = {'error': f'{entry_id} was not found in def'}
        with self._assert_expected_exception_and_error(exception, err):
            Submission.update_submission(entry_id, data)

    def assert_update_submission_raises_validation_error(self, entry_id, data):
        exception = ValidationError
        err = {'error': 'Missing: location'}
        with self._assert_expected_exception_and_error(exception, err):
            Submission.update_submission(entry_id, data)

    def assert_update_submission_returns_success(
            self, entry_id, data, expected):
        self.assertEqual(
            expected, Submission.update_submission(entry_id, data))


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

    def assert_get_returns_redirect(self, path):
        expected_response = None
        return self.assert_expected_code_and_response(
            'get', path, '302 FOUND', expected_response,
            content_type="text/html; charset=utf-8")

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


def populate_mock_submissions(entries):
    mock_db = MockFirestore()
    for key, data in entries.items():
        mock_db.collection('submissions').add(data, key)

    return mock_db


@contextlib.contextmanager
def make_test_client(environ=None):
    auth_credentials = {
        "web": {
            "client_id": "abc123"
        }
    }
    environ = environ or {}
    environ.setdefault("DATABASE_URI", encode_json_uri("firestore", {}))
    environ.setdefault(AUTH, encode_json_uri("firebase", auth_credentials))
    environ.setdefault(TOKEN, encode_json_uri("sqlite", {}))
    environ.setdefault(CLIENT_ID, "123")
    app = create_app(environ)
    with app.test_client() as client:
        yield client


def make_test_springapi_app(scheme, env_additional=None, remove=None):
    auth_credentials = {
        "web": {
            "client_id": "abc123"
        }
    }
    env = {
        AUTH: encode_json_uri(scheme, auth_credentials),
        TOKEN: encode_json_uri("sqlite", {}),
    }
    if env_additional:
        env.update(env_additional)
    if remove:
        for r in remove:
            env.pop(r)
    config = create_config(env)

    app = create_app(config)
    return app
