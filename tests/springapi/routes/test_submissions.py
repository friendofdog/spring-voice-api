import unittest
from unittest import mock
from tests.springapi.helpers import make_test_client, MockDatabase


class TestSubmissionsRoute(unittest.TestCase):

    @mock.patch('springapi.routes.submissions.get_collection')
    def test_get_returns_empty_list_without_submissions(self, mocked):
        empty_list = []
        mocked.return_value = empty_list

        with make_test_client() as client:
            response = client.get("/api/v1/submissions")
            self.assertEqual("200 OK", response.status)
            json = response.get_json()
            self.assertEqual(
                "application/json", response.headers["Content-type"])
            self.assertEqual({"submissions": empty_list}, json)

    @mock.patch('springapi.routes.submissions.get_collection')
    def test_get_returns_submissions_in_list(self, mocked):
        mock_db = MockDatabase()
        mock_submission = {"name": "Foo Bar", "message": "foobar"}
        mock_db.add_submission(mock_submission)
        mocked.return_value = mock_db.get_submissions()

        with make_test_client() as client:
            response = client.get("/api/v1/submissions")
            self.assertEqual("200 OK", response.status)
            json = response.get_json()
            self.assertEqual(
                "application/json", response.headers["Content-type"])
            self.assertEqual({"submissions": [mock_submission]}, json)
