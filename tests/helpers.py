import contextlib
import unittest
from mockfirestore import MockFirestore  # type: ignore
from springapi.app import create_app


class MockDatabase(object):

    def __init__(self):
        self._submissions = []

    def add_entry(self, submission):
        self._submissions.append(submission)
        return self._submissions[-1], 201

    def update_entry(self, update):
        i, sub = next(([i, s] for i, s in enumerate(self._submissions)
                       if s['id'] == update['id']), ['', ''])
        if sub:
            self._submissions[i] = update
            return self._submissions[i], 200
        else:
            add = self.add_entry(update)
            return add

    def get_collection(self):
        return self._submissions


class ResponseAssertions(unittest.TestCase):

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
                print(response_body, expected_resp)
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
def make_test_client():
    app = create_app()
    with app.test_client() as client:
        yield client
