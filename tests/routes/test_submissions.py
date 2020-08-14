import unittest
from springapi.models import exceptions
from tests.helpers import make_test_client, ResponseAssertions
from unittest import mock


class TestSubmissionsRoute(unittest.TestCase, ResponseAssertions):

    @mock.patch('springapi.routes.submissions.Submission.get_submissions')
    def test_get_all_returns_404_if_not_found(self, mocked):
        err = mocked.side_effect = exceptions.CollectionNotFound('submissions')
        self.assert_get_raises_not_found(
            f'/api/v1/submissions', err.error_response_body())

    @mock.patch('springapi.routes.submissions.Submission.get_submissions')
    def test_get_all_returns_empty_list(self, mocked):
        entries = mocked.return_value = {}
        self.assert_get_raises_ok(
            '/api/v1/submissions', {'submissions': entries})

    @mock.patch('springapi.routes.submissions.Submission.get_submissions')
    def test_get_all_returns_submissions_in_list(self, mocked):
        entries = mocked.return_value = {
            "1": {"name": "Some Guy", "message": "Hi there"},
            "2": {"name": "Another Fellow", "message": "Goodbye"}
        }
        self.assert_get_raises_ok(
            '/api/v1/submissions', {'submissions': entries})

    @mock.patch('springapi.routes.submissions.Submission.get_submission')
    def test_get_single_returns_404_if_not_found(self, mocked):
        entry_id = 'abc'
        collection = 'submissions'
        err = mocked.side_effect = exceptions.EntryNotFound(
            entry_id, collection)
        self.assert_get_raises_not_found(
            f'/api/v1/{collection}/{entry_id}', err.error_response_body())

    @mock.patch('springapi.routes.submissions.Submission.get_submission')
    def test_get_single_returns_entry_if_found(self, mocked):
        entry_id = 'abc'
        data = mocked.return_value = {'name': 'Guy', 'location': 'There'}
        self.assert_get_raises_ok(
            f'/api/v1/submissions/{entry_id}', {entry_id: data})

    @mock.patch('springapi.routes.submissions.Submission.create_submission')
    def test_create_single_returns_409_if_already_exists(self, mocked):
        err = mocked.side_effect = exceptions.EntryAlreadyExists(
            'abc', 'submissions')

        with make_test_client() as client:
            r = client.post("/api/v1/submissions", json={})
            self.assertEqual(r.status, '409 CONFLICT')
            self.assertEqual(r.get_json(), err.error_response_body())
            self.assertEqual(
                "application/json", r.headers["Content-type"])

    def test_create_single_rejects_invalid_json(self):
        pass

    @mock.patch('springapi.routes.submissions.Submission.create_submission')
    def test_create_single_returns_201_on_success(self, mocked):
        entry_id = 'abc'
        data = {"message": "Greetings", "name": "This Person"}
        status = '201 CREATED'
        mocked.return_value = {entry_id: data}

        with make_test_client() as client:
            r = client.post("/api/v1/submissions", json=data)
            self.assertEqual(r.status, status)
            self.assertEqual(r.get_json(), {entry_id: data})
            self.assertEqual(
                "application/json", r.headers["Content-type"])

    @mock.patch('springapi.routes.submissions.Submission.update_submission')
    def test_update_single_returns_404_if_not_found(self, mocked):
        entry_id = 'abc'
        err = mocked.side_effect = exceptions.EntryNotFound(
            entry_id, 'submissions')

        with make_test_client() as client:
            r = client.put("/api/v1/submissions/abc", json={})
            self.assertEqual(r.status, '404 NOT FOUND')
            self.assertEqual(r.get_json(), err.error_response_body())
            self.assertEqual(
                "application/json", r.headers["Content-type"])

    @mock.patch('springapi.routes.submissions.Submission.update_submission')
    def test_update_single_returns_updated_entry_on_success(self, mocked):
        entry_id = 'abc'
        data = {"message": "Greetings", "name": "This Person"}
        status = '200 OK'
        mocked.return_value = {entry_id: data}

        with make_test_client() as client:
            r = client.put(f"/api/v1/submissions/{entry_id}", json={})
            self.assertEqual(r.status, status)
            self.assertEqual(r.get_json(), {entry_id: data})
            self.assertEqual(
                "application/json", r.headers["Content-type"])

    def test_update_single_rejects_invalid_json(self):
        self.assert_put_raises_invalid_body("/api/v1/submissions/abc")
