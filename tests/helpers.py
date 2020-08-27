import contextlib
import unittest
from mockfirestore import MockFirestore  # type: ignore
from springapi.app import create_app
from springapi.config_helpers import encode_json_uri
from springapi.models import exceptions
from springapi.models.submission import Submission


class SubmissionResponseAssertions(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(SubmissionResponseAssertions, self).__init__(*args, **kwargs)
        self.submission = Submission()

    def _assert_expected_response_on_no_error(
            self, method, expected_resp, *data):
        call = getattr(self.submission, method)
        if data:
            response = call(*data)
        else:
            response = call()
        self.assertEqual(response, expected_resp)

    def _assert_expected_exception_and_error(
            self, method, expected_exception, expected_err, *data):
        with self.assertRaises(expected_exception) as context:
            call = getattr(self.submission, method)
            call(*data)
        if expected_err:
            self.assertEqual(
                context.exception.error_response_body(), expected_err)

    def assert_get_submissions_raises_not_found(self):
        exception = exceptions.CollectionNotFound
        err = {'error': 'Collection submissions not found'}
        return self._assert_expected_exception_and_error(
            'get_submissions', exception, err)

    def assert_get_submissions_returns_all_submissions(self, expected_resp):
        return self._assert_expected_response_on_no_error(
            'get_submissions', expected_resp)

    def assert_get_single_submission_raises_not_found(self, entry_id):
        exception = exceptions.EntryNotFound
        err = {'error': f'{entry_id} was not found in submissions'}
        return self._assert_expected_exception_and_error(
            'get_submission', exception, err, entry_id)

    def assert_get_single_submission_returns_single(
            self, expected_resp, entry_id):
        return self._assert_expected_response_on_no_error(
            'get_submission', expected_resp, entry_id)

    def assert_create_submission_raises_validation_error(self, data):
        exception = exceptions.ValidationError
        return self._assert_expected_exception_and_error(
            'create_submission', exception, {}, data)

    def assert_create_submission_raises_already_exists(self, entry_id, data):
        exception = exceptions.EntryAlreadyExists
        err = {'error': f'{entry_id} already exists in submissions'}
        return self._assert_expected_exception_and_error(
            'create_submission', exception, err, data)

    def assert_create_submission_returns_success(self, entry_id, data):
        expected_resp = {entry_id: data}
        return self._assert_expected_response_on_no_error(
            'create_submission', expected_resp, data)

    def assert_update_submission_raises_not_found(self, entry_id, data):
        exception = exceptions.EntryNotFound
        err = {'error': f'{entry_id} was not found in def'}
        return self._assert_expected_exception_and_error(
            'update_submission', exception, err, entry_id, data)

    def assert_update_submission_raises_validation_error(self, entry_id, data):
        exception = exceptions.ValidationError
        err = {'error': 'Missing: location'}
        return self._assert_expected_exception_and_error(
            'update_submission', exception, err, entry_id, data)

    def assert_update_submission_returns_success(self, entry_id, data):
        expected_resp = {entry_id: data}
        return self._assert_expected_response_on_no_error(
            'update_submission', expected_resp, entry_id, data)


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
            if expected_resp:
                self.assertEqual(response_body, expected_resp)
            self.assertEqual(
                "application/json", r.headers["Content-type"])

    def assert_get_raises_ok(self, path, expected_response=None):
        return self._assert_expected_code_and_response(
            'get', path, '200 OK', expected_response)

    def assert_get_raises_not_found(self, path, expected_response=None):
        return self._assert_expected_code_and_response(
            'get', path, '404 NOT FOUND', expected_response)

    def assert_post_raises_ok(self, path, expected_response=None):
        return self._assert_expected_code_and_response(
            'post', path, '201 CREATED', {}, expected_response)

    def assert_post_raises_invalid_body(self, path, expected_response=None):
        invalid_body = b'FOOBAR'
        return self._assert_expected_code_and_response(
            'post', path, '400 BAD REQUEST', invalid_body, expected_response)

    def assert_post_raises_already_exists(self, path, expected_response=None):
        return self._assert_expected_code_and_response(
            'post', path, '409 CONFLICT', {}, expected_response)

    def assert_put_raises_ok(self, path, expected_response=None):
        return self._assert_expected_code_and_response(
            'put', path, '200 OK', {}, expected_response)

    def assert_put_raises_not_found(self, path, expected_response=None):
        return self._assert_expected_code_and_response(
            'put', path, '404 NOT FOUND', {}, expected_response)

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
