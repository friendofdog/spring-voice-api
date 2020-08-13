import unittest
from unittest import mock
from tests.helpers import make_test_client
from springapi.models.exceptions import *


class TestSubmissionsRoute(unittest.TestCase):

    @mock.patch('springapi.routes.submissions.Submission.get_submissions')
    def test_get_all_returns_404_if_not_found(self, mocked):
        err = mocked.side_effect = CollectionNotFound('submissions')

        with make_test_client() as client:
            r = client.get(f'/api/v1/submissions')
            self.assertEqual('404 NOT FOUND', r.status)
            self.assertEqual(r.get_json(), err.error_response_body())
            self.assertEqual(
                "application/json", r.headers["Content-type"])

    @mock.patch('springapi.routes.submissions.Submission.get_submissions')
    def test_get_all_returns_empty_list(self, mocked):
        mocked.return_value = {}

        with make_test_client() as client:
            r = client.get("/api/v1/submissions")
            self.assertEqual("200 OK", r.status)
            self.assertEqual({"submissions": {}}, r.get_json())
            self.assertEqual(
                "application/json", r.headers["Content-type"])

    @mock.patch('springapi.routes.submissions.Submission.get_submissions')
    def test_get_all_returns_submissions_in_list(self, mocked):
        entries = mocked.return_value = {
            "1": {"name": "Some Guy", "message": "Hi there"},
            "2": {"name": "Another Fellow", "message": "Goodbye"}
        }

        with make_test_client() as client:
            r = client.get("/api/v1/submissions")
            self.assertEqual("200 OK", r.status)
            self.assertEqual({"submissions": entries}, r.get_json())
            self.assertEqual(
                "application/json", r.headers["Content-type"])

    @mock.patch('springapi.routes.submissions.Submission.get_submission')
    def test_get_single_returns_404_if_not_found(self, mocked):
        entry_id = 'abc'
        err = mocked.side_effect = EntryNotFound(entry_id, 'submissions')

        with make_test_client() as client:
            r = client.get(f'/api/v1/submissions/{entry_id}')
            self.assertEqual('404 NOT FOUND', r.status)
            self.assertEqual(r.get_json(), err.error_response_body())
            self.assertEqual(
                "application/json", r.headers["Content-type"])

    @mock.patch('springapi.routes.submissions.Submission.get_submission')
    def test_get_single_returns_entry_if_found(self, mocked):
        entry_id = 'abc'
        data = {'name': 'Guy', 'location': 'There'}
        mocked.return_value = data

        with make_test_client() as client:
            r = client.get(f'/api/v1/submissions/{entry_id}')
            self.assertEqual('200 OK', r.status)
            self.assertEqual({entry_id: data}, r.get_json())
            self.assertEqual(
                "application/json", r.headers["Content-type"])

    @mock.patch('springapi.routes.submissions.Submission.create_submission')
    def test_create_single_returns_409_if_already_exists(self, mocked):
        err = mocked.side_effect = EntryAlreadyExists('abc', 'submissions')

        with make_test_client() as client:
            r = client.post("/api/v1/submissions", json={})
            self.assertEqual(r.status, '409 CONFLICT')
            self.assertEqual(r.get_json(), err.error_response_body())
            self.assertEqual(
                "application/json", r.headers["Content-type"])

    @mock.patch('springapi.routes.submissions.Submission.create_submission')
    def test_create_single_returns_entry_on_success(self, mocked):
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
        err = mocked.side_effect = EntryNotFound(entry_id, 'submissions')

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
