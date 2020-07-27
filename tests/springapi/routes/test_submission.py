import unittest
from unittest import mock
from tests.springapi.helpers import make_test_client, MockDatabase


class TestSubmissionRoute(unittest.TestCase):

    @mock.patch('springapi.routes.submission.add_entry')
    def test_post_returns_submission(self, mocked):
        mock_db = MockDatabase()
        mock_submission = {"name": "Some Guy", "message": "Hi there"}
        mocked.return_value = mock_db.add_submission(mock_submission)

        with make_test_client() as client:
            response = client.post("/api/v1/submission", data=mock_submission)
            self.assertEqual("200 OK", response.status)
            json = response.get_json()
            self.assertEqual(
                "application/json", response.headers["Content-type"])
            self.assertEqual(mock_submission, json)

    @mock.patch('springapi.routes.submission.update_entry')
    def test_put_returns_updated_submission(self, mocked):
        mock_db = MockDatabase()
        mock_submission = {"name": "Other Guy", "message": "Hi there"}
        mock_update = {"name": "Some Guy", "message": "Goodbye"}
        mock_db.add_submission(mock_submission)
        mocked.return_value = mock_db.update_submission(mock_update)

        with make_test_client() as client:
            response = client.put("/api/v1/submission", data=mock_update)
            self.assertEqual("200 OK", response.status)
            json = response.get_json()
            self.assertEqual(
                "application/json", response.headers["Content-type"])
            self.assertEqual(mock_update, json)
