import contextlib
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


class ResponseAssertions(object):

    def _assert_get_returns_code_and_response(
            self, path, expected_code, expected_response=None):
        print(path, expected_code, expected_response)
        with make_test_client() as client:
            r = client.get(path)
            self.assertEqual(expected_code, r.status)
            response_body = r.get_json()
            if expected_response:
                self.assertEqual(response_body, expected_response)
            self.assertEqual(
                "application/json", r.headers["Content-type"])

    def _assert_post_returns_code_and_response(
            self, path, body, expected_code, expected_response=None):
        with make_test_client() as client:
            r = client.post(path, data=body)
            self.assertEqual(expected_code, r.status)
            response_body = r.get_json()
            if expected_response:
                self.assertEqual(response_body, expected_response)
            self.assertEqual(
                "application/json", r.headers["Content-type"])

    def _assert_put_returns_code_and_response(
            self, path, body, expected_code, expected_response=None):
        with make_test_client() as client:
            r = client.put(path, data=body)
            self.assertEqual(expected_code, r.status)
            response_body = r.get_json()
            if expected_response:
                self.assertEqual(response_body, expected_response)
            self.assertEqual(
                "application/json", r.headers["Content-type"])

    def assert_get_raises_not_found(self, path, expected_response=None):
        return self._assert_get_returns_code_and_response(
            path, '404 NOT FOUND', expected_response)

    def assert_get_raises_ok(self, path, expected_response=None):
        return self._assert_get_returns_code_and_response(
            path, '200 OK', expected_response)

    def assert_post_raises_invalid_body(self, path, expected_response=None):
        invalid_body = b'FOOBAR'
        return self._assert_post_returns_code_and_response(
            path, invalid_body, '400 BAD REQUEST', expected_response)

    def assert_put_raises_invalid_body(self, path, expected_response=None):
        invalid_body = b'FOOBAR'
        return self._assert_put_returns_code_and_response(
            path, invalid_body, '400 BAD REQUEST', expected_response)


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
