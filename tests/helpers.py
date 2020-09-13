import contextlib
import json
import unittest
from mockfirestore import MockFirestore  # type: ignore
from springapi.app import create_app
from springapi.config_helpers import encode_json_uri
from springapi.models import exceptions
from springapi.models.submission import Submission


class SubmissionResponseAssertions(unittest.TestCase):

    @contextlib.contextmanager
    def _assert_expected_exception_and_error(
            self, expected_exception, expected_err=None):
        with self.assertRaises(expected_exception) as context:
            yield

        if expected_err is not None:
            self.assertEqual(
                context.exception.error_response_body(),
                expected_err)

    def assert_missing_fields_get_default_values(self, data, expected):
        submission = Submission.from_json(data)
        self.assertEqual(submission.to_json(), expected)

    def assert_get_submissions_raises_not_found(self):
        with self._assert_expected_exception_and_error(
                exceptions.CollectionNotFound,
                {'error': 'Collection submissions not found'}):
            Submission.get_submissions()

    def assert_get_submissions_returns_all_submissions(self, expected_resp):
        result = Submission.get_submissions()
        self.assertEqual(result, expected_resp)

    def assert_get_single_submission_raises_not_found(self, entry_id):
        exception = exceptions.EntryNotFound
        err = {'error': f'{entry_id} was not found in submissions'}
        with self._assert_expected_exception_and_error(exception, err):
            Submission.get_submission(entry_id)

    def assert_get_single_submission_returns_single(
            self, expected_resp, entry_id):
        self.assertEqual(expected_resp, Submission.get_submission(entry_id))

    def assert_create_submission_raises_validation_error(self, data):
        exception = exceptions.ValidationError
        with self._assert_expected_exception_and_error(exception):
            Submission.create_submission(data)

    def assert_create_submission_raises_already_exists(self, entry_id, data):
        exception = exceptions.EntryAlreadyExists
        err = {'error': f'{entry_id} already exists in submissions'}
        data["id"] = entry_id
        with self._assert_expected_exception_and_error(exception, err):
            Submission.create_submission(data)

    def assert_create_submission_returns_success(self, entry_id, data):
        result = Submission.create_submission(data)
        data["id"] = entry_id
        expected = Submission.from_json(data)
        self.assertEqual(expected, result)

    def assert_update_submission_raises_not_found(self, entry_id, data):
        exception = exceptions.EntryNotFound
        err = {'error': f'{entry_id} was not found in def'}
        with self._assert_expected_exception_and_error(exception, err):
            Submission.update_submission(entry_id, data)

    def assert_update_submission_raises_validation_error(self, entry_id, data):
        exception = exceptions.ValidationError
        err = {'error': 'Missing: location'}
        with self._assert_expected_exception_and_error(exception, err):
            Submission.update_submission(entry_id, data)

    def assert_update_submission_returns_success(self, entry_id, data):
        self.assertEqual(
            Submission.from_json(data),
            Submission.update_submission(entry_id, data))


class RouteResponseAssertions(unittest.TestCase):

    def _assert_expected_code_and_response(
            self, method, path, expected_code, body=None, expected_resp=None):
        with make_test_client() as client:
            call = getattr(client, method)
            if method in ['post', 'put']:
                r = call(path, data=body)
            else:
                r = call(path)
            self.assertEqual(expected_code, r.status)
            response_body = r.get_json()
            if expected_resp is not None:
                self.assertEqual(response_body, expected_resp)
            self.assertEqual(
                "application/json", r.headers["Content-type"])

    def assert_get_raises_ok(self, path, expected_response=None):
        return self._assert_expected_code_and_response(
            'get', path, '200 OK', expected_response)

    def assert_get_raises_not_found(self, path, expected_response=None):
        return self._assert_expected_code_and_response(
            'get', path, '404 NOT FOUND', expected_response)

    def assert_post_raises_ok(self, path, body, expected_response=None):
        return self._assert_expected_code_and_response(
            'post', path, '201 CREATED', json.dumps(body), expected_response)

    def assert_post_raises_invalid_body(self, path, expected_response=None):
        invalid_body = b'FOOBAR'
        return self._assert_expected_code_and_response(
            'post', path, '400 BAD REQUEST', invalid_body, expected_response)

    def assert_post_raises_already_exists(
            self, path, body, expected_response=None):
        return self._assert_expected_code_and_response(
            'post', path, '409 CONFLICT', json.dumps(body), expected_response)

    def assert_put_raises_ok(self, path, body, expected_response=None):
        return self._assert_expected_code_and_response(
            'put', path, '200 OK', json.dumps(body), expected_response)

    def assert_put_raises_not_found(self, path, body, expected_response=None):
        return self._assert_expected_code_and_response(
            'put', path, '404 NOT FOUND', json.dumps(body), expected_response)

    def assert_put_raises_invalid_body(self, path, expected_response=None):
        invalid_body = b'FOOBAR'
        return self._assert_expected_code_and_response(
            'put', path, '400 BAD REQUEST', invalid_body, expected_response)


def populate_mock_submissions(entries):

    mock_db = MockFirestore()
    for key, data in entries.items():
        mock_db.collection('submissions').add(data, key)

    return mock_db


@contextlib.contextmanager
def make_test_client(environ=None):
    environ = environ or {}
    environ.setdefault("DATABASE_URI", encode_json_uri("firestore", {}))
    app = create_app(environ)
    with app.test_client() as client:
        yield client
