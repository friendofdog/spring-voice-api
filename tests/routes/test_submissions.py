import unittest
from unittest import mock
from tests.helpers import make_test_client, MockDatabase


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
        mock_db.add_entry(mock_submission)
        mocked.return_value = mock_db.get_collection()

        with make_test_client() as client:
            response = client.get("/api/v1/submissions")
            self.assertEqual("200 OK", response.status)
            json = response.get_json()
            self.assertEqual(
                "application/json", response.headers["Content-type"])
            self.assertEqual({"submissions": [mock_submission]}, json)

    @mock.patch('springapi.routes.submissions.add_entry')
    def test_post_returns_submission(self, mocked):
        mock_db = MockDatabase()
        mock_submission = {"name": "Some Guy", "message": "Hi there"}
        mocked.return_value = mock_db.add_entry(mock_submission)

        with make_test_client() as client:
            response = client.post("/api/v1/submissions", data=mock_submission)
            self.assertEqual("201 CREATED", response.status)
            json = response.get_json()
            self.assertEqual(
                "application/json", response.headers["Content-type"])
            self.assertEqual(mock_submission, json)

    @mock.patch('springapi.routes.submissions.update_entry')
    def test_put_returns_201_if_submission_not_found(self, mocked):
        mock_db = MockDatabase()
        mock_update = {"id": "123", "message": "Goodbye"}
        mocked.return_value = mock_db.update_entry(mock_update)

        with make_test_client() as client:
            response = client.put("/api/v1/submissions", data=mock_update)
            self.assertEqual("201 CREATED", response.status)
            json = response.get_json()
            self.assertEqual(
                "application/json", response.headers["Content-type"])
            self.assertEqual(mock_update, json)

    @mock.patch('springapi.routes.submissions.update_entry')
    def test_put_returns_200_if_submission_found(self, mocked):
        mock_db = MockDatabase()
        mock_submission = {"id": "123", "message": "Hi there"}
        mock_update = {"id": "123", "message": "Goodbye"}
        mock_db.add_entry(mock_submission)
        mocked.return_value = mock_db.update_entry(mock_update)

        with make_test_client() as client:
            response = client.put("/api/v1/submissions", data=mock_update)
            self.assertEqual("200 OK", response.status)
            json = response.get_json()
            self.assertEqual(
                "application/json", response.headers["Content-type"])
            self.assertEqual(mock_update, json)
