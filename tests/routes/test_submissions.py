import unittest
from unittest import mock
from tests.helpers import make_test_client


class TestSubmissionsRoute(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSubmissionsRoute, self).__init__(*args, **kwargs)
        self.entries = {
            "1": {"name": "Some Guy", "message": "Hi there"},
            "2": {"name": "Another Fellow", "message": "Goodbye"}
        }

    @mock.patch('springapi.routes.submissions.Submission.get_submissions')
    def test_db_get_submissions_returns_empty_list(self, mocked):
        mocked.return_value = {}

        with make_test_client() as client:
            response = client.get("/api/v1/submissions")
            self.assertEqual("200 OK", response.status)
            json = response.get_json()
            self.assertEqual(
                "application/json", response.headers["Content-type"])
            self.assertEqual({"submissions": {}}, json)

    @mock.patch('springapi.routes.submissions.Submission.get_submissions')
    def test_db_get_submissions_returns_submissions_in_list(self, mocked):
        mocked.return_value = self.entries

        with make_test_client() as client:
            response = client.get("/api/v1/submissions")
            self.assertEqual("200 OK", response.status)
            json = response.get_json()
            self.assertEqual(
                "application/json", response.headers["Content-type"])
            self.assertEqual({"submissions": self.entries}, json)

    @mock.patch('springapi.routes.submissions.Submission.get_submission')
    def test_db_get_submission_returns_submission_if_found(self, mocked):
        entry_id = 'abc'
        expected_response = {'name': 'Guy', 'location': 'There'}
        expected_status = '200'
        mocked.return_value = [expected_response, expected_status]

        with make_test_client() as client:
            response = client.get(f'/api/v1/submissions/{entry_id}')
            self.assertEqual(expected_status, response.status)
            self.assertEqual(expected_response, response.get_json()[entry_id])
            self.assertEqual(
                "application/json", response.headers["Content-type"])

    @mock.patch('springapi.routes.submissions.Submission.create_submission')
    def test_db_create_submission_returns_submission_on_success(self, mocked):
        data = {"message": "Greetings", "name": "This Person"}
        expected_status = '201'
        mocked.return_value = [data, expected_status]

        with make_test_client() as client:
            response = client.post("/api/v1/submissions", json=data)
            self.assertEqual(response.status, expected_status)
            self.assertEqual(response.get_json(), data)
            self.assertEqual(
                "application/json", response.headers["Content-type"])

    @mock.patch('springapi.routes.submissions.Submission.update_submission')
    def test_db_update_submission_returns_404_if_not_found(self, mocked):
        expected_response = {'error': 'This is an error message'}
        expected_status = '404'
        mocked.return_value = [expected_response, expected_status]

        with make_test_client() as client:
            response = client.put("/api/v1/submissions/abc", json={})
            self.assertEqual(response.status, expected_status)
            self.assertEqual(response.get_json(), expected_response)
            self.assertEqual(
                "application/json", response.headers["Content-type"])

    @mock.patch('springapi.routes.submissions.Submission.update_submission')
    def test_db_update_submission_returns_update_on_success(self, mocked):
        data = {"message": "Greetings", "name": "This Person"}
        expected_status = '200'
        mocked.return_value = [data, expected_status]

        with make_test_client() as client:
            response = client.put("/api/v1/submissions/abc", json={})
            self.assertEqual(response.status, expected_status)
            self.assertEqual(response.get_json(), data)
            self.assertEqual(
                "application/json", response.headers["Content-type"])
